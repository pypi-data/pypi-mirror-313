from typing import List

import torch
import math
# import kenlm
import numpy as np
import multiprocessing as mp
from functools import partial


def insert_blank(label: torch.Tensor, blank_id: int = 0) -> torch.Tensor:
    """Insert blank token between every two label token.

    "abcdefg" -> "-a-b-c-d-e-f-g-"

    Args:
        label ([torch.Tensor]): label ids, List[int], (L).
        blank_id (int, optional): blank id. Defaults to 0.

    Returns:
        [torch.Tensor]: (2L+1).
    """
    label = torch.unsqueeze(label, 1)  # [L, 1]
    blanks = torch.zeros((label.shape[0], 1), dtype=label.dtype) + blank_id
    label = torch.concatenate([blanks, label], dim=1)  # [L, 2]
    label = label.reshape(-1)  # [2L], -l-l-l
    label = torch.concat((label, label[0].unsqueeze(0)))  # [2L + 1], -l-l-l-
    return label


def forced_align(ctc_probs: torch.Tensor, y: torch.Tensor,
                 blank_id=0) -> List[int]:
    """ctc forced alignment.

    https://distill.pub/2017/ctc/

    Args:
        ctc_probs (torch.Tensor): hidden state sequence, 2d tensor (T, D)
        y (torch.Tensor): label id sequence tensor, 1d tensor (L)
        blank_id (int): blank symbol index
    Returns:
        List[int]: best alignment result, (T).
    """
    y_insert_blank = insert_blank(y, blank_id)  # (2L+1)

    log_alpha = torch.zeros(
        (ctc_probs.shape[0], len(y_insert_blank)))  # (T, 2L+1)
    log_alpha = log_alpha - float('inf')  # log of zero
    state_path = (torch.zeros(
        (ctc_probs.shape[0], len(y_insert_blank)), dtype=torch.int32) - 1
                  )  # state path, Tuple((T, 2L+1))

    # init start state
    log_alpha[0, 0] = ctc_probs[0][int(y_insert_blank[0])]  # State-b, Sb
    log_alpha[0, 1] = ctc_probs[0][int(y_insert_blank[1])]  # State-nb, Snb

    for t in range(1, ctc_probs.shape[0]):  # T
        for s in range(len(y_insert_blank)):  # 2L+1
            if s == 0:
                candidates = torch.tensor([log_alpha[t - 1, s], ])
                prev_state = [s, ]
            elif y_insert_blank[s] == blank_id or s < 2 or y_insert_blank[s] == y_insert_blank[s - 2]:
                candidates = torch.tensor([log_alpha[t - 1, s], log_alpha[t - 1, s - 1]])
                prev_state = [s, s - 1]
            else:
                candidates = torch.tensor([
                    log_alpha[t - 1, s],
                    log_alpha[t - 1, s - 1],
                    log_alpha[t - 1, s - 2],
                ])
                prev_state = [s, s - 1, s - 2]
            log_alpha[t, s] = torch.max(candidates) + ctc_probs[t][int(
                y_insert_blank[s])]
            state_path[t, s] = prev_state[torch.argmax(candidates)]
    state_seq = -1 * torch.ones((ctc_probs.shape[0], 1), dtype=torch.int32)

    candidates = torch.tensor([
        log_alpha[-1, len(y_insert_blank) - 1],  # Sb
        log_alpha[-1, len(y_insert_blank) - 2]  # Snb
    ])
    prev_state = [len(y_insert_blank) - 1, len(y_insert_blank) - 2]
    state_seq[-1] = prev_state[torch.argmax(candidates)]
    for t in range(ctc_probs.shape[0] - 2, -1, -1):
        state_seq[t] = state_path[t + 1, state_seq[t + 1, 0]]

    output_alignment = []
    for t in range(0, ctc_probs.shape[0]):
        output_alignment.append(y_insert_blank[state_seq[t, 0]].item())

    return output_alignment


def log_sum_exp(lps):
    """
    实现对数概率的相加, 最后结果为对数概率
    """
    _inf = -float('inf')
    if all(lp == _inf for lp in lps): return _inf
    mlp = max(lps)
    return mlp + math.log(sum(math.exp(lp - mlp) for lp in lps))


# class Scorer(object):
#     """
#     A class for scoring CTC decoders with language model and WER.
#     """
#
#     def __init__(self, alpha, beta, model_path, vocab_list):
#         """
#         Initialize the scorer.
#
#         Args:
#             alpha: the weight of language model.
#             beta: the weight of word count.
#             model_path: the path of the language model file.
#         """
#         self.alpha = alpha
#         self.beta = beta
#         self.lm = kenlm.Model(model_path)
#         self.vocab_list = vocab_list
#
#     def score(self, sentence):
#         """
#         Score a sentence with language model and word count.
#
#         Args:
#             sentence: a list of words.
#
#         Returns:
#             a float score.
#         """
#         log_prob = self.lm.score(' '.join(sentence), bos=True, eos=True)
#         word_count = len(sentence)
#         return self.alpha * log_prob + self.beta * word_count


