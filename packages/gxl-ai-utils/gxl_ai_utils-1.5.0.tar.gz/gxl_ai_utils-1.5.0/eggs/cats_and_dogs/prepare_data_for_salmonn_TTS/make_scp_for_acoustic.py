import tqdm

from gxl_ai_utils.utils import utils_file
utils_file.logging_limit_print('开始得到acoustic.scp')
# timer = utils_file.GxlTimer()
# input_dir = "/home/work_nfs11/hfxue/corpus/wenetspeech/features/wavlm_features/token_4096/1"
# res_dict_1 = utils_file.do_get_scp_for_wav_dir(input_dir, suffix=".npy")
# input_dir = "/home/work_nfs11/hfxue/corpus/wenetspeech/features/wavlm_features/token_4096/2"
# res_dict_2 = utils_file.do_get_scp_for_wav_dir(input_dir, suffix=".npy")
# res_dict_1.update(res_dict_2)
# output_dir = '/home/work_nfs8/xlgeng/data/raw/wenetspeech_acoustic'
# utils_file.makedir_sil(output_dir)
# output_path = utils_file.join_path(output_dir, 'acoustic.scp')
# utils_file.write_dict_to_scp(res_dict_1, output_path)
# sec = timer.stop_halfway_and_print('结束得到acoustic.scp')
#
# file_row_lines = utils_file.do_get_file_rows_num_shell(output_path)
# utils_file.logging_print('开始得到结果scp文件的一些信息')
# print(f"文件行数为{file_row_lines}")
# lines = utils_file.load_list_file_clean(output_path)
# little_lines = lines[:10]
# utils_file.print_list(little_lines)

utils_file.logging_print('开始复制文件')
output_dir = '/home/work_nfs8/xlgeng/data/raw/wenetspeech_acoustic/npy'
# utils_file.makedir(output_path)
# utils_file.do_copy_files_by_manifest(output_path, output_dir, manifest_type='scp', num_thread=32)
new_scp_path = utils_file.join_path('/home/work_nfs8/xlgeng/data/raw/wenetspeech_acoustic', 'acoustic_new.scp')
utils_file.do_get_scp_for_wav_dir(output_dir, suffix='.npy', wav_scp_file_path=new_scp_path)

from gxl_ai_utils.utils import utils_file
import numpy as np
import tqdm
input_path = '/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn_TTS/wenetspeech_acoustic/cv.scp'
the_dict = utils_file.load_dict_from_scp(input_path)
for key, value in tqdm.tqdm(the_dict.items()):
    s = np.load(value)
    if 0 in s:
        print(0)
    if 4096  in s:
        print(4096)
    if 4095 in s:
        print(4095)