import gzip
import os
import pickle
from abc import ABC
from pathlib import Path

import numpy as np
from PIL import Image
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import requests
import torch.utils.data
from torch.utils.data import Dataset, DataLoader
from gxl_ai_utils.AiConstant import DATA_PATH

from . import store_dataloader
from . import store_data_name
from .store_dataset import store_dataset


class DataStore:
    """数据仓库
    如果指定数据集的位置, 则代表已经自己下载数据集, 如果没有指定位置, 则代表还没有下载, 程序自动下载到默认目录,
    下载的位置不能自己指定
    """

    def __init__(self, data_name, data_path=None):
        self.data_name = data_name
        self.data_path = data_path
        self.PATH = Path(DATA_PATH) / data_name if data_path is None else Path(data_path)
        self.str_path = str(self.PATH)
        self.PATH.mkdir(parents=True, exist_ok=True)

    def get_dataset(self):
        if self.data_name == store_data_name.MNIST:

            pipeline = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
            # 下载数据集

            train_set = datasets.MNIST(root=self.str_path, train=True,
                                       download=self.data_path is None, transform=pipeline)
            test_set = datasets.MNIST(root=self.str_path, train=False,
                                      download=self.data_path is None, transform=pipeline)
            return train_set, test_set
        elif self.data_name == store_data_name.MNIST_RANDOM:
            # 定义一个随机数据集
            return store_dataset.RandomDataset(50000, 1, 28), store_dataset.RandomDataset(10000, 1, 28)
        elif self.data_name == store_data_name.FLOWER_CLASSIFY:
            data_dir = self.PATH
            train_dir = data_dir / 'handled' / 'train'
            valid_dir = data_dir / 'handled' / 'valid'
            data_transforms = store_dataset.FlowerDataset.data_transforms
            image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in
                              ['train', 'valid']}
            return image_datasets['train'], image_datasets['valid']
        elif self.data_name == store_data_name.FLOWER_CLASSIFY_SELF_DATASET:
            train_set = store_dataset.FlowerDataset(
                resource_dir=self.str_path + '/flower_data/train_filelist',
                mapping_list_file=self.str_path + '/flower_data/train.txt',
                transform=store_dataset.FlowerDataset.data_transforms['train']
            )
            valid_set = store_dataset.FlowerDataset(
                resource_dir=self.str_path + '/flower_data/val_filelist',
                mapping_list_file=self.str_path + '/flower_data/val.txt',
                transform=store_dataset.FlowerDataset.data_transforms['valid']
            )
            return train_set, valid_set
        elif self.data_name == store_data_name.TEXT_CLASSIFY:
            return store_dataset.get_text_classify_dataset(self.str_path)
        else:
            print('找不到数据集')
            return None

    def get_dataloader(self, batch_size=64):
        X = self.get_dataset()
        if len(X) == 2:
            train_set, test_set = X
            train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
            test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)
            return train_loader, test_loader
        elif len(X) == 3:
            train_set, valid_set, test_set = X
            train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
            valid_loader = DataLoader(valid_set, batch_size=batch_size, shuffle=True)
            test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)
            return train_loader, valid_loader, test_loader
        elif len(X) == 1:
            train_set = X
            train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
            return train_loader
        else:
            return None
