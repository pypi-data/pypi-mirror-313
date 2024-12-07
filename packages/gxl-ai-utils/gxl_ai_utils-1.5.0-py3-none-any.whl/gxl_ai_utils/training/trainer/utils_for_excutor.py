import datetime
import os
import re
import time
from contextlib import nullcontext
from typing import Optional, List

import torch.distributed as dist
import torch
import yaml
from sympy import false
from gxl_ai_utils.utils import utils_file

class GxlStepTimer:
    def __init__(self, step):
        self.last_time = None
        self.last_step = step
        self.start()

    def start(self):
        self.last_time = time.time()

    def steps_per_second(self, now_step, restart = True):
        step_used = now_step - self.last_step
        time_used = time.time() - self.last_time
        res = step_used / time_used
        if restart:
            self.start()
            self.last_step = now_step
        return res

def is_torch_npu_available() -> bool:
    '''
        check if torch_npu is available.
        torch_npu is a npu adapter of PyTorch
    '''
    try:
        import torch_npu  # noqa
        return True
    except ImportError:
        if not torch.cuda.is_available():
            print("Module \"torch_npu\" not found. \"pip install torch_npu\" \
                if you are using Ascend NPU, otherwise, ignore it")
    return False

def do_batch_forward(model, batch, info_dict, scaler, device:torch.device):
    """
    就是做一个前项调用， 得到loss_dict, 只是考虑到amp多精度混合训练罢了
    :param model:
    :param batch:
    :param info_dict:
    :param scaler:
    :param device:
    :return:
    """
    dtype = info_dict.get('dtype','fp32')
    train_engine = info_dict.get('train_engine', 'torch_ddp')
    dtype = torch.float16 if dtype == 'fp16' else torch.bfloat16 if dtype == 'bf16' else None
    amp_autocast = torch.cuda.amp.autocast
    if 'npu' in device.__str__() and is_torch_npu_available():
        amp_autocast = torch.npu.amp.autocast
    autocast_context_invoking = {
        'deepspeed': amp_autocast(
            enabled=dtype is not None,
            dtype=dtype,
            cache_enabled=False
        ),
        'torch_ddp': amp_autocast(
            enabled=scaler is not None
        ),
        'torch_fsdp': amp_autocast(
            enabled=True, dtype = dtype
        ) if dtype is not None else nullcontext()
    }[train_engine]
    with autocast_context_invoking:
        loss_dict = model(batch, device)
        info_dict['loss_dict'] = loss_dict
    return loss_dict


def do_tensor2scalar(value):
    if torch.is_tensor(value):
        return value.item()
    return value


def do_batch_backward(model, scaler, info_dict):
    """
    本函数只是将loss取出然后进行.backward(),
    特殊的是，首先需要得到accum_grad,然后将损失除以该值，因为这个loss是单元平均过的，
    进行梯度累计后相当于损失的相加，如果不除以accum_grad，相当于损失被放大了倍数。
    第二个特殊点是，得到train_engine,然后根据引擎的不同进行混合精度下的backward
    :param model:
    :param scaler:
    :param info_dict:
    :return:
    """
    accum_grad = info_dict['accum_grad']
    train_engine = info_dict['train_engine']
    loss = info_dict['loss_dict']['loss']
    scaled_loss = loss / accum_grad
    if train_engine == 'deepspeed':
        scaled_loss = model.backward(loss) # deepspeed 自己的配置中有设置accum_grad
    else:
        if scaler is not None: # ddp策略中的常规混合精度。
            scaler.scale(scaled_loss).batchward()
        else:
            scaled_loss.backward() # fsdp的混合精度或者常规下的不混合
    info_dict['loss_dict']['loss'] = scaled_loss  # 此时loss_dict 中的loss值都是带梯度的完全形态的张量，经过反向后多余的梯度信息就没用了
    # 消除loss值们的张良形态，只保留标量值就行了
    for loss_name, loss_value in info_dict['loss_dict'].items():
        info_dict['loss_dict']['loss_name'] = do_tensor2scalar(loss_value)
    return info_dict

def do_training_join(group_join, info_dict):
    """
    就是做一个多进程的集合点检查， 一定时间内必须所有进程都到达该地点才算集合成功，不然就直接返回true,代表集合失败， 该进程未能在
    规定是timeout时间内到达集合点，将其break掉， 返回true即break
    :param group_join:
    :param info_dict:
    :return:
    """
    world_size = os.environ.get('WORLD_SIZE', 1)
    local_rank = os.environ.get('LOCAL_RANK',0)
    rank = os.environ.get('RANK',0) # 都是用于报错时给出具体进程信息的提示

    if info_dict['batch_idx'] == 0 and info_dict.get('train_engine','torch_ddp')=='torch_ddp':
        """
        说明这是第一个batch,此时由于dataloader需要初始化，很可能很长时间不能进行完，花费时间一般超过30秒，此时的集合超时是
        可以接受和理解的，所以直接返回false,不进行集合点的检查
        """
        return False

    try:
        dist.monitored_barrier(group=group_join,
                               timeout=group_join.options._timeout)
    except RuntimeError as e:
        utils_file.logging_error(f"检测到不均匀的任务量分布，集合点检查失败{e}, world_size：{world_size}, local_rank:{local_rank},rank:{rank}")
        return True
    return False


