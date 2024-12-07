import torch
from torch.optim.lr_scheduler import LambdaLR

class bWarmupDecayLR(LambdaLR):
    def __init__(self, optimizer, min_lr, warmup_steps=10, decay_steps=20, decay_factor=0.9):
        '''
        先以lr的0.1倍训练warmup_steps,
        然后回到默认的lr,
        每训练decay_steps次lr衰减decay_factor,
        最小不低于min_lr
        :param optimizer:
        :param min_lr:
        :param warmup_steps:
        :param decay_steps:
        :param decay_factor:
        '''
        self.optimizer = optimizer
        self.min_lr = min_lr
        self.warmup_steps = warmup_steps
        self.base_lr = optimizer.param_groups[0]['lr']
        self.warmup_lr = self.base_lr * 0.1
        self.decay_factor = decay_factor
        self.decay_steps = decay_steps

        # 使用LambdaLR调度器来管理学习率
        super().__init__(optimizer, lr_lambda=self.__lr_lambda)

    def __lr_lambda(self, epoch):
        if epoch < self.warmup_steps:
            # 从self.warmup_lr过度到self.base_lr
            lr = self.warmup_lr + (self.base_lr - self.warmup_lr) * (epoch / self.warmup_steps)
            return lr / self.base_lr  # 返回学习率的比例
        else:
            decay_epoch = (epoch - self.warmup_steps) // self.decay_steps
            decay_lr = self.base_lr * (self.decay_factor ** decay_epoch)
            if decay_lr < self.min_lr:
                decay_lr = self.min_lr
            return decay_lr / self.base_lr  # 返回学习率的比例
