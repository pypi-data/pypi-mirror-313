import os
import sys

import tqdm

sys.path.insert(0,'../../../')
from gxl_ai_utils.utils import utils_file
def do_remove():
    """"""
    data_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/"
    dataset_names_list = os.listdir(data_dir)
    for dataset_name in dataset_names_list:
        utils_file.logging_print('开始处理的dataset_name:{}'.format(dataset_name))
        temp_data_dir = os.path.join(data_dir,dataset_name)
        utils_file.logging_print('先判断是否处理完毕')
        text_path = os.path.join(temp_data_dir,'text')
        text_path_2 = os.path.join(temp_data_dir,'all_2.text')
        wav_path = os.path.join(temp_data_dir,'wav.scp')
        wav_path_2 = os.path.join(temp_data_dir,'all_wav.scp')
        if (os.path.exists(text_path) and os.path.exists(wav_path)) or (os.path.exists(text_path_2) and os.path.exists(wav_path_2)):
            utils_file.logging_print('改数据集已经处理完毕,可以开启删除进程')
            now_wav_path = ""
            now_text_path = ""
            if (os.path.exists(text_path) and os.path.exists(wav_path)):
                now_text_path = text_path
                now_wav_path = wav_path
            elif (os.path.exists(text_path_2) and os.path.exists(wav_path_2)):
                now_text_path = text_path_2
                now_wav_path = wav_path_2
            temp_long_old_clean_wav_dir = os.path.join(temp_data_dir,'temp_long_old_clean_wav')
            final_wav_dir = os.path.join(temp_data_dir,'final_wav')
            utils_file.logging_print('首先 删除temp_long_old_clean_wav_dir')
            if os.path.exists(temp_long_old_clean_wav_dir):
                utils_file.remove_dir(temp_long_old_clean_wav_dir)
            utils_file.logging_print('再 删除final_wav_dir中多余的音频')
            all_wav_scp_dict = utils_file.get_scp_for_wav_dir(final_wav_dir)
            my_wav_scp_dict = utils_file.load_dict_from_scp(now_wav_path)
            utils_file.logging_print("一共存在音频数:{}".format(len(all_wav_scp_dict)))
            utils_file.logging_print("真正有效的音频数:{}".format(len(my_wav_scp_dict)))
            del_wav_dict = {}
            for k,v in all_wav_scp_dict.items():
                if k not in my_wav_scp_dict:
                    del_wav_dict[k] = v
            utils_file.logging_print('需要删除音频数:{}'.format(len(del_wav_dict)))
            if len(del_wav_dict) > 0:
                for wav_path in tqdm.tqdm(del_wav_dict.values(), desc='删除音频进度', total=len(del_wav_dict)):
                    utils_file.remove_file(wav_path)
            utils_file.logging_print('删除完毕')
        else:
            utils_file.logging_print('改数据集还未处理完毕')
            continue

if __name__ == '__main__':
    do_remove()