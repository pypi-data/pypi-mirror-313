"""
@File  :test.py
@Author:Xuelong Geng
@Date  :2024/6/5 2:25
@Desc  :
"""
from gxl_ai_utils.utils import utils_file

utils_file.do_convert_wav_text_scp_to_jsonl()
utils_file.do_make_shard_file(wav_scp_file_path="", text_scp_file_path="", output_dir="")