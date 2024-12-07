import os
import random
import sys

import torch
import torchaudio

from gxl_ai_utils.utils import utils_file

class NoiceAugmentWorker:
    def __init__(self, noice_scp_or_list_path_list,
                 min_srn:float,
                 max_srn:float,
                 replacement_frequency:int=100):
        self.noice_wav_list = []
        self.min_srn = min_srn
        self.max_srn = max_srn
        self.replacement_frequency = replacement_frequency
        for noice_scp_or_list_path in noice_scp_or_list_path_list:
            assert os.path.exists(noice_scp_or_list_path)
            if noice_scp_or_list_path.endswith(".scp"):
                tmp_wav_dict = utils_file.load_dict_from_scp(noice_scp_or_list_path)
                self.noice_wav_list.extend(list(tmp_wav_dict.values()))
            else:
                self.noice_wav_list.extend(utils_file.load_list_file_clean(noice_scp_or_list_path))
        self.num_count = 0 # 作为计数，如果计算到replacement_frequency，就更换当前noice wav
        self.now_noice_wav,_ = torchaudio.load(random.choice(self.noice_wav_list))

    def do_apply_augment(self,input_clear_wav:torch.Tensor):
        """"""
        srn = self._get_a_random_noise_snr()
        self.num_count += 1
        if self.num_count >= self.replacement_frequency:
            self.now_noice_wav, _ = torchaudio.load(random.choice(self.noice_wav_list))
            self.num_count = 0
        return self._do_noice_augment(input_clear_wav, self.now_noice_wav, srn)

    @staticmethod
    def _do_noice_augment(input_clear_wav: torch.Tensor, input_noice_wav: torch.Tensor, snr: float = 5):
        """
        信噪比具体情况如下：
        30： 隐约能听到背景噪音。
        15： 还是只能感受到最后的呲呲声音
        10： 开始能听到真正的敲门声音
        -30： 人话声有些小了
        -40： 隐约有点说话声音
        -45： 主要是噪音，基本没法听到人声
        训练的时候推荐从30到-30
        AI给出的比例：
        20-30： 10%  安静的图书馆或自习室 乡村户外安静的自然环境
        10-20: 35% 普通的室内办公室环境 街边的咖啡馆或餐厅
        0-10: 40%  热闹的商场或超市 正在行驶的公交车或地铁内
        -10 -0: 10% 嘈杂的工厂车间 喧闹的酒吧或夜总会
        -30 - -10: 5% 大型建筑工地  飞机起飞或降落的跑道附近

        :param input_clear_wav:(1,samples)
        :param input_noice_wav:(1,samples)
        :param snr: 信噪比
        :return:
        """
        while input_noice_wav.size(1) < input_clear_wav.size(1):
            input_noice_wav = torch.cat([input_noice_wav, input_noice_wav], dim=1)

        # 先计算语音的功率（这里明确在样本数量维度求平均来近似功率，保持维度方便后续计算）
        clean_power = torch.mean(input_clear_wav ** 2, dim=1, keepdim=True)
        # 计算噪声的功率，同样在对应维度求平均
        noise_power = torch.mean(input_noice_wav ** 2, dim=1, keepdim=True)

        # 根据信噪比公式推导出噪声需要缩放的因子
        scale_factor = torch.sqrt(clean_power / (noise_power * (10 ** (snr / 10))))
        # 先按照干净语音的长度裁剪噪声张量
        input_noice_wav = input_noice_wav[:, :input_clear_wav.shape[1]]
        # 对裁剪后的噪声张量进行缩放，以达到期望的信噪比
        scaled_noise_tensor = input_noice_wav * scale_factor
        # 将缩放后的噪声张量和干净语音张量相加，实现添加噪声进行语音增强
        augmented_speech_tensor = input_clear_wav + scaled_noise_tensor
        return augmented_speech_tensor

    def _get_a_random_noise_snr(self):
        """
            信噪比具体情况如下：
        30： 隐约能听到背景噪音。
        15： 还是只能感受到最后的呲呲声音
        10： 开始能听到真正的敲门声音
        -30： 人话声有些小了
        -40： 隐约有点说话声音
        -45： 主要是噪音，基本没法听到人声
        训练的时候推荐从30到-30
        AI给出的比例：
        20-30： 10%  安静的图书馆或自习室 乡村户外安静的自然环境
        10-20: 35% 普通的室内办公室环境 街边的咖啡馆或餐厅
        0-10: 40%  热闹的商场或超市 正在行驶的公交车或地铁内
        -10 -0: 10% 嘈杂的工厂车间 喧闹的酒吧或夜总会
        -30 - -10: 5% 大型建筑工地  飞机起飞或降落的跑道附近
        :return:
        """
        # 根据上面的比例随机给出一个信噪比
        # 定义各个区间的边界和对应的概率
        assert self.min_srn < self.max_srn and self.min_srn <-10 and self.max_srn > 20
        intervals = [(20, self.max_srn), (10, 20), (0, 10), (-10, 0), (self.min_srn, -10)]
        probabilities = [0.1, 0.35, 0.4, 0.1, 0.05]
        # 根据概率从区间中选择一个区间
        selected_interval = random.choices(intervals, weights=probabilities)[0]
        # 在选定的区间内生成一个均匀分布的随机数
        random_number = random.uniform(selected_interval[0], selected_interval[1])
        return random_number

# global_noise_augment_worker = NoiceAugmentWorker([
#     '/home/work_nfs15/asr_data/data/musan/music/wav.scp',
#     '/home/work_nfs15/asr_data/data/musan/noise/wav.scp',
# ],min_srn=-20, max_srn=30, replacement_frequency=100)
