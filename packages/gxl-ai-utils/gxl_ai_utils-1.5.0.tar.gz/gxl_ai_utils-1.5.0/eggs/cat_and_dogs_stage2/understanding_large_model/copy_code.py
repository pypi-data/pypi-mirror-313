import sys
sys.path.insert(0,'../../../')
from gxl_ai_utils.utils import utils_file

"""
把杨泽使用的代码拷贝到我的目录下，但是不拷贝大的pt文件
"""
input_dir = "/home/node54_tmpdata/yzli/wenet_whisper_finetune"
output_dir = "/home/node54_tmpdata/xlgeng/code/wenet_whisper_finetune"
utils_file.remove_dir(output_dir)
utils_file.do_copy_directory_only_codefile_with_false_suffix(
    input_dir, output_dir, false_suffix_tuple=()
)