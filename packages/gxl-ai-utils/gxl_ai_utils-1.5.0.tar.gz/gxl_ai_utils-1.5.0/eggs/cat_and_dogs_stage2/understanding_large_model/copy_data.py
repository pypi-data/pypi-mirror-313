import tqdm
import sys
sys.path.insert(0, '/home/work_nfs11/code/xlgeng/gxl_ai_utils')

from gxl_ai_utils.utils import utils_file
from tmp_utils import do_get_formatted_datalist_for_asr_task
# 把测试集 从 nfs15搬运到 54本地盘

input_dir = "/home/work_nfs15/asr_data/data/asr_test_sets"
output_dir = "/home/node54_tmpdata/xlgeng/asr_test_sets"
dataset_names,_ = utils_file.do_listdir(input_dir, return_path=False)

def little_func_for_cp(input_wav_dict, output_dir, index ):
    if index == 0:
        for key, wav_path in tqdm.tqdm(input_wav_dict.items(), total=len(input_wav_dict), desc='复制文件'):
            utils_file.copy_file2(wav_path, output_dir, is_jump=True, is_log=False)
    else:
        for key, wav_path in input_wav_dict.items():
            utils_file.copy_file2(wav_path, output_dir, is_jump=True, is_log=False)


for dataset_name in dataset_names:
    utils_file.logging_print('开始处理', dataset_name)
    multi_process_runner = utils_file.GxlFixedProcessPool(20)
    input_dir_tmp = utils_file.join_path(input_dir, dataset_name)
    wav_dir = utils_file.join_path(input_dir_tmp, "wav")
    wav_scp_path = utils_file.join_path(input_dir_tmp, "wav.scp")
    text_path = utils_file.join_path(input_dir_tmp, "text")
    if not utils_file.if_file_exist(wav_scp_path)  or not utils_file.if_dir_exist(wav_dir) or not utils_file.if_file_exist(text_path):
        utils_file.logging_print("skip:", dataset_name, '因为wav.scp text or wav dir不存在')
        continue
    output_wav_dir = utils_file.join_path(output_dir, dataset_name, 'wav')
    utils_file.makedir_sil(output_wav_dir)
    output_wav_scp_path = utils_file.join_path(output_dir, dataset_name, 'wav.scp')
    output_text_path = utils_file.join_path(output_dir, dataset_name, 'text')
    output_data_list_path = utils_file.join_path(output_dir, dataset_name, 'data.list')
    wav_path_dict = utils_file.load_dict_from_scp(wav_scp_path)
    # 进行文件复制
    utils_file.logging_print('开始进行文件复制, 使用20个进程')
    numb_dict_list = utils_file.do_split_dict(wav_path_dict, 20)
    for i, dict_i in enumerate(numb_dict_list):
        multi_process_runner.add_thread(little_func_for_cp, [dict_i, output_wav_dir, i])
    multi_process_runner.start()
    utils_file.logging_print('复制完成')
    utils_file.logging_print('开始得到data.list')
    new_wav_path_dict = {}
    for key, wav_path in wav_path_dict.items():
        new_wav_path = utils_file.do_replace_dir(wav_path, output_wav_dir)
        new_wav_path_dict[key] = new_wav_path
    text_dict = utils_file.load_dict_from_scp(text_path)
    res_dict_list = do_get_formatted_datalist_for_asr_task(new_wav_path_dict, text_dict, dataset_name)
    utils_file.write_dict_list_to_jsonl(res_dict_list, output_data_list_path)
    utils_file.write_dict_to_scp(new_wav_path_dict, output_wav_scp_path)
    utils_file.write_dict_to_scp(text_dict, output_text_path)


