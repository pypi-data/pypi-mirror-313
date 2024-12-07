from typing import List

import torch
from gxl_ai_utils.utils import utils_file

try:
    from .transducer import Transducer
except ImportError:
    pass


def greedy_search(model: "Transducer", encoder_out: torch.Tensor, ) -> List[int]:
    """
    推理的时候，我们已知的只有encoder的输出特征
    目前仅支持batch_size=1， nbest=1
    :param model:
    :param encoder_out:
    :return:
    """
    assert encoder_out.ndim == 3, encoder_out.shape
    assert encoder_out.size(0) == 1, encoder_out.shape  # 目前仅支持batch_size=1
    blank_id = model.decoder.blank_id
    sos = torch.ones([1, 1], device=encoder_out.device, dtype=torch.int32) * blank_id
    decoder_out, (c, h) = model.decoder(sos)
    T = encoder_out.size(1)
    U = 1000  # 默认最大解码步数为1000
    t = 0
    u = 0
    res = []
    while True:
        encoder_now = encoder_out[:, t:t + 1, :]
        logits = model.joiner(encoder_now, decoder_out)  # (B, 1, 1, vocab_size)
        probs = logits.log_softmax(dim=-1)
        # tensor.argmax(dim=-1)会消除掉最后一维，并得到index的内容
        y_id_now = probs.argmax(dim=-1)
        y_id_now = y_id_now.reshape(probs.size(0), 1)
        if y_id_now == blank_id:
            t += 1
        else:
            decoder_out, (h, c) = model.decoder(y_id_now, (h, c))
            u += 1
            res.append(y_id_now.item())

        if u >= U or t >= T:
            break
    return res
