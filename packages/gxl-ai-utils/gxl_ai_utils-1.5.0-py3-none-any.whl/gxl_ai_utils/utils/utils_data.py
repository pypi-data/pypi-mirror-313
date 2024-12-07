import codecs
import glob
import io
import multiprocessing
import os
import re
import sys
import tarfile
from io import StringIO
from logging import Logger

import types
import torch
import torchaudio
import wave
import platform
from torch.utils.data import DataLoader, Dataset
import torchaudio.compliance.kaldi as kaldi
from tqdm import tqdm
import logging
from ..config.gxl_config import GxlNode

# if platform.system().lower() == 'windows':
#     torchaudio.set_audio_backend("soundfile")
# elif platform.system().lower() == 'linux':
#     torchaudio.set_audio_backend("sox_io")
# else:
#     pass

HAS_SET_LOGGING = False


def set_logging():
    """
    设置日志输出的格式
    :return: 
    """
    global HAS_SET_LOGGING
    HAS_SET_LOGGING = True
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')


def logging_print(*args):
    global HAS_SET_LOGGING
    if not HAS_SET_LOGGING:
        set_logging()
    string_temp = " ".join([str(arg) for arg in args])
    logging.info(string_temp)
    
    
is_python2 = sys.version_info[0] == 2


def torchaudio_load(wav_path: str, normalize=True, **kwargs):
    """
    
    :param normalize:
    :param wav_path:
    :param kwargs: 
    :return: waveform: torch.tensor: shape(1, sample_num)
    """
    waveform, sr = torchaudio.load(wav_path, normalize=normalize, **kwargs)
    return waveform, sr


def torchaudio_save(save_path: str, waveform, sr, is_normal_waveform: bool = True, **kwargs):
    if is_normal_waveform:
        waveform = waveform * (1 << 15)
    if platform.system().lower() == 'windows':
        torchaudio.save(save_path, waveform, sr, bits_per_sample=16, channels_first=True, format="wav", **kwargs)
    else:
        torchaudio.save(save_path, waveform, sr, precision=16, channels_first=True, format="wav", **kwargs)


def torchaudio_info(wav_path: str, **kwargs):
    return torchaudio.info(wav_path, **kwargs)


def torchaudio_resample(orig_freq, new_freq, waveform: torch.Tensor) -> torch.Tensor:
    """
    重采样,
    torchaudio.transforms.Resample是一个用于对音频信号进行重采样的类，它可以将一个频率的信号转换为另一个频率的信号12。
    重采样的原理是使用带限插值法，即在原始信号的采样点之间插入新的采样点，以达到目标频率
    重采样的效果是改变了信号的采样率，但不会改变信号的持续时间。例如，如果一个信号的原始频率是16000 Hz，持续时间是10 秒，那么重采样到8000 Hz后，信号的持续时间仍然是10 秒，但采样点的数量减少了一半。
    重采样的目的是为了适应不同的应用场景，例如降低信号的存储空间，提高信号的处理效率，或者匹配不同的设备要求14。
    重采样的缺点是可能会损失信号的一些信息，导致信号的质量下降。为了减少这种损失，重采样的过程中会使用低通滤波器来去除高于目标频率一半的信号分量，以避免混叠现象13。
    :param orig_freq:
    :param new_freq:
    :param waveform:(1, sample_num)
    :return: waveform:(1, sample_num)
    """
    # wav: shape(1,len)
    wav = torchaudio.transforms.Resample(orig_freq, new_freq)(waveform)
    return wav


def torchaudio_respeed(orig_freq: int, factor: float, waveform: torch.Tensor):
    """
    改变音频速度 , 采样率不变, 波形长度变为1/factor
    :param factor:  变更后的速度
    :param orig_freq: 原始采样率
    :param waveform: (1, num_sample)
    :return: waveform: (1, num_sample)
    """
    # wav: shape(1,len), _: None, 传入waveform需要是float
    wav, _ = torchaudio.transforms.Speed(orig_freq=orig_freq, factor=factor)(waveform)
    return wav


