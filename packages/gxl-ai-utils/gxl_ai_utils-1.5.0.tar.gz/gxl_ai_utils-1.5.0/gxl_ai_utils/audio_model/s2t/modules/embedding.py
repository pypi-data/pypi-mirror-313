import math
from typing import Tuple

import torch
import torch.nn as nn


class PositionalEncodingInterface:
    def forward(self, x: torch.Tensor,
                offset: int = 0) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute positional encoding.
        Args:
            x (Tensor): Input tensor (batch, time, `*`).
            offset (int, optional): start offset. Defaults to 0.
        Returns:
            Tensor: Encoded tensor (batch, time, `*`).
            Tensor: Positional embedding tensor (1, time, `*`).
        """
        raise NotImplementedError("forward method is not implemented")

    def position_encoding(self, offset: int, size: int) -> torch.Tensor:
        """ For getting encoding in a streaming fashion
        Args:
            offset (int): start offset
            size (int): requried size of position encoding
        Returns:
            Tensor: Corresponding position encoding
        """
        raise NotImplementedError("position_encoding method is not implemented")


class PositionalEncoding(nn.Module, PositionalEncodingInterface):
    """
    位置编码嵌入层
    """

    def __init__(self,
                 d_model: int,
                 dropout_rate: float,
                 max_len: int = 5000,
                 reverse: bool = False):
        """Positional encoding.
            PE(pos, 2i)   = sin(pos/(10000^(2i/dmodel)))
            PE(pos, 2i+1) = cos(pos/(10000^(2i/dmodel)))
        Args:
            d_model (int): embedding dim.
            dropout_rate (float): dropout rate.
            max_len (int, optional): maximum input length. Defaults to 5000.
            reverse (bool, optional): Not used. Defaults to False.
        """
        nn.Module.__init__(self)
        self.d_model = d_model
        self.max_len = max_len
        self.xscale = torch.tensor(math.sqrt(self.d_model))
        self.dropout = nn.Dropout(p=dropout_rate)
        self.base = torch.tensor(10000.0)
        self.pe = torch.zeros([1, self.max_len, self.d_model])  # [B=1,T,D]

        position = torch.arange(
            0, self.max_len, dtype=torch.float32).unsqueeze(1)  # [T, 1]
        # base^{-2(i-1)/d)}, i \in (1,2...,d/2)
        div_term = torch.exp(
            -torch.arange(0, self.d_model, 2, dtype=torch.float32) *
            (torch.log(self.base) / self.d_model))

        # [B,T,D]
        self.pe[:, :, 0::2] = torch.sin(position * div_term)
        self.pe[:, :, 1::2] = torch.cos(position * div_term)

    def forward(self, x: torch.Tensor,
                offset: int = 0) -> Tuple[torch.Tensor, torch.Tensor]:
        """Add positional encoding.
        Args:
            x (torch.Tensor): Input. Its shape is (batch, time, ...)
            offset (int): position offset
        Returns:
            torch.Tensor: Encoded tensor. Its shape is (batch, time, ...)
            torch.Tensor: for compatibility to RelPositionalEncoding, (batch=1, time, ...)
        """
        assert offset + x.shape[
            1] < self.max_len, "offset: {} + x.shape[1]: {} is larger than the max_len: {}".format(
            offset, x.shape[1], self.max_len)
        pos_emb = self.pe[:, offset:offset + x.shape[1]]
        x = x * self.xscale + pos_emb
        return self.dropout(x), self.dropout(pos_emb)

    def position_encoding(self, offset: int, size: int) -> torch.Tensor:
        """ For getting encoding in a streaming fashion
        Attention!!!!!
        we apply dropout only once at the whole utterance level in a none
        streaming way, but will call this function several times with
        increasing input size in a streaming scenario, so the dropout will
        be applied several times.
        Args:
            offset (int): start offset
            size (int): requried size of position encoding
        Returns:
            torch.Tensor: Corresponding position encoding, #[1, T, D].
        """
        assert offset + size < self.max_len
        return self.dropout(self.pe[:, offset:offset + size])


class RelPositionalEncoding(PositionalEncoding):
    """Relative positional encoding module.
    在相对位置编码中, 返回的x只是除以一个常数, 并没有加上嵌入值
    See : Appendix B in https://arxiv.org/abs/1901.02860
    """

    def __init__(self, d_model: int, dropout_rate: float, max_len: int = 5000):
        """
        Args:
            d_model (int): Embedding dimension.
            dropout_rate (float): Dropout rate.
            max_len (int, optional): [Maximum input length.]. Defaults to 5000.
        """
        super().__init__(d_model, dropout_rate, max_len, reverse=True)

    def forward(self, x: torch.Tensor,
                offset: int = 0) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute positional encoding.
        Args:
            x (torch.Tensor): Input tensor (batch, time, `*`).
        Returns:
            torch.Tensor: Encoded tensor (batch, time, `*`).
            torch.Tensor: Positional embedding tensor (1, time, `*`).
        """
        assert offset + x.shape[
            1] < self.max_len, "offset: {} + x.shape[1]: {} is larger than the max_len: {}".format(
            offset, x.shape[1], self.max_len)

        x = x * self.xscale
        pos_emb = self.pe[:, offset:offset + x.shape[1]]
        return self.dropout(x), self.dropout(pos_emb)
