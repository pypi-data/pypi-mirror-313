import os
import pickle
from abc import ABC

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

from gxl_ai_utils import AiConstant
from gxl_ai_utils.utils import utils_data


class RandomDataset(Dataset):
    def __init__(self, dataset_size, channel=3, image_size=32):
        images = torch.randn(dataset_size, channel, image_size, image_size)
        labels = torch.zeros(dataset_size)
        self.data = list(zip(images, labels))

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


class CommonDataset(Dataset):
    def __init__(self, data_list: list, dtype=torch.float32):
        self.dtype = dtype
        self.data_list = self._to_tensor(data_list)

    def __getitem__(self, index):
        return self.data_list[index]

    def __len__(self):
        return len(self.data_list)

    def _to_tensor(self, datas):
        will_be_zip = []
        if len(datas) < 1 or datas is None:
            print("数据为空,无法使用,from store_data.py")
            return torch.zeros(0)
        column = len(datas[0])
        for i in range(column):
            x = torch.tensor([_[i] for _ in datas], dtype=self.dtype)
            will_be_zip.append(x)
        return list(zip(*will_be_zip))


class FlowerDataset(Dataset, ABC):
    data_transforms = {
        'train':
            transforms.Compose([
                transforms.Resize(64),
                transforms.RandomRotation(45),  # 随机旋转，-45到45度之间随机选
                transforms.CenterCrop(64),  # 从中心开始裁剪
                transforms.RandomHorizontalFlip(p=0.5),  # 随机水平翻转 选择一个概率概率
                transforms.RandomVerticalFlip(p=0.5),  # 随机垂直翻转
                transforms.ColorJitter(brightness=0.2, contrast=0.1, saturation=0.1, hue=0.1),
                # 参数1为亮度，参数2为对比度，参数3为饱和度，参数4为色相
                transforms.RandomGrayscale(p=0.025),  # 概率转换成灰度率，3通道就是R=G=B
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 均值，标准差
            ]),
        'valid':
            transforms.Compose([
                transforms.Resize(64),
                transforms.CenterCrop(64),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
    }

    def __init__(self, resource_dir, mapping_list_file, transform=None):
        self.resource_dir = resource_dir
        self.mapping_list_file = mapping_list_file
        self.info_dict = self.load_data_from_disk()
        self.image_paths_list = [os.path.join(self.resource_dir, x) for x in list(self.info_dict.keys())]
        self.labels_list = [x for x in list(self.info_dict.values())]
        self.transform = transform

    def __len__(self):
        return len(self.image_paths_list)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths_list[idx])
        label = self.labels_list[idx]
        if self.transform is not None:
            image = self.transform(image)
        label = torch.from_numpy(label)
        return image, label

    def load_data_from_disk(self):
        data_infos = {}
        with open(self.mapping_list_file) as f:
            samples = [x.strip().split(" ") for x in f.readlines()]
            for path, label in samples:
                data_infos[path] = np.array(label, dtype=np.int64)
        return data_infos


def get_text_classify_dataset(data_path: str):
    def build_dataset(vocab_path, train_path, valid_path, test_path, use_word: bool = False):
        if use_word:
            tokenizer = lambda x: x.split("")  # 用词作为基本单位,中文为true
        else:
            tokenizer = lambda x: [y for y in x]  # 以字符为单位,对于中文来说就是以字为单位
        if os.path.exists(vocab_path):
            vocab = pickle.load(open(vocab_path, 'rb'))
        else:
            vocab = utils_data.build_vocab(train_path, tokenizer)
            pickle.dump(vocab, open(vocab_path, 'wb'))
        print(f'vocab size:{len(vocab):.4f}')
        train_list = utils_data.load_list_from_disk(train_path, vocab, tokenizer)
        valid_list = utils_data.load_list_from_disk(valid_path, vocab, tokenizer)
        test_list = utils_data.load_list_from_disk(test_path, vocab, tokenizer)
        train_set = CommonDataset(train_list, dtype=torch.int64)
        valid_set = CommonDataset(valid_list, dtype=torch.int64)
        test_set = CommonDataset(test_list, dtype=torch.int64)
        return train_set, valid_set, test_set

    # data_path = AiConstant.DATA_PATH + 'text_data/'  # 路径可访问
    return build_dataset(vocab_path=data_path + '/vocab.pkl',
                         train_path=data_path + '/train.txt',
                         valid_path=data_path + '/dev.txt',
                         test_path=data_path + '/test_gxl_ai_utils.txt')
