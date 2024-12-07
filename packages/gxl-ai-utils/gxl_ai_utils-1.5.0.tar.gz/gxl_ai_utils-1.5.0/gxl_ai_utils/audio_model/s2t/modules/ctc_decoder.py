from typing import Union, Optional

import torch
import torch.nn as nn
from torch.nn import CTCLoss
import torch.nn.functional as F

from gxl_ai_utils.audio_model.s2t.utils import ctc_utils


class CTCDecoderBase(nn.Module):
    def __init__(self,
                 odim,
                 enc_n_units,
                 blank_id=0,
                 dropout_rate: float = 0.0,
                 reduction: Union[str, bool] = True,
                 batch_average: bool = True,
                 grad_norm_type: Optional[str] = None):
        """CTC decoder

        Args:
            odim ([int]): text.txt vocabulary size
            enc_n_units ([int]): encoder output dimention
            dropout_rate (float): dropout rate (0.0 ~ 1.0)
            reduction (bool): reduce the CTC loss into a scalar, True for 'sum' or 'none'
            batch_average (bool): do batch dim wise average.
            grad_norm_type (str): Default, None. one of 'instance', 'batch', 'frame', None.
        """
        super().__init__()

        self.probs = None  # 正式的概率形式
        self.blank_id = blank_id
        self.odim = odim
        self.dropout = nn.Dropout(dropout_rate)
        self.ctc_lo = nn.Linear(enc_n_units, self.odim)
        if isinstance(reduction, bool):
            reduction_type = "sum" if reduction else "none"
        else:
            reduction_type = reduction
        self.criterion = CTCLoss(
            blank=self.blank_id,
            reduction=reduction_type,
        )

    def forward(self, hs_pad, hlens, ys_pad, ys_lens):
        """Calculate CTC loss.

        Args:
            hs_pad (Tensor): batch of padded hidden state sequences (B, Tmax, D)
            hlens (Tensor): batch of lengths of hidden state sequences (B)
            ys_pad (Tensor): batch of padded character id sequence tensor (B, Lmax)
            ys_lens (Tensor): batch of lengths of character sequence (B)
        Returns:
            loss (Tensor): ctc loss value, scalar.
        """
        logits = self.ctc_lo(self.dropout(hs_pad))
        loss = self.criterion(logits.transpose(0, 1), ys_pad, hlens, ys_lens)
        return loss

    def softmax(self, eouts: torch.Tensor, temperature: float = 1.0):
        """Get CTC probabilities.
        Args:
            eouts (FloatTensor): `[B, T, enc_units]`
            temperature (float): softmax temperature
        Returns:
            probs (FloatTensor): `[B, T, odim]`
        """
        self.probs = F.softmax(self.ctc_lo(eouts) / temperature, dim=2)
        return self.probs

    def log_softmax(self, hs_pad: torch.Tensor,
                    temperature: float = 1.0) -> torch.Tensor:
        """log_softmax of frame activations
        Args:
            Tensor hs_pad: 3d tensor (B, Tmax, eprojs)
        Returns:
            torch.Tensor: log softmax applied 3d tensor (B, Tmax, odim)
        """
        return F.log_softmax(self.ctc_lo(hs_pad) / temperature, dim=2)

    def argmax(self, hs_pad: torch.Tensor) -> torch.Tensor:
        """argmax of frame activations
        Args:
            torch.Tensor hs_pad: 3d tensor (B, Tmax, eprojs)
        Returns:
            torch.Tensor: argmax applied 2d tensor (B, Tmax)
        """
        return torch.argmax(self.ctc_lo(hs_pad), dim=2)

    def _decode_batch_greedy_offline(self, probs_split: list | torch.Tensor,
                                     vocab_list, num_processes=8):
        raise NotImplemented()

    def _decode_batch_beam_search_offline(self, probs_split: list | torch.Tensor, vocab_list: list,
                                          beam_size: int = 10,
                                          cutoff_prob: float = -float("Inf"),
                                          cutoff_top_n: int = 10,
                                          num_processes: int = 8,
                                          ):
        raise NotImplemented()

    @classmethod
    def forced_align(cls,
                     ctc_probs: torch.Tensor,
                     y: torch.Tensor,
                     blank_id=0) -> list:
        """ctc forced alignment.
        Args:
            ctc_probs (torch.Tensor): hidden state sequence, 2d tensor (T, D)
            y (torch.Tensor): label id sequence tensor, 1d tensor (L)
            blank_id (int): blank symbol index
        Returns:
            list(int): best alignment result, (T).
        """
        return ctc_utils.forced_align(ctc_probs, y, blank_id)


if __name__ == '__main__':
    input1 = torch.tensor([1, 2, 3])
    input = torch.randn(123, 100, 64)
    input = input.to(torch.float32)
    input_lens = torch.randint(30, 100, (123,))
    y_input = torch.randint(0, 10000, (123, 20,))
    y_lens = torch.randint(20, 21, (123,))
    decoder = CTCDecoderBase(10000, 64, reduction=False)
    loss = decoder(input, input_lens, y_input, y_lens)
    decoder2 = CTCDecoderBase(10000, 64, reduction=True)
    loss2 = decoder2(input, input_lens, y_input, y_lens)
    docoder3 = CTCDecoderBase(10000, 64, reduction='mean')
    loss3 = docoder3(input, input_lens, y_input, y_lens)
    print('-----')
    print(loss)
    print(loss2)
    print(loss3)


class CTCDecoder(CTCDecoderBase):
    def __init__(self,
                 odim,
                 enc_n_units,
                 blank_id=0,
                 dropout_rate: float = 0.0,
                 reduction: Union[str, bool] = True,
                 *args, **kwargs):
        super().__init__(odim,
                         enc_n_units,
                         blank_id,
                         dropout_rate,
                         reduction, *args, **kwargs)

    def decode_batch_greedy_offline(self, probs_split: list | torch.Tensor,
                                    vocab_list: list | None, num_processes=8):
        return ctc_utils.ctc_greedy_search_decoding_batch(
            probs_split, vocab_list, num_processes, self.blank_id
        )

    def decode_batch_beam_search_offline(self, probs_split: list | torch.Tensor,
                                         input_lens: list | torch.Tensor,
                                         vocab_list: list | None,
                                         beam_size: int = 10,
                                         cutoff_prob: float = -float("Inf"),
                                         cutoff_top_n: int = 10,
                                         num_processes: int = 8,
                                         ):
        return ctc_utils.ctc_beam_search_decoding_batch(
            probs_split,
            input_lens,
            vocab_list,
            beam_size,
            cutoff_prob,
            cutoff_top_n,
            num_processes,
            self.blank_id
        )
