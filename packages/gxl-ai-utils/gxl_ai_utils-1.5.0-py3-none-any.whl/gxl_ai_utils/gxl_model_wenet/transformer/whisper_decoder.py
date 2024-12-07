import copy
import os
from typing import Any, List, Tuple

import torch

class OpenAIWhisperDecoder(torch.nn.Module):
    """Transformer-based Speech-to-Text Decoder from OpenAI's Whisper Model:

    URL: https://github.com/openai/whisper
    """

    def __init__(
        self,
        vocab_size: int,
        dropout_rate: float = 0.0,
        whisper_model: str = "small",
        use_lora: bool = False, # add to use Lora
        train: bool = False,
    ):
        try:
            from ... import gxl_whisper as whisper
        except Exception as e:
            print("Error: whisper is not properly installed.")
            print(
                "Please install whisper with: cd ${MAIN_ROOT}/tools && "
                "./installers/install_whisper.sh"
            )
            raise e

        super().__init__()

        if not use_lora:
            assert whisper_model in whisper.available_models()
            _model = whisper.load_model(whisper_model, download_root=os.environ.get('WHISPER_CACHE',
                                                                                    '/home/work_nfs7/xlgeng/workspace/whisper'),
                                        device='cpu')
        # add for lora
        # if use_lora:
        #     from espnet2.asr.whisper_lora import Whisper_lora
        #     from whisper import ModelDimensions
        #     from whisper import _ALIGNMENT_HEADS
        #     import loralib as lora
        #
        #     device = "cuda" if torch.cuda.is_available() else "cpu"
        #     checkpoint = torch.load(f"/home/work_nfs5_ssd/pkchen/workspace/whisper/{whisper_model}.pt", map_location=device)
        #     dims = ModelDimensions(**checkpoint["dims"])
        #     _model = Whisper_lora(dims)
        #     _model.load_state_dict(checkpoint["model_state_dict"], strict=False)
        #     _model.set_alignment_heads(_ALIGNMENT_HEADS[whisper_model])
        #     lora.mark_only_lora_as_trainable(_model)
        # add for lora

        self.decoders = copy.deepcopy(_model.decoder)
        attention_dim = self.decoders.token_embedding.embedding_dim

        # note that originally Whisper doesn't use dropouts
        self.dropout = torch.nn.Dropout(dropout_rate)

        # vocab size mismatch -> reinitialize embedding
        # orig vocab size (multilingual): 51865
        # orig vocab size (english): 51864
        if vocab_size != self.decoders.token_embedding.num_embeddings:
            orig_emb_std, orig_emb_mean = torch.std_mean(
                self.decoders.token_embedding.weight
            )
            self.decoders.token_embedding = torch.nn.Embedding(
                vocab_size, attention_dim
            )
            torch.nn.init.normal_(
                self.decoders.token_embedding.weight,
                orig_emb_mean.item(),
                orig_emb_std.item(),
            )
        if train:
            self.decoders.train()
        else:
            self.decoders.eval()
        del _model

    def forward(
        self,
        hs_pad: torch.Tensor,
        masks: torch.Tensor,
        ys_in_pad: torch.Tensor,
        ys_in_lens: torch.Tensor,
        r_ys_in_pad: torch.Tensor = torch.empty(0),
        reverse_weight: float = 0.0,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward decoder.

        Args:
            hs_pad: encoded memory, float32  (batch, maxlen_in, feat)
            hlens: (batch)
            ys_in_pad:
                input token ids, int64 (batch, maxlen_out)
                if input_layer == "embed"
                input tensor (batch, maxlen_out, #mels) in the other cases
            ys_in_lens: (batch)
        Returns:
            (tuple): tuple containing:

            x: decoded token score before softmax (batch, maxlen_out, token)
                if use_output_layer is True,
            olens: (batch, )
        """
        tgt, memory = ys_in_pad, hs_pad
        tgt = (
            self.decoders.token_embedding(tgt)
            + self.decoders.positional_embedding[: tgt.size(1)]
        )

        tgt = self.dropout(tgt)

        x = tgt.to(memory.dtype)

        for layer, block in enumerate(self.decoders.blocks):
            x = block(x, memory, mask=self.decoders.mask)
            if layer < len(self.decoders.blocks) - 1:
                x = self.dropout(x)

        x = self.decoders.ln(x)
        x = (
            x @ torch.transpose(self.decoders.token_embedding.weight.to(x.dtype), 0, 1)
        ).float()

        return x, torch.tensor(0.0), ys_in_lens

    def forward_one_step(
        self,
        memory: torch.Tensor,
        memory_mask: torch.Tensor,
        tgt: torch.Tensor,
        tgt_mask: torch.Tensor,
        cache: List[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, List[torch.Tensor]]:
        """Forward one step.

        Args:
            tgt: input token ids, int64 (batch, maxlen_out)
            tgt_mask: input token mask,  (batch, maxlen_out)
                      dtype=torch.uint8 in PyTorch 1.2-
                      dtype=torch.bool in PyTorch 1.2+ (include 1.2)
            memory: encoded memory, float32  (batch, maxlen_in, feat)
            cache: cached output list of (batch, max_time_out-1, size)
        Returns:
            y, cache: NN output value and cache per `self.decoders`.
            y.shape` is (batch, maxlen_out, token)
        NOTE (Shih-Lun):
            cache implementation is ignored for now
            for simplicity & correctness
        """
        x = (
            self.decoders.token_embedding(tgt)
            + self.decoders.positional_embedding[: tgt.size(1)]
        )
        x = self.dropout(x)
        x = x.to(memory.dtype)

        for layer, block in enumerate(self.decoders.blocks):
            x = block(x, memory, mask=self.decoders.mask)
            if layer < len(self.decoders.blocks) - 1:
                x = self.dropout(x)

        x = self.decoders.ln(x)
        y = x[:, -1]
        y = (
            y @ torch.transpose(self.decoders.token_embedding.weight.to(x.dtype), 0, 1)
        ).float()
        y = torch.log_softmax(y, dim=-1)

        return y, None