"""
将游戏音频的爬虫数据跳出几份给tom
"""
import os

from gxl_ai_utils.utils import utils_file

input_jsonl_path1 = "/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki/audio4persons/侠盗猎车手：罪恶都市/all_audio.jsonl"
input_jsonl_path2 = "/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki_gxl/王者荣耀/all_audio.jsonl"
output_dir_path1 = "./tmpdir1"
output_dir_path2 = "./tmpdir2"
utils_file.makedir_sil(output_dir_path1)
utils_file.makedir_sil(output_dir_path2)
data_list1 = utils_file.load_dict_list_from_jsonl(input_jsonl_path1)
for i, dict_item in enumerate(data_list1):
    if "en_text" not in dict_item or "en_file_path" not in dict_item:
        continue
    en_text = dict_item["en_text"]
    en_file_path = dict_item["en_file_path"]
    key = utils_file.get_file_pure_name_from_path(en_file_path)
    utils_file.write_list_to_file([en_text], os.path.join(output_dir_path1, key + ".txt"))
    utils_file.copy_file(en_file_path, os.path.join(output_dir_path1, key + ".wav"))
    if i == 10:
        break

utils_file.do_compress_directory_by_tar_form(output_dir_path1,"./")

data_list2 = utils_file.load_dict_list_from_jsonl(input_jsonl_path2)
for i, dict_item in enumerate(data_list2):
    if "en_text" not in dict_item or "cn_text" not in dict_item or "cn_file_path" not in dict_item or "en_file_path" not in dict_item:
        continue
    en_text = dict_item["en_text"]
    en_file_path = dict_item["en_file_path"]
    cn_text = dict_item["cn_text"]
    cn_file_path = dict_item["cn_file_path"]
    key = utils_file.get_file_pure_name_from_path(cn_file_path)
    key_cn = key + "_cn"
    key_en = key + "_en"
    utils_file.write_list_to_file([cn_text], os.path.join(output_dir_path2, key_cn + ".txt"))
    utils_file.copy_file(cn_file_path, os.path.join(output_dir_path2, key_cn + ".wav"))
    utils_file.write_list_to_file([en_text], os.path.join(output_dir_path2, key_en + ".txt"))
    utils_file.copy_file(en_file_path, os.path.join(output_dir_path2, key_en + ".wav"))
    if i == 10:
        break

utils_file.do_compress_directory_by_tar_form(output_dir_path2,"./")