def wer(ref, hyp):
    """
    Calculate the word error rate (WER) between reference and hypothesis.

    Args:
        ref: a list of words as reference.
        hyp: a list of words as hypothesis.

    Returns:
        a float WER.
    """
    # Convert to numpy array
    ref = np.array(ref)
    hyp = np.array(hyp)

    # Initialize the edit distance matrix
    dist = np.zeros((len(ref) + 1, len(hyp) + 1))

    # 动态规划的初始化
    dist[0, :] = np.arange(len(hyp) + 1)
    dist[:, 0] = np.arange(len(ref) + 1)

    # Fill the matrix with dynamic programming
    """
    动态规划, 计算两个序列的差距距离
            hyp+1
        . . . . . . . . 
    ref . . . . . . . . 
    +1  . . . . . . . .
    """
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            if ref[i - 1] == hyp[j - 1]:
                #  当前节点的字相同, i和j都是生活意义的序列, 带入数组要减一
                dist[i, j] = dist[i - 1, j - 1]
            else:
                dist[i, j] = min(dist[i - 1, j], dist[i, j - 1], dist[i - 1, j - 1]) + 1

    # Return the WER
    return dist[-1, -1] / len(ref)


def ctc_greedy_decoding(probs_seq: torch.Tensor, vocabulary: list | None, blank_id: int) -> List[int | str]:
    """
    probs_seq: 概率图, a 2-D probability matrix, shape: (time, class_num)
    vocabulary: a list of strings, the i-th string is the i-th class
    blank_id: an integer, the index of the blank class in the vocabulary
    return: a strings list, representing the most probable sentence

    initialize an empty list to store the best path
    """
    assert probs_seq.size(1) == len(vocabulary), "vocabulary size does not match probs size"
    if torch.any(probs_seq > 0):
        probs_seq = probs_seq.to(torch.float32)
        probs_seq = torch.log_softmax(probs_seq, dim=1)
    best_path = []
    # loop over the probability sequence
    for probs in probs_seq:
        # find the index of the most probable character
        max_index = torch.argmax(probs)
        # append the index to the best path
        best_path.append(max_index)
    # initialize an empty string to store the decoded output
    decoded_output = []

    # loop over the best path
    for i, index in enumerate(best_path):
        # if the index is not blank and not repeated, append the corresponding character to the decoded output
        if index != blank_id and (i == 0 or index != best_path[i - 1]):
            if vocabulary:
                decoded_output.append(vocabulary[index])
            else:
                decoded_output.append(index)
    return decoded_output


def ctc_beam_decoding(probs, vocabulary=None,
                      beam_size=10, cutoff_prob=-torch.inf,
                      cutoff_top_n=10,
                      blank_id=0) \
        -> list[list[str | int]]:
    """
    probs: 概率空间，shape为[sequence_len,vocab_size]的torch tensor, 其中的概率均为对数概率
    input_len: input_len
    beam_size: beam_size
    vocabulary: vocabulary
    cutoff_prob: cutoff_prob, 概率阈值, 小于该阈值的class直接将其概率置为0
    cutoff_top_n: cutoff_top_n,每次取的前n值
    blank: blank index
    标签序列的概率都会使用两个变量存储，一个负责累加以字符结尾的原生序列概率，另一个负责累加以blank结尾的原生序列概率
    seqs中的是标签序列
    更新规则:
    1. 当前值为blank， 标签序列不变， 更新以blank结尾的概率
    2. 原生序列结尾为blank，当前值为相同字符,也就是与目前标签序列的最后一个字符相同， 标签序列更新， 更新非blank概率
    3. 原生序列结尾为字符，当前值为相同字符， 标签序列不变， 更新非blank概率；
    4. 当前值为不同字符， 标签序列更新， 更新非blank概率。
    """
    assert probs.size(1) == len(vocabulary), "vocabulary size does not match probs size"
    if torch.any(probs > 0):
        probs = probs.to(torch.float32)
        probs = torch.log_softmax(probs, dim=1)
    _inf = -float("inf")
    probs = torch.where(probs >= cutoff_prob, probs, torch.zeros_like(probs))
    # if idx.item() != blank 也就是情况1
    # 初始化
    seqs = [((idx.item(),), (lp.item(), _inf)) if idx.item() != blank_id
            else (tuple(), (_inf, lp.item()))
            for lp, idx in zip(*(probs[0].topk(cutoff_top_n)))]
    for i in range(1, probs.size(0)):
        new_seqs = {}
        for seq, (lps, blps) in seqs:
            last = seq[-1] if len(seq) > 0 else None
            for lp, idx in zip(*probs[i].topk(cutoff_top_n)):
                lp = lp.item()
                idx = idx.item()
                if idx == blank_id:
                    """
                    当当前为blank时, 直接标签不变, 更新以blank结尾的概率
                    原始序列有三种情况: 
                    1. seq_+_ : blps + lp,
                    2. seq +_ : lps + lp,
                    3. ....
                    """
                    nlps, nblps = new_seqs.get(seq, (_inf, _inf))
                    new_seqs[seq] = (nlps, log_sum_exp([nblps, lps + lp, blps + lp]))
                elif idx == last:
                    """
                    相同字符的情况,
                    分为aa和a-a两种情况
                    """
                    # aa
                    nlps, nblps = new_seqs.get(seq, (_inf, _inf))
                    new_seqs[seq] = (log_sum_exp([nlps, lps + lp]), nblps)
                    # a-a
                    new_seq = seq + (idx,)
                    nlps, nblps = new_seqs.get(new_seq, (_inf, _inf))
                    new_seqs[new_seq] = (log_sum_exp([nlps, blps + lp]), nblps)
                else:
                    """
                    不同字符的情况, 三种情况
                    1. seq+a: lps + lp,
                    2. seq_+a: blps + lp,
                    3. ...
                    """
                    new_seq = seq + (idx,)
                    nlps, nblps = new_seqs.get(new_seq, (_inf, _inf))
                    new_seqs[new_seq] = (log_sum_exp([nlps, lps + lp, blps + lp]), nblps)
        new_seqs = sorted(
            new_seqs.items(),
            key=lambda x: log_sum_exp(list(x[1])),
            reverse=True)
        seqs = new_seqs[:beam_size]
    seqs = [list(seq[0]) for seq in seqs]
    if vocabulary is not None:
        decoded_paths = [[vocabulary[label] for label in beam] for beam in seqs]
    else:
        decoded_paths = seqs
    return decoded_paths


