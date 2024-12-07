import logging
import os
import random
import re
import shutil
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Any, Tuple, Dict

import numpy as np

try:
    import k2
except:
    pass
import torch
from tqdm import tqdm

Lexicon = List[Tuple[str, List[str]]]


def copy_family_file(input_dir, output_dir, num=-1):
    from .utils_file import makedir_sil, copy_file, load_dict_from_scp, do_convert_wav_text_scp_to_jsonl, \
        write_dict_to_scp
    makedir_sil(output_dir)
    text_path = os.path.join(input_dir, "text")
    target_text_path = os.path.join(output_dir, "text")
    wav_path = os.path.join(input_dir, "wav.scp")
    target_wav_path = os.path.join(output_dir, "wav.scp")
    data_list_path = os.path.join(input_dir, "data.list")
    target_data_list_path = os.path.join(output_dir, "data.list")
    assert os.path.exists(text_path) or os.path.exists(wav_path) or os.path.exists(
        data_list_path), f"{input_dir} 不存在"
    if num == -1:
        copy_file(text_path, target_text_path)
        copy_file(wav_path, target_wav_path)
        copy_file(data_list_path, target_data_list_path)
    else:
        key_list = []
        text_dict = {}
        wav_dict = {}
        if os.path.exists(text_path):
            text_dict = load_dict_from_scp(text_path)
            key_list_all = list(text_dict.keys())
            random.shuffle(key_list_all)
            key_list = key_list_all[:num]
        if os.path.exists(wav_path):
            wav_dict = load_dict_from_scp(wav_path)
            if len(key_list) == 0:
                key_list_all = list(wav_dict.keys())
                random.shuffle(key_list_all)
                key_list = key_list_all[:num]
        if len(key_list) >= 0:
            little_text_dict = {}
            little_wav_dict = {}
            for key in key_list:
                little_text_dict[key] = text_dict[key]
                little_wav_dict[key] = wav_dict[key]
            write_dict_to_scp(little_text_dict, target_text_path)
            write_dict_to_scp(little_wav_dict, target_wav_path)
            do_convert_wav_text_scp_to_jsonl(target_wav_path, target_text_path, target_data_list_path)


