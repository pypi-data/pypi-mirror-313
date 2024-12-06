import torch
import torch.optim

from .utils import warmup, ScheduleFree, exp_avg_sq_, beta_debias, get_ckp1, promote, \
    _compilable_schedule_free_, copy_stochastic_list_, decorator_knowngood


@decorator_knowngood
def _compilable_step_(y, grad, exp_avg_sq, z, beta1, beta2, step, ckp1, eps, decay, lr):
    old_debiased2 = beta_debias(beta2, step)

    g32 = [promote(g_) for g_ in grad]
    exp_avg_sq32 = [promote(e_) for e_ in exp_avg_sq]

    denom = exp_avg_sq_(exp_avg_sq32, g32, old_debiased2, eps)
    torch._foreach_div_(g32, denom)
    if decay != 0:
        torch._foreach_add_(g32, y, alpha=decay)
    for p, z_, g in zip(y, z, g32):
        _compilable_schedule_free_(p, z_, ckp1, g, lr, beta1)

    copy_stochastic_list_(exp_avg_sq, exp_avg_sq32)


class PaLMForeachSFAdamW(ScheduleFree):
    def __init__(self, params, lr=0.0025, beta=0.9, betas=(None, None), eps=1e-8, weight_decay=0, warmup_steps=0, r=0.0,
                 weight_lr_power=2.0, beta2_scale: float = 0.8, foreach: bool = True, storage_dtype: str = 'float32',
                 mars: bool = False, caution: bool = False, mars_gamma: float = 0.0025):
        if betas[0] is not None:
            beta = betas[0]

        assert not caution, "Caution not implemented for SFAdamW"

        defaults = dict(lr=lr, beta=beta, eps=eps, r=r, k=0, warmup_steps=warmup_steps, train_mode=True, weight_sum=0.0,
                        lr_max=-1.0, weight_lr_power=weight_lr_power, weight_decay=weight_decay,
                        beta2_scale=beta2_scale, storage_dtype=storage_dtype, mars=mars, caution=caution,
                        mars_gamma=mars_gamma)
        super().__init__(params, defaults, foreach)

    def _step(self, group):
        eps = group['eps']
        decay = group['weight_decay']
        k = group['k']

        if not group['train_mode']:
            raise Exception("Not in train mode!")

        active_p = [p for p in group['params'] if p.grad is not None]

        if not active_p:
            return

        storage_dtype = getattr(torch, group['storage_dtype'])

        for p in active_p:
            if 'z' not in self.state_(p):
                self.state_(p)['z'] = torch.clone(p.data, memory_format=torch.preserve_format)
                self.state_(p)['exp_avg_sq'] = torch.zeros_like(p.data, dtype=storage_dtype, memory_format=torch.preserve_format)

        # Decay the first moment running average coefficient
        beta2 = 1 - (k + 1) ** -group['beta2_scale']

        y, grad, exp_avg_sq, z = zip(*[(p.data, p.grad, self.state_(p)['exp_avg_sq'], self.state_(p)['z'])  #
                                       for p in active_p])

        if group['mars']:
            self.mars_correct_list(group, y, grad, group['mars_gamma'], group['betas'][0])

        lr = warmup(group['lr'], k + 1, group['warmup_steps'])
        ckp1, group['weight_sum'] = get_ckp1(lr, group['weight_lr_power'], group['weight_sum'], group['r'], k + 1)

        step = torch.empty((), dtype=torch.int32, device=y[0].device).fill_(k + 1)
        ckp1 = torch.empty((), dtype=torch.float32, device=y[0].device).fill_(ckp1)
        beta2 = torch.empty((), dtype=torch.float32, device=y[0].device).fill_(beta2)
        lr = torch.empty((), dtype=torch.float32, device=y[0].device).fill_(lr)
        _compilable_step_(y, grad, exp_avg_sq, z, group['beta'], beta2, step, ckp1, eps, decay, lr)
        group['k'] = k + 1
