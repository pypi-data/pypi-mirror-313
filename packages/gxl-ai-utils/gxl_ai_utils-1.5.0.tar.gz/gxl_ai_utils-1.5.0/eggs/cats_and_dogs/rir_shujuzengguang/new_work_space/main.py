import os
import random

from scipy.io import wavfile

from gxl_ai_utils.utils import utils_file
from scipy.signal import fftconvolve
from rir_utils import read_audio, write_wav_with_normal


# 首先得到所有rir音频
def do_get_rir():
    input_wav_dir = "/home/work_nfs8/xlgeng/data/rir_data/simulated_rirs_16k"
    wav_list = utils_file.do_get_list_for_wav_dir(input_wav_dir, recursive=True)
    print(f'len: {len(wav_list)}')
    output_wav_list_path = './result/rir_list_173M.txt'
    utils_file.write_list_to_file(wav_list, output_wav_list_path)


def do_conv_rir_to_one_wav(input_wav_path, output_dir, rir_wav_path):
    """"""
    fs, audio = wavfile.read(input_wav_path)
    output_path = utils_file.do_replace_dir(input_wav_path, output_dir)
    print(output_path)
    # 将RIR应用到音频上
    rir = read_audio(rir_wav_path)
    audio_reverb = fftconvolve(audio, rir)[:len(audio)]
    write_wav_with_normal(output_path, audio_reverb, fs)


def do_conv_rir_to_list_wav(input_wav_list, output_dir, rir_list_path):
    """"""
    rir_path_list = utils_file.load_list_file_clean(rir_list_path)
    rir_num = len(rir_path_list)
    for input_wav_path in utils_file.tqdm(input_wav_list, desc='do_conv_rir_to_list_wav', total=len(input_wav_list)):
        rir_index = random.randint(0, rir_num - 1)
        rir_wav_path = rir_path_list[rir_index]
        fs, audio = wavfile.read(input_wav_path)
        output_path = utils_file.do_replace_dir(input_wav_path, output_dir)
        # 将RIR应用到音频上
        rir = read_audio(rir_wav_path)
        audio_reverb = fftconvolve(audio, rir)[:len(audio)]
        write_wav_with_normal(output_path, audio_reverb, fs)

        # do_conv_rir_to_one_wav(input_wav_path, output_dir, rir_wav_path)


# 构造将rir加入普通wav的脚本
def do_conv_rir_to_wav_main():
    big_name = 'pici_45093H'
    second_name = 'tiqianpi_1_3500H'
    input_wav_scp = f"/home/work_nfs8/xlgeng/aslp_spider_data/{big_name}/{second_name}/wav.scp"
    text_text_scp = f"/home/work_nfs8/xlgeng/aslp_spider_data/{big_name}/{second_name}/text"
    output_wav_store_dir_root_path = "/home/work_nfs10/xlgeng/data/pachong_row_data/rir_wav/"
    output_wav_store_dir = f"{output_wav_store_dir_root_path}/{big_name}/{second_name}"
    output_wav_scp_dir_root_path = "/home/work_nfs8/xlgeng/data/pachong_row_scp/"
    output_wav_scp_dir = f"{output_wav_scp_dir_root_path}/{big_name}/{second_name}"
    utils_file.makedir_sil(output_wav_store_dir)
    utils_file.makedir_sil(output_wav_store_dir)
    input_wav_list = list(utils_file.load_dict_from_scp(input_wav_scp).values())
    input_wav_list_list = utils_file.do_split_list(input_wav_list, 20)
    runner = utils_file.GxlDynamicProcessPool()
    rir_list_path = './result/rir_list_173M.txt'
    for i, input_wav_list in enumerate(input_wav_list_list):
        output_wav_store_dir_i = os.path.join(output_wav_store_dir, f"split_{i}")
        utils_file.makedir_sil(output_wav_store_dir_i)
        runner.add_task(do_conv_rir_to_list_wav, [input_wav_list, output_wav_store_dir_i, rir_list_path])
    runner.run()
    utils_file.do_get_scp_for_wav_dir(output_wav_store_dir, wav_scp_file_path=os.path.join(output_wav_scp_dir, 'wav.scp'), recursive=True)
    utils_file.copy_file(source_path=text_text_scp, destination_path=os.path.join(output_wav_scp_dir, 'text'), use_shell=True)


if __name__ == '__main__':
    do_conv_rir_to_wav_main()
