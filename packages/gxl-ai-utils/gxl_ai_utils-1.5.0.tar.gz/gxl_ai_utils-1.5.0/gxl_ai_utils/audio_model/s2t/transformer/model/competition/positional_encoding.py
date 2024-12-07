import torch
from torch import nn
import numpy as np


class PositionalEncoding(nn.Module):
    """
    Positional encoding
    位置 编码
    """

    def __init__(self, model_dim, max_len):
        super(PositionalEncoding, self).__init__()
        """
        2.0 * (j // 2) : 含义: 得到j的向下取最近偶数的值, 并将整数转为float数, 5->4,6->6, 9->8
        """
        position_encoding = np.array(
            [
                [pos / np.power(10000, 2.0 * (j // 2) / model_dim)
                 for j in range(model_dim)]
                for pos in range(max_len)
            ]
        )
        position_encoding[:, 0::2] = np.sin(position_encoding[:, 0::2])
        position_encoding[:, 1::2] = np.cos(position_encoding[:, 1::2])
        pad_row = torch.zeros([1, model_dim])
        position_encoding = torch.cat([pad_row, torch.from_numpy(position_encoding)])
        self.position_encoding = nn.Embedding(max_len + 1, model_dim)
        self.position_encoding.weight = nn.Parameter(position_encoding, requires_grad=False)

    def forward(self, input_len):
        """
        Args:
            input_len (batch_size, 1): input length
        """
        max_len = torch.max(input_len)
        tensor = torch.cuda.LongTensor if input_len.is_cuda else torch.LongTensor
        input_pos = tensor(
            [list(range(1, lens.item() + 1)) + [0] * (max_len - lens.item()) for lens in input_len]
        )
        return self.position_encoding(input_pos)


if __name__ == '__main__':
    """"""
    model = PositionalEncoding(512, 100)
    print(model.position_encoding.weight.data)
