import torch
from gxl_ai_utils.utils import utils_file


# torch.gather(input, dim, index, out=None, sparse_grad=False) -> Tensor
def do_test_gather():
    input_tensor = torch.tensor([
        [ [11, 12, 13, ], [1, 2, 3] ],  # (1,2,3)
    ])
    print(input_tensor.shape)
    print(input_tensor.dim())
    index = torch.tensor([ # (1,X, 3),  X 可以任意多个, 其中具体的值为index in dim1,也就是只能是(0,1).然后再dim根据index找到对应的位置的数值
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
    ])
    print(index.shape)
    """
    tensor([[[11, 12, 13],
         [ 1,  2,  3],
         [11,  2, 13]]])
    """
    print(input_tensor.gather(1, index))


def get_rnnt_logit(am,
                   lm,
                   symbols,
                   termination_symbol):
    """

    :param am: (B, T, C)
    :param lm: (B, S+1, C) , C 的词表大小, 这两个都是没标准化的概率分布
    :param symbols: (B, S)
    :param termination_symbol: int , 0 <= termination_symbol < C
    :return:
    """
    B, S, T = am.size(0), lm.size(1) - 1, lm.size(1)
    am_max, _ = torch.max(am, dim=2, keepdim=True)  # am_max: [B][T][1]
    lm_max, _ = torch.max(lm, dim=2, keepdim=True)  # lm_max: [B][S+1][1]
    am_probs = (am - am_max).exp()  # 最大值的位置exp值为1,其他都是小于1大于0的值
    lm_probs = (lm - lm_max).exp()
    print(lm_probs)
    normalizers = (
            torch.matmul(lm_probs, am_probs.transpose(1, 2))  # (B, S+1, T)
            + torch.finfo(am_probs.dtype).tiny
    ).log()
    print(normalizers)
    # add lm_max and am_max to normalizers, to make it as if we had not
    # subtracted am_max and lm_max above.
    normalizers = normalizers + lm_max + am_max.transpose(1, 2)  # [B][S+1][T] # 已证明^*

    # px is the probs of the actual symbols..
    px_am = torch.gather(
        am.transpose(1, 2),  # (B, C, T)
        dim=1,
        index=symbols.unsqueeze(2).expand(B, S, T),
    )  # (B, S, T) # 如果转回(B,T,S)会更好理解一点,就是T时间步上S个字符的概率

    px_am = torch.cat(
        (
            px_am,
            torch.full(
                (B, S, 1),
                float("-inf"),
                device=px_am.device,
                dtype=px_am.dtype,
            ),
        ),
        dim=2,
    )  # now: [B][S][T+1], index [:,:,T] has -inf..   ,regular的时候,我们暂时只考虑regular

    px_lm = torch.gather(
        lm[:, :S], dim=2, index=symbols.unsqueeze(-1)
    )  # [B][S][1]
    px = px_am + px_lm  # [B][S][T+1], last slice with indexes out of
    # boundary is  -inf
    px[:, :, :T] -= normalizers[:, :S, :]  # px: [B][S][T+1]

    # py is the probs of termination symbols, of shape [B][S+1][T]
    py_am = am[:, :, termination_symbol].unsqueeze(1)  # [B][1][T]
    py_lm = lm[:, :, termination_symbol].unsqueeze(2)  # [B][S+1][1]
    py = py_am + py_lm - normalizers
    return px, py



def do_test_get_rnnt_logit():
    B = 4
    T = 21
    C = 108
    S = 10
    am_input = torch.randn(B, T, C)
    lm_input = torch.randn(B, S + 1, C)
    symbols = torch.randint(0, C, (B, S))
    termination_symbol = 107
    get_rnnt_logit(am_input, lm_input, symbols, termination_symbol)


if __name__ == '__main__':
    """"""
    # do_test_get_rnnt_logit()
    do_test_gather()
