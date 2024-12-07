from typing import List, Union

import math
import warnings
import torch
from numpy.matlib import empty
from torch.optim.lr_scheduler import LRScheduler


class WarmupLR(LRScheduler):
    """
    scheduler: warmuplr
    scheduler_conf:
      warmup_steps: 100000

    The WarmupLR scheduler

    This scheduler is almost same as NoamLR Scheduler except for following
    difference:

    NoamLR:
        lr = optimizer.lr * model_size ** -0.5
             * min(step ** -0.5, step * warmup_step ** -1.5)
    WarmupLR:
        lr = optimizer.lr * warmup_step ** 0.5
             * min(step ** -0.5, step * warmup_step ** -1.5)
        #  step * warmup_step ** -1.5 在step 小于 warmup_step的时候，是小值，因为x^-1.5是递减的。。对于这个项，只有step是变量，是个单调正比递增的
        # step**0.5  = step * step**-1.5 ,在step大于warmup_step时，该值更小 。 也就是step**0.5,是个递减的项

    Note that the maximum lr equals to optimizer.lr in this scheduler.

    """
    def __init__(self, optimizer: torch.optim.Optimizer,
                 warmup_step: Union[int, float, List[Union[int, float]]] = 25000,
                 last_epoch: int = -1):
        self.warmup_steps = warmup_step
        # __init__() must be invoked before setting field
        # because step() is also invoked in __init__()
        super.__init__(optimizer, last_epoch)

    def __repr__(self):
        return f"{self.__class__.__name__}(warmup_steps={self.warmup_steps})"

    def get_lr(self):
        step_num = self.last_epoch +1
        warmup_steps = self.warmup_steps
        if not isinstance(self.warmup_steps, List):
            warmup_steps = [warmup_steps] * len(self.base_lrs)
        def initlr_fr(lr):
            return lr * step_num **-0.5

        def warmuplr_fn(lr, warmup_step):
            return lr * warmup_step**-0.5 * min(step_num**-0.5, step_num * warmup_steps**-1.5)

        return [
            initlr_fr(lr) if warmup_steps[i] ==0 else warmuplr_fn(lr, warmup_steps[i])
            for (i,lr) in enumerate(self.base_lrs)
        ]

    def set_step(self, step: int):
        self.last_epoch = step



