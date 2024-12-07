import os.path

import torch

from gxl_ai_utils.utils import utils_file


def get_scp():
    """"""
    wav_dir_path = "/Users/xuelonggeng/Desktop"
    wav_dict = utils_file.get_scp_for_wav_dir(wav_dir_path, suffix='.wav')
    text_dict = {}
    for key, value in wav_dict.items():
        text_dict[key] = '我是耿雪龙'
    utils_file.write_dict_to_scp(text_dict, './data/text')
    utils_file.write_dict_to_scp(wav_dict, './data/wav.scp')

def get_fbank_dir():
    """"""
    torch.set_num_threads(1)
    wav_scp_path = '/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/data/wav.scp'
    text_scp_path = '/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/data/text'
    output_dir = '/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/data/k2'
    manifest_dir = '/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/data/k2/manifest'
    fbank_dir = '/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/other/data/k2/fbank'
    utils_file.do_make_data4icefall(wav_scp_path, text_scp_path, manifest_dir, fbank_dir, partition='train', prefix='gxldata', )

if __name__ == '__main__':
    get_fbank_dir()
