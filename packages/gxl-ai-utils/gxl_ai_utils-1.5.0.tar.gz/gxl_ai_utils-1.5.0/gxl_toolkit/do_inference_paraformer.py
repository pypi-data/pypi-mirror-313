import tqdm

from gxl_ai_utils.utils import utils_file

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import sys

arg_num = len(sys.argv)

input_wav_scp_path = sys.argv[1]
output_dir = sys.argv[2]
if len(sys.argv) > 3:
    lab_text_path = sys.argv[3]
else:
    lab_text_path = None

utils_file.do_inference_paraformer(input_wav_scp_path, output_dir, lab_text_path)
