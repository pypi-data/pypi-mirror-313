import torch
from torch import nn
from gxl_ai_utils.utils import utils_file
import torchaudio
from .encoder import Tdnn
from .decoder import LSTMDecoder
from .joiner import Joiner
from .transducer_decode import greedy_search_for_one_batch

class Transducer(nn.Module):
    def __init__(self,
                 encoder,
                 decoder,
                 joiner):
        """"""
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.joiner = joiner

    def forward(self,
                x: torch.Tensor,
                x_lens: torch.Tensor,
                y: torch.Tensor,
                y_lens: torch.Tensor):
        """"""
        assert x.ndim == 3, x.ndim
        assert x_lens.ndim == 1, x_lens.ndim
        assert y.ndim == 2, y.shape[-1]
        assert y_lens.ndim == 1, y_lens.ndim

        blank_id = self.decoder.blank_id
        sos = torch.ones(x.shape[0], 1, dtype=torch.long) * blank_id
        sos_y = torch.cat([sos, y], dim=1)
        sos_y_padded = utils_file.do_padding_ids_by_lens(sos_y, x_lens, blank_id)
        decoder_out, _ = self.decoder(sos_y_padded)

        encoder_out, x_lens = self.encoder(x, x_lens)
        assert torch.all(x_lens >= 0), x_lens
        logits = self.joiner(encoder_out, decoder_out)
        # rnnt_loss need 0 padded targets
        y_padded_with_zero = utils_file.do_padding_ids_by_lens(y, y_lens, 0)
        print(logits.shape)
        print(y_padded_with_zero.shape)
        print(x_lens)
        print(y_lens)
        loss = torchaudio.functional.rnnt_loss(
            logits=logits,
            targets=y_padded_with_zero,
            logit_lengths=x_lens,
            target_lengths=y_lens,
            blank=blank_id,
            reduction='mean'
        )
        return loss

    def decode(self, x, x_lens):
        return greedy_search_for_one_batch(x, x_lens, self)


def test_transducer():
    """"""
    input_tensor = torch.randint(0, 1023, size=(3, 12))
    lengths = torch.randint(5, 12, size=(3,))
    print()
    print(input_tensor)
    print(lengths)
    output_y = utils_file.do_padding_ids_by_lens(input_tensor, lengths, 120)
    print()
    print(output_y)
    input_tensor = torch.randn(3, 5, 8)
    lengths = torch.randint(2, 6, size=(3,))
    print(lengths)
    output_y = utils_file.do_padding_embeds_by_lens(input_tensor, lengths, 10)
    print(output_y)

    x = torch.randn(3, 40, 18)
    x_lens = torch.randint(30, 41, size=(3,), dtype=torch.int32)
    x_lens[-1] = 40
    y = torch.randint(0, 100, size=(3, 10), dtype=torch.int32)
    y_lens = torch.randint(0, 11, size=(3,), dtype=torch.int32)
    y_lens[-1] = 10  # x_lens 和 y_lens必须有一个值顶到最大长度，不然算rnnt_loss时会报错

    encoder = Tdnn(
        input_size=18,
        output_size=32,
        num_layers=3,
        output_size_list=[32, 32, 32],
        kernel_size_list=[3, 5, 5],
        dilation_size_list=[1, 2, 4],
    )
    decoder = LSTMDecoder(
        vocab_size=100,
        num_layers=3,
        hidden_dim=32,
        embedding_dim=32,
        blank_id=0,
        embedding_dropout=0.01,
        rnn_dropout=0.01
    )
    joiner = Joiner(32, 100)
    model = Transducer(encoder, decoder, joiner)
    loss = model(x, x_lens, y, y_lens)
    print(loss)

    res_list = model.decode(x, x_lens)
    print(res_list)
    print(len(res_list))
    print(len(res_list[0]))
    print(len(res_list[1]))
    print(len(res_list[2]))


if __name__ == '__main__':
    test_transducer()
