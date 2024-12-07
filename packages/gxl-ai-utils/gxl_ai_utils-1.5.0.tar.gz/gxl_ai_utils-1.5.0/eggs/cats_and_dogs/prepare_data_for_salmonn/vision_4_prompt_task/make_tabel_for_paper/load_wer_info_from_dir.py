import glob
import os

import numpy as np

from gxl_ai_utils.gxl_whisper.utils import optional_float
from gxl_ai_utils.utils import utils_file


def get_data_from_first_dir():
    # 名称   前10 common  icl  icl_with_label  random1 common icl  random2 common icl
    # 针对前十:
    root_dir = "/home/work_nfs15/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v15/5_epoch_ICL_train"
    res_dict = {
        'common': {},
        'icl': {},
        'icl_with_label': {}
    }
    common_path = os.path.join(root_dir, "*Common*first10*")
    icl_path = os.path.join(root_dir, "*ICL*first10*")
    icl_with_label_path = os.path.join(root_dir, "*label_replace*first10*")
    # 得到具体的path
    common_path_list = glob.glob(common_path)
    icl_path_list = glob.glob(icl_path)
    icl_with_label_path_list = glob.glob(icl_with_label_path)
    print(common_path_list)
    print(icl_path_list)
    print(icl_with_label_path_list)
    for i in range(0,17):
        key = f'speechio_{i}'
        for path in common_path_list:
            wer_path = utils_file.join_path(path, key, "wer")
            if os.path.exists(wer_path):
                res_dict['common'][key] = optional_float(utils_file.get_wer_from_wer_file(wer_path))
        for path in icl_path_list:
            wer_path = utils_file.join_path(path, key, "wer")
            if os.path.exists(wer_path):
                res_dict['icl'][key] = optional_float(utils_file.get_wer_from_wer_file(wer_path))
        for path in icl_with_label_path_list:
            wer_path = utils_file.join_path(path, key, "wer")
            if os.path.exists(wer_path):
                res_dict['icl_with_label'][key] = optional_float(utils_file.get_wer_from_wer_file(wer_path))

    icl_info_dict = utils_file.load_data_from_xlsx("./xlsx_data/ICL.xlsx", return_cols=True)
    first_10_common = icl_info_dict["前10"]
    fisrt_10_icl = icl_info_dict["前10 icl"]
    fisrt_10_icl_label = icl_info_dict["前10 icl with inference label"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]
    fisrt_10_icl_label = [item for item in fisrt_10_icl_label if not np.isnan(item)]
    for i in range(17,27):
        index = i - 17
        key = f'speechio_{i}'
        res_dict['common'][key] = first_10_common[index]
        res_dict['icl'][key] = fisrt_10_icl[index]
        res_dict['icl_with_label'][key] = fisrt_10_icl_label[index]
    print(res_dict)
    utils_file.write_dict_to_json(res_dict, "./json_data/first_10_res_dict.json")

def get_data_from_first_dir_for_random(index = 1):
    # 名称   前10 common  icl  icl_with_label  random1 common icl  random2 common icl
    # 针对前十:
    root_dir = "/home/work_nfs15/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v15/5_epoch_ICL_train"
    res_dict = {
        'common': {},
        'icl': {},
        'icl_with_label': {}
    }
    key_word= f"random10_{index}"
    common_path = os.path.join(root_dir, f"*Common*{key_word}*")
    icl_path = os.path.join(root_dir, f"*ICL*{key_word}*")
    # 得到具体的path
    common_path_list = glob.glob(common_path)
    icl_path_list = glob.glob(icl_path)
    print(common_path_list)
    print(icl_path_list)
    for i in range(0,17):
        key = f'speechio_{i}'
        for path in common_path_list:
            wer_path = utils_file.join_path(path, key, "wer")
            if os.path.exists(wer_path):
                res_dict['common'][key] = optional_float(utils_file.get_wer_from_wer_file(wer_path))
        for path in icl_path_list:
            wer_path = utils_file.join_path(path, key, "wer")
            if os.path.exists(wer_path):
                res_dict['icl'][key] = optional_float(utils_file.get_wer_from_wer_file(wer_path))


    icl_info_dict = utils_file.load_data_from_xlsx("./xlsx_data/ICL.xlsx", return_cols=True)
    first_10_common = icl_info_dict[f"{'random10' if index == 1 else 'random10-2'}"]
    fisrt_10_icl = icl_info_dict[f"{'random10' if index == 1 else 'random10-2'} icl"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]
    for i in range(17,27):
        index = i - 17
        key = f'speechio_{i}'
        res_dict['common'][key] = first_10_common[index]
        res_dict['icl'][key] = fisrt_10_icl[index]
    print(res_dict)
    utils_file.write_dict_to_json(res_dict, f"./json_data/{'random10' if index == 1 else 'random10-2'}_res_dict.json")




if __name__ == '__main__':
    """"""
    get_data_from_first_dir_for_random(1)
    get_data_from_first_dir_for_random(2)