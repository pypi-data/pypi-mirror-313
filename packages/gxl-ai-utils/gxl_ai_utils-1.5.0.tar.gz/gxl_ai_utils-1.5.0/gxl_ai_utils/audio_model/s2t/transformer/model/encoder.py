from torch import nn
from .competition.multi_head_attention import MultiHeadAttention
from .competition.positional_encoding import PositionalEncoding
from .competition.positional_wise_feed_forward import PositionWiseFeedForward

from .utils.padding_mask import padding_mask


class EncoderLayer(nn.Module):
    def __init__(self, model_dim: int = 512, num_heads: int = 8, ffn_dim: int = 2048, dropout: float = 0.0):
        super(EncoderLayer, self).__init__()
        self.multi_head_attention = MultiHeadAttention(model_dim, num_heads, dropout)
        self.position_wise_feed_forward = PositionWiseFeedForward(model_dim, ffn_dim, dropout)

    def forward(self, input, attn_mask):
        context, attention = self.multi_head_attention(input, input, input, attn_mask)
        output = self.position_wise_feed_forward(context)
        return output, attention


class Encoder(nn.Module):
    """
    input->
    inputs: (batch_size, seq_len)
    input_len: (batch_size, 1)
    output->
    output: (batch_size, seq_len, model_dim)
    attentions: list(num_layers, tensor[batch_size, h, seq_len, seq_len])
    """

    def __init__(self, vocab_size: int, max_seq_lens: int,
                 num_layers: int = 6, model_dim: int = 512, num_heads: int = 8, ffn_dim: int = 2048,
                 dropout: float = 0.0, padding_idx: int = 0):
        super(Encoder, self).__init__()
        self.seq_embedding = nn.Embedding(vocab_size, model_dim, padding_idx=padding_idx)
        self.pos_embedding = PositionalEncoding(model_dim, max_seq_lens)
        self.encoder_layers = nn.ModuleList(
            [EncoderLayer(model_dim, num_heads, ffn_dim, dropout) for _ in range(num_layers)])

    def forward(self, inputs, input_len):
        """
        input->
        inputs: (batch_size, seq_len)
        input_len: (batch_size, 1)
        output->
        output: (batch_size, seq_len, model_dim)
        attentions: list(num_layers, tensor[batch_size, h, seq_len, seq_len])
        """
        output = self.seq_embedding(inputs)
        output += self.pos_embedding(input_len)
        self_attention_mask = padding_mask(inputs, inputs)
        attentions = []
        for layer in self.encoder_layers:
            output, attn = layer(output, self_attention_mask)
            attentions.append(attn)
        return output, attentions
