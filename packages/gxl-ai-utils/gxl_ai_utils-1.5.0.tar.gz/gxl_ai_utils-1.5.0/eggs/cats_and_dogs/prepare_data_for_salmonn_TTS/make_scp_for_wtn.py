# wav_text_npy 文件

import tqdm
import os
from gxl_ai_utils.utils import utils_file

input_npy_scp_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn_TTS/wenetspeech_acoustic/train.scp"
# temp_npy_dict = utils_file.load_dict_from_scp(input_npy_scp_path)
# new_npy_dict = {f'{key}_wenet': value for key, value in temp_npy_dict.items()}
# utils_file.write_dict_to_scp(new_npy_dict, input_npy_scp_path)
input_wav_scp_path = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all/wav.scp"
input_text_scp_path = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all/text"
res_list = []
output_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn_TTS/wenetspeech_acoustic/wtn_train.list"
npy_dict = utils_file.load_dict_from_scp(input_npy_scp_path)
wav_dict = utils_file.load_dict_from_scp(input_wav_scp_path)
text_dict = utils_file.load_dict_from_scp(input_text_scp_path)
for key, value in tqdm.tqdm(npy_dict.items()):
    if key in wav_dict and key in text_dict:
        item_dict = dict(
            key=key,
            wav=wav_dict[key],
            txt=text_dict[key],
            npy=value
        )
        res_list.append(item_dict)
utils_file.write_dict_list_to_jsonl(res_list, output_path)
output_path_2 = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn_TTS/wenetspeech_acoustic/wtn_cv.list"
input_npy_scp_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn_TTS/wenetspeech_acoustic/cv.scp"
temp_npy_dict = utils_file.load_dict_from_scp(input_npy_scp_path)
new_npy_dict = {f'{key}_wenet': value for key, value in temp_npy_dict.items()}
utils_file.write_dict_to_scp(new_npy_dict, input_npy_scp_path)

npy_dict_2 = utils_file.load_dict_from_scp(input_npy_scp_path)
res_list_2 = []
for key, value in tqdm.tqdm(npy_dict_2.items()):
    if key in wav_dict and key in text_dict:
        item_dict = dict(
            key=key,
            wav=wav_dict[key],
            txt=text_dict[key],
            npy=value
        )
        res_list_2.append(item_dict)
utils_file.write_dict_list_to_jsonl(res_list_2, output_path_2)