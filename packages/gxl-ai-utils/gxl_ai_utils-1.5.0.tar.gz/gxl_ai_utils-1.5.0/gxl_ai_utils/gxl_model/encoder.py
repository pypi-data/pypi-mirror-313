from typing import List, Tuple

import torch
import torch.nn as nn
from torch import Tensor

from gxl_ai_utils.config.gxl_config import GxlNode

#  tdnn encoder
"""
encoder_config:
    layer_num: int
    output_size: 
"""


class Tdnn(nn.Module):
    def __init__(self, input_size, output_size,
                 num_layers,
                 output_size_list,
                 kernel_size_list,
                 dilation_size_list,):
        super(Tdnn, self).__init__()
        self.tdnn = nn.Sequential()
        self.difference_lens = 0
        for i in range(num_layers):
            self.tdnn.append(
                nn.Conv1d(
                    in_channels=input_size,
                    out_channels=output_size_list[i],
                    kernel_size=kernel_size_list[i],
                    dilation=dilation_size_list[i]
                )
            )
            self.tdnn.append(nn.ReLU(
                inplace=False))  # inplace=False：这表示是否进行原地操作。当设置为False时，
            # 模块会创建一个新的输出张量，而不会修改输入张量。当设置为True时，模块会在原地修改输入张量，节省内存空间。
            self.tdnn.append(nn.BatchNorm1d(output_size_list[i], affine=False))  # affine 是否应用仿射变换
            input_size = output_size_list[i]
            self.difference_lens += dilation_size_list[i] * (kernel_size_list[i] - 1)
        self.output_linear = nn.Linear(output_size_list[-1], output_size)

    def forward(self, x: torch.Tensor, x_lens: torch.Tensor) -> tuple[Tensor, Tensor]:
        x = x.permute(0, 2, 1)  # (N, T, C) -> (N, C, T)
        x = self.tdnn(x)
        x = x.permute(0, 2, 1)  # (N, C, T) -> (N, T, C)
        logits = self.output_linear(x)
        x_lens = x_lens - self.difference_lens
        return logits, x_lens


def test_tdnn():
    input_tensor = torch.rand(3, 92, 80)
    input_lens = torch.tensor([92, 91, 83])
    config = GxlNode.get_config_from_yaml("./config.yaml")
    print(config)
    num_layer = config.encoder_conf.layer_num
    output_size_list = config.encoder_conf.output_size_list
    kernel_size_list = config.encoder_conf.kernel_size_list
    dilation_size_list = config.encoder_conf.dilation_size_list
    model = Tdnn(80, 128, num_layer, output_size_list, kernel_size_list, dilation_size_list)
    output, lens2 = model(input_tensor, input_lens)
    print(output.shape)
    print(lens2.shape)
    print(lens2)
    print(model)


