from tqdm import tqdm

from gxl_ai_utils.audio_dataset.common_data_handler import *

import pickle
import torch
import torch.nn.utils.rnn as rnn
import os

from gxl_ai_utils.config.gxl_config import GxlNode

from sortedcontainers import SortedSet
from torch.utils.data import DataLoader


class LabelTokenizer:
    UNK_TOKEN = "<UNK>"
    UNK_ID = -1

    def __init__(self, vocab_file_path='./output/label_vocab_dict.pkl'):
        """"""
        self.vocab_file_path = vocab_file_path
        self._id_to_token = {}
        self._token_to_id = {}
        os.makedirs(os.path.dirname(vocab_file_path), exist_ok=True)

    def build_vocab(self, label_list):
        sortedSet = SortedSet(label_list)
        self._token_to_id = {token: index for index, token in enumerate(sortedSet)}
        self._token_to_id[self.UNK_TOKEN] = self.UNK_ID
        self._id_to_token = {token_id: token for token, token_id in self._token_to_id.items()}
        with open(self.vocab_file_path, "wb") as f:
            pickle.dump(list(sortedSet), f)

    def load_vocab(self, ):
        """加载已保存的字典"""
        with open(self.vocab_file_path, "rb") as f:
            sortedSet = SortedSet(pickle.load(f))
        self._token_to_id = {token: index for index, token in enumerate(sortedSet)}
        self._token_to_id[self.UNK_TOKEN] = self.UNK_ID
        self._id_to_token = {token_id: token for token, token_id in self._token_to_id.items()}

    def __len__(self):
        return len(self._token_to_id)

    def encode(self, x: str | list) -> list[int]:
        if isinstance(x, str):
            return [self._token_to_id.get(x, self.UNK_ID)]
        elif isinstance(x, list):
            return [self._token_to_id.get(token, self.UNK_ID) for token in x]

    def decode(self, x: int | list | torch.Tensor) -> list[str]:
        """解码，输入int, int_list, int_tensor，只支持一维ids
        return -> token list"""
        if isinstance(x, int):
            return [self._id_to_token.get(x, self.UNK_TOKEN)]
        if isinstance(x, list):
            assert isinstance(x[0], int)
            return [self._id_to_token.get(token_id, self.UNK_TOKEN) for token_id in x]
        elif isinstance(x, torch.Tensor):
            assert x.dim() == 1
            return [self._id_to_token.get(token_id, self.UNK_TOKEN) for token_id in x]

    def show_token_id(self):
        for token, id in self._token_to_id.items():
            print(token + ' --- ' + str(id))


class ChineseVocabTokenizer:
    SOD_TOKEN = "<SOD>"
    EOD_TOKEN = "<EOD>"
    UNK_TOKEN = "<UNK>"
    PAD_TOKEN = "<PAD>"
    BLANK_TOKEN = "_BLANK_"
    SOD_ID = 0
    EOD_ID = 1
    UNK_ID = 2
    PAD_ID = 3
    BLANK_ID = 4

    def __init__(self, tokenizer=lambda x: [y for y in x], vocab_file_path='./output/vocab_set.pkl'):
        self.vocab_set = SortedSet()
        self._token_to_id = {}
        self._id_to_token = {}
        self.tokenizer = tokenizer
        self.vocab_file_path = vocab_file_path

    def load_vocab(self, ):
        """加载已保存的字典"""
        with open(self.vocab_file_path, "rb") as f:
            self.vocab_set = SortedSet(pickle.load(f))
        self._from_set_build_dict()

    def build_vocab(self, label_list):
        """构建字典"""
        for label in label_list:
            self.vocab_set.update(self.tokenizer(label))
        self._from_set_build_dict()
        with open(self.vocab_file_path, "wb") as f:
            pickle.dump(list(self.vocab_set), f)

    def _from_set_build_dict(self):
        self._token_to_id = {token: id + 5 for id, token in enumerate(self.vocab_set)}
        self._token_to_id[self.SOD_TOKEN] = self.SOD_ID
        self._token_to_id[self.EOD_TOKEN] = self.EOD_ID
        self._token_to_id[self.UNK_TOKEN] = self.UNK_ID
        self._token_to_id[self.PAD_TOKEN] = self.PAD_ID
        self._token_to_id[self.BLANK_TOKEN] = self.BLANK_ID
        self._id_to_token = {token_id: token for token, token_id in self._token_to_id.items()}

    def __len__(self):
        return len(self._token_to_id)

    def encode(self, x):
        """x: str, list, 只能是一维的token_list
        return -> id_list"""
        if isinstance(x, str) and self._token_to_id.get(x, None):
            return [self._token_to_id[x]]  # 如果为单个token
        if isinstance(x, str):
            x = self.tokenizer(x)
        assert isinstance(x, list)
        if len(x) == 0:
            return []
        assert isinstance(x[0], str)
        return [self._token_to_id.get(token, self.UNK_ID) for token in x]

    def decode(self, x: int | list | torch.Tensor):
        """解码，输入int, int_list, int_tensor，只支持一维ids
        return -> token list"""
        if isinstance(x, int):
            return [self._id_to_token.get(x, self.UNK_TOKEN)]
        if isinstance(x, list):
            assert isinstance(x[0], int)
            return [self._id_to_token.get(token_id, self.UNK_TOKEN) for token_id in x]
        elif isinstance(x, torch.Tensor):
            assert x.dim() == 1
            return [self._id_to_token.get(token_id, self.UNK_TOKEN) for token_id in x]

    def show_token_id(self):
        for token, id in self._token_to_id.items():
            print(token + ' --- ' + str(id))


