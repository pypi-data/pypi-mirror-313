import torch
from torch import nn
import numpy as np
import torch.nn.functional as F


def padding_mask(seq_q: torch.Tensor, seq_k: torch.Tensor, pad_id: int = 0):
    """
    根据seq_k 中pad_id的位置， 得到seq_q对于seq_k的padding_attn_mask,
    seq_q 只是提供q_len,并不影响mask的分布,
    input->
    seq_q: (batch_size, len_q)
    seq_k: (batch_size, len_k)
    output->
    mask: (batch_size, len_q, len_k)
    """
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    mask = seq_k.eq(pad_id)
    mask = mask.unsqueeze(1).expand(batch_size, len_q, len_k)
    return mask


def sequence_mask(seq):
    """
    得到一个序列的self-attention的mask
    input->
    seq: [batch_size, seq_len]
    output->
    mask: [batch_size, seq_len, seq_len]
    """
    batch_size, seq_len = seq.size()
    mask = torch.triu(torch.ones((seq_len, seq_len), dtype=torch.uint8, device=seq.device), diagonal=1)
    mask = mask.unsqueeze(0).expand(batch_size, -1, -1)
    return mask


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
        attention = torch.matmul(q, k.transpose(-2, -1))
        if scale:
            attention = scale * attention
        if attn_mask is not None:
            attention = attention.masked_fill_(attn_mask, -np.inf)
        attention = self.softmax(attention)
        attention = self.dropout(attention)
        context = torch.matmul(attention, v)
        return context, attention


class MultiHeadAttention(nn.Module):
    def __init__(self, model_dim=512, num_heads=8, dropout=0.0):
        super(MultiHeadAttention, self).__init__()
        self.dim_per_head = model_dim // num_heads
        self.num_heads = num_heads

        self.query = nn.Linear(model_dim, model_dim)
        self.key = nn.Linear(model_dim, model_dim)
        self.value = nn.Linear(model_dim, model_dim)
        self.out = nn.Linear(model_dim, model_dim)

        self.attn = ScaledDotProductAttention(dropout)

        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(model_dim)

    def forward(self, query, key, value, attn_mask=None):
        """
        query: [batch_size, query_len, model_dim]
        key: [batch_size, key_len, model_dim]
        value: [batch_size, value_len, model_dim]
        attn_mask: [batch_size, query_len, key_len]
        """
        residual = query
        batch_size = query.size(0)
        num_heads = self.num_heads
        dim_per_head = self.dim_per_head

        query = self.query(query)
        key = self.key(key)
        value = self.value(value)
        query = query.view(batch_size, -1, num_heads, dim_per_head).transpose(1, 2)
        key = key.view(batch_size, -1, num_heads, dim_per_head).transpose(1, 2)
        value = value.view(batch_size, -1, num_heads, dim_per_head).transpose(1, 2)
        if attn_mask is not None:
            attn_mask = attn_mask.unsqueeze(1)
            attn_mask = attn_mask.repeat(1, num_heads, 1, 1)
        scale = key.size(-1) ** -0.5
        context, attention = self.attn(query, key, value, scale, attn_mask)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, num_heads * dim_per_head)
        output = self.out(context)
        output = self.dropout(output) + residual
        output = self.layer_norm(output)
        return output, attention


class PositionWiseFeedForward(nn.Module):
    """
    Position-wise feed forward layer
    位置智能 前馈 层
    后置层标准化
    """

    def __init__(self, model_dim=512, ffn_dim=2048, dropout=0.0):
        super(PositionWiseFeedForward, self).__init__()
        self.w1 = nn.Conv1d(model_dim, ffn_dim, 1)
        self.w2 = nn.Conv1d(ffn_dim, model_dim, 1)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(model_dim)

    def forward(self, x):
        """
        :param x: [batch_size, seq_len, model_dim]
        return:
            [batch_size, seq_len, model_dim]
        """
        residual = x
        x = self.w1(x.transpose(1, 2))
        x = F.relu(x)
        x = self.w2(x)
        x = self.dropout(x.transpose(1, 2))
        x = x + residual
        x = self.layer_norm(x)
        return x


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