def torchaudio_fbank(waveform: torch.Tensor, num_mel_bins=80, frame_length=25, frame_shift=10, dither=0.0,
                     sample_rate=16000):
    """
    计算fbank特征
    :param waveform:  要求使用torchaudio.load(wav_path)得到, 其采用了默认的normal参数, 数据压缩到了float32:[-1.0,1.0], 原始音频多是int16
    :param num_mel_bins:
    :param frame_length:
    :param frame_shift:
    :param dither:
    :param sample_rate:
    :return:
    """
    waveform = waveform * (1 << 15)
    # waveform = waveform.float()
    return torchaudio.compliance.kaldi.fbank(waveform,
                                             num_mel_bins=num_mel_bins,
                                             frame_length=frame_length,
                                             frame_shift=frame_shift,
                                             dither=dither,
                                             sample_frequency=sample_rate,
                                             energy_floor=0.0, )


def torchaudio_mfcc(waveform,
                    num_mel_bins=23, frame_length=25, frame_shift=10, dither=0.0,
                    num_ceps=40, high_freq=0.0, low_freq=20.0, sample_rate=16000, ):
    """
    计算mfcc特征
    :param waveform:
    :param num_mel_bins:
    :param frame_length:
    :param frame_shift:
    :param dither:
    :param sample_rate:
    :param num_ceps:
    :param high_freq:
    :param low_freq:
    :return:
    """
    waveform = waveform * (1 << 15)
    return kaldi.mfcc(waveform,
                      num_mel_bins=num_mel_bins,
                      frame_length=frame_length,
                      frame_shift=frame_shift,
                      dither=dither,
                      num_ceps=num_ceps,
                      high_freq=high_freq,
                      low_freq=low_freq,
                      sample_frequency=sample_rate)


def get_sample_count(audio_file_path: str):
    """
    得到路径所指音频的采样点数
    output->
    sample_count: 采样点数
    sample_rate: 采样率
    """
    return _get_sample_count_wave(audio_file_path)


def _get_sample_count_wave(file_path):
    """比较快"""
    with wave.open(file_path, 'rb') as audio_file:
        sample_count = audio_file.getnframes()
        sample_rate = audio_file.getframerate()
    return sample_count, sample_rate


def _get_sample_count_torchaudio(file_path):
    """比较慢"""
    waveform, sr = torchaudio.load(file_path)
    return len(waveform[0]), sr


def get_padding_mask(seq_q: torch.Tensor, seq_k: torch.Tensor, pad_id: int = 0):
    """
    根据seq_k 中pad_id的位置， 得到seq_q对于seq_k的padding_attn_mask,
    seq_q 只是提供q_len,并不影响mask的分布,
    input->
    seq_q: (batch_size, len_q)
    seq_k: (batch_size, len_k)
    output->
    mask: (batch_size, len_q, len_k)
    """
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    mask = seq_k.eq(pad_id)
    mask = mask.unsqueeze(1).expand(batch_size, len_q, len_k)
    return mask


def get_sequence_mask(seq):
    """
    得到一个序列的self-attention的mask
    input->
    seq: [batch_size, seq_len]
    output->
    mask: [batch_size, seq_len, seq_len]
    """
    batch_size, seq_len = seq.size()
    mask = torch.triu(torch.ones((seq_len, seq_len), dtype=torch.uint8, device=seq.device), diagonal=1)
    mask = mask.unsqueeze(0).expand(batch_size, -1, -1)
    return mask


def get_scp_for_wav_dir(wav_dir: str, wav_scp_file_path: str):
    from .utils_file import makedir_for_file, join_path, get_file_pure_name_from_path, get_other_file_in_same_dir
    makedir_for_file(wav_scp_file_path)
    # text_scp = get_other_file_in_same_dir(wav_scp_file_path, 'text.txt.scp')
    wav_path_list = glob.glob(join_path(wav_dir, "*.wav"))
    # with codecs.open(wav_scp_file_path, 'w', encoding='utf-8') as f, open(text_scp, 'w', encoding='utf-8') as f2:
    with codecs.open(wav_scp_file_path, 'w', encoding='utf-8') as f:
        for wav_path in wav_path_list:
            f.write(f"{get_file_pure_name_from_path(wav_path)} {wav_path}\n")
            # f2.write(f"{get_file_pure_name_from_path(wav_path)} 我是耿雪龙焚烧发电萨芬\n")


