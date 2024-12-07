import os

from gxl_ai_utils.utils import utils_file

def data_handler():
    """"""
    input_dir = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all"
    output_dir = "/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data"
    wav_path = os.path.join(input_dir, "wav.scp")
    text_path = os.path.join(input_dir, "text")
    wav_file_list = utils_file.load_list_file_clean(wav_path)
    wav_file_list_list = utils_file.do_split_list(wav_file_list, 2)
    text_all_dict = utils_file.load_dict_from_scp(text_path)
    for i in range(len(wav_file_list_list)):
        output_dir_i = os.path.join(output_dir, f'wenetspeech_{i}')
        os.makedirs(output_dir_i, exist_ok=True)
        utils_file.write_list_to_file(wav_file_list_list[i], os.path.join(output_dir_i, "wav.scp"))
        temp_wav_dict = utils_file.load_dict_from_scp(os.path.join(output_dir_i, "wav.scp"))
        temp_text_dict = {k:text_all_dict[k] for k in temp_wav_dict.keys()}
        utils_file.write_dict_to_scp(temp_text_dict, os.path.join(output_dir_i, "text"))

def data_handler2():
    """"""
    input_dir = "/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data"
    input_dir_i = os.path.join(input_dir, f'wenetspeech_{0}')
    wav_path = os.path.join(input_dir_i, "wav.scp")
    text_path = os.path.join(input_dir_i, "text")
    # utils_file.do_make_data4icefall(wav_path, text_path, parent_dir=input_dir_i)
    manifest_dir = os.path.join(input_dir_i, 'manifest')
    fbank_dir = os.path.join(input_dir_i, 'fbank_common')
    utils_file.makedir_sil(manifest_dir)
    utils_file.makedir_sil(fbank_dir)
    utils_file._do_compute_fbank4icefall(
            manifests_dir=manifest_dir,
            fbank_dir=fbank_dir,
            partition='train',
            prefix='wenetspeech_0',
            perturb_speed=True
        )

import torch
if __name__ == '__main__':
    data_handler()