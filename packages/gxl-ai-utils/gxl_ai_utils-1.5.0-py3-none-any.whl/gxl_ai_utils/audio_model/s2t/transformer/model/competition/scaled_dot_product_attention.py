import torch
from torch import nn
import numpy as np


class ScaledDotProductAttention(nn.Module):
    """
    Scaled Dot-Product Attention
    缩放 点积 注意力
    """
    def __init__(self, attention_dropout=0.0):
        super().__init__()
        self.softmax = nn.Softmax(dim=2)
        self.dropout = nn.Dropout(attention_dropout)

    def forward(self, q, k, v, scale=None, attn_mask=None):
        """
        q: query , (B,h, T_q, D_q)
        k: key    , (B,h, T_k, D_k)
        v: value  , (B,h, T_v, D_v), 这里在实现上认为D_q=D_k, T_k=T_v
        scale: 缩放因子, int
        attn_mask: (B,h, T_q, T_k), bool, 在需要遮蔽的地方设为true
        return:
            context: (B,h, T_q, D_v),
            attention: (B,h, T_q, T_k)
        """
        attention = torch.bmm(q, k.transpose(1, 2))
        if scale:
            attention = scale * attention
        if attn_mask is not None:
            attention = attention.masked_fill_(attn_mask, -np.inf)
        attention = self.softmax(attention)
        attention = self.dropout(attention)
        context = torch.bmm(attention, v)
        return context, attention
