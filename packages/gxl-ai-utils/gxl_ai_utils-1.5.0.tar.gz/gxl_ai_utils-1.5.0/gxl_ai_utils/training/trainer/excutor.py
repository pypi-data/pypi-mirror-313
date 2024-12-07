import copy
import datetime
import sys
from contextlib import nullcontext


import torch
from gxl_ai_utils.training.trainer.utils_for_excutor import do_training_join, do_batch_forward, do_batch_backward, \
    do_update_parameter_and_lr, log_per_step, save_model
from gxl_ai_utils.training.trainer.utils_for_excutor import GxlStepTimer
from gxl_ai_utils.utils import utils_file
class Executor:
    def __init__(self, global_step:int=0,
                 device: torch.device = torch.device('cpu')):
        """"""
        self.step = global_step + 1
        self.train_step_timer = None
        self.cv_step_timer = None
        self.device = device

    def train(self,
              model,
              optimizer,
              scheduler,
              scaler,
              configs,
              writer,
              group_join,
              train_data_loader,
              cv_data_loader):
        """
        训一个epoch
        :return:
        """
        if self.train_step_timer is None:
            self.train_step_timer = GxlStepTimer(self.step)
        model.train()
        info_dict = copy.deepcopy(configs)
        utils_file.logging_info('使用梯度累计， 新的batch_size是之前的{}倍'.format(info_dict['accum_grad']))
        if isinstance(model, torch.nn.parallel.DistributedDataParallel):
            model_context = model.join
        else:
            model_context = nullcontext
        info_dict['tag'] = 'TRAIN'
        with model_context():
            for batch_idx, batch in enumerate(train_data_loader):
                info_dict['step'] = self.step
                info_dict['batch_idx'] = batch_idx
                if do_training_join(group_join, info_dict):
                    break
                if batch['target_lengths'].size(0) == 0:
                    continue
                if info_dict['train_engine'] in ['torch_ddp','torch_fsdp'] and (batch_idx+1)%info_dict['accum_grad']!=0:
                    no_sync_context = model.no_sync # 不到梯度累计的时候，就不进行梯度同步
                else:
                    no_sync_context = nullcontext
                with no_sync_context():
                    info_dict = do_batch_forward(model, batch, scaler, info_dict, self.device)
                    info_dict = do_batch_backward(model, scaler, info_dict)
                # loss.backward()反向传导后才具有梯度，但是并不会更改参数，需要自己手动根据梯度进行参数更改，也就是该函数所做的事情
                info_dict = do_update_parameter_and_lr(model, optimizer, scheduler, scaler, info_dict)
                log_per_step(writer, info_dict, timer=self.train_step_timer)
                save_interval = info_dict.get('save_interval', sys.maxsize)
                if (self.step +
                    1) % save_interval == 0 and self.step != 0 and (
                        batch_idx + 1) % info_dict["accum_grad"] == 0:
                    import torch.distributed as dist
                    # Ensure all ranks start CV at the same time in step mode
                    dist.barrier()
                    loss_dict = self.cv(model, cv_data_loader, configs)
                    model.train()
                    info_dict.update({
                        "tag":
                            "step_{}".format(self.step),
                        "loss_dict":
                            loss_dict,
                        "save_time":
                            datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                        "lrs":
                            [group['lr'] for group in optimizer.param_groups]
                    })
                    save_model(model, info_dict)
                    # write final cv: tensorboard
                    log_per_step(writer, info_dict)
                    # Ensure all ranks start Train at the same time in step mode
                    dist.barrier()
                self.step += 1 if (batch_idx +
                                   1) % info_dict["accum_grad"] == 0 else 0






    def cv(self, model, cv_data_loader, configs):
        """"""
        if self.cv_step_timer is None:
            self.cv_step_timer = GxlStepTimer(0.0)
        else:
            self.cv_step_timer.last_iteration = 0.0
        model.eval()
        info_dict = copy.deepcopy(configs)
        num_seen_utts, loss_dict, total_acc = 1, {}, []  # avoid division by 0
        with torch.no_grad():
            for batch_idx, batch_dict in enumerate(cv_data_loader):
                info_dict["tag"] = "CV"
                info_dict["step"] = self.step
                info_dict["batch_idx"] = batch_idx
                info_dict["cv_step"] = batch_idx

                num_utts = batch_dict["target_lengths"].size(0)
                if num_utts == 0:
                    continue

                info_dict = do_batch_forward(model, batch_dict,  info_dict,None,
                                          self.device)
                _dict = info_dict["loss_dict"]

                num_seen_utts += num_utts
                total_acc.append(_dict['th_accuracy'].item(
                ) if _dict.get('th_accuracy', None) is not None else 0.0)
                for loss_name, loss_value in _dict.items():
                    if loss_value is not None and "loss" in loss_name \
                            and torch.isfinite(loss_value):
                        loss_value = loss_value.item()
                        loss_dict[loss_name] = loss_dict.get(loss_name, 0) + \
                                               loss_value * num_utts
                # write cv: log
                log_per_step(writer=None,
                             info_dict=info_dict,
                             timer=self.cv_step_timer)
        for loss_name, loss_value in loss_dict.items():
            loss_dict[loss_name] = loss_dict[loss_name] / num_seen_utts
        loss_dict["acc"] = sum(total_acc) / len(total_acc)
        return loss_dict


