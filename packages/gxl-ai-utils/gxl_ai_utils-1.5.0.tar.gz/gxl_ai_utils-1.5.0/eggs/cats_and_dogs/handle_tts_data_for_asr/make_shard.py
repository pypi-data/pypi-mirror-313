import os
import re

import tqdm
import sys

sys.path.insert(0, '../../../')
from gxl_ai_utils.utils import utils_file


def do_remove_punctuation(text):
    # 使用正则表达式去除标点符号，只保留汉字、英文和数字
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)


def make_shard():
    """"""
    target_dir = "/home/work_nfs14/xlgeng/asr_data_shard/pachong_data"
    dataname_list = ["ximalaya_lishi_10T-1", "ximalaya_lishi_10T", "ximalaya_redian_2T"]
    utils_file.logging_print('开始清理text, 清理完毕')
    utils_file.logging_print('开始合并')
    all_list = []
    for dataname in dataname_list:
        temp_dir = os.path.join(target_dir, dataname)
        shards_list_path = os.path.join(temp_dir, "shards_list.txt")
        temp_shard_list = utils_file.load_list_file_clean(shards_list_path)
        all_list.extend(temp_shard_list)
    utils_file.write_list_to_file(all_list, os.path.join(target_dir, "all_shards_list.txt"))
if __name__ == '__main__':
    make_shard()
