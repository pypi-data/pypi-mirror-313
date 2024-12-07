"""
@File  :do_compute_wer.py
@Author:Xuelong Geng
@Date  :2024/6/10 23:40
@Desc  :
"""
from gxl_ai_utils.utils import utils_file
true_path, hyp_path, output_dir = utils_file.do_get_commandline_param(3, ["true_path", "hyp_path", "output_dir"])
utils_file.do_compute_wer(true_text_path=true_path, hyp_text_path=hyp_path, output_dir=output_dir)
