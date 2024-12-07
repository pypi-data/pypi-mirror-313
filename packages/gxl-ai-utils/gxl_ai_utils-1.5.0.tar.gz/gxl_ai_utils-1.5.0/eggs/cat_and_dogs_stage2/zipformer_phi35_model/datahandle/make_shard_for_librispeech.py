import os
import sys
sys.path.insert(0,'../../../../')
from gxl_ai_utils.utils import utils_file


input_dir = "/home/work_nfs15/asr_data/data/LibriSpeech"
output_dir = "/home/work_nfs15/asr_data/data/LibriSpeech/LibriSpeech_shard"
parts = ["train-clean-100",  "train-other-500", "train-clean-360"]
for part in parts:
    utils_file.logging_info('开始处理：', part)
    input_dir_part = os.path.join(input_dir, part)
    output_dir_part = os.path.join(output_dir, part)
    utils_file.makedir_sil(output_dir_part)
    scp_wav_path = os.path.join(output_dir_part, "wav.scp")
    text_path = os.path.join(output_dir_part, "text")
    if part == 'train-other-500':
        utils_file.logging_info('获取wav.scp')
        file_path_list = utils_file.do_get_list_for_wav_dir(input_dir_part, None, '.flac', True)
        wav_dict = utils_file.do_convert_file_list_to_dict(file_path_list)
        utils_file.write_dict_to_scp(wav_dict, scp_wav_path)
        text_all_dict = utils_file.load_dict_from_scp("/home/work_nfs15/asr_data/data/LibriSpeech/LibriSpeech_shard/text")
        text_dict = {k: text_all_dict[k] for k in wav_dict.keys()}
        utils_file.write_dict_to_scp(text_dict, text_path)
        utils_file.logging_info('得到scp完毕， 开始通过scp得到shard包')
        utils_file.do_make_shard_file(scp_wav_path, text_path, os.path.join(output_dir_part, 'shards'),
                                      num_utt_per_shard=1000, num_threads=50)
        continue

    else:
        pass

    utils_file.logging_info('获取wav.scp')
    list_path = os.path.join(input_dir_part, "list")
    file_path_list = utils_file.do_replace_str_to_file_and_return_list(
        source_str="/home/disk2/librispeech/LibriSpeech",
        target_str="/home/work_nfs15/asr_data/data/LibriSpeech",
        input_file=list_path
    )
    wav_dict = utils_file.do_convert_file_list_to_dict(file_path_list)
    utils_file.write_dict_to_scp(wav_dict, scp_wav_path)

    source_text_path = os.path.join(input_dir_part, f"{part}.trans")
    utils_file.copy_file(source_text_path, text_path)
    utils_file.logging_info('得到scp完毕， 开始通过scp得到shard包')
    utils_file.do_make_shard_file(scp_wav_path, text_path, os.path.join(output_dir_part, 'shards'), num_utt_per_shard=1000, num_threads=50)



