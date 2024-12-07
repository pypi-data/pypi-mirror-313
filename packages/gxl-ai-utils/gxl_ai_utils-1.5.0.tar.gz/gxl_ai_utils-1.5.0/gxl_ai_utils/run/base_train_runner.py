import os

import torch
import time
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils import AiConstant
from gxl_ai_utils.utils import utils_model


class GxlBaseRunner:
    def __init__(self, model, optim, loss_f, train_loader, config: GxlNode,
                 valid_loader=None, scheduler=None, multi=False,
                 local_rank=0, is_class=True,
                 device=torch.device('cpu')):
        self.model = model
        self.optim = optim
        self.scheduler = scheduler
        self.config = config
        self.loss_f = loss_f
        self.device = device

        self.train_loader = train_loader
        self.valid_loader = valid_loader

        self.multi = multi
        self.local_rank = local_rank
        self.is_class = is_class
        self.logger = AiConstant.AI_LOGGER(config.logger.log_file)
        if not self.multi:
            self.model.to(self.device)
        else:
            self.device = self.model.device  # 此时model不是nn.Module ,而是分布式模型对象,有device属性
        self.logger.info(f'使用设备: {self.model.device if self.multi else self.device}')

    def run(self, epochs=None):
        if epochs is None:
            epochs = self.config.train.epochs
        self.model.train()
        start_time = time.time()
        if self.config.checkpoint.load_path:
            epoch, step = self.load_checkpoint(self.config.checkpoint.load_path)
            self.train_function(epochs, epoch, step)  # 训练过程函数，自定义
        else:
            self.train_function(epochs)
        end_time = time.time()
        duration = end_time - start_time
        if self.local_rank == 0:
            self.logger.info(f'训练完毕！用时:{duration:.2f}s,平均{duration * 1.0 / epochs:.2f}s/epoch')

    def train_function(self, epochs, start_epoch=0, start_step=-1):
        """
        start_epoch,和start_step来自已保存的checkpoint,其当前的step已经被执行过了
        """
        full_step = len(self.train_loader)
        if (start_step + 1) >= full_step:
            start_epoch += 1
        for epoch in range(start_epoch, epochs):
            step = (start_step + 1) % full_step
            init_step = step
            st = time.time()
            epoch_accumulate_loss = 0
            for i, batch in enumerate(self.train_loader):
                # if i < step:
                #     if self.local_rank ==0:
                #         self.logger.info(f'epoch:{epoch};start_step:{init_step};skip batch:{i}/{full_step}')
                #     continue
                if step >= full_step:
                    break
                step_st = time.time()
                self.model.train()
                self.optim.zero_grad()
                loss = self.handle_batch(batch)
                if isinstance(loss, torch.Tensor):
                    loss = loss.sum().item()
                epoch_accumulate_loss += loss
                step_et = time.time()
                if self.local_rank == 0:
                    self.log_step(epoch, step, full_step, loss, step_et - step_st)
                    self.checkpoint_save_step(epoch, step, )
                step += 1

            epoch_train_loss = epoch_accumulate_loss / (full_step - init_step)
            et = time.time()
            if self.local_rank == 0:
                self.log_epoch(epoch, epoch_train_loss, (et - st))
                self.checkpoint_save_epoch(epoch, full_step)

    def checkpoint_save_epoch(self, epoch, full_step):
        if self.config.checkpoint.save_level == 'epoch' and epoch % self.config.checkpoint.save_interval == 0:
            self.save_checkpoint(epoch, full_step - 1)

    def checkpoint_save_step(self, epoch, step):
        if self.config.checkpoint.save_level == 'step' and step % self.config.checkpoint.save_interval == 0:
            self.save_checkpoint(epoch, step)

    def _handle_log_valid(self, epoch):
        st = time.time()
        valid_loss = 0
        do_valid = False
        if epoch % self.config.train.valid_interval == 0:
            do_valid = True
        try:
            valid_loss = self.calculate_valid_loss()
        except Exception as e:
            do_valid = False

        do_accuracy = do_valid and self.is_class
        valid_accuracy = 0
        try:
            valid_accuracy = self.calculate_valid_accuracy()
        except RuntimeError | BaseException:
            do_accuracy = False
        et = time.time()
        time_internal = et - st
        return do_valid, do_accuracy, valid_loss, valid_accuracy, time_internal

    def log_epoch(self, epoch, epoch_train_loss, time_interval_one):
        if (self.config.train.log_level == 'epoch' and
                epoch % self.config.train.log_interval == 0):
            do_valid, do_accuracy, valid_loss, valid_accuracy, valid_time_internal = self._handle_log_valid(epoch)
            consume_time = time_interval_one * self.config.train.log_interval + valid_time_internal if epoch != 0 else time_interval_one + valid_time_internal
            if do_accuracy:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};valid_loss:{valid_loss:.6f};'
                    f'valid_accuracy:{valid_accuracy:.6f};consume_time:{consume_time :.4f}s')
            elif do_valid:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};valid_loss:{valid_loss:.6f};'
                    f'consume_time:{consume_time :.4f}s')
            else:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};consume_time:{consume_time:.4f}s')
        elif self.config.train.log_level == 'step':
            do_valid, do_accuracy, valid_loss, valid_accuracy, valid_time_internal = self._handle_log_valid(epoch)
            if do_accuracy:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};valid_loss:{valid_loss:.6f};valid_accuracy:{valid_accuracy:.6f};consume_time:{valid_time_internal:.4f}s')
            elif do_valid:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};valid_loss:{valid_loss:.6f};consume_time:{valid_time_internal:.4f}s')
            else:
                self.logger.info(
                    f'epoch{epoch};train_loss:{epoch_train_loss:.6f};consume_time:{valid_time_internal:.4f}s')

    def log_step(self, epoch, step, full_step, loss, time_interval_one):
        if self.config.train.log_level == 'step' and step % self.config.train.log_interval == 0:
            time_interval = time_interval_one * self.config.train.log_interval if step != 0 else time_interval_one
            self.logger.info(
                f'epoch:{epoch};step{step}/{full_step};train_loss:{loss:.6f};consume_time:{time_interval:.4f}s')

    def calculate_valid_loss(self):
        raise NotImplementedError()

    def calculate_valid_accuracy(self, dataloader: torch.utils.data.DataLoader = None):
        raise NotImplementedError()

    def handle_batch(self, batch):
        raise NotImplementedError()

    def save_checkpoint(self, epoch, step):
        file_dir = self.config.checkpoint.save_dir
        os.makedirs(file_dir, exist_ok=True)
        self.logger.info(f'保存checkpoint到{file_dir},所保存的checkpoint为: epoch_{epoch}_step_{step}.pth')
        utils_model.save_checkpoint(self.model, self.optim, self.scheduler, epoch, step, file_dir)

    def load_checkpoint(self, load_path: str):
        if not os.path.exists(load_path):
            self.logger.error('No checkpoint found at %s, not load checkpoint' % load_path)
            return 0, -1
        self.logger.info('load checkpoint from %s' % load_path)
        if self.device == torch.device('cpu'):
            return utils_model.load_checkpoint(self.model, self.optim, self.scheduler, load_path,
                                                  local_rank=-1, is_distributed=False)
        epoch, step = utils_model.load_checkpoint(self.model, self.optim, self.scheduler, load_path,
                                                  local_rank=self.local_rank, is_distributed=self.multi)
        return epoch, step

    def inference(self, data_loader: torch.utils.data.DataLoader, jsonl_file_path: str):
        raise NotImplementedError()

    @staticmethod
    def accuracy(y_hat: torch.Tensor, y: torch.Tensor):
        """
        计算一个个batch的正确率
        y_hat: (batch, num_classes)
        y: (batch,)
        """
        # 返回每一行中最大元素的索引，也就是对每个样本预测的类别。其中，axis=1表示按行计算。具体来说，
        # 如果y_hat的shape为(n_samples,n_classes)，那么y_hat.argmax(dim=1)的shape就为
        # (n_samples,)，其中每个元素是一个整数，表示对应样本的预测类别。
        if len(y_hat.shape) > 1 and y_hat.shape[0] > 1:
            y_hat = y_hat.argmax(dim=1)
        one_hot_array_one_dim = y_hat.type(y.dtype) == y
        sums = float(one_hot_array_one_dim.type(y.dtype).sum())
        return sums / len(y)