def do_update_parameter_and_lr(
        model, info_dict, scaler,optimizer, scheduler
):
    """
    进行参数更新和学习率的更新。最简单得来说其实就是将optimizer和scheduler分别进行下.step()就行了，具体来说就是
    先optimizer进行.step()来根据梯度和lr进行参数更新，然后optimizer.zero_grad()进行梯度置零，最后scheduler进行.step()来更新
    optimizer的学习率
    这里的特殊点又3个：
    1. 根据grad_clip的数值进行梯度放缩，防止梯度爆炸
    2. 根据accum_grad的数值选择是否更更新
    3. 对混合精度进行一些特殊处理
    :param model:
    :param info_dict:
    :param scaler:
    :param optimizer:
    :param scheduler:
    :return:
    """
    train_engine= info_dict['train_engine']
    accum_grad = info_dict['accum_grad']
    grad_clip = info_dict['grad_clip']
    batch_idx = info_dict['batch_idx']
    # 因为混合精度和梯度裁剪在deep speed中都有他自己的控制，所有我们什么页不用管
    if train_engine == 'deepspeed':
        info_dict["is_gradient_accumulation_boundary"] = \
            model.is_gradient_accumulation_boundary()
        model.step()
        grad_norm = model.get_global_grad_norm()
    else: # 对于torch_ddp torch_fsdp
        if (batch_idx +1) % accum_grad:
            # 只有这样才要做事情
            #不论如何先进行梯度裁剪
            if train_engine == 'troch_ddp':  # 默认计算第二范数的值，看是不是超过了grad_clip
                grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            else:  # torch_fsdp
                grad_norm = model.clip_grad_norm_(grad_clip)  # 返回梯度的范式
            # 根据是否为多精度进行分别step
            if scaler is None:
                # 最简单的情况，不考虑混合精度
                if torch.isfinite(grad_clip):
                    optimizer.step()
            else:
                # 考虑到混合精度的事情
                scaler.unscale_(optimizer)
                scaler.step(optimizer)
                scaler.update()
            optimizer.zero_grad()
            scheduler.step()
        else:
            grad_norm = 0.0
            pass

    info_dict['lrs'] = [group['lr'] for group in optimizer.param_groups]
    info_dict['grad_norm'] = do_tensor2scalar(grad_norm)
    return info_dict

def lrs_to_str(lrs: List):
    return " ".join(["{:.4e}".format(lr) for lr in lrs])
def log_per_step(writer, info_dict, timer: Optional[GxlStepTimer] = None):
    tag = info_dict["tag"]
    step = info_dict["step"]
    batch_idx = info_dict["batch_idx"]
    loss_dict = info_dict['loss_dict']
    epoch = info_dict.get('epoch', 0)
    train_engine = info_dict.get("train_engine", "torch_ddp")
    accum_grad = info_dict.get('accum_grad', 1) if tag != "CV" else 1
    log_interval = info_dict.get('log_interval', 10)
    lrs = info_dict.get("lrs", [0.0])
    is_gradient_accumulation_boundary = info_dict.get(
        "is_gradient_accumulation_boundary", False)

    rank = int(os.environ.get('RANK', 0))
    # TRAIN Tensorboard
    if tag == "TRAIN" and rank == 0 and writer is not None:
        if (train_engine == "deepspeed" and is_gradient_accumulation_boundary
            ) or (train_engine in ["torch_ddp", "torch_fsdp"] and
                  (batch_idx + 1) % accum_grad == 0):
            writer.add_scalar('train/train_loss',
                              do_tensor2scalar(loss_dict['loss']) * accum_grad,
                              step)
            writer.add_scalar('train/grad_norm', info_dict['grad_norm'], step)
            for name, value in loss_dict.items():
                if name != 'loss' and value is not None:
                    writer.add_scalar('train/{}'.format(name),
                                      do_tensor2scalar(value), step)
            # lr
            for i, lr in enumerate(lrs):
                writer.add_scalar('train/lr_{}'.format(i), lr, step)
    # CV Tensorboard
    elif "step_" in tag and rank == 0 and writer is not None:
        for name, value in loss_dict.items():
            writer.add_scalar('cv/{}'.format(name), do_tensor2scalar(value),
                              step)
        utils_file.logging_info(
            'Epoch {} Step {} CV info lr {} cv_loss {} rank {} acc {}'.format(
                epoch, step + 1, lrs_to_str(lrs),
                do_tensor2scalar(loss_dict["loss"]), rank,
                do_tensor2scalar(loss_dict["acc"])))
        return

    # TRAIN & CV, Shell log (stdout)
    if (batch_idx + 1) % log_interval == 0:
        log_str = '{} | '.format(tag)
        if timer is not None:
            timer_step = step
            if info_dict.get("cv_step", None) is not None:
                timer_step = info_dict['cv_step']
            steps_per_second = timer.steps_per_second(timer_step)
            log_str += 'steps/sec {:.3f}| '.format(steps_per_second)
        log_str += 'Batch {}/{} loss {:.6f} '.format(
            epoch, batch_idx + 1 if 'save_interval' not in info_dict else
            (step + 1) * accum_grad,
            do_tensor2scalar(loss_dict['loss']) * accum_grad)
        for name, value in loss_dict.items():
            if name != 'loss' and value is not None:
                log_str += '{} {:.6f} '.format(name, do_tensor2scalar(value))
        if tag == "TRAIN":
            log_str += 'lr {} grad_norm {:.6f} rank {}'.format(
                lrs_to_str(lrs), info_dict['grad_norm'], rank)
        utils_file.logging_info(log_str)


