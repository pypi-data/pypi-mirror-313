from torch import nn
import torch.nn.functional as F


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
