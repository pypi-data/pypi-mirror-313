"""
为wenet训练框架加入musan噪音增强功能
"""
import os
import random
import sys

import torch
import torchaudio
from gxl_ai_utils.utils.utils_file import global_timer

sys.path.insert(0, '../../../')
from gxl_ai_utils.utils import utils_file

# 先把musan音频搬运到nfs15
def do_copy_musan():
    source_dir = "/home/work_nfs8/asr_data/data/musan"
    partions = ["music", "noise"]
    output_dir = '/home/work_nfs15/asr_data/data/musan'
    utils_file.makedir_sil(output_dir)
    for partion in partions:
        print("processing {}".format(partion))
        output_dir_tmp = os.path.join(output_dir, partion)
        source_dir_tmp = os.path.join(source_dir, partion)
        utils_file.makedir_sil(output_dir_tmp)
        # 得到wav.scp
        wav_scp_path = os.path.join(output_dir_tmp, 'wav.scp')
        wav_dict = utils_file.get_scp_for_wav_dir(source_dir_tmp, recursive=True)
        new_wav_dict_for_write = {}
        for key, value in wav_dict.items():
            wav_name_with_suffix = os.path.basename(value)
            new_value = os.path.join(output_dir_tmp, wav_name_with_suffix)
            new_wav_dict_for_write[key] = new_value
        utils_file.write_dict_to_scp(new_wav_dict_for_write, wav_scp_path)
        # 开始复制数据
        num_thread = 20
        runner = utils_file.GxlFixedProcessPool(num_thread)
        wav_dict_list = utils_file.do_split_dict(wav_dict, num_thread)
        for i, wav_dict_item in enumerate(wav_dict_list):
            runner.add_thread(utils_file.little_func_for_cp_from_dict, [wav_dict_item, output_dir_tmp, i])
        runner.start()
def do_fix_scp_wav():
    source_dir = "/home/work_nfs15/asr_data/data/musan"
    partions = ["music", "noise"]
    for partion in partions:
        wav_scp_path = os.path.join(source_dir, partion, "wav.scp")
        wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
        new_wav_dict = {}
        for key, value in wav_dict.items():
            new_wav_dict[key] = value +'.wav'
        utils_file.write_dict_to_scp(new_wav_dict, wav_scp_path)


# 得到对干净语音进行增强的函数
def do_noice_augment(input_clear_wav:torch.Tensor, input_noice_wav:torch.Tensor, snr:float=5):
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
    torchaudio.save(f"./augmented_speech_snr_{snr}.wav", augmented_speech_tensor, sample_rate=16000)


def get_a_random_noise_snr():
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
    intervals = [(20, 30), (10, 20), (0, 10), (-10, 0), (-30, -10)]
    probabilities = [0.1, 0.35, 0.4, 0.1, 0.05]
    # 根据概率从区间中选择一个区间
    selected_interval = random.choices(intervals, weights=probabilities)[0]
    # 在选定的区间内生成一个均匀分布的随机数
    random_number = random.uniform(selected_interval[0], selected_interval[1])
    return random_number


