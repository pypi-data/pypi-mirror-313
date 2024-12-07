from torch import nn
from .scaled_dot_product_attention import ScaledDotProductAttention


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
        if attn_mask:
            attn_mask.repeat(1, num_heads, 1, 1)
        scale = key.size(-1) ** -0.5
        context, attention = self.attn(query, key, value, scale, attn_mask)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, num_heads * dim_per_head)
        output = self.out(context)
        output = self.dropout(output) + residual
        output = self.layer_norm(output)
        return output, attention
