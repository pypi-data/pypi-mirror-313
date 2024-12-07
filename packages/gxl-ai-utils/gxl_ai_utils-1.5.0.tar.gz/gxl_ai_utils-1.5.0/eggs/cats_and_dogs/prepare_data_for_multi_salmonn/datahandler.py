"""
@File  :datahandler.py
@Author:Xuelong Geng
@Date  :2024/7/9 20:12
@Desc  :
"""
from gxl_ai_utils.utils import utils_file
from tqdm import tqdm
def get_language_dict():
    """"""
    language_dict = {}
    input_scp = '/home/work_nfs11/hfxue/corpus/fleurs/train/train_wav.scp'
    data_dict = utils_file.load_dict_from_scp(input_scp)
    keys_list = list(data_dict.keys())
    language_index = 0
    for key in tqdm(keys_list):
        language = key.split('_')[1]
        if language not in language_dict:
            language_dict[language] = language_index
            language_index += 1
        else:
            continue
    utils_file.write_dict_to_scp(language_dict, './language.scp')
    return language_dict

if __name__ == '__main__':
    get_language_dict()