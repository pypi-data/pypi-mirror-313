import random
from abc import ABC
from typing import Callable, Iterable

import torch
import torch.distributed as dist
from torch.utils.data import IterableDataset
from . import gxl_processor


class GxlDistributedSampler:
    def __init__(self, shuffle=True, partition=True):
        self.num_workers = None
        self.worker_id = None
        self.world_size = None
        self.rank = None
        self.epoch = -1
        self.update()
        self.shuffle = shuffle
        self.partition = partition

    def update(self):
        # assert dist.is_available()
        if not dist.is_available():
            self.worker_id = 0
            self.num_workers = 1
            self.worker_id = 0
            self.num_workers = 1
            return dict(rank=self.rank,
                        world_size=self.world_size,
                        worker_id=self.worker_id,
                        num_workers=self.num_workers)
        if dist.is_initialized():
            self.rank = dist.get_rank()
            self.world_size = dist.get_world_size()
        else:
            #  代表单卡系统, 多级系统会在训练代码中进行dict初始化
            self.rank = 0
            self.world_size = 1
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:
            self.worker_id = 0
            self.num_workers = 1
        else:
            self.worker_id = worker_info.id
            self.num_workers = worker_info.num_workers
        return dict(rank=self.rank,
                    world_size=self.world_size,
                    worker_id=self.worker_id,
                    num_workers=self.num_workers)

    def set_epoch(self, epoch):
        self.epoch = epoch

    def sample(self, data):
        """ Sample gxl_data according to rank/world_size/num_workers

            Args:
                data(List): input gxl_data list

            Returns:
                List: gxl_data list after sample
        """
        data = list(range(len(data)))
        # TODO(Binbin Zhang): fix this
        # We can not handle uneven gxl_data for CV on DDP, so we don't
        # sample gxl_data by rank, that means every GPU gets the same
        # and all the CV gxl_data
        if self.partition:
            if self.shuffle:
                random.Random(self.epoch).shuffle(data)
            data = data[self.rank::self.world_size]
        data = data[self.worker_id::self.num_workers]
        return data


class GxlDataList(IterableDataset, ABC):
    def __init__(self, lists: list, shuffle=True, partition=True):
        """
        对string_list加上一层sampler包装, 迭代的数据:
        {str: json_string, num_workers: 1, worker_id: 0, num_world:1, rank: 0}
        :param lists:  string_list
        :param shuffle:
        :param partition:
        """
        self.lists = lists
        self.sampler = GxlDistributedSampler(shuffle, partition)

    def set_epoch(self, epoch):
        self.sampler.set_epoch(epoch)

    def __iter__(self):
        sampler_info = self.sampler.update()
        indexes = self.sampler.sample(self.lists)
        for index in indexes:
            data = dict(src=self.lists[index])
            data.update(sampler_info)
            yield data


class GxlProcessor(IterableDataset, ABC):
    def __init__(self, source: Iterable, f: Callable, *args, **kw):
        """
        处理者: 使用处理函数进行处理
        :param source: 形如list的可迭代对象
        :param f: 处理函数
        :param args:
        :param kw:
        """
        assert callable(f)
        self.source = source
        self.f = f
        self.args = args
        self.kw = kw

    def set_epoch(self, epoch):
        self.source.set_epoch(epoch)

    def __iter__(self):
        """ Return an iterator over the source dataset processed by the
            given processor.
        """
        assert self.source is not None
        assert callable(self.f)
        return self.f(iter(self.source), *self.args, **self.kw)

    def apply(self, f):
        assert callable(f)
        return GxlProcessor(self, f, *self.args, **self.kw)


def GxlAsrDataset(data_type,
                  data_list_file,
                  symbol_table,
                  conf,
                  bpe_model=None,
                  non_lang_syms=None,
                  partition=True):
    """

    :param data_type:  in ['raw', 'shard']
    :param data_list_file:
    :param symbol_table:
    :param conf:
    :param bpe_model:
    :param non_lang_syms:
    :param partition:  whether to do gxl_data partition in terms of rank
    :return:
    """
    assert data_type in ['raw', 'shard']
    from ..utils.utils_file import load_list_file_clean
    lists = load_list_file_clean(data_list_file)
    shuffle = conf.get('shuffle', True)
    dataset = GxlDataList(lists, shuffle=shuffle, partition=partition)
    if data_type == 'shard':
        """"""
        # dataset = GxlProcessor(dataset, gxl_processor.url_opener)
        # dataset = Processor(dataset, processor.tar_file_and_group)
    else:
        dataset = GxlProcessor(dataset, gxl_processor.parse_raw)

    dataset = GxlProcessor(dataset, gxl_processor.tokenize, symbol_table, bpe_model,
                           non_lang_syms, conf.get('split_with_space', False))
    filter_conf = conf.get('filter_conf', {})
    dataset = GxlProcessor(dataset, gxl_processor.gxl_filter, **filter_conf)

    resample_conf = conf.get('resample_conf', {})
    dataset = GxlProcessor(dataset, gxl_processor.resample, **resample_conf)

    speed_perturb = conf.get('speed_perturb', False)
    if speed_perturb:
        dataset = GxlProcessor(dataset, gxl_processor.speed_perturb)

    feats_type = conf.get('feats_type', 'fbank')
    assert feats_type in ['fbank', 'mfcc']
    if feats_type == 'fbank':
        fbank_conf = conf.get('fbank_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.compute_fbank, **fbank_conf)
    elif feats_type == 'mfcc':
        mfcc_conf = conf.get('mfcc_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.compute_mfcc, **mfcc_conf)

    spec_aug = conf.get('spec_aug', True)
    spec_sub = conf.get('spec_sub', False)
    spec_trim = conf.get('spec_trim', False)
    if spec_aug:
        spec_aug_conf = conf.get('spec_aug_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.spec_augmentation, **spec_aug_conf)
    if spec_sub:
        spec_sub_conf = conf.get('spec_sub_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.spec_substitute, **spec_sub_conf)
    if spec_trim:
        spec_trim_conf = conf.get('spec_trim_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.spec_trim, **spec_trim_conf)

    if shuffle:
        shuffle_conf = conf.get('shuffle_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.shuffle, **shuffle_conf)

    sort = conf.get('sort', True)
    if sort:
        sort_conf = conf.get('sort_conf', {})
        dataset = GxlProcessor(dataset, gxl_processor.sort, **sort_conf)

    batch_conf = conf.get('batch_conf', {})
    dataset = GxlProcessor(dataset, gxl_processor.batch, **batch_conf)
    dataset = GxlProcessor(dataset, gxl_processor.padding)
    return dataset
