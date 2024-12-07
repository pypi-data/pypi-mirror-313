import torch


def Adam(model_params, optim_conf):
    """
    optim: adam
    optim_conf:
        lr: 0.001
    :param model_params:
    :param optim_conf:
    :return:
    """
    optimizer = torch.optim.Adam(model_params, **optim_conf)
    return optimizer

def AdamW(model_params, optim_conf):
    """
    optim: adamw
    optim_conf:
        lr: 8.e-4
        weight_decay: 4.e-5
    :param model_params:
    :param optim_conf:
    :return:
    """
    optimizer = torch.optim.AdamW(model_params, **optim_conf)
    return optimizer