import torch
import torch.optim

from .utils import warmup, exp_avg_sq_, beta_debias, update_param_, StatefulOptimizer, promote, copy_stochastic_list_, decorator_knowngood


@decorator_knowngood
def _compilable_step_(y, grad, exp_avg_sq, exp_avg, beta1, beta2, step, lr, eps, decay, caution):
    g32, exp_avg32, exp_avg_sq32 = [list(map(promote, x)) for x in [grad, exp_avg, exp_avg_sq]]

    denom = exp_avg_sq_(exp_avg_sq32, g32, beta_debias(beta2, step), eps)

    beta1 = beta_debias(beta1, step)
    torch._foreach_mul_(exp_avg32, beta1)
    [ea32.addcdiv_(g, d, value=1 - beta1) for ea32, g, d in zip(exp_avg32, g32, denom)]

    update_param_(y, exp_avg32, lr, decay, caution=caution, grad=g32)

    copy_stochastic_list_(exp_avg, exp_avg32)
    copy_stochastic_list_(exp_avg_sq, exp_avg_sq32)


class ForeachLaProp(StatefulOptimizer):

    def __init__(self, params, lr=0.0025, betas=(0.9, 0.99), eps=1e-8, weight_decay=0, warmup_steps=1,
                 foreach: bool = True, storage_dtype: str = 'float32', mars: bool = False, caution: bool = False,
                 mars_gamma: float = 0.0025):
        defaults = dict(lr=lr, betas=betas, eps=eps, k=0, warmup_steps=warmup_steps, train_mode=True, weight_sum=0.0,
                        lr_max=-1.0, weight_decay=weight_decay, storage_dtype=storage_dtype, mars=mars, caution=caution,
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
            if 'exp_avg' not in self.state_(p):
                self.state_(p)['exp_avg'] = torch.zeros_like(p.data, dtype=storage_dtype, memory_format=torch.preserve_format)
                self.state_(p)['exp_avg_sq'] = torch.zeros_like(p.data, dtype=storage_dtype, memory_format=torch.preserve_format)

        y, grad, exp_avg_sq, exp_avg = zip(
            *[(p.data, p.grad, self.state_(p)['exp_avg_sq'], self.state_(p)['exp_avg'])  #
              for p in active_p])

        if group['mars']:
            self.mars_correct_list(group, y, grad, group['mars_gamma'], group['betas'][0])

        lr = -warmup(group['lr'], k + 1, group['warmup_steps'])
        lr = torch.empty((), dtype=torch.float32, device=y[0].device).fill_(lr)
        step = torch.empty((), dtype=torch.int32, device=y[0].device).fill_(k + 1)

        _compilable_step_(y, grad, exp_avg_sq, exp_avg, group['betas'][0], group['betas'][1], step, lr, eps, decay,
                          group['caution'])

        group['k'] = k + 1
