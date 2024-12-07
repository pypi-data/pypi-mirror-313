import copy
import os
from typing import Optional, Tuple, Union

import torch
import torch.nn.functional as F

try:
    from espnet2.asr.specaug.specaug import SpecAug
except ImportError:
    SpecAug = None
from ..utils.mask import make_pad_mask, add_optional_chunk_mask


class OpenAIWhisperEncoder(torch.nn.Module):
    """Transformer-based Speech Encoder from OpenAI's Whisper Model:

    URL: https://github.com/openai/whisper
    """

    def __init__(
            self,
            dropout_rate: float = 0.0,
            whisper_model: str = "small",
            use_specaug: bool = False,
            specaug_conf: Optional[dict] = None,
            do_pad_trim: bool = False,
            use_lora: bool = False,  # add to use lora
            freeze: bool = False
    ):
        try:
            from ... import gxl_whisper as whisper
            from ...gxl_whisper.audio import HOP_LENGTH, N_FFT, N_SAMPLES
            N_MELS = 80
        except Exception as e:
            print("Error: whisper is not properly installed.")
            print(
                "Please install whisper with: cd ${MAIN_ROOT}/tools &&",
                "./installers/install_whisper.sh",
            )
            raise e

        super().__init__()

        self.n_fft = N_FFT  # 快速傅里叶变换的长度
        self.win_length = N_FFT
        self.hop_length = HOP_LENGTH
        self.n_mels = N_MELS

        self.mel_filters = whisper.audio.mel_filters

        # note that originally Whisper doesn't use dropouts
        self.dropout = torch.nn.Dropout(dropout_rate)

        if not use_lora:
            assert whisper_model in whisper.available_models()
            _model = whisper.load_model(whisper_model, download_root=os.environ.get('WHISPER_CACHE','/home/work_nfs7/xlgeng/workspace/whisper'),
                                        device='cpu')
        else:
            _model = None
        # add for lora
        # if use_lora:
        #     from espnet2.asr.whisper_lora import Whisper_lora
        #     from whisper import ModelDimensions
        #     from whisper import _ALIGNMENT_HEADS
        #     import loralib as lora
        #
        #     device = "cuda" if torch.cuda.is_available() else "cpu"
        #     checkpoint = torch.load(f"/home/work_nfs7/xlgeng/workspace/whisper/{whisper_model}.pt", map_location=device)
        #     dims = ModelDimensions(**checkpoint["dims"])
        #     _model = Whisper_lora(dims)
        #     _model.load_state_dict(checkpoint["model_state_dict"], strict=False)
        #     _model.set_alignment_heads(_ALIGNMENT_HEADS[whisper_model])
        #     lora.mark_only_lora_as_trainable(_model)
        # add for lora

        self.encoders = copy.deepcopy(_model.encoder)
        self.encoders.train()
        del _model
        if use_specaug:  # 频谱增强
            self.specaug = SpecAug(**specaug_conf)
        else:
            self.specaug = None

        self.do_pad_trim = do_pad_trim
        self.pad_samples = N_SAMPLES

    def gxl_forward(self,
                    xs: torch.Tensor,
                    xs_lens: torch.Tensor,):
        """
        xs: (B, T, D)
        xs_lens: (B,)
        :param xs:
        :param xs_lens:
        :return:
        """
        T = xs.size(1)
        # mask为真实值为true
        masks = ~make_pad_mask(xs_lens, T).unsqueeze(1)  # (B, 1, T)
        # if self.global_cmvn is not None:
        #     xs = self.global_cmvn(xs)
        inputs = xs.permute(0, 2, 1)
        x = F.gelu(self.encoders.conv1(inputs))
        x = F.gelu(self.encoders.conv2(x))
        x = x.permute(0, 2, 1)
        mask_pad = masks  # (B, 1, T/subsample_rate)
        for layer in self.encoders.blocks:
            xs = layer(xs, mask=mask_pad)
        if self.normalize_before:
            xs = self.after_norm(xs)
        # Here we assume the mask is not changed in encoder layers, so just
        # return the masks before encoder layers, and the masks will be used
        # for cross attention with decoder later
        return xs, masks

    def output_size(self) -> int:
        return self.encoders.ln_post.normalized_shape[-1]

    def pad_or_trim(
            self,
            array: torch.Tensor,
            length: int,
            axis: int = -1,
    ) -> torch.Tensor:
        """Pad or trim the audio array to N_SAMPLES.

        Used in zero-shot inference cases.
        """
        if array.shape[axis] > length:
            array = array.index_select(
                dim=axis, index=torch.arange(length).to(array.device)
            )

        if array.shape[axis] < length:
            pad_widths = [(0, 0)] * array.ndim
            pad_widths[axis] = (0, length - array.shape[axis])
            array = F.pad(array, [pad for sizes in pad_widths[::-1] for pad in sizes])

        return array

    def log_mel_spectrogram(
            self,
            audio: torch.Tensor,
            ilens: torch.Tensor = None,
    ) -> torch.Tensor:
        """Use log-mel spectrogram computation native to Whisper training"""
        window = torch.hann_window(self.win_length).to(audio.device)
        stft = torch.stft(
            audio, self.n_fft, self.hop_length, window=window, return_complex=True
        )

        # whisper deletes the last frame by default (Shih-Lun)
        magnitudes = stft[..., :-1].abs() ** 2

        filters = self.mel_filters(audio.device, self.n_mels)
        mel_spec = filters @ magnitudes

        log_spec = torch.clamp(mel_spec, min=1e-10).log10()

        if ilens is not None:
            olens = ilens // self.hop_length
        else:
            olens = None

        log_spec = torch.maximum(
            log_spec,
            log_spec.view(audio.size(0), -1).max(dim=-1)[0][:, None, None] - 8.0,
        )
        log_spec = (log_spec + 4.0) / 4.0

        return log_spec, olens

    def whisper_encode(
            self,
            input: torch.Tensor,
            ilens: torch.Tensor = None,
    ) -> torch.Tensor:
        x = F.gelu(self.encoders.conv1(input))
        x = F.gelu(self.encoders.conv2(x))
        x = x.permute(0, 2, 1)

        n_frames = x.size(1)
        max_pos = self.encoders.positional_embedding.size(0)
        if n_frames <= max_pos:
            x = (x + self.encoders.positional_embedding[: x.size(1), :]).to(x.dtype)
        else:
            # due to positional encoding, audios >30 sec won't be accepted
            x = x[:, :max_pos, :] + self.encoders.positional_embedding

        x = self.dropout(x)

        for layer, block in enumerate(self.encoders.blocks):
            x = block(x)
            if layer < len(self.encoders.blocks) - 1:
                x = self.dropout(x)

        x = self.encoders.ln_post(x)

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
            T = x.size(2)
            masks = ~make_pad_mask(olens, T).unsqueeze(1)
        else:
            masks = None

        return x, masks

    def forward(
            self,
            xs_pad: torch.Tensor,
            ilens: torch.Tensor,
            decoding_chunk_size: int = 0,
            num_decoding_left_chunks: int = -1,
    ) -> Tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]:
        if self.do_pad_trim:
            xs_pad = self.pad_or_trim(xs_pad, self.pad_samples)

        feats, feats_lens = self.log_mel_spectrogram(xs_pad, ilens)
        raw_shape = xs_pad.shape
        mel_shape = feats.shape

        if self.specaug is not None and self.encoders.training:
            feats = feats.reshape(mel_shape[0], mel_shape[2], mel_shape[1])
            feats, feats_lens = self.specaug(feats, feats_lens)
            feats = feats.reshape(mel_shape[0], mel_shape[1], mel_shape[2])

        xs_pad, masks = self.whisper_encode(feats, feats_lens)

        return xs_pad, masks
