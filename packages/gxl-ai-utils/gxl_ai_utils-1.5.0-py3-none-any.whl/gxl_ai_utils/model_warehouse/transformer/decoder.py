import torch
from torch import nn

from .component import MultiHeadAttention
from .component import PositionalEncoding
from .component import PositionWiseFeedForward
from .component import padding_mask
from .component import sequence_mask


class DecoderLayer(nn.Module):
    def __init__(self, model_dim: int, num_heads: int = 8, ffn_dim: int = 2048, dropout: float = 0.0):
        super(DecoderLayer, self).__init__()
        self.self_attention = MultiHeadAttention(model_dim, num_heads, dropout)
        self.context_attention = MultiHeadAttention(model_dim, num_heads, dropout)
        self.feed_forward = PositionWiseFeedForward(model_dim, ffn_dim, dropout)

    def forward(self, decoder_input, encoder_output,
                self_attn_mask=None, context_attn_mask=None):
        decoder_output, self_attention = self.self_attention(decoder_input, decoder_input,
                                                             decoder_input, self_attn_mask)
        decoder_output, context_attention = self.context_attention(decoder_output, encoder_output,
                                                                   encoder_output, context_attn_mask)
        decoder_output = self.feed_forward(decoder_output)
        return decoder_output, self_attention, context_attention


class Decoder(nn.Module):
    def __init__(self, vocab_size: int, max_seq_len: int,
                 num_layers: int = 6, model_dim: int = 512, num_heads: int = 8, ffn_dim: int = 2048,
                 dropout: float = 0.0, padding_idx: int = 0):
        super(Decoder, self).__init__()
        self.seq_embedding = nn.Embedding(vocab_size, model_dim, padding_idx=padding_idx)
        self.pos_embedding = PositionalEncoding(model_dim, max_seq_len)

        self.num_layers = num_layers

        self.decoder_layers = nn.ModuleList(
            [DecoderLayer(model_dim, num_heads, ffn_dim, dropout) for _ in range(num_layers)])

    def forward(self, input_data, input_lens, encoder_output, context_attn_mask):
        """
        input->
        input_data: (batch_size, seq_len1)
        input_lens: (batch_size, 1)
        encoder_output: (batch_size, seq_len2, model_dim)
        context_attn_mask: (batch_size, seq_len1, seq_len2)
        """
        self_padding_mask = padding_mask(input_data, input_data)
        self_seq_mask = sequence_mask(input_data)
        self_attn_mask = torch.gt(self_seq_mask + self_padding_mask, 0)
        output = self.seq_embedding(input_data)
        output += self.pos_embedding(input_lens)
        self_attentions = []
        context_attentions = []
        for layer in self.decoder_layers:
            output, self_attn, context_attn = layer(output, encoder_output, self_attn_mask, context_attn_mask)
            self_attentions.append(self_attn)
            context_attentions.append(context_attn)
        return output, self_attentions, context_attentions
