import torch


def sequence_mask(seq):
    """
    得到一个序列的self-attention的mask
    input->
    seq: [batch_size, seq_len]
    output->
    mask: [batch_size, seq_len, seq_len]
    """
    batch_size, seq_len = seq.size()
    mask = torch.triu(torch.ones((seq_len, seq_len), dtype=torch.uint8, device=seq.device), diagonal=1)
    mask = mask.unsqueeze(0).expand(batch_size, -1, -1)
    return mask
