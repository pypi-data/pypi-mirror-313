import re

import torch

from gxl_ai_utils.utils import utils_file
from gxl_ai_utils.utils import utils_data


def seg_char(sent):
    pattern = re.compile(r'([\u4e00-\u9fa5])')
    chars = pattern.split(sent)
    chars = [w for w in chars if len(w.strip()) > 0]
    return chars


if __name__ == '__main__':
    """"""
    wav_path = "E:\gengxuelong_study\server_local_adapter\\ai\data\small_aishell/dev\BAC009S0724W0121.wav"
    waveform,sr = utils_data.torchaudio_load(wav_path)

