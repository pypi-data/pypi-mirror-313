import torch
import sys
sys.path.insert(0,'/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils')

from gxl_ai_utils.utils import utils_file

def get_error_wav_list():
    """"""
    error_key_list = [
        '2dlcYQi51Sk__20190615_CCTV_100',
        '2dlcYQi51Sk__20190615_CCTV_102',
        '2dlcYQi51Sk__20190615_CCTV_103',
        'XzBJBIwvqSw__20190115_CCTV_203',
        'XzBJBIwvqSw__20190115_CCTV_208',
        'XzBJBIwvqSw__20190115_CCTV_58',
        'XzBJBIwvqSw__20190115_CCTV_68'
    ]
    right_key_list = [
        'XzBJBIwvqSw__20190115_CCTV_204',
        'XzBJBIwvqSw__20190115_CCTV_205',
        'XzBJBIwvqSw__20190115_CCTV_206',
        'XzBJBIwvqSw__20190115_CCTV_207',
        'XzBJBIwvqSw__20190115_CCTV_209',
        'XzBJBIwvqSw__20190115_CCTV_70'
    ]
    error_dict_list = []
    right_dict_list = []
    dict_list = utils_file.load_dict_list_from_jsonl('./data.list')
    for d in dict_list:
        if d['key'] in error_key_list:
            error_dict_list.append(d)
        if d['key'] in right_key_list:
            right_dict_list.append(d)
    utils_file.write_dict_list_to_jsonl(error_dict_list, './error.list')
    utils_file.write_dict_list_to_jsonl(right_dict_list, './right.list')
    for d in error_dict_list:
        wav_path = d['wav']
        utils_file.copy_file_to_dir(wav_path, './error')
    for d in right_dict_list:
        wav_path = d['wav']
        utils_file.copy_file_to_dir(wav_path, './right')



if __name__ == "__main__":
    """"""
    import torch
    get_error_wav_list()