def ctc_greedy_search_decoding_batch(
        probs_split,
        input_lens,
        vocabulary,
        num_processes=8,
        blank_id=0, ):
    """
    Returns:
        a list of lists of strings, each sublist is a sentence (list of words).
    """
    # Use multiprocessing to speed up the decoding
    pool = mp.Pool(processes=num_processes)
    probs_split = [prob[:input_len] for prob, input_len in zip(probs_split, input_lens)]
    results = pool.map(
        partial(
            ctc_greedy_decoding,
            vocabulary=vocabulary,
            blank_id=blank_id),
        probs_split)
    pool.close()
    pool.join()
    return results


def ctc_beam_search_decoding_batch(
        probs_split,
        input_lens,
        vocabulary,
        beam_size=10,
        cutoff_prob=-float("Inf"),
        cutoff_top_n=10,
        num_processes=8,
        blank_id=0):
    """
    Perform CTC beam search decoding for a batch of probability matrices.

    Args:
        input_lens: a list of integers, the lengths of input sequences.
        probs_split: a list of 2-D numpy arrays, each with shape (time_steps, num_classes),
                     representing the probabilities of each class for each time step.
        vocabulary: a list of strings, representing the possible output classes,
                    including the blank symbol as the first element.
        beam_size: an integer, the beam width used in beam search.
        num_processes: an integer, the number of processes to use for parallel decoding.
        blank_id: an integer, the index of the blank symbol in the vocabulary.
        cutoff_prob: a float, a threshold for pruning.
        cutoff_top_n: an integer, the cutoff for the topN.

    Returns:
        a list of lists of strings, each sublist is a sentence (list of words).
    """
    # Use multiprocessing to speed up the decoding
    pool = mp.Pool(processes=num_processes)
    probs_split = [prob[:input_len] for prob, input_len in zip(probs_split, input_lens)]
    results = pool.map(
        partial(
            ctc_beam_decoding,
            vocabulary=vocabulary,
            beam_size=beam_size,
            cutoff_prob=cutoff_prob,
            cutoff_top_n=cutoff_top_n,
            blank_id=blank_id),
        probs_split)
    pool.close()
    pool.join()

    return results


if __name__ == '__main__':
    # input = torch.randn(100, 422)
    # print(forced_align(input, torch.tensor([1, 2, 3, 421, 15, 32, 7, 8, 9, 10])))

    input = torch.tensor([
        [[1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [10000, 2, 3, 421, 15, 32, 7, 8, 9, 10],
         [1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [1, 2121, 3, 421, 15, 32, 7, 8, 9, 10]],
        [[1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [10000, 2, 3, 421, 15, 32, 7, 8, 9, 10],
         [1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [1, 2121, 3, 421, 15, 32, 7, 8, 9, 10]]
    ])
    input_single = torch.tensor([[1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [10000, 2, 3, 421, 15, 32, 7, 8, 9, 10],
                                 [1, 2, 3, 421, 15, 32, 7, 8, 9, 10], [1, 2121, 3, 421, 15, 32, 7, 8, 9, 10]], )
    vocab_List = ['_', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print(ctc_beam_search_decoding_batch(input, [3, 2], vocab_List, 2))
    print(ctc_beam_decoding(input_single, vocab_List, 2))
