import os
import shutil

import tqdm

from gxl_ai_utils.utils import utils_file


input_dir = "/home/work_nfs11/hfxue/workspace/wenet_MLS2T_LLM"
output_dir = '/home/work_nfs8/xlgeng/new_workspace/MLS2T_LLM'
utils_file.do_copy_directory_only_codefile(input_dir, output_dir)