class WavScpAudioDataset(Dataset):
    def __init__(self, data_file):
        from .utils_file import load_tuple_list_from_scp
        self.items = load_tuple_list_from_scp(data_file)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


class CollateFuncForCMVN(object):
    """
    Collate function for AudioDataset
    """

    def __init__(self, feat_dim, resample_rate):
        self.feat_dim = feat_dim
        self.resample_rate = resample_rate
        pass

    def __call__(self, batch):
        mean_stat = torch.zeros(self.feat_dim)
        var_stat = torch.zeros(self.feat_dim)
        number = 0
        for item in batch:
            value = item[1].strip().split(",")
            # len(value) == 3 means segmented wav.scp,->path, start_frame, end_frame
            # len(value) == 1 means original wav.scp
            assert len(value) == 3 or len(value) == 1
            wav_path = value[0]
            sample_rate = torchaudio.info(wav_path).sample_rate
            resample_rate = sample_rate
            if len(value) == 3:
                start_frame = int(float(value[1]) * sample_rate)
                end_frame = int(float(value[2]) * sample_rate)
                waveform, sample_rate = torchaudio.load(
                    filepath=wav_path,
                    num_frames=end_frame - start_frame,
                    frame_offset=start_frame)
            else:
                waveform, sample_rate = torchaudio.load(item[1])

            waveform = waveform * (1 << 15)
            if self.resample_rate != 0 and self.resample_rate != sample_rate:
                resample_rate = self.resample_rate
                waveform = torchaudio.transforms.Resample(
                    orig_freq=sample_rate, new_freq=resample_rate)(waveform)

            mat = kaldi.fbank(waveform,
                              num_mel_bins=self.feat_dim,
                              dither=0.0,
                              energy_floor=0.0,
                              sample_frequency=resample_rate)
            mean_stat += torch.sum(mat, dim=0)
            var_stat += torch.sum(torch.square(mat), dim=0)
            number += mat.shape[0]
        return number, mean_stat, var_stat


class GxlStringBuffer:
    def __init__(self):
        self.strings = ""

    @property
    def linefeed(self):
        if platform.system().lower() == 'windows':
            return '\r\n'
        else:
            return '\n'

    def print(self, string_data: str, end=None):
        if end is None:
            end = self.linefeed
        self.strings += (string_data + end)

    def to_string(self):
        """
        返回缓冲区的字符串
        :return:
        """
        return self.strings

    def to_list(self):
        """
        末尾带有换行符
        :return:
        """
        return [str_i + self.linefeed for str_i in self.to_list_clean()]

    def to_list_clean(self):
        """
        末尾不带换行符
        :return:
        """
        return self.strings.split(self.linefeed)

    def __str__(self):
        return self.to_string()


def do_compute_cmvn_stats(num_workers: int, config_yaml_path: str,
                          in_wav_scp_path: str, out_cmvn_json_path: str,
                          log_interval: int = 1000):
    """
    compute cmvn stats
    config_yaml内容要求:
    dataset_conf:
        resample_conf:
            resample_rate: 16000 -------->采样率
        fbank_conf:
            num_mel_bins: 80------>特征维度

    :param num_workers:
    :param config_yaml_path:
    :param in_wav_scp_path:
    :param out_cmvn_json_path:
    :param log_interval:
    :return:
    """
    from .utils_file import makedir_for_file
    configs = GxlNode.get_config_from_yaml(config_yaml_path)
    feat_dim = configs.dataset_conf.fbank_conf.num_mel_bins
    makedir_for_file(out_cmvn_json_path)
    resample_rate = 0
    if 'resample_conf' in configs['dataset_conf']:
        resample_rate = configs['dataset_conf']['resample_conf']['resample_rate']
        print('using resample and new sample rate is {}'.format(resample_rate))
    collate_func = CollateFuncForCMVN(feat_dim, resample_rate)
    dataset = WavScpAudioDataset(in_wav_scp_path)
    batch_size = 20
    data_loader = DataLoader(dataset,
                             batch_size=batch_size,
                             shuffle=True,
                             sampler=None,
                             num_workers=num_workers,
                             collate_fn=collate_func)
    with torch.no_grad():
        all_number = 0
        all_mean_stat = torch.zeros(feat_dim)
        all_var_stat = torch.zeros(feat_dim)
        wav_number = 0
        for i, batch in enumerate(data_loader):
            number, mean_stat, var_stat = batch
            all_mean_stat += mean_stat
            all_var_stat += var_stat
            all_number += number
            wav_number += batch_size

            if wav_number % log_interval == 0:
                print(f'processed {wav_number} wavs, {all_number} frames',
                      file=sys.stderr,
                      flush=True)
    cmvn_info = {
        'mean_stat': list(all_mean_stat.tolist()),
        'var_stat': list(all_var_stat.tolist()),
        'frame_num': all_number
    }
    from .utils_file import write_dict_to_json
    write_dict_to_json(cmvn_info, out_cmvn_json_path)


