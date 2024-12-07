import random

import numpy as np
import pyroomacoustics as pra
import tqdm
from scipy.io import wavfile
from scipy.signal import fftconvolve
from gxl_ai_utils.utils import utils_file


def get_rir():
    # 创建一个房间
    room_x = round(random.uniform(5, 8), 1)
    room_y = round(random.uniform(3, 5), 1)
    room_z = round(random.uniform(3, 4), 1)
    room_dim = [room_x, room_y, room_z]

    rt60_tgt = round(random.uniform(0.2, 1.2), 2)
    e_absorption, max_order = pra.inverse_sabine(rt60_tgt, room_dim)  # 0.1614901799818631 95
    print(e_absorption, max_order)
    room_dim = [10, 10, 3]  # 房间的尺寸
    mic_array_loc = [5, 5, 1]  # 麦克风阵列的位置
    source_loc = [3, 3, 1]  # 声源的位置
    room = pra.ShoeBox(room_dim, fs=16000, max_order=max_order, absorption=e_absorption)

    # 添加麦克风阵列
    mic_array = pra.MicrophoneArray(np.array([mic_array_loc]).T, room.fs)
    room.add_microphone_array(mic_array)

    # 添加声源
    room.add_source(source_loc)

    # 计算RIR
    room.compute_rir()
    rir = room.rir[0][0]
    return rir

EPS = np.finfo(float).eps
def normalize(audio, target_level=-25):
    '''Normalize the signal to the target level'''
    rms = (audio ** 2).mean() ** 0.5
    scalar = 10 ** (target_level / 20) / (rms + EPS)
    audio = audio * scalar
    return audio


def write_wav_with_normal(output_path, audio_reverb, fs):
    level_db = random.uniform(-45, -15)
    audio = normalize(audio_reverb.astype(np.int16), -15)
    # 保存带有混响的音频
    wavfile.write(output_path, fs, audio)


def apply_rir_to_wav(wav_dict, output_dir, rir):
    # import pdb;pdb.set_trace()
    utils_file.makedir_sil(output_dir)
    # 音频文件列表
    # wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
    for key, audio_path in tqdm.tqdm(wav_dict.items(), desc="apply_rir_to_wav", total=len(wav_dict)):
        # 读取音频文件
        fs, audio = wavfile.read(audio_path)
        output_path = utils_file.do_replace_dir(audio_path, output_dir)
        # 将RIR应用到音频上
        audio_reverb = fftconvolve(audio, rir)[:len(audio)]
        write_wav_with_normal(output_path, audio_reverb, fs)

def main(input_scp_path, output_dir):
    now = utils_file.do_get_now_time()
    rir = get_rir()
    utils_file.logging_print('get rir耗时: %s' % (utils_file.do_get_now_time() - now))
    thread_num = 32
    wav_dict = utils_file.load_dict_from_scp(input_scp_path)
    wav_dict_list = utils_file.do_split_dict(wav_dict, thread_num)
    runner = utils_file.GxlFixedThreadPool(thread_num)
    now = utils_file.do_get_now_time()
    for wav_dict_i in wav_dict_list:
        runner.add_thread(apply_rir_to_wav, [wav_dict_i, output_dir, rir])
    runner.start()
    utils_file.logging_print('耗时: %s' % (utils_file.do_get_now_time() - now))


import numpy as np
import soundfile as sf


def read_audio(filename):
    audio, sr = sf.read(filename)
    if sr != 16000:
        audio = sf.resample(audio, 16000)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)  # 合并多个通道
        print('多通道')
    audio = audio.flatten()
    return audio


if __name__ == "__main__":
    #  (72核)CPU
    # 20进程:   4.918259620666504/7176个
    # 32进程:    4.5718605518341064/7176个
    # 40进程  4.63465428352356/7176个
    # 72进程  5.503162145614624/7176个
    # 140进程   6.536927223205566/7176个
    # input_scp_path= "/home/work_nfs8/xlgeng/data/scp_test/aishell/wav.scp"
    # output_dir = './wav_output/aishell_test2'
    # main(input_scp_path, output_dir)
    rir = get_rir()
    print(rir)
    print(rir.shape)
    print(type(rir))
    print(rir.dtype)
    # rir_my = read_audio(
    #     "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/simulated_rirs_16k/largeroom/Room001/Room001-00001.wav")
    # print(rir_my)
    # print(rir_my.shape)
    # print(type(rir_my))
    # print(rir_my.dtype)
    thread_num = 2
    input_scp_path = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/scp/wav.scp"
    output_dir = 'data/wav_output/aishell_test_my'
    wav_dict = utils_file.load_dict_from_scp(input_scp_path)
    wav_dict_list = utils_file.do_split_dict(wav_dict, thread_num)
    runner = utils_file.GxlFixedThreadPool(thread_num)
    now = utils_file.do_get_now_time()
    for wav_dict_i in wav_dict_list:
        runner.add_thread(apply_rir_to_wav, [wav_dict_i, output_dir, rir])
    runner.start()
    utils_file.logging_print('耗时: %s' % (utils_file.do_get_now_time() - now))

    output_dir = 'data/wav_output/aishell_test_gen'
    wav_dict = utils_file.load_dict_from_scp(input_scp_path)
    wav_dict_list = utils_file.do_split_dict(wav_dict, thread_num)
    runner = utils_file.GxlFixedThreadPool(thread_num)
    now = utils_file.do_get_now_time()
    for wav_dict_i in wav_dict_list:
        runner.add_thread(apply_rir_to_wav, [wav_dict_i, output_dir, rir])
    runner.start()
    utils_file.logging_print('耗时: %s' % (utils_file.do_get_now_time() - now))