def log_per_epoch(writer, info_dict):
    epoch = info_dict["epoch"]
    loss_dict = info_dict["loss_dict"]
    lrs = info_dict['lrs']
    rank = int(os.environ.get('RANK', 0))
    step = info_dict["step"]
    utils_file.logging_info(
        'Epoch {} Step {} CV info lr {} cv_loss {} rank {} acc {}'.format(
            epoch, step, lrs_to_str(lrs), do_tensor2scalar(loss_dict["loss"]),
            rank, do_tensor2scalar(loss_dict["acc"])))

    if int(os.environ.get('RANK', 0)) == 0:
        for i, lr in enumerate(info_dict["lrs"]):
            writer.add_scalar('epoch/lr_{}'.format(i), lr, epoch)
        for name, value in loss_dict.items():
            writer.add_scalar('epoch/{}'.format(name), do_tensor2scalar(value),
                              epoch)


def fsdp_save_model(model, save_model_path, info_dict):
    pass

def save_state_dict_and_infos(state_dict, path: str, infos=None):
    rank = int(os.environ.get('RANK', 0))
    utils_file.logging_info('[Rank {}] Checkpoint: save to checkpoint {}'.format(
        rank, path))
    torch.save(state_dict, path)
    info_path = re.sub('.pt$', '.yaml', path)
    if infos is None:
        infos = {}
    infos['save_time'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(info_path, 'w') as fout:
        data = yaml.dump(infos)
        fout.write(data)


def save_checkpoint(model: torch.nn.Module, path: str, infos=None):
    '''
    Args:
        infos (dict or None): any info you want to save.
    '''
    if isinstance(model, torch.nn.DataParallel):
        state_dict = model.module.state_dict()
    elif isinstance(model, torch.nn.parallel.DistributedDataParallel):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    save_state_dict_and_infos(state_dict, path, infos)


def save_model(model, info_dict):
    rank = int(os.environ.get('RANK', 0))
    tag = info_dict["tag"]
    model_dir = info_dict["model_dir"]
    save_model_path = os.path.join(model_dir, '{}.pt'.format(tag))
    # save ckpt
    if info_dict["train_engine"] == "deepspeed":
        # NOTE(xcsong): All ranks should call this API, but only rank 0
        #   save the general model params. see:
        #   https://github.com/microsoft/DeepSpeed/issues/2993
        from deepspeed.utils.zero_to_fp32 import (
            convert_zero_checkpoint_to_fp32_state_dict)
        with torch.no_grad():
            model.save_checkpoint(save_dir=model_dir,
                                  tag=tag,
                                  client_state=info_dict)
            if info_dict["save_states"] == "model_only" and rank == 0:
                convert_zero_checkpoint_to_fp32_state_dict(model_dir,
                                                           save_model_path,
                                                           tag=tag)
                os.system("rm -rf {}/{}".format(model_dir, tag))

    elif info_dict['train_engine'] == "torch_fsdp":
        fsdp_save_model(model, save_model_path, info_dict)
    elif rank == 0:
        # NOTE(xcsong): For torch_ddp, only rank-0 should call this.
        save_checkpoint(model, save_model_path, info_dict)
    # save yaml
    if rank == 0:
        with open("{}/{}.yaml".format(model_dir, tag), 'w') as fout:
            data = yaml.dump(info_dict)
            fout.write(data)