def do_text2token(text_scp_path: str, output_path: str,
                  nchar: int = 1, skip_ncols: int = 1,
                  space: str = '<space>', bpe_model_path: str = None,
                  non_lang_syms_path: str = None,
                  trans_type: str = 'char',
                  ):
    """
    do text.txt to token
    :param output_path:
    :param nchar:number of characters to split, i.e., \
                        aabb -> a a b b with -n 1 and aa bb with -n 2
    :param skip_ncols:skip first n columns, 是跳过处理, 直接保留,而不是放弃
    :param space:space symbol
    :param bpe_model_path:bpe model for english part
    :param non_lang_syms_path:list of non-linguistic symobles,
                         e.g., <NOISE> etc.
    :param text_scp_path:input text.txt
    :param trans_type:  choices=["char", "phn", "cn_char_en_bpe"],
                        help=Transcript type. char/phn. e.g., for TIMIT
                             FADG0_SI1279 -
                             If trans_type is char, read from
                             SI1279.WRD file -> "bricks are an alternative"
                             Else if trans_type is phn,
                             read from SI1279.PHN file ->
                             "sil b r ih sil k s aa r er n aa l
                             sil t er n ih sil t ih v sil)
    :return:
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    def exist_or_not(i, match_pos):
        start_pos = None
        end_pos = None
        for pos in match_pos:
            if pos[0] <= i < pos[1]:
                start_pos = pos[0]
                end_pos = pos[1]
                break
        return start_pos, end_pos

    def seg_char(sent):
        """
        返回汉字和分割的字符
        :param sent:
        :return:
        """
        pattern = re.compile(r'([\u4e00-\u9fa5])')
        # 返回汉字和分割是字符
        chars = pattern.split(sent)
        chars = [w for w in chars if len(w.strip()) > 0]
        return chars

    rs = []
    if non_lang_syms_path is not None:
        from .utils_file import load_list_file
        nls = load_list_file(non_lang_syms_path)
        rs = [re.compile(re.escape(x)) for x in nls]
    sp = None
    if bpe_model_path is not None:
        import sentencepiece as spm
        sp = spm.SentencePieceProcessor()
        sp.load(bpe_model_path)

    if text_scp_path is not None:
        f = codecs.open(text_scp_path, encoding="utf-8")
    else:
        f = codecs.getreader("utf-8")(
            sys.stdin if is_python2 else sys.stdin.buffer)
    buffer = GxlStringBuffer()
    # line = f.readline()
    n = nchar
    lines_totals = f.readlines()
    for line in tqdm(lines_totals, total=len(lines_totals), desc='text2tokening'):
        x = line.split()
        buffer.print(' '.join(x[:skip_ncols]), end=" ")
        a = ' '.join(x[skip_ncols:])

        # get all matched positions
        match_pos = []
        for r in rs:
            i = 0
            while i >= 0:
                m = r.search(a, i)
                if m:
                    match_pos.append([m.start(), m.end()])
                    i = m.end()
                else:
                    break

        if len(match_pos) > 0:
            #  如果有特殊符号, 那么只能支持char分类
            chars = []
            i = 0
            while i < len(a):
                start_pos, end_pos = exist_or_not(i, match_pos)
                if start_pos is not None:
                    chars.append(a[start_pos:end_pos])
                    i = end_pos
                else:
                    chars.append(a[i])
                    i += 1
            a = chars

        if trans_type == "phn":
            a = a.split(" ")
        elif trans_type == "cn_char_en_bpe":
            b = seg_char(a)
            a = []
            for j in b:
                # we use "▁" to instead of blanks among english words
                # warning: here is "▁", not "_"
                for l in j.strip().split("▁"):
                    if not l.encode('UTF-8').isalpha():
                        a.append(l)
                    else:
                        if sp is None:
                            raise Exception("please set bpe_model_path when trans_type is cn_char_en_bpe")
                        for k in sp.encode_as_pieces(l):
                            a.append(k)
        else:
            a = [a[j:j + n] for j in range(0, len(a), n)]

        a_flat = []
        # 确保都是字符串
        for z in a:
            a_flat.append("".join(z))

        a_chars = [z.replace(' ', space) for z in a_flat]
        if trans_type == "phn":
            a_chars = [z.replace("sil", space) for z in a_chars]
        buffer.print(' '.join(a_chars))
        # line = f.readline()
    lines = buffer.to_list_clean()
    cut_result = [line.split()[1:] for line in lines]
    # 将列表展平，并用换行符连接
    tr_result = "\n".join("\n".join(row) for row in cut_result)
    # 对行进行排序
    sort_result = "\n".join(sorted(tr_result.split("\n")))
    # 去除重复行
    uniq_result = "\n".join(sorted(set(sort_result.split("\n"))))
    # 过滤掉只包含空白字符的行
    grep_result = "\n".join(line for line in uniq_result.split("\n") if line.strip())
    # 在每一行末尾添加数字
    items = grep_result.split("\n")
    awk_result = "<blk> 0\n"
    awk_result += "\n".join(f"{line} {i + 1}" for i, line in enumerate(items))
    awk_result += f"\n<sos/eos> {len(items) + 1}\n"
    from .utils_file import makedir_for_file
    makedir_for_file(output_path)
    # 将结果追加到文件
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(awk_result)


def do_make_raw_list(wav_scp_path: str, text_scp_path: str,
                     output_jsonl_path, segments_path: str = None):
    """
    do make raw list
    将wav_scp text_scp合并成一个jsonl:gxl_data.list
    :param wav_scp_path:
    :param text_scp_path:
    :param output_jsonl_path:
    :param segments_path:
    :return:
    """
    from .utils_file import load_dict_from_scp, write_dict_list_to_jsonl, makedir_for_file
    makedir_for_file(output_jsonl_path)
    wav_dict = load_dict_from_scp(wav_scp_path)
    text_dict = load_dict_from_scp(text_scp_path)
    segments_dict = {}
    if segments_path is not None:
        with open(segments_path, 'r', encoding='utf8') as fin:
            for line in fin:
                arr = line.strip().split()
                assert len(arr) == 4
                segments_dict[arr[0]] = (arr[1], float(arr[2]), float(arr[3]))
    json_list = []
    for key, txt in text_dict.items():
        if segments_path is None:
            if key not in wav_dict:
                print('warning from gxl: {} in text_scp is not in wav_dict'.format(key))
                continue
            wav_path = wav_dict[key]
            json_line = dict(key=key, wav=wav_path, txt=txt)
        else:
            if key not in segments_dict:
                print('warning from gxl: {} in text_scp is not in segments_dict'.format(key))
                continue
            wav_key = segments_dict[key][0]
            start_time = segments_dict[key][1]
            end_time = segments_dict[key][2]
            if wav_key not in wav_dict:
                print(f'warning from gxl: {wav_key} in segments_dict[{key}][0] is not in wav_dict')
                continue
            wav_path = wav_dict[wav_key]
            json_line = dict(key=key, wav=wav_path, txt=txt, start_time=start_time, end_time=end_time)
        json_list.append(json_line)
    write_dict_list_to_jsonl(json_list, output_jsonl_path)
def do_change_file_suffix(tar_file_path, param):
    str_1 = tar_file_path.split('.')[:-1]
    return '.'.join(str_1) + '.' + param

def write_to_tar_file(data_list: list[tuple], tar_file_path: str, resample=16000, i=-1):
    """
    将数据写入tar文件，
    data_list: item: (key, text.txt, wav_path)
    """
    print(f'开始处理第{i}个shard')
    AUDIO_FORMAT_SETS = {'flac', 'mp3', 'm4a', 'ogg', 'opus', 'wav', 'wma'}
    from .utils_file import makedir_for_file
    makedir_for_file(tar_file_path)
    finished_path = do_change_file_suffix(tar_file_path, 'finished')
    with tarfile.open(tar_file_path, "w") as tar:
        for item in tqdm(data_list, total=len(data_list), desc=f"shard_{i}"):
            key, txt, wav = item
            suffix = wav.split('.')[-1]
            assert suffix in AUDIO_FORMAT_SETS, f"不支持的音频格式{suffix},仅支持{AUDIO_FORMAT_SETS}"
            # read & resample
            audio, sample_rate = torchaudio.load(wav, normalize=False)
            if sample_rate != resample:
                audio = torchaudio.transforms.Resample(
                    sample_rate, resample)(audio.float())
                audio = audio.to(torch.int16)
            # change format to wav
            f = io.BytesIO()
            torchaudio.save(f, audio, resample, format="wav", bits_per_sample=16)
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
    with open(finished_path, 'w') as f:
        pass


def do_make_shard_file(wav_scp_file_path: str, text_scp_file_path: str, output_dir: str, num_utt_per_shard: int = 1000,
                       num_threads=32, prefix_for_tar_file: str = "shard", resample: int = 16000,
                       ):
    """
    得到一个shard文件组成的目录, logger must is not None
    """
    logging_print('开始打shard for ' + prefix_for_tar_file)
    logging_print('wav_scp: ' + wav_scp_file_path)
    logging_print('text_scp: ' + text_scp_file_path)
    from .utils_file import load_dict_from_scp
    wav_dic = load_dict_from_scp(wav_scp_file_path)
    data = []
    text_dic = load_dict_from_scp(text_scp_file_path)
    for k, text in text_dic.items():
        if k not in wav_dic:
            logging_print(f"warning: {k}不在wav_scp文件中")
            continue
        data.append((k, text, wav_dic[k]))
    logging_print(f"共有{len(data)}个utt")
    chunks = [data[i:i + num_utt_per_shard] for i in range(0, len(data), num_utt_per_shard)]
    os.makedirs(output_dir, exist_ok=True)
    logging_print(f"共有{len(chunks)}个shard")
    # Using thread pool to speedup
    pool = multiprocessing.Pool(processes=num_threads)
    shards_list = []
    for i, chunk in enumerate(chunks):
        tar_file_path = os.path.join(output_dir,
                                     '{}_{:09d}.tar'.format(prefix_for_tar_file, i))
        shards_list.append(tar_file_path)
        finished_file_path = do_change_file_suffix(tar_file_path, 'finished')
        if os.path.exists(finished_file_path):
            continue
        pool.apply_async(
            write_to_tar_file,
            (chunk, tar_file_path, resample, i))

    pool.close()
    pool.join()
    logging_print('打shard结束, 保存shard列表')
    with open(os.path.join(output_dir, 'shards_list.txt'), 'w', encoding='utf8') as fout:
        for name in shards_list:
            fout.write(name + '\n')
    logging_print('打shard完全结束')


def do_remove_blank_for_text_scp(text_scp_path: str, ):
    """
    删除text_scp中的空白行
    """
    dir_name = os.path.dirname(text_scp_path)
    temp_file = os.path.join(dir_name, 'temp.txt')
    with open(text_scp_path, 'r', encoding='utf8') as fin, open(temp_file, 'w', encoding='utf8') as fout:
        for line in fin:
            items = line.strip().split()
            key = items[0]
            txt = "".join(items[1:])
            fout.write(f"{key} {txt}\n")
    from .utils_file import load_dict_from_scp, write_dict_to_scp
    dic = load_dict_from_scp(temp_file)
    os.remove(temp_file)
    write_dict_to_scp(dic, text_scp_path)


def do_dict2simpleNamespaceObj(dict_obj: dict):
    """
    将一个字典转换为命名空间对象,
    命名空间对象可以修改key对应的value值
    可以通过.的方式调用键值对用的value值,如果调用没设置的键值,则直接报错,
    :param dict_obj:
    :return:
    """
    return types.SimpleNamespace(**dict_obj)
