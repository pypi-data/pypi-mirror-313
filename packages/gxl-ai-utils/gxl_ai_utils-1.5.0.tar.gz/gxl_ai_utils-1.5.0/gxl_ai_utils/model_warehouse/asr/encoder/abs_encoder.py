from typing import Optional

import torch
from torch import nn


class AbsEncoder(nn.Module):
    def output_size(self):
        raise NotImplementedError

    def forward(self, xs_pad: torch.Tensor,
                ilens: torch.Tensor,
                pre_states: torch.tensor = None
                ) -> tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]:
        raise NotImplementedError
