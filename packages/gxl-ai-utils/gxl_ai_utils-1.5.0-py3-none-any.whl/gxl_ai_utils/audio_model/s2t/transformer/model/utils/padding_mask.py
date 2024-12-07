import torch


def padding_mask(seq_q: torch.Tensor, seq_k: torch.Tensor, pad_id: int = 0):
    """
    根据seq_k 中pad_id的位置， 得到seq_q对于seq_k的padding_attn_mask,
    seq_q 只是提供q_len,并不影响mask的分布,
    input->
    seq_q: (batch_size, len_q)
    seq_k: (batch_size, len_k)
    output->
    mask: (batch_size, len_q, len_k)
    """
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    mask = seq_k.eq(pad_id)
    mask = mask.unsqueeze(1).expand(batch_size, len_q, len_k)
    return mask

