import os
import sys
sys.path.insert(0,'../../../../')
from gxl_ai_utils.utils import utils_file

wav_path = "/home/work_nfs8/xlgeng/new_workspace/data/scp_asr/aishell4/wav.scp"
text_path = "/home/work_nfs8/xlgeng/new_workspace/data/scp_asr/aishell4/text"
output_dir = "/home/work_nfs10/asr_data/data/aishell4/shards"
utils_file.makedir_sil(output_dir)
now_time = utils_file.do_get_now_time()
utils_file.do_make_shard_file(wav_path, text_path, output_dir)
print("done")
time_elapsed = utils_file.do_get_elapsed_time(now_time)
utils_file.logging_info(f'耗时：{time_elapsed} s')
