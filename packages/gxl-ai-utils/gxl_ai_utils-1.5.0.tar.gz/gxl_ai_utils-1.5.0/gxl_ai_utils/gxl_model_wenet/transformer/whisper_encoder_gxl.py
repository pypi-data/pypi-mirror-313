import copy

import torch.nn
import whisper
import os
from gxl_ai_utils.utils import utils_model
from ..utils.mask import make_pad_mask
import torch.nn.functional as F


class GxlWhisperEncoder(torch.nn.Module):
    def __init__(self,
                 freeze: bool,
                 whisper_model: str,
                 dropout_rate: float, ):
        super().__init__()
        _model = whisper.load_model(whisper_model,
                                    download_root=os.environ.get('WHISPER_CACHE',
                                                                 '/home/work_nfs7/xlgeng/workspace/whisper'))

        self.encoders = copy.deepcopy(_model.encoder)
        del _model
        self.dropout = torch.nn.Dropout(dropout_rate)
        if freeze:
            utils_model.make_freeze_all_params(self.encoders)
        else:
            self.encoders.train()

    def forward(self,
                xs: torch.nn.Module,
                ilens: torch.nn.Module, ):
        """
        :param xs: (b, t, d)
        :param ilens: (b,)
        :return:
        """
        xs = xs.permute(0, 2, 1)
        x = F.gelu(self.encoders.conv1(xs))
        x = F.gelu(self.encoders.conv2(x))
        x = x.permute(0, 2, 1)
        n_frames = x.size(1)
        max_pos = self.encoders.positional_embedding.size(0)
        if n_frames <= max_pos:
            x = (x + self.encoders.positional_embedding[: x.size(1), :]).to(x.dtype)
        else:
            # due to positional encoding, audios >30 sec won't be accepted
            x = x[:, :max_pos, :] + self.encoders.positional_embedding
        if ilens is not None:
            olens = (
                    1
                    + (
                            ilens
                            - self.encoders.conv2.kernel_size[0]
                            + 2 * self.encoders.conv2.padding[0]
                    )
                    // self.encoders.conv2.stride[0]
            )
            olens = torch.clamp(olens, max=max_pos)
            T = x.size(1)
            # 真值为True
            masks = ~make_pad_mask(olens, T).unsqueeze(1)
        else:
            masks = None

        x = self.dropout(x)

        for layer, block in enumerate(self.encoders.blocks):
            x = block(x, masks)
            if layer < len(self.encoders.blocks) - 1:
                x = self.dropout(x)

        x = self.encoders.ln_post(x)

        return x, masks

    def output_size(self):
        return self.encoders.ln_post.normalized_shape[-1]
