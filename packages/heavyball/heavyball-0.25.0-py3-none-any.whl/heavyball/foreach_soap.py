import torch

from .utils import init_preconditioner, update_preconditioner, project, beta_debias, exp_avg_sq_, update_param_, set_, \
    StatefulOptimizer, exp_avg_


class ForeachSOAP(StatefulOptimizer):
    """
    SFPaLMForeachSOAP

    Sources:
        Baseline SOAP:
            SOAP: Improving and Stabilizing Shampoo using Adam
            Nikhil Vyas, Depen Morwani, Rosie Zhao, Itai Shapira, David Brandfonbrener, Lucas Janson, Sham Kakade
            https://arxiv.org/abs/2409.11321
            https://github.com/nikhilvyas/SOAP

        ScheduleFree:
            The Road Less Scheduled
            Aaron Defazio, Xingyu Alice Yang, Harsh Mehta, Konstantin Mishchenko, Ahmed Khaled, Ashok Cutkosky
            https://arxiv.org/abs/2405.15682
            https://github.com/facebookresearch/schedule_free
    """

    def __init__(self, params, lr: float = 3e-3, betas=(0.9, 0.95), shampoo_beta: float = 0.95, eps: float = 1e-8,
                 weight_decay: float = 0.01, precondition_frequency: int = 2, max_precond_dim: int = 2048,  #
                 merge_dims: bool = True, precondition_1d: bool = False, normalize_grads: bool = False,
                 data_format: str = "channels_first", correct_bias: bool = True, warmup_steps: int = 1,
                 split: bool = False, foreach: bool = True, mars: bool = False, caution: bool = False,
                 mars_gamma: float = 0.0025):
        defaults = {"lr": lr, "betas": betas, "shampoo_beta": shampoo_beta, "eps": eps, "weight_decay": weight_decay,
                    "precondition_frequency": precondition_frequency, "max_precond_dim": max_precond_dim,
                    "merge_dims": merge_dims, "precondition_1d": precondition_1d, "normalize_grads": normalize_grads,
                    "correct_bias": correct_bias, 'warmup_steps': warmup_steps, 'split': split, 'mars': mars,
                    'caution': caution, 'mars_gamma': mars_gamma}
        super().__init__(params, defaults, foreach)
        self._data_format = data_format

    def _step(self, group):
        vals = []
        step = 0

        max_precond_dim = group['max_precond_dim']
        precondition_1d = group['precondition_1d']

        for p, g in self.split_p_and_g_in_group(group, beta1=group['betas'][0]):
            state = self.state_(p)
            step = state['step'] = state.get("step", -1) + 1

            if "exp_avg" not in state:
                state["exp_avg"] = torch.zeros_like(g, dtype=torch.float32, memory_format=torch.preserve_format)
                state["exp_avg_sq"] = torch.zeros_like(g, dtype=torch.float32, memory_format=torch.preserve_format)
                init_preconditioner(g, state, max_precond_dim, precondition_1d)
                update_preconditioner(g, state, max_precond_dim, precondition_1d, 0, True)
                continue  # first step is skipped so that we never use the current gradients in the projection.

            # Projecting gradients to the eigenbases of Shampoo's preconditioner
            # i.e. projecting to the eigenbases of matrices in state['GG']
            grad_projected = project(g, state['Q'], False)
            exp_avg, exp_avg_sq = state["exp_avg"], state["exp_avg_sq"]
            vals.append((p, g, grad_projected, exp_avg, exp_avg_sq))

        if not vals:
            return

        p_list, grad, grad_projected, exp_avg, exp_avg_sq = zip(*vals)
        beta1, beta2 = group["betas"]

        old_debiased2 = beta_debias(beta2, step)

        # Decay the first and second moment running average coefficient
        # In-place operations to update the averages at the same time
        step_tensor = torch.empty((), dtype=torch.int32, device=p_list[0].device).fill_(step)

        step_size = -group["lr"] * min(step / group['warmup_steps'], 1)

        for p, g, gp, ea, eas in zip(p_list, grad, grad_projected, exp_avg, exp_avg_sq):
            d = exp_avg_(ea, eas, g, gp, beta1, beta2, step_tensor)[0]
            # Projecting the exponential moving average of gradients to the eigenbases of Shampoo's preconditioner
            # i.e. projecting to the eigenbases of matrices in state['GG']
            exp_avg_projected = project(ea, state['Q'], False)

            # Projecting back the preconditioned (by Adam) exponential moving average of gradients
            # to the original space
            # CANT DO /= HERE AS EXP_AVG MAY POINT TO THE BUFFER
            precond = project(exp_avg_projected / d, state['Q'], True)

            update_preconditioner(g, state, max_precond_dim, precondition_1d, old_debiased2,
                                  step > 0 and step % group['precondition_frequency'] == 0)

            update_param_([p], [precond], step_size, group["weight_decay"], caution=group['caution'], grad=[g])
