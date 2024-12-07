from gxl_ai_utils.audio_dataset.common_data_handler import *

import pickle
import torch
import torch.nn.utils.rnn as rnn
import os

from gxl_ai_utils.config.gxl_config import GxlNode

from sortedcontainers import SortedSet
from torch.utils.data import Dataset, DataLoader


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
        print('vocab build done!')
        self.show_token_id()

    def load_vocab(self, ):
        """加载已保存的字典"""
        with open(self.vocab_file_path, "rb") as f:
            sortedSet = SortedSet(pickle.load(f))
        self._token_to_id = {token: index for index, token in enumerate(sortedSet)}
        self._token_to_id[self.UNK_TOKEN] = self.UNK_ID
        self._id_to_token = {token_id: token for token, token_id in self._token_to_id.items()}
        print('vocab load done!')
        self.show_token_id()

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


def build_tokenizer(label_list):
    tokenizer = LabelTokenizer()
    tokenizer.build_vocab(label_list)
    return tokenizer


def load_tokenizer():
    tokenizer = LabelTokenizer()
    tokenizer.load_vocab()
    return tokenizer


class ClassifyDataset(GxlAudioDataset):
    def __init__(self, wav_path_list, label_list, config: GxlNode):
        super(ClassifyDataset, self).__init__(wav_path_list, label_list, config)
        self.tokenizer = build_tokenizer(label_list)

    def __getitem__(self, index):
        mel_num = self.config.dataset.mel_num
        min_sec = self.config.dataset.min_sec
        max_sec = self.config.dataset.max_sec
        label = self.tokenizer.encode(self.label_list[index])[0]
        wav = compute_fbank(self.wav_path_list[index], mel_num=mel_num, min_sec=min_sec, max_sec=max_sec)
        if wav is None:
            return None, None
        return wav, torch.tensor(label, dtype=torch.int32)


def collate_fn(batch):
    # batch 是一个列表，每个元素是一个元组 (wav, label)
    batch = [(wav, label) for (wav, label) in batch if wav is not None and label is not None]
    data_list, target_list = zip(*batch)
    data_lens = torch.tensor([len(item) for item in data_list])
    wav_input = rnn.pad_sequence(data_list, batch_first=True)
    target_list = torch.tensor(target_list, dtype=torch.long)
    return wav_input, data_lens, target_list


def get_iter_by_json(json_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_json(json_file_path)
    dataset = ClassifyDataset(wav_path_list, label_list, config)
    dataloader = DataLoader(dataset, batch_size=config.dataset.batch_size, drop_last=True, shuffle=True,
                            collate_fn=collate_fn, num_workers=2, pin_memory=True)
    return dataloader


def get_iter_by_jsonl(jsonl_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_jsonl(jsonl_file_path)
    dataset = ClassifyDataset(wav_path_list, label_list, config)
    dataloader = DataLoader(dataset, batch_size=config.dataset.batch_size, drop_last=True, shuffle=True,
                            collate_fn=collate_fn, num_workers=2, pin_memory=True)
    return dataloader


def get_dataset_by_json(json_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_json(json_file_path)
    dataset = ClassifyDataset(wav_path_list, label_list, config)
    return dataset


def get_dataset_by_jsonl(json_file_path, config: GxlNode):
    wav_path_list, label_list = get_wavfilepath_and_label_from_jsonl(json_file_path)
    dataset = ClassifyDataset(wav_path_list, label_list, config)
    return dataset
