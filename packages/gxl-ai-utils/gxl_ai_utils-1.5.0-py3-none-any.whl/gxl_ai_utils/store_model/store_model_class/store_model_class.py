import torch
from torch import nn
from torchvision import models
from torchvision.models import ResNet152_Weights, ResNet18_Weights

from gxl_ai_utils import utils

from .rnn_model import *
from .cnn_model import *
from .attention_model import * # 这三个文件中的类对象均可以通过get_model_by_name直接由字符串得到
from .mlp_model import *

class MnistModel0(nn.Module):
    def __init__(self, ) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)  # 28->26
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)  # 26->24
        self.pool = nn.MaxPool2d(kernel_size=2)  # ->减半
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)  # 10 classes for MNIST

    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.pool(x)
        x = x.view(-1, 64 * 5 * 5)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return torch.nn.functional.softmax(x, dim=1)


class ResNet152FlowerModel(nn.Module):
    def __init__(self, output_num=102, feature_extract=True):
        self.resnet_block = models.resnet152(weights=ResNet152_Weights.DEFAULT)
        utils.utils_model.set_parameter_requires_grad(self.resnet_block, feature_extract)
        fc_in = self.resnet_block.fc.in_features
        self.resnet_block.fc = nn.Linear(fc_in, output_num)

    def forward(self, X):
        return self.resnet_block(X)


class ResNet18FlowerModel(nn.Module):
    def __init__(self, output_num=102, feature_extract=True):
        super(ResNet18FlowerModel, self).__init__()
        self.resnet_block = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        utils.utils_model.set_parameter_requires_grad(self.resnet_block, feature_extract)
        fc_in = self.resnet_block.fc.in_features
        self.resnet_block.fc = nn.Linear(fc_in, output_num)

    def forward(self, X):
        return self.resnet_block(X)


def get_model_by_name(name, **kwargs):
    b = utils.utils_model.create_instance_by_name("gxl_ai_utils.store_model.store_model_class.store_model_class", name, **kwargs)
    return b.to(torch.device('cpu'))
