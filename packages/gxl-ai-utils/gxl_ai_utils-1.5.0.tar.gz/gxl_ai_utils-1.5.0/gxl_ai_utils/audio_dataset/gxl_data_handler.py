import io
import multiprocessing
import os
import random
import tarfile
from logging import Logger
import tqdm
from torch.utils.data import Dataset
import torchaudio
import torchaudio.backend.soundfile_backend as sox
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils.utils import utils_file


class GxlAudioDataset(Dataset):
    def __init__(self, wav_path_list, label_list, config: GxlNode):
        """"""
        assert len(wav_path_list) == len(label_list)
        self.wav_path_list = wav_path_list
        self.label_list = label_list
        self.config = config

    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        return len(self.wav_path_list)


def compute_fbank(filepath, mel_num=100, min_sec=-5, max_sec=200000):
    """
    对音频提取fbank特征,
    :param filepath: 音频路径
    :param mel_num: mel特征维度
    :param min_sec: 音频最短长度, 小于此长度直接忽略
    :param max_sec: 音频最长长度, 超过此长度的进行截断
    :return fbank_feature: tensor:(num_frames, mel_num)
    """
    # waveform: tensor:(1, num_samples)
    waveform, sample_rate = torchaudio.load(filepath)
    if len(waveform[0]) < sample_rate * min_sec:
        return None
    if len(waveform[0]) > sample_rate * max_sec:
        waveform = waveform[:, :sample_rate * max_sec]
    # fbank: tensor:(num_frames, mel_num)
    fbank = torchaudio.compliance.kaldi.fbank(waveform=waveform, sample_frequency=sample_rate, num_mel_bins=mel_num)
    return fbank


def get_wavfilepath_and_label_from_json(json_file_path, wav_key='wav', target_key='spk_id'):
    dic_list = utils_file.load_dict_from_json(json_file_path)
    wav_path_list = []
    label_list = []
    for dic in dic_list.values():
        wav_path_list.append(dic[wav_key])
        label_list.append(dic[target_key])
    tuple_list = [(wav, spk_id) for wav, spk_id in zip(wav_path_list, label_list)]
    random.shuffle(tuple_list)
    wav_path_list, label_list = zip(*tuple_list)
    return wav_path_list, label_list


def get_wavfilepath_and_label_from_jsonl(jsonl_file_path, wav_key='wav', target_key='spk_id'):
    dic_list = utils_file.load_dict_list_from_jsonl(jsonl_file_path)
    wav_path_list = []
    label_list = []
    for dic in dic_list:
        wav_path_list.append(dic[wav_key])
        label_list.append(dic[target_key])
    tuple_list = [(wav, spk_id) for wav, spk_id in zip(wav_path_list, label_list)]
    random.shuffle(tuple_list)
    wav_path_list, label_list = zip(*tuple_list)
    return wav_path_list, label_list


def write_to_tar_file(data_list: list[tuple], tar_file_path: str, resample=16000, i=-1):
    """
    将数据写入tar文件，
    data_list: item: (key, wav_path, text.txt)
    """
    print(f'开始处理第{i}个shard')
    AUDIO_FORMAT_SETS = {'flac', 'mp3', 'm4a', 'ogg', 'opus', 'wav', 'wma'}
    utils_file.makedir_for_file_or_dir(tar_file_path)
    with tarfile.open(tar_file_path, "w") as tar:
        for item in tqdm.tqdm(data_list, total=len(data_list), desc=f"shard_{i}"):
            key, txt, wav = item
            suffix = wav.split('.')[-1]
            assert suffix in AUDIO_FORMAT_SETS, f"不支持的音频格式{suffix},仅支持{AUDIO_FORMAT_SETS}"
            # read & resample
            audio, sample_rate = sox.load(wav, normalize=False)
            if sample_rate != resample:
                audio = torchaudio.transforms.Resample(
                    sample_rate, resample)(audio)
            # change format to wav
            f = io.BytesIO()
            sox.save(f, audio, resample, format="wav", bits_per_sample=16)
            suffix = "wav"
            f.seek(0)
            data = f.read()
            assert isinstance(txt, str), f"txt必须是str类型"
            txt_file_name = key + '.txt'
            txt = txt.encode('utf8')
            txt_data = io.BytesIO(txt)
            txt_info = tarfile.TarInfo(txt_file_name)
            txt_info.size = len(txt)
            tar.addfile(txt_info, txt_data)

            wav_file = key + '.' + suffix
            wav_data = io.BytesIO(data)
            wav_info = tarfile.TarInfo(wav_file)
            wav_info.size = len(data)
            tar.addfile(wav_info, wav_data)
    print(f'第{i}个shard处理完成')


def make_shard_file(wav_scp_file_path: str, text_scp_file_path: str, output_dir: str, num_utt_per_shard: int = 1000,
                    num_threads=32, prefix_for_tar_file: str = "shard", resample: int = 16000, logger: Logger = None):
    """
    得到一个shard文件组成的目录, logger must is not None
    """
    assert logger is not None
    logger.info('开始打shard for ' + prefix_for_tar_file)
    logger.info('wav_scp: ' + wav_scp_file_path)
    logger.info('text_scp: ' + text_scp_file_path)
    wav_dic = utils_file.load_dict_from_scp(wav_scp_file_path)
    data = []
    text_dic = utils_file.load_dict_from_scp(text_scp_file_path)
    for k, text in text_dic.items():
        if k not in wav_dic:
            logger.info(f"warning: {k}不在wav_scp文件中")
            continue
        data.append((k, text, wav_dic[k]))
    logger.info(f"共有{len(data)}个utt")
    chunks = [data[i:i + num_utt_per_shard] for i in range(0, len(data), num_utt_per_shard)]
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"共有{len(chunks)}个shard")
    # Using thread pool to speedup
    pool = multiprocessing.Pool(processes=num_threads)
    shards_list = []
    for i, chunk in enumerate(chunks):
        tar_file_path = os.path.join(output_dir,
                                     '{}_{:09d}.tar'.format(prefix_for_tar_file, i))
        shards_list.append(tar_file_path)
        pool.apply_async(
            write_to_tar_file,
            (chunk, tar_file_path, resample, i))

    pool.close()
    pool.join()
    logger.info('打shard结束, 保存shard列表')
    with open(os.path.join(output_dir, 'shards_list.txt'), 'w', encoding='utf8') as fout:
        for name in shards_list:
            fout.write(name + '\n')
    logger.info('打shard完全结束')
