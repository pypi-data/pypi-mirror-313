"""
@File  :do_convert_wav_text_scp_to_jsonl.py
@Author:Xuelong Geng
@Date  :2024/6/5 2:26
@Desc  :
"""
import os

from gxl_ai_utils.utils import utils_file

wav_path, text_path, output_dir = utils_file.do_get_commandline_param(3, ["wav_path", "text_path", "output_dir"])
output_path = os.path.join(output_dir, "data.list")
utils_file.do_convert_wav_text_scp_to_jsonl(wav_path, text_path, output_path)
