import os.path
import random


import numpy as np
import torch
from torch import nn
import time


def set_parameter_requires_grad(model, feature_extracting):
    """是否提取预训练模型的参数,如果提取,则该参数不再更新"""
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False


def create_instance_by_name(module_name, class_name, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(**kwargs)
    return obj


def put_data_to_device(*args):
    device = args[-1]
    res = list()
    for i in range(len(args) - 1):
        X = args[i]
        res.append(X.to(device))
    return tuple(res)


def print_attributes_of_object(obj):
    """打印指定对象的属性名-属性值"""
    attribute_names = dir(obj)
    # 打印属性名和对应的属性值
    for name in attribute_names:
        if not name.startswith('__'):  # 排除特殊方法和属性
            value = getattr(obj, name)
            print(f"Attribute: {name}, Value: {value}")


def get_attributes_of_object_to_dict(obj):
    """打印指定对象的属性名-属性值"""
    dict = {}
    attribute_names = dir(obj)
    # 打印属性名和对应的属性值
    for name in attribute_names:
        if not name.startswith('__'):  # 排除特殊方法和属性
            value = getattr(obj, name)
            dict[name] = value
    return dict


def set_random_seed(seed, cuda=True):
    """
    设置训练的随机种子
    """
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    if cuda:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def grad_clipping(net, theta):
    """Clip the gradient."""
    if isinstance(net, nn.Module):
        params = [p for p in net.parameters() if p.requires_grad]
    else:
        params = net.params
    norm = torch.sqrt(sum(torch.sum((p.grad ** 2)) for p in params))
    if norm > theta:
        for param in params:
            param.grad[:] *= theta / norm


def get_model_param_num(model):
    """
    存在打印行为
    得到：
    总参数数量，在训练的参数数量"""
    total_num = sum(p.numel() for p in model.parameters())
    trainable_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f'total_num: {total_num / 1024 / 1024}M, trainable_num: {trainable_num / 1024 / 1024}M')
    return total_num, trainable_num


def get_output_dim_for_conv(input_dim, kernel_size, stride=1, padding=0, dilation=1):
    """
    得到卷积后的输出维度, 不区分几维度的卷积.
    正确性已得到验证
    """
    return (input_dim + 2 * padding - (dilation * (kernel_size - 1) + 1)) // stride + 1


def get_output_dim_for_multi_conv(input_dim: int, kernel_size: list, stride: list, padding: list, dilation: list):
    assert len(kernel_size) == len(stride) == len(padding) == len(dilation)
    res = input_dim
    for kernel_size, stride, padding, dilation in zip(kernel_size, stride, padding, dilation):
        res = get_output_dim_for_conv(res, kernel_size, stride, padding, dilation)
    return res


def get_receptive_field_size_for_continuous_conv(kernel_sizes: list, strides: list):
    """
    得到连续卷积后的感受野, 不区分几维度的卷积.
    第一层的感受野即为卷积核大小, 后面层的感受野受到前面层的感受野
    正确性得到验证
    .   .   .   .   .   . 第一层
    . . . . . . . . . . . . . . . . .输入
    """
    assert len(kernel_sizes) == len(strides)
    assert len(kernel_sizes) > 0 and len(strides) > 0
    res = kernel_sizes[0]
    for kernel_size, stride in zip(kernel_sizes[1:], strides[1:]):
        res = (kernel_size - 1) * stride + res
    return res



class FormalCheckpoint:
    model_name: str
    model_state_dict: dict
    optimizer_state_dict: dict
    scheduler_state_dict: dict
    epoch: int
    step: int

    @property
    def data_dict(self):
        return {
            "model_state_dict": self.model_state_dict,
            "optimizer_state_dict": self.optimizer_state_dict,
            "scheduler_state_dict": self.scheduler_state_dict,
            "epoch": self.epoch,
            "step": self.step,
        }


def save_checkpoint(model, optimizer, scheduler, epoch, step, sava_dir: str):
    checkpoint = FormalCheckpoint(
        model_name=model.__class__.__name__,
        model_state_dict=model.state_dict(),
        optimizer_state_dict=optimizer.state_dict(),
        scheduler_state_dict=scheduler.state_dict(),
        epoch=epoch,
        step=step,
    ) if scheduler is not None else FormalCheckpoint(
        model_name=model.__class__.__name__,
        model_state_dict=model.state_dict(),
        optimizer_state_dict=optimizer.state_dict(),
        scheduler_state_dict={},
        epoch=epoch,
        step=step,
    )
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    filename = f'checkpoint_{checkpoint.model_name}_epoch_{epoch}_step_{step}_{now_time}.pth'
    save_path = os.path.join(sava_dir, filename)
    torch.save(checkpoint.data_dict, save_path)


def load_checkpoint(model, optimizer, scheduler, pth_file_path, local_rank=0, is_distributed=True):
    checkpoint = torch.load(pth_file_path, map_location=torch.device(
        'cuda:' + str(local_rank) if local_rank >= 0 else 'cpu'))
    epoch = checkpoint['epoch']
    step = checkpoint['step']
    params_with_prefix = checkpoint['model_state_dict']
    if is_distributed:
        params_ready = params_with_prefix
    else:
        params_ready = {k.replace("module.", ""): v for k, v in params_with_prefix.items()}

    model.load_state_dict(params_ready)
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    return epoch, step


def get_model_structure_chart_by_netron(model: torch.nn.Module, input_data: torch.Tensor):
    import netron
    onnx_path = "./onnx_model_name.onnx"
    torch.onnx.export(model, input_data, onnx_path)
    netron.start(onnx_path)


def make_freeze_all_params(model):
    for param in model.parameters():
        param.requires_grad = False