def show_musan_augment():
    input_clear_wav, _ = torchaudio.load(
        "/home/work_nfs15/asr_data/data/aishell_1/origin_wav/data_aishell/wav/test/S0764/BAC009S0764W0126.wav")
    input_noice_wav, _ = torchaudio.load("/home/work_nfs15/asr_data/data/musan/noise/noise-free-sound-0788.wav")
    utils_file.global_timer.start()
    do_noice_augment(input_clear_wav, input_noice_wav, 45)
    do_noice_augment(input_clear_wav, input_noice_wav, 40)
    do_noice_augment(input_clear_wav, input_noice_wav, 35)
    do_noice_augment(input_clear_wav, input_noice_wav, 30)  # 隐约能感觉到
    do_noice_augment(input_clear_wav, input_noice_wav, 25)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, 20)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, 15)  # 还是只能感受到最后的呲呲声音
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, 10)  # 开始能听到真正的敲门声音
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, 5)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, 0)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav, -5)
    do_noice_augment(input_clear_wav, input_noice_wav, -10)
    do_noice_augment(input_clear_wav, input_noice_wav, -15)
    do_noice_augment(input_clear_wav, input_noice_wav, -20)
    do_noice_augment(input_clear_wav, input_noice_wav, -25)
    do_noice_augment(input_clear_wav, input_noice_wav, -30)  # 人话声有点小了
    do_noice_augment(input_clear_wav, input_noice_wav, -35)
    do_noice_augment(input_clear_wav, input_noice_wav, -40)  # 隐约有点说话声音
    do_noice_augment(input_clear_wav, input_noice_wav, -45)  # 主要是噪音，基本没法听到人声
    utils_file.global_timer.stop_halfway_and_print()

def show_random_srn():
    random.seed(10086)
    utils_file.global_timer.start()
    for i in range(3):
        print(get_a_random_noise_snr())
    utils_file.global_timer.stop_halfway_and_print()

# 下面考虑如何在wenet的dataloader中加载该augmentation
# 首先需要加载好big data_dict,包括音乐和噪声， 然后为了效率，每百条音频使用一个噪音（包含音乐）音频进行增强， 每个音频随机出一个信噪比数值。
class NoiceAugmentWorker:
    def __init__(self, noice_scp_or_list_path_list, replacement_frequency:int=100):
        self.noice_wav_list = []
        self.replacement_frequency = replacement_frequency
        for noice_scp_or_list_path in noice_scp_or_list_path_list:
            assert os.path.exists(noice_scp_or_list_path) and (noice_scp_or_list_path.endswith(".scp") or noice_scp_or_list_path.endswith(".list") or noice_scp_or_list_path.endswith(".txt"))
            if noice_scp_or_list_path.endswith(".scp"):
                tmp_wav_dict = utils_file.load_dict_from_scp(noice_scp_or_list_path)
                self.noice_wav_list.extend(list(tmp_wav_dict.values()))
            else:
                self.noice_wav_list.extend(utils_file.load_list_file_clean(noice_scp_or_list_path))
        self.num_count = 0 # 作为计数，如果计算到replacement_frequency，就更换当前noice wav
        self.now_noice_wav = torchaudio.load(random.choice(self.noice_wav_list))

    def do_apply_augment(self,input_clear_wav:torch.Tensor):
        """"""
        srn = self.get_a_random_noise_snr()
        self.do_noice_augment(input_clear_wav, self.now_noice_wav, srn)
        self.num_count += 1
        if self.num_count >= self.replacement_frequency:
            self.now_noice_wav = torchaudio.load(random.choice(self.noice_wav_list))
            self.num_count = 0

    @staticmethod
    def do_noice_augment(input_clear_wav: torch.Tensor, input_noice_wav: torch.Tensor, snr: float = 5):
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
        torchaudio.save(f"./augmented_speech_snr_{snr}.wav", augmented_speech_tensor, sample_rate=16000)

    @staticmethod
    def get_a_random_noise_snr():
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
        intervals = [(20, 30), (10, 20), (0, 10), (-10, 0), (-30, -10)]
        probabilities = [0.1, 0.35, 0.4, 0.1, 0.05]
        # 根据概率从区间中选择一个区间
        selected_interval = random.choices(intervals, weights=probabilities)[0]
        # 在选定的区间内生成一个均匀分布的随机数
        random_number = random.uniform(selected_interval[0], selected_interval[1])
        return random_number

global_noise_augment_worker = NoiceAugmentWorker([
    '/home/work_nfs15/asr_data/data/musan/music/wav.scp',
    '/home/work_nfs15/asr_data/data/musan/noice/wav.scp',
], replacement_frequency=100)


if __name__ == '__main__':
    """"""
    show_random_srn()