def compute_wer(true_text_path, hyp_text_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    command = "python compute-wer.py --char=1 --v=1 \
          {} {} > {}/wer".format(true_text_path, hyp_text_path, output_dir)
    # 执行命令
    subprocess.run(command, shell=True)


def do_compute_wer(true_text_path, hyp_text_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    relative_path = __file__
    # 转换为绝对路径
    absolute_path = os.path.abspath(__file__)
    absolute_dir = os.path.dirname(absolute_path)
    command = "python {}/compute-wer.py --char=1 --v=1 \
          {} {} > {}/wer".format(absolute_dir,true_text_path, hyp_text_path, output_dir)
    # 执行命令
    subprocess.run(command, shell=True)


def add_self_loops(
        arcs: List[List[Any]], disambig_token: int, disambig_word: int
) -> List[List[Any]]:
    """Adds self-loops to states of an FST to propagate disambiguation symbols
    through it. They are added on each state with non-epsilon output symbols
    on at least one arc out of the state.

    See also fstaddselfloops.pl from Kaldi. One difference is that
    Kaldi uses OpenFst style FSTs and it has multiple final states.
    This function uses k2 style FSTs and it does not need to add self-loops
    to the final state.

    The input label of a self-loop is `disambig_token`, while the output
    label is `disambig_word`.

    Args:
      arcs:
        A list-of-list. The sublist contains
        `[src_state, dest_state, label, aux_label, score]`
      disambig_token:
        It is the token ID of the symbol `#0`.
      disambig_word:
        It is the word ID of the symbol `#0`.

    Return:
      Return new `arcs` containing self-loops.
    """
    states_needs_self_loops = set()
    for arc in arcs:
        src, dst, ilabel, olabel, score = arc
        if olabel != 0:
            states_needs_self_loops.add(src)

    ans = []
    for s in states_needs_self_loops:
        ans.append([s, s, disambig_token, disambig_word, 0])

    return arcs + ans


def add_disambig_symbols(lexicon: Lexicon) -> Tuple[Lexicon, int]:
    """It adds pseudo-token disambiguation symbols #1, #2 and so on
    at the ends of tokens to ensure that all pronunciations are different,
    and that none is a prefix of another.

    See also add_lex_disambig.pl from kaldi.

    Args:
      lexicon:
        It is returned by :func:`read_lexicon`.
    Returns:
      Return a tuple with two elements:

        - The output lexicon with disambiguation symbols
        - The ID of the max disambiguation symbol that appears
          in the lexicon
    """

    # (1) Work out the count of each token-sequence in the
    # lexicon.
    count = defaultdict(int)
    for _, tokens in lexicon:
        count[" ".join(tokens)] += 1

    # (2) For each left sub-sequence of each token-sequence, note down
    # that it exists (for identifying prefixes of longer strings).
    issubseq = defaultdict(int)
    for _, tokens in lexicon:
        tokens = tokens.copy()
        tokens.pop()
        while tokens:
            issubseq[" ".join(tokens)] = 1
            tokens.pop()

    # (3) For each entry in the lexicon:
    # if the token sequence is unique and is not a
    # prefix of another word, no disambig symbol.
    # Else output #1, or #2, #3, ... if the same token-seq
    # has already been assigned a disambig symbol.
    ans = []

    # We start with #1 since #0 has its own purpose
    first_allowed_disambig = 1
    max_disambig = first_allowed_disambig - 1
    last_used_disambig_symbol_of = defaultdict(int)

    for word, tokens in lexicon:
        tokenseq = " ".join(tokens)
        assert tokenseq != ""
        if issubseq[tokenseq] == 0 and count[tokenseq] == 1:
            ans.append((word, tokens))
            continue

        cur_disambig = last_used_disambig_symbol_of[tokenseq]
        if cur_disambig == 0:
            cur_disambig = first_allowed_disambig
        else:
            cur_disambig += 1

        if cur_disambig > max_disambig:
            max_disambig = cur_disambig
        last_used_disambig_symbol_of[tokenseq] = cur_disambig
        tokenseq += f" #{cur_disambig}"
        ans.append((word, tokenseq.split()))
    return ans, max_disambig


def write_mapping(filename: str, sym2id: Dict[str, int]) -> None:
    """Write a symbol to ID mapping to a file.

    Note:
      No need to implement `read_mapping` as it can be done
      through :func:`k2.SymbolTable.from_file`.

    Args:
      filename:
        Filename to save the mapping.
      sym2id:
        A dict mapping symbols to IDs.
    Returns:
      Return None.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for sym, i in sym2id.items():
            f.write(f"{sym} {i}\n")


def lexicon_to_fst_no_sil(
        lexicon: Lexicon,
        token2id: Dict[str, int],
        word2id: Dict[str, int],
        need_self_loops: bool = False,
):
    """Convert a lexicon to an FST (in k2 format).

    Args:
      lexicon:
        The input lexicon. See also :func:`read_lexicon`
      token2id:
        A dict mapping tokens to IDs.
      word2id:
        A dict mapping words to IDs.
      need_self_loops:
        If True, add self-loop to states with non-epsilon output symbols
        on at least one arc out of the state. The input label for this
        self loop is `token2id["#0"]` and the output label is `word2id["#0"]`.
    Returns:
      Return an instance of `k2.Fsa` representing the given lexicon.
    """
    loop_state = 0  # words enter and leave from here
    next_state = 1  # the next un-allocated state, will be incremented as we go

    arcs = []

    # The blank symbol <blk> is defined in local/train_bpe_model.py
    assert token2id["<blank>"] == 0
    assert word2id["<eps>"] == 0

    eps = 0

    for word, pieces in lexicon:
        assert len(pieces) > 0, f"{word} has no pronunciations"
        cur_state = loop_state

        word = word2id[word]
        pieces = [
            token2id[i] if i in token2id else token2id["<unk>"] for i in pieces
        ]

        for i in range(len(pieces) - 1):
            w = word if i == 0 else eps
            arcs.append([cur_state, next_state, pieces[i], w, 0])

            cur_state = next_state
            next_state += 1

        # now for the last piece of this word
        i = len(pieces) - 1
        w = word if i == 0 else eps
        arcs.append([cur_state, loop_state, pieces[i], w, 0])

    if need_self_loops:
        disambig_token = token2id["#0"]
        disambig_word = word2id["#0"]
        arcs = add_self_loops(
            arcs,
            disambig_token=disambig_token,
            disambig_word=disambig_word,
        )

    final_state = next_state
    arcs.append([loop_state, final_state, -1, -1, 0])
    arcs.append([final_state])

    arcs = sorted(arcs, key=lambda arc: arc[0])
    arcs = [[str(i) for i in arc] for arc in arcs]
    arcs = [" ".join(arc) for arc in arcs]
    arcs = "\n".join(arcs)

    fsa = k2.Fsa.from_str(arcs, acceptor=False)
    return fsa


def contain_oov(token_sym_table: Dict[str, int], tokens: List[str]) -> bool:
    """Check if all the given tokens are in token symbol table.

    Args:
      token_sym_table:
        Token symbol table that contains all the valid tokens.
      tokens:
        A list of tokens.
    Returns:
      Return True if there is any token not in the token_sym_table,
      otherwise False.
    """
    for tok in tokens:
        if tok not in token_sym_table:
            return True
    return False


def generate_lexicon(token_sym_table: Dict[str, int],
                     words: List[str]) -> Lexicon:
    """Generate a lexicon from a word list and token_sym_table.

    Args:
      token_sym_table:
        Token symbol table that mapping token to token ids.
      words:
        A list of strings representing words.
    Returns:
      Return a dict whose keys are words and values are the corresponding
          tokens.
    """
    lexicon = []
    for word in tqdm(words, desc="Generating lexicon", total=len(words)):
        chars = list(word.strip(" \t"))
        if contain_oov(token_sym_table, chars):
            continue
        lexicon.append((word, chars))

    # The OOV word is <UNK>
    lexicon.append(("<UNK>", ["<unk>"]))
    return lexicon


def generate_tokens(text_file: str) -> Dict[str, int]:
    """Generate tokens from the given text file.

    Args:
      text_file:
        A file that contains text lines to generate tokens.
    Returns:
      Return a dict whose keys are tokens and values are token ids ranged
      from 0 to len(keys) - 1.
    """
    token2id: Dict[str, int] = dict()
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            char, index = line.replace('\n', '').split()
            assert char not in token2id
            token2id[char] = int(index)
    assert token2id['<blank>'] == 0
    return token2id


def generate_words(text_file: str) -> Dict[str, int]:
    from .utils_file import makedir, logging_print, GxlTimer, load_list_file_clean
    """Generate words from the given text file.

    Args:
      text_file:
        A file that contains text lines to generate words.
    Returns:
      Return a dict whose keys are words and values are words ids ranged
      from 0 to len(keys) - 1.
    """
    words = []
    lines = load_list_file_clean(text_file)
    for line in tqdm(lines, desc="Generating words", total=len(lines)):
        word = line.replace('\n', '')
        # assert word not in words
        words.append(word)
    words = list(set(words))
    words.sort()
    logging_print('耿雪龙: 生成词典list len: {}'.format(len(words)))

    # We put '<eps>' '<UNK>' at begining of word2id
    # '#0', '<s>', '</s>' at end of word2id
    words = [
        word for word in words
        if word not in ['<eps>', '<UNK>', '#0', '<s>', '</s>']
    ]
    words.insert(0, '<eps>')
    words.insert(1, '<UNK>')
    words.append('#0')
    words.append('<s>')
    words.append('</s>')
    word2id = {j: i for i, j in enumerate(words)}
    return word2id


def do_compile_HLG(lang_dir: str, lm: str = "G_3_gram"):
    from .utils_file import makedir, logging_print, GxlTimer, load_list_file_clean
    try:
        from icefall.lexicon import Lexicon as Lexicon_icefall
    except:
        pass
    lang_dir = str(lang_dir)
    if lang_dir.endswith("/"):
        lang_dir = lang_dir[:-1]
    lexicon = Lexicon_icefall(lang_dir)
    max_token_id = max(lexicon.tokens)
    logging_print(f"Building ctc_topo. max_token_id: {max_token_id}")
    H = k2.ctc_topo(max_token_id)
    L = k2.Fsa.from_dict(torch.load(f"{lang_dir}/L_disambig.pt"))
    # if Path(f"{lang_dir}/{lm}.pt").is_file():
    #     # 不应该被执行
    #     logging_print(f"Loading pre-compiled {lm}")
    #     d = torch.load(f"{lang_dir}/{lm}.pt")
    #     G = k2.Fsa.from_dict(d)
    # else:
    #     logging_print(f"Loading {lm}.fst.txt")
    #     with open(f"{lang_dir}/{lm}.fst.txt") as f:
    #         G = k2.Fsa.from_openfst(f.read(), acceptor=False)
    #         torch.save(G.as_dict(), f"{lang_dir}/{lm}.pt")
    logging_print(f"Loading {lm}.fst.txt")
    with open(f"{lang_dir}/{lm}.fst.txt") as f:
        G = k2.Fsa.from_openfst(f.read(), acceptor=False)
        torch.save(G.as_dict(), f"{lang_dir}/{lm}.pt")

    first_token_disambig_id = lexicon.token_table["#0"]
    first_word_disambig_id = lexicon.word_table["#0"]

    L = k2.arc_sort(L)
    G = k2.arc_sort(G)

    logging_print("Intersecting L and G")
    LG = k2.compose(L, G)
    logging_print(f"LG shape: {LG.shape}")

    logging_print("Connecting LG")
    LG = k2.connect(LG)
    logging_print(f"LG shape after k2.connect: {LG.shape}")

    logging_print(type(LG.aux_labels))
    logging_print("Determinizing LG")

    LG = k2.determinize(LG)
    logging_print(type(LG.aux_labels))

    logging_print("Connecting LG after k2.determinize")
    LG = k2.connect(LG)

    logging_print("Removing disambiguation symbols on LG")

    # LG.labels[LG.labels >= first_token_disambig_id] = 0
    # see https://github.com/k2-fsa/k2/pull/1140
    labels = LG.labels
    labels[labels >= first_token_disambig_id] = 0
    LG.labels = labels

    print(LG.aux_labels)
    # LG.aux_labels=k2.RaggedTensor(LG.aux_labels.numpy().tolist())
    assert isinstance(LG.aux_labels, k2.RaggedTensor)
    LG.aux_labels.values[LG.aux_labels.values >= first_word_disambig_id] = 0

    LG = k2.remove_epsilon(LG)
    logging_print(f"LG shape after k2.remove_epsilon: {LG.shape}")

    LG = k2.connect(LG)
    LG.aux_labels = LG.aux_labels.remove_values_eq(0)

    logging_print("Arc sorting LG")
    LG = k2.arc_sort(LG)

    logging_print("Composing H and LG")
    # CAUTION: The name of the inner_labels is fixed
    # to `tokens`. If you want to change it, please
    # also change other places in icefall that are using
    # it.
    HLG = k2.compose(H, LG, inner_labels="tokens")

    logging_print("Connecting LG")
    HLG = k2.connect(HLG)

    logging_print("Arc sorting LG")
    HLG = k2.arc_sort(HLG)
    logging_print(f"HLG.shape: {HLG.shape}")

    return HLG


def do_prepare_char4hlg(input_words_dict_path, input_tokens_dict_path, output_dir):
    from .utils_file import makedir, logging_print, GxlTimer, load_list_file_clean
    try:
        from icefall.lexicon import read_lexicon, write_lexicon
    except:
        pass
    logging_print('耿雪龙: 首先进行 prepare_char ')
    timer = GxlTimer()
    timer.start()
    logging_print('耿雪龙: 开始生成 token2id')
    token2id = generate_tokens(input_tokens_dict_path)
    logging_print('耿雪龙: 生成token2id 完成, len: {}'.format(len(token2id)))
    timer.stop_halfway()
    logging_print('耿雪龙: 开始生成word2id')
    word2id = generate_words(input_words_dict_path)
    logging_print('耿雪龙: 生成word2id完成, len: {}'.format(len(word2id)))
    timer.stop_halfway()

    words = [
        word for word in word2id.keys() if word not in
                                           ["<eps>", "!SIL", "<SPOKEN_NOISE>", "<UNK>", "#0", "<s>", "</s>"]
    ]
    logging_print('耿雪龙: 开始生成 lexicon')
    lexicon = generate_lexicon(token2id, words)
    logging_print('耿雪龙: 生成lexicon 完成, len: {}'.format(len(lexicon)))
    timer.stop_halfway()

    logging_print('耿雪龙: 开始生成 消歧义 并得到各种txt')
    lexicon_disambig, max_disambig = add_disambig_symbols(lexicon)
    next_token_id = max(token2id.values()) + 1
    for i in range(max_disambig + 1):
        disambig = f"#{i}"
        assert disambig not in token2id
        token2id[disambig] = next_token_id
        next_token_id += 1
    tgt_dir = Path(output_dir)
    write_mapping(os.path.join(output_dir, 'tokens.txt'), token2id)
    write_mapping(os.path.join(output_dir, 'words.txt'), word2id)
    write_lexicon(os.path.join(output_dir, 'lexicon.txt'), lexicon)
    write_lexicon(os.path.join(output_dir, 'lexicon_disambig.txt'), lexicon_disambig)
    L = lexicon_to_fst_no_sil(
        lexicon,
        token2id=token2id,
        word2id=word2id,
    )
    L_disambig = lexicon_to_fst_no_sil(
        lexicon_disambig,
        token2id=token2id,
        word2id=word2id,
        need_self_loops=True,
    )
    torch.save(L.as_dict(), tgt_dir / "L.pt")
    torch.save(L_disambig.as_dict(), tgt_dir / "L_disambig.pt")
    logging_print('耿雪龙: 生成 消歧义 并得到各种txt 完成')
    timer.stop_halfway()


def do_make_HLG(input_words_dict_path, input_tokens_dict_path, input_arpa_file_path, output_dir):
    """

    :param input_words_dict_path:
    :param input_tokens_dict_path:
    :param input_arpa_file_path:
    :return:
    """
    from .utils_file import makedir, logging_print, GxlTimer, load_list_file_clean
    import subprocess
    makedir(output_dir)
    do_prepare_char4hlg(input_words_dict_path, input_tokens_dict_path, output_dir)
    timer = GxlTimer()
    logging_print('开始生成 .fst.txt')
    tgt_dir = output_dir
    if tgt_dir.endswith("/"):
        tgt_dir = tgt_dir[:-1]
    arpa_path = input_arpa_file_path
    # 构建命令
    command = [
        "python", "-m", "kaldilm",
        "--read-symbol-table=" + tgt_dir + "/words.txt",
        "--disambig-symbol='#0'",
        "--max-order=3",
        arpa_path
    ]
    # 执行命令并重定向输出到文件
    output_file = tgt_dir + "/G_3_gram.fst.txt"
    with open(output_file, "w") as f:
        subprocess.run(command, stdout=f)

    logging_print('生成 .fst.txt 完成')
    timer.stop_halfway()

    logging_print('开始生成HLG.pt')
    lang_dir = Path(output_dir)
    if (lang_dir / "HLG.pt").is_file():
        logging_print(f"{lang_dir}/HLG.pt already exists - skipping")
    logging_print(f"Processing {output_dir}")
    lm = "G_3_gram"
    HLG = do_compile_HLG(output_dir, lm)
    logging_print(f"Saving HLG.pt to {output_dir}")
    torch.save(HLG.as_dict(), f"{output_dir}/HLG.pt")
    logging_print('生成HLG.pt 完成')
    timer.stop_halfway()


def do_get_utt2spk(input_kaldi_dir, name='gxl'):
    """"""
    from .utils_file import load_dict_from_scp, write_dict_to_scp, logging_print
    res_path = os.path.join(input_kaldi_dir, 'utt2spk')
    if os.path.exists(res_path):
        logging_print('do_get_utt2spk: utt2spk文件已存在，不用重复生成')
        return
    text_path = os.path.join(input_kaldi_dir, 'text')
    text_dict = load_dict_from_scp(text_path)
    res_dict = {k: name for k in text_dict.keys()}
    write_dict_to_scp(res_dict, res_path)


def make_cuts_from_scp(input_kaldi_dir, output_dir, prefix='gxldata', patition='train'):
    import lhotse
    from lhotse import CutSet
    from .utils_file import do_get_utt2spk, logging_print, do_compress_file_by_gzip
    assert os.path.exists(input_kaldi_dir) and os.path.exists(
        os.path.join(input_kaldi_dir, 'wav.scp')) and os.path.exists(os.path.join(input_kaldi_dir, 'text'))
    if not os.path.exists(os.path.join(input_kaldi_dir, 'utt2spk')):
        do_get_utt2spk(input_kaldi_dir)
    logging_print("开始load manifests")
    records, superisions, _ = lhotse.load_kaldi_data_dir(input_kaldi_dir, 16000)
    logging_print("开始fix manifests")
    records, superisions = lhotse.fix_manifests(records, superisions)
    logging_print("开始validate manifests")
    lhotse.validate_recordings_and_supervisions(records, superisions)
    records.to_file(os.path.join(output_dir, f"{prefix}_recordings_{patition}.jsonl"))
    do_compress_file_by_gzip(os.path.join(output_dir, f"{prefix}_recordings_{patition}.jsonl"))
    superisions.to_file(os.path.join(output_dir, f"{prefix}_supervisions_{patition}.jsonl"))
    do_compress_file_by_gzip(os.path.join(output_dir, f"{prefix}_supervisions_{patition}.jsonl"))
    cuts = CutSet.from_manifests(recordings=records, supervisions=superisions)
    cuts.to_file(os.path.join(output_dir, f"{prefix}_cuts_{patition}.jsonl"))
    do_compress_file_by_gzip(os.path.join(output_dir, f"{prefix}_cuts_{patition}.jsonl"))


def do_make_cuts_from_scp_multi_thread(input_kaldi_dir,
                                       output_dir,
                                       prefix='gxldata',
                                       partition='train',
                                       temp_dir='./temp_dir',
                                       thread_num=100):
    """"""
    from .utils_file import (GxlTimer, do_remove_last_slash, logging_print, load_dict_from_scp,
                             do_split_dict, GxlDynamicThreadPool, makedir_sil, write_dict_to_scp,
                             load_list_file_clean, write_list_to_file, do_compress_file_by_gzip, remove_dir)
    timer_obj = GxlTimer()
    random_int = random.randint(1, 100000000)
    temp_dir = do_remove_last_slash(temp_dir)
    temp_dir = f'{temp_dir}_{random_int}'
    output_dir = do_remove_last_slash(output_dir)
    logging_print("开始load kaldi dir")
    # 这个目录下要确保有wav.scp text
    wav_dict = load_dict_from_scp(input_kaldi_dir + '/wav.scp')
    text_dict = load_dict_from_scp(input_kaldi_dir + '/text')
    wav_dict_list = do_split_dict(wav_dict, thread_num)
    runner = GxlDynamicThreadPool()
    for i, wav_dict_i in enumerate(wav_dict_list):
        text_dict_i = {k: text_dict[k] for k in wav_dict_i.keys() if k in text_dict}
        temp_dir_i = f'{temp_dir}/split/split_{i}'
        makedir_sil(temp_dir_i)
        write_dict_to_scp(wav_dict_i, f'{temp_dir_i}/wav.scp')
        write_dict_to_scp(text_dict_i, f'{temp_dir_i}/text')
        do_get_utt2spk(temp_dir_i)
        output_dir_i = f'{output_dir}/split_{i}'
        makedir_sil(output_dir_i)
        runner.add_thread(make_cuts_from_scp, [temp_dir_i, output_dir_i, prefix, partition])
    runner.start()
    logging_print('全部小线程都完结,开始合并')
    res_list_1 = []
    res_list_2 = []
    res_list_3 = []
    for i in range(thread_num):
        output_dir_i = f'{output_dir}/split/split_{i}'
        cuts_path_i = f'{output_dir_i}/{prefix}_cuts_{partition}.jsonl'
        recordings_path_i = f'{output_dir_i}/{prefix}_recordings_{partition}.jsonl'
        supervisions_path_i = f'{output_dir_i}/{prefix}_supervisions_{partition}.jsonl'
        cut_list_i = load_list_file_clean(cuts_path_i)
        res_list_1.append(cut_list_i)
        recordings_list_i = load_list_file_clean(recordings_path_i)
        res_list_2.append(recordings_list_i)
        supervisions_list_i = load_list_file_clean(supervisions_path_i)
        res_list_3.append(supervisions_list_i)
    cuts_output_path = f'{output_dir}/{prefix}_cuts_{partition}.jsonl'
    recordings_output_path = f'{output_dir}/{prefix}_recordings_{partition}.jsonl'
    supervisions_output_path = f'{output_dir}/{prefix}_supervisions_{partition}.jsonl'
    write_list_to_file(res_list_1, cuts_output_path)
    write_list_to_file(res_list_2, recordings_output_path)
    write_list_to_file(res_list_3, supervisions_output_path)
    do_compress_file_by_gzip(cuts_output_path)
    do_compress_file_by_gzip(recordings_output_path)
    do_compress_file_by_gzip(supervisions_output_path)
    remove_dir(temp_dir)
    timer_obj.stop_halfway()


def _do_jieba_fenci(str_input:str):
    import jieba.posseg as pseg
    string = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1 \2', str_input)
    str_input = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1 \2', string)
    words = pseg.cut(str_input)
    res = []
    for word, flag in words:
        res.append(word)
    res = [item for item in res if len(item.strip()) != 0]
    return res
thu1= None
def _do_thulab_fenci(str_input:str):
    string = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1 \2', str_input)
    string = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1 \2', string)
    words = thu1.cut(string, text=True)  # 进行分词
    res = words.split(' ')  # 分词结果是一个字符串，每个词之间用空格分隔，所以我们需要用split函数来将其转换为列表
    return res



def do_fenci(str_input:str, fenci_obj_type:str='thulac'):
    """
    对str_input进行分词, 默认选择thulac,比jiaba更好
    :param str_input:
    :param fenci_obj_type:
    :return:
    """
    global thu1
    if thu1 is None:
        import thulac
        thu1 = thulac.thulac(seg_only=True)  # 设置只进行分词，不进行词性标注

    if fenci_obj_type == 'jieba':
        return _do_jieba_fenci(str_input)
    elif fenci_obj_type == 'thulac':
        return _do_thulab_fenci(str_input)
    else:
        raise NotImplementedError


def do_judge_str_is_all_chinese(str_input:str):
    """
    判断str_input是否全是中文
    :param str_input:
    :return:
    """
    for ch in str_input:
        if not '\u4e00' <= ch <= '\u9fff':
            return False
    return True

def do_judge_str_is_all_english(str_input:str):
    """
    判断str_input是否全是英文
    :param str_input:
    :return:
    """
    for ch in str_input:
        if not '\u0041' <= ch <= '\u007a':
            return False
    return True

def do_judge_str_is_contain_chinese(str_input:str):
    """
    判断str_input是否包含中文
    :param str_input:
    :return:
    """
    for ch in str_input:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def do_judge_str_is_contain_english(str_input:str):
    """
    判断str_input是否包含英文
    :param str_input:
    :return:
    """
    for ch in str_input:
        if '\u0041' <= ch <= '\u007a':
            return True
    return False


def do_get_logger(logger_name,log_dir, prefix="log"):
    # logging INFO
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_name = time.asctime().replace(':', "-").replace(" ", "_")
    print(__file__)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{}/{}_{}_log.txt".format(log_dir, prefix, log_name), mode='w',
                                  encoding='utf-8')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 2. 添加终端显示的 StreamHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    # 添加到 logger
    logger.addHandler(console_handler)

    return logger

def do_config_root_logger(log_dir=None, prefix="log"):
    """
    如果没有指定 log_dir 则只输出到终端
    如果指定了 log_dir 则同时输出到文件和终端
    """
    log_name = time.asctime().replace(':', "-").replace(" ", "_")
    # log_format = '%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s'
    log_format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    if log_dir is not None:
        handlers = [
            # FileHandler 以 utf-8 编码写入日志文件
            logging.FileHandler("{}/{}_{}_log.txt".format(log_dir, prefix, log_name), mode='w',
                                encoding='utf-8'),
            # StreamHandler 用于将日志输出到终端
            logging.StreamHandler()
        ]
    else:
        handlers = [
            # StreamHandler 用于将日志输出到终端
            logging.StreamHandler()
        ]

    logging.basicConfig(level=logging.INFO,  # 设置日志级别为 INFO
                        format=log_format,  # 设置日志格式
                        handlers=handlers)

def do_set_random_seed(seed):
    # Set seeds for determinism
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


def do_copy_dir(input_dir, output_dir):
    """
    使用shutil.copytree来复制目录
    :param input_dir: 源目录路径
    :param output_dir: 目标目录路径（包含要创建的子目录名） ,如果输出目录存在, 则不去覆盖,而是直接返回
    """
    # 确保目标目录的基目录存在
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    # 复制目录
    try:
        shutil.copytree(input_dir, output_dir)
    except FileExistsError:
        # 如果目标目录已存在，可以选择删除后重新复制，或者跳过复制（这里选择跳过）
        print(f"目标目录 {output_dir} 已存在，跳过复制。")
    except Exception as e:
        # 处理其他可能的异常
        print(f"复制目录时发生错误: {e}")


def do_compress_directory_by_tar_form(source_dir, output_dir):
    """
    将源目录压缩到output_dir，格式为tar.
    :param source_dir:
    :param output_dir:
    :return:
    """
    # 获取要压缩目录的名称
    base_name = os.path.basename(source_dir)
    # 设置压缩后的文件路径，不包含文件扩展名
    output_path = os.path.join(output_dir, base_name)

    # 压缩文件，格式为 tar
    shutil.make_archive(str(output_path), 'tar', source_dir)

def do_judge_file_exist(file_path):
    return os.path.exists(file_path)

def if_file_exist(file_path):
    return os.path.exists(file_path)

def if_dir_exist(dir_path):
    return os.path.isdir(dir_path)