import os

import torch
from matplotlib import pyplot as plt
from gxl_ai_utils import AiConstant

from . import store_model_class
from . import store_model_name


def load_model(name, **kwargs):
    return store_model_class.store_model_class.get_model_by_name(name, **kwargs)


def loader_checkpoint_by_modelname_epoch(model_name, epochs=None):
    model_dir = AiConstant.OUTPUT_PATH + model_name + "/"
    file_name_list = os.listdir(model_dir)
    file_name_list = [x for x in file_name_list if x.startswith(model_name + '_epoch')]
    if epochs:
        file_with_the_epoch = [x for x in file_name_list if x.startswith(model_name + '_epoch-' + str(epochs))]
        if len(file_with_the_epoch) != 0:
            model_path = model_dir + file_with_the_epoch[-1]
            return loader_checkpoint_by_path(model_path)
    if len(file_name_list) != 0:
        model_path = model_dir + file_name_list[-1]
        return loader_checkpoint_by_path(model_path)
    print('找不到模型参数文件,from store_model.py')
    return None


def loader_checkpoint_by_path(local=AiConstant.OUTPUT_PATH + 'mnist_0_epoch2.pth'):
    outpath = AiConstant.OUTPUT_PATH
    file_name = local.split('/').pop()
    parts = file_name.split('_')
    if len(parts) <= 1:
        print('文件名格式不正确,文件名应为 模型名_epoch{i}.pth,from store_model.py')
        return None
    else:
        parts.pop()
        model_name = '_'.join(parts)
        model = load_model(model_name)
        if model is None:
            print("未找到被加载的模型")
            return None
        # Load the model state_dict
        loaded_state_dict = torch.load(local, map_location=torch.device('cpu'))
        # Remove 'module.' prefix from keys
        new_state_dict = {k.replace('module.', ''): v for k, v in loaded_state_dict.items()}
        # Load the new state_dict into the model
        model.load_state_dict(new_state_dict)
        return model


if __name__ == '__main__':
    """"""
    # test_loader_model()
