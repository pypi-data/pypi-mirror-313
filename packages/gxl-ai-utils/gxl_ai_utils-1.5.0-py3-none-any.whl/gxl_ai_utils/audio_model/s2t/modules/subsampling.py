from typing import Tuple

import torch
from torch import nn
from .embedding import PositionalEncoding
from gxl_ai_utils.utils import utils_model


class BaseSubsampling(nn.Module):
    def __init__(self, pos_enc_class: PositionalEncoding):
        super().__init__()
        self.pos_enc = pos_enc_class
        # window_size = (1 + right_context) + (chunk_size -1) * subsampling_rate
        self.right_context = 0
        # stride = subsampling_rate * chunk_size
        self.subsampling_rate = 1

    def position_encoding(self, offset: int, size: int) -> torch.Tensor:
        return self.pos_enc.position_encoding(offset, size)


class Conv2dSubsampling(BaseSubsampling):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Conv2dSubsampling4(Conv2dSubsampling):
    """Convolutional 2D subsampling (to 1/4 length)."""

    def __init__(self,
                 idim: int,
                 odim: int,
                 dropout_rate: float,
                 pos_enc_class: PositionalEncoding = None):
        """Construct an Conv2dSubsampling4 object.

        Args:
            idim (int): Input dimension.
            odim (int): Output dimension.
            dropout_rate (float): Dropout rate.
        """
        if pos_enc_class is None:
            pos_enc_class = PositionalEncoding(odim, dropout_rate)
        super().__init__(pos_enc_class)
        self.conv = nn.Sequential(
            nn.Conv2d(1, odim, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(odim, odim, kernel_size=3, stride=2),
            nn.ReLU(), )
        self.out = nn.Sequential(
            #  计算公式: (input - filter + 2 * padding)/stride + 1
            nn.Linear(odim * (((idim - 1) // 2 - 1) // 2), odim))
        self.subsampling_rate = 4
        # The right context for every conv layer is computed by:
        # (kernel_size - 1) * frame_rate_of_this_layer
        # 6 = (3 - 1) * 1 + (3 - 1) * 2
        self.right_context = 6

    def forward(self, x: torch.Tensor, x_mask: torch.Tensor, offset: int = 0
                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Subsample x.
        Args:
            x (torch.Tensor): Input tensor (#batch, time, idim).
            x_mask (torch.Tensor): Input mask (#batch, 1, time).
            offset (int): position encoding offset.
        Returns:
            torch.Tensor: Subsampled tensor (#batch, time', odim),
                where time' = time // 4.
            torch.Tensor: positional encoding
            torch.Tensor: Subsampled mask (#batch, 1, time'),
                where time' = time // 4.
        """
        x = x.unsqueeze(1)  # (b, c=1, t, f)
        x = self.conv(x)
        b, c, t, f = x.shape
        x = self.out(x.transpose(2, 1).reshape(b, -1, c * f))
        x, pos_emb = self.pos_enc(x, offset)
        return x, pos_emb, x_mask[:, :, :-2:2][:, :, :-2:2]


class Conv2dSubsampling4Pure(Conv2dSubsampling4):
    """
    纯粹的conv2d subsampling, 不考虑位置编码和mask
    """

    def __init__(self, idim, odim, dropout_rate):
        super().__init__(idim, odim, dropout_rate, None)
        self.output_dim = utils_model.get_output_dim_for_conv(utils_model.get_output_dim_for_conv(idim, 3, 2), 3,
                                                              2) * odim
        self.receptive_field_length = utils_model.get_receptive_field_size_for_continuous_conv([3, 3], [2, 2])

    def forward(self, x: torch.Tensor, x_len: torch.Tensor
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        x = x.unsqueeze(1)  # (b, c=1, t, f)
        x = self.conv(x)
        b, c, t, f = x.shape
        x = x.transpose(2, 1).reshape(b, -1, c * f)  # (b, t, f*c)
        x_len = utils_model.get_output_dim_for_conv(utils_model.get_output_dim_for_conv(x_len, 3, 2), 3,
                                                    2)
        return x, x_len


class Conv2dSubsampling6(Conv2dSubsampling):
    """Convolutional 2D subsampling (to 1/6 length)."""

    def __init__(self,
                 idim: int,
                 odim: int,
                 dropout_rate: float,
                 pos_enc_class: PositionalEncoding = None):
        """Construct an Conv2dSubsampling6 object.

        Args:
            idim (int): Input dimension.
            odim (int): Output dimension.
            dropout_rate (float): Dropout rate.
        """
        if pos_enc_class is None:
            pos_enc_class = PositionalEncoding(odim, dropout_rate)
        super().__init__(pos_enc_class)
        self.conv = nn.Sequential(
            nn.Conv2d(1, odim, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(odim, odim, kernel_size=5, stride=3),
            nn.ReLU(), )
        conv_output_dim = utils_model.get_output_dim_for_conv(utils_model.get_output_dim_for_conv(idim, 3, 2), 5, 3)
        self.out = nn.Sequential(
            #  计算公式: (input - filter + 2 * padding)/stride + 1
            nn.Linear(odim * conv_output_dim, odim))
        # The right context for every conv layer is computed by:
        # (kernel_size - 1) * frame_rate_of_this_layer
        # 10 = (3 - 1) * 1 + (5 - 1) * 2
        self.subsampling_rate = 6
        self.right_context = 10

    def forward(self, x: torch.Tensor, x_mask: torch.Tensor, offset: int = 0
                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Subsample x.
        Args:
            x (paddle.Tensor): Input tensor (#batch, time, idim).
            x_mask (paddle.Tensor): Input mask (#batch, 1, time).
            offset (int): position encoding offset.
        Returns:
            Tensor: Subsampled tensor (#batch, time', odim),
                where time' = time // 6.
            Tensor: positional encoding
            Tensor: Subsampled mask (#batch, 1, time'),
                where time' = time // 6.
        """
        x = x.unsqueeze(1)  # (b, c=1, t, f)
        x = self.conv(x)
        b, c, t, f = x.shape
        x = self.out(x.transpose(2, 1).reshape(b, -1, c * f))
        x, pos_emb = self.pos_enc(x, offset)
        #  关于x_mask的取值: -2 = filter1-1, -4 = filter2-1, 2 = stride1, 3=stride2
        return x, pos_emb, x_mask[:, :, :-2:2][:, :, :-4:3]


class Conv2dSubsampling8(Conv2dSubsampling):
    """Convolutional 2D subsampling (to 1/8 length)."""

    def __init__(self,
                 idim: int,
                 odim: int,
                 dropout_rate: float,
                 pos_enc_class: PositionalEncoding = None):
        """Construct an Conv2dSubsampling8 object.

        Args:
            idim (int): Input dimension.
            odim (int): Output dimension.
            dropout_rate (float): Dropout rate.
        """
        if pos_enc_class is None:
            pos_enc_class = PositionalEncoding(odim, dropout_rate)
        super().__init__(pos_enc_class)
        self.conv = nn.Sequential(
            nn.Conv2d(1, odim, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(odim, odim, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(odim, odim, kernel_size=3, stride=2),
            nn.ReLU(),
        )
        conv_output_dim = utils_model.get_output_dim_for_conv(
            utils_model.get_output_dim_for_conv(utils_model.get_output_dim_for_conv(idim, 3, 2), 3, 2), 3, 2)
        self.out = nn.Sequential(
            #  计算公式: (input - filter + 2 * padding)/stride + 1
            nn.Linear(odim * conv_output_dim, odim))
        # The right context for every conv layer is computed by:
        # (kernel_size - 1) * frame_rate_of_this_layer
        # 14 = (3 - 1) * 1 + (3 - 1) * 2 + (3 - 1) * 4 = 2 + 4 + 8
        self.subsampling_rate = 8
        self.right_context = 14

    def forward(self, x: torch.Tensor, x_mask: torch.Tensor, offset: int = 0
                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Subsample x.
        Args:
            x (paddle.Tensor): Input tensor (#batch, time, idim).
            x_mask (paddle.Tensor): Input mask (#batch, 1, time).
            offset (int): position encoding offset.
        Returns:
            Tensor: Subsampled tensor (#batch, time', odim),
                where time' = time // 8.
            Tensor: positional encoding
            Tensor: Subsampled mask (#batch, 1, time'),
                where time' = time // 8.
        """
        x = x.unsqueeze(1)  # (b, c=1, t, f)
        x = self.conv(x)
        b, c, t, f = x.shape
        x = self.out(x.transpose(2, 1).reshape(b, -1, c * f))
        x, pos_emb = self.pos_enc(x, offset)
        return x, pos_emb, x_mask[:, :, :-2:2][:, :, :-2:2][:, :, :-2:2]
