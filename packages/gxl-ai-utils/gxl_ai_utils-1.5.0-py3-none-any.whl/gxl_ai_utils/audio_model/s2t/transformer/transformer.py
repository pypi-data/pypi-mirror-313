from torch import nn
from .model.encoder import Encoder
from .model.decoder import Decoder
from .model.utils.padding_mask import padding_mask


class Transformer(nn.Module):
    def __init__(self, src_vocab_size, src_max_len, tgt_vocab_size, tgt_max_len,
                 num_layers=6, model_dim=512, num_heads=8, ffn_dim=2048, dropout=0.2):
        super(Transformer, self).__init__()
        self.encoder = Encoder(src_vocab_size, src_max_len, num_layers, model_dim, num_heads, ffn_dim, dropout)
        self.decoder = Decoder(tgt_vocab_size, tgt_max_len, num_layers, model_dim, num_heads, ffn_dim, dropout)
        self.linear = nn.Linear(model_dim, tgt_vocab_size)
        self.softmax = nn.Softmax(dim=2)

    def forward(self, src_seq, src_len, tgt_seq, tgt_len):
        context_attn_mask = padding_mask(tgt_seq, src_seq)
        encoder_output, encoder_self_attn = self.encoder(src_seq, src_len)
        decoder_output, decoder_self_attn, decoder_context_attn = self.decoder(tgt_seq, tgt_len, encoder_output,
                                                                               context_attn_mask)
        output = self.linear(decoder_output)
        output = self.softmax(output)
        return output, encoder_self_attn, decoder_self_attn, decoder_context_attn

