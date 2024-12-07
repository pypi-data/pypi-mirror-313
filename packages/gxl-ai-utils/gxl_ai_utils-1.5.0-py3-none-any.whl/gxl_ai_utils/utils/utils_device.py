import torch


def get_a_available_device():
    if not torch.cuda.is_available():
        print('非gpu环境,使用设备:cpu')
        return torch.device('cpu')
    for i in range(torch.cuda.device_count()):
        try:
            return torch.device(f'cuda:{i}')
        except RuntimeError:
            print(f'cuda{i}忙...')
    print('无可用gpu,使用设备:cpu')
    return torch.device('cpu')
