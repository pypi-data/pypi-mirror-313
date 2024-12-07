import torch
from torch import nn
from .mlp_model import GPTMLP


class GxlAttention(nn.Module):
    def __init__(self, embed_dim=768, num_heads=12):
        super(GxlAttention, self).__init__()

        # Multi-Head Self Attention
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        # Query, Key, and Value projections
        self.c_attn = nn.Conv1d(embed_dim, embed_dim * 3, kernel_size=1, bias=False)
        self.c_proj = nn.Conv1d(embed_dim, embed_dim, kernel_size=1, bias=False)

        # Dropout layers
        self.attn_dropout = nn.Dropout(p=0.1, inplace=False)
        self.resid_dropout = nn.Dropout(p=0.1, inplace=False)

    def forward(self, x):
        # Input x: [batch_size, seq_length, embed_dim]

        batch_size, seq_length, embed_dim = x.size()

        # Project the input into query, key, and value
        qkv = self.c_attn(x.transpose(1, 2))  # [batch_size, 3 * embed_dim, seq_length]
        q, k, v = qkv.chunk(3, dim=1)  # Split into query, key, and value

        # Reshape for multi-head attention
        q = q.view(batch_size, self.num_heads, self.head_dim, seq_length).transpose(2,
                                                                                    3)  # [batch_size, num_heads, seq_length, head_dim]
        k = k.view(batch_size, self.num_heads, self.head_dim, seq_length).transpose(2,
                                                                                    3)  # [batch_size, num_heads, seq_length, head_dim]
        v = v.view(batch_size, self.num_heads, self.head_dim, seq_length).transpose(2,
                                                                                    3)  # [batch_size, num_heads, seq_length, head_dim]

        # Compute attention scores and apply softmax
        attn_scores = torch.matmul(q, k.transpose(-2, -1)) / (
                self.head_dim ** 0.5)  # [batch_size, num_heads, seq_length, seq_length]
        attn_probs = nn.functional.softmax(attn_scores, dim=-1)  # Apply softmax along the last dimension

        # Apply attention dropout
        attn_probs = self.attn_dropout(attn_probs)

        # Compute weighted sum of values
        attn_output = torch.matmul(attn_probs, v)  # [batch_size, num_heads, seq_length, head_dim]

        # Reshape and concatenate heads
        attn_output = attn_output.transpose(2, 3).contiguous().view(batch_size, seq_length,
                                                                    embed_dim)  # [batch_size, seq_length, embed_dim]

        # Project back to model's dimension
        attn_output = self.c_proj(attn_output.transpose(1, 2))  # [batch_size, embed_dim, seq_length]
        attn_output = self.resid_dropout(attn_output)

        # Add residual connection and LayerNorm
        output = x + attn_output
        return output


class GXLMLP(nn.Module):
    def __init__(self, embed_dim=768):
        super(GXLMLP, self).__init__()

        # Point-wise feedforward network
        self.c_fc = nn.Conv1d(embed_dim, embed_dim * 4, kernel_size=1, bias=True)
        self.c_proj = nn.Conv1d(embed_dim * 4, embed_dim, kernel_size=1, bias=True)
        self.act = nn.ReLU()
        # Dropout layer
        self.dropout = nn.Dropout(p=0.081024, inplace=False)

    def forward(self, x):
        # Input x: [batch_size, seq_length, embed_dim]

        # Apply feedforward network and activation
        h = self.act(self.c_fc(x.transpose(1, 2)))  # [batch_size, 4 * embed_dim, seq_length]
        h2 = self.c_proj(h)  # [batch_size, embed_dim, seq_length]

        # Apply dropout
        h2 = self.dropout(h2)

        # Add residual connection
        output = x + h2
        return output


class GPT2Block(nn.Module):
    def __init__(self):
        super(GPT2Block, self).__init__()
        self.ln_1 = nn.LayerNorm(768, eps=1e-05, elementwise_affine=True)
        self.attn = GxlAttention()
        self.ln_2 = nn.LayerNorm(768, eps=1e-05, elementwise_affine=True)
        self.mlp = GPTMLP()

    def forward(self, x):
        # Apply LayerNorm1
        x_normalized = self.ln_1(x)
        # Apply the self-attention mechanism (assuming self.attn is a nn.Module)
        attn_output = self.attn(x_normalized)  # Adjust this line based on input shape
        # Residual connection and LayerNorm2
        x_residual = x + attn_output
        x_normalized_residual = self.ln_2(x_residual)
        # Apply MLP
        mlp_output = self.mlp(x_normalized_residual)  # Adjust this line based on input shape
        # Residual connection and final output
        output = x_residual + mlp_output
        return output


class GXLTransformer(nn.Module):
    def __init__(self):
        super(GXLTransformer, self).__init__()
        self.wte = nn.Embedding(30000, 768)
        self.wpe = nn.Embedding(1024, 768)
        self.drop = nn.Dropout(p=0.1, inplace=False)
        self.h = nn.ModuleList([GPT2Block() for _ in range(12)])
        self.ln_f = nn.LayerNorm(768, eps=1e-05, elementwise_affine=True)

    def forward(self, input_ids):
        # input_ids shape: (batch_size, sequence_length)
        # Embedding
        wte_output = self.wte(input_ids)  # shape: (batch_size, sequence_length, 768)
        b, t, c = wte_output.size()
        # Positional encodings
        wpe_output = self.wpe(torch.arange(t, device=wte_output.device))[None, :, :].expand(b, t, c)
        # wpe_output shape: (batch_size, sequence_length, 768)

        # Combine embeddings and positional encodings
        hidden_states = wte_output + wpe_output
        # hidden_states shape: (batch_size, sequence_length, 768)

        # Apply dropout
        hidden_states = self.drop(hidden_states)
        # hidden_states shape: (batch_size, sequence_length, 768)

        # Loop through GPT2Blocks
        for block in self.h:
            hidden_states = block(hidden_states)
            # hidden_states shape: (batch_size, sequence_length, 768)

        # Apply LayerNorm
        output = self.ln_f(hidden_states)
        # output shape: (batch_size, sequence_length, 768)

        return output
