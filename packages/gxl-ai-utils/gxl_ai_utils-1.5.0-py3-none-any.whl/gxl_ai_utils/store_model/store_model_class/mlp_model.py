import torch
import torch.nn as nn


class GPTMLP(nn.Module):
    def __init__(self, embed_dim=768):
        super(GPTMLP, self).__init__()

        # Point-wise feedforward network
        self.c_fc = nn.Conv1d(embed_dim, embed_dim * 4, kernel_size=1, bias=True)
        self.c_proj = nn.Conv1d(embed_dim * 4, embed_dim, kernel_size=1, bias=True)

        # Activation function (GELU)
        self.act = nn.GELU()

        # Dropout layer
        self.dropout = nn.Dropout(p=0.1, inplace=False)

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