def build_tokenizer_by_jsonl(jsonl_file, config: GxlNode):
    _, label_list = get_wavfilepath_and_label_from_jsonl(jsonl_file, config.dataset.wav_key, config.dataset.label_key)
    tokenizer = ChineseVocabTokenizer()
    tokenizer.build_vocab(label_list)
    tokenizer.show_token_id()


def build_tokenizer_by_json(json_file, config: GxlNode):
    _, label_list = get_wavfilepath_and_label_from_json(json_file, config.dataset.wav_key, config.dataset.label_key)
    tokenizer = ChineseVocabTokenizer()
    tokenizer.build_vocab(label_list)
    tokenizer.show_token_id()


def load_tokenizer():
    tokenizer = ChineseVocabTokenizer()
    tokenizer.load_vocab()
    return tokenizer


class RecognitionDataset(GxlAudioDataset):
    def __init__(self, wav_path_list, label_list, config: GxlNode):
        super(RecognitionDataset, self).__init__(wav_path_list, label_list, config)
        self.tokenizer = load_tokenizer()
        if config.dataset.global_cmvn_file:
            cmvn_dict = utils_file.load_dict_from_json(config.dataset.global_cmvn_file)
            self.global_means = torch.tensor(cmvn_dict['global_means'])
            self.global_vars = torch.tensor(cmvn_dict['global_vars'])

    def __getitem__(self, index):
        mel_num = self.config.dataset.mel_num
        min_sec = self.config.dataset.min_sec
        max_sec = self.config.dataset.max_sec
        label = self.tokenizer.encode(self.label_list[index])
        wav = compute_fbank(self.wav_path_list[index], mel_num=mel_num, min_sec=min_sec, max_sec=max_sec)
        if wav is None:
            return None, None
        if self.global_vars is not None:
            wav = apply_cmvn(self.global_means, self.global_vars, wav)
        return wav, torch.tensor(label, dtype=torch.int32)


def compute_cmvn(fbank_feature: torch.Tensor):
    """
    :param fbank_feature: tensor:(frame_num, mel_len)
    """
    mean = torch.mean(fbank_feature, dim=0)
    var = torch.var(fbank_feature, dim=0)
    return mean, var


def calculate_fbank_cmvn(json_file: str, config: GxlNode):
    """"""
    if config.dataset.global_cmvn_file is None:
        return
    os.makedirs(os.path.dirname(config.dataset.global_cmvn_file), exist_ok=True)
    big_dic = utils_file.load_dict_from_json(json_file)
    means = []
    vars = []
    values = list(big_dic.values())
    for dic in tqdm(values, total=len(values)):
        wav_path = dic[config.dataset.wav_key]
        fbank_feature = compute_fbank(wav_path, config.dataset.mel_num, config.dataset.min_sec, config.dataset.max_sec)
        if fbank_feature is None:
            continue
        mean, var = compute_cmvn(fbank_feature)
        means.append(mean)
        vars.append(var)
    means_tensor = torch.stack(means)
    vars_tensor = torch.stack(vars)
    global_means = torch.mean(means_tensor, dim=0)
    global_vars = torch.mean(vars_tensor, dim=0)
    res_dict = {"global_means": global_means.tolist(), "global_vars": global_vars.tolist()}
    utils_file.write_dict_to_json(res_dict, config.dataset.global_cmvn_file, )


def apply_cmvn(mean: torch.Tensor, var: torch.Tensor, fbank_feature: torch.Tensor):
    return (fbank_feature - mean) / var


def collate_fn(batch):
    # batch 是一个列表，每个元素是一个元组 (wav, label)
    batch = [(wav, label) for (wav, label) in batch if wav is not None and label is not None]
    data_list, target_list = zip(*batch)
    data_lens = torch.tensor([len(item) for item in data_list], dtype=torch.int32)
    wav_input = rnn.pad_sequence(data_list, batch_first=True)
    target_lens = torch.tensor([len(item) for item in target_list], dtype=torch.int32)
    target_input = rnn.pad_sequence(target_list, batch_first=True)
    return wav_input, data_lens, target_input, target_lens


def get_iter_by_json(json_file_path, config: GxlNode):
    dataset = get_dataset_by_json(json_file_path, config)
    dataloader = DataLoader(dataset, batch_size=config.dataset.batch_size, drop_last=config.dataset.drop_last,
                            shuffle=config.dataset.shuffle,
                            collate_fn=collate_fn, num_workers=config.dataset.num_workers,
                            pin_memory=config.dataset.pin_memory)
    return dataloader


def get_iter_by_jsonl(jsonl_file_path, config: GxlNode):
    dataset = get_dataset_by_jsonl(jsonl_file_path, config)
    dataloader = DataLoader(dataset, batch_size=config.dataset.batch_size, drop_last=config.dataset.drop_last,
                            shuffle=config.dataset.shuffle,
                            collate_fn=collate_fn, num_workers=config.dataset.num_workers,
                            pin_memory=config.dataset.pin_memory)
    return dataloader


def get_dataset_by_json(json_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_json(json_file_path, config.dataset.wav_key,
                                                                    config.dataset.label_key)
    dataset = RecognitionDataset(wav_path_list, label_list, config)
    return dataset


def get_dataset_by_jsonl(json_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_jsonl(json_file_path, config.dataset.wav_key,
                                                                     config.dataset.label_key)
    dataset = RecognitionDataset(wav_path_list, label_list, config)
    return dataset
