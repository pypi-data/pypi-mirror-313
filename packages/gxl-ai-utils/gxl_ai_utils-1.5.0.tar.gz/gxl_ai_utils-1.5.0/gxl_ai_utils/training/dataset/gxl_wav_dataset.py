import random

import torch.utils.data
from torch.utils.data import IterableDataset
import torch.distributed as dist
from gxl_ai_utils.utils import utils_file
import gxl_ai_utils.training.dataset.processor as processor


class Processor(IterableDataset):
    def __init__(self, source, f, *args, **kwargs):
        self.source = source
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def set_epoch(self, epoch):
        self.source.set_epoch(epoch)

    def __iter__(self):
        return self.f(iter(self.source), *self.args, **self.kwargs)




class DistributedSampler:
    def __init__(self, shuffle, partition):
        self.epoch = -1
        self.update()
        self.shuffle = shuffle
        self.partition = partition
    def update(self):
        assert dist.is_available()
        if dist.is_initialized():
            self.rank = dist.get_rank()
            self.world_size = dist.get_world_size()
        else:
            self.rank = 0
            self.world_size = 1

        work_info = torch.utils.data.get_worker_info()
        if work_info is None:
            self.worker_id = 0
            self.num_workers = 1
        else:
            self.worker_id = work_info.id
            self.num_workers = work_info.num_workers
        return dict(
            rank = self.rank,
            world_size = self.world_size,
            worker_id = self.worker_id,
            num_workers = self.num_workers
        )

    def set_epoch(self, epoch):
        self.epoch = epoch

    def sample(self, data):
        """
        根据worker_id ,rank进行sample
        :param data:
        :return:
        """
        data = list(range(len(data)))
        if self.shuffle:
            random.Random(self.epoch).shuffle(data)
        if self.partition:
            data = data[self.rank::self.world_size]
        data = data[self.worker_id::self.num_workers]
        return data



class DataList(IterableDataset):
    def __init__(self,
                 lists,
                 shuffle=True,
                 partition = True):
        """"""
        self.lists = lists
        self.sampler = DistributedSampler(shuffle, partition)

    def set_epoch(self, epoch):
        self.sampler.set_epoch(epoch)

    def __iter__(self):
        """"""
        sample_info = self.sampler.update()
        indexs = self.sampler.sample(self.lists)
        for index in indexs:
            data = dict(src=self.lists[index])
            data.update(sample_info)
            yield data

def Dataset(
        data_type,
        data_list_file,
        tokenizer,
        conf,
        partition=True
):
    """"""
    assert data_type in ['raw', 'shard'], f'data_type is {data_type}'
    shuffle = conf.get('shuffle', True)
    data_list = utils_file.load_dict_from_scp(data_list_file)
    dataset = DataList(
        lists=data_list,
        shuffle=shuffle,
        partition=partition
    )
    if data_type == 'shard':
        dataset = Processor(dataset, processor.url_opener)
        dataset = Processor(dataset, processor.tar_file_and_group)
    else:
        dataset = Processor(dataset, processor.parse_raw)

    speaker_conf = conf.get('speaker_conf', None)
    if speaker_conf is not None:
        dataset = Processor(dataset, processor.parse_speaker, **speaker_conf)

    dataset = Processor(dataset, processor.tokenize, tokenizer)
    filter_conf = conf.get('filter_conf', {})
    dataset = Processor(dataset, processor.filter, **filter_conf)

    resample_conf = conf.get('resample_conf', {})
    dataset = Processor(dataset, processor.resample, **resample_conf)

    speed_perturb = conf.get('speed_perturb', False)
    if speed_perturb:
        dataset = Processor(dataset, processor.speed_perturb)
    noice_augment = conf.get('noice_augment', False)
    # 开启噪音增广
    if noice_augment:
        noice_augment_conf = conf.get('noice_augment_conf', {})
        dataset = Processor(dataset, processor.gxl_noise_augment, **noice_augment_conf)

    feats_type = conf.get('feats_type', 'fbank')
    assert feats_type in ['fbank', 'mfcc', 'log_mel_spectrogram']
    if feats_type == 'fbank':
        fbank_conf = conf.get('fbank_conf', {})
        dataset = Processor(dataset, processor.compute_fbank, **fbank_conf)
    elif feats_type == 'mfcc':
        mfcc_conf = conf.get('mfcc_conf', {})
        dataset = Processor(dataset, processor.compute_mfcc, **mfcc_conf)
    elif feats_type == 'log_mel_spectrogram':
        log_mel_spectrogram_conf = conf.get('log_mel_spectrogram_conf', {})
        dataset = Processor(dataset, processor.compute_log_mel_spectrogram,
                            **log_mel_spectrogram_conf)

    spec_aug = conf.get('spec_aug', True)
    spec_sub = conf.get('spec_sub', False)
    spec_trim = conf.get('spec_trim', False)
    if spec_aug:
        spec_aug_conf = conf.get('spec_aug_conf', {})
        dataset = Processor(dataset, processor.spec_aug, **spec_aug_conf)
    if spec_sub:
        spec_sub_conf = conf.get('spec_sub_conf', {})
        dataset = Processor(dataset, processor.spec_sub, **spec_sub_conf)
    if spec_trim:
        spec_trim_conf = conf.get('spec_trim_conf', {})
        dataset = Processor(dataset, processor.spec_trim, **spec_trim_conf)

    if shuffle:
        shuffle_conf = conf.get('shuffle_conf', {})
        dataset = Processor(dataset, processor.shuffle, **shuffle_conf)

    sort = conf.get('sort', True)
    if sort:
        sort_conf = conf.get('sort_conf', {})
        dataset = Processor(dataset, processor.sort, **sort_conf)

    batch_conf = conf.get('batch_conf', {})
    dataset = Processor(dataset, processor.batch, **batch_conf)
    dataset = Processor(dataset, processor.padding)
    return dataset




if __name__ == '__main__':
    fake_list = []
    for i in range(10000):
        fake_list.append(str(i).zfill(7))
    dataset = DataList(fake_list)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=None, num_workers=4)
    for epoch_i in range(5):
        for data in dataloader:
            print(data)



