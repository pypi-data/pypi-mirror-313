import random

import numpy as np
from scipy.io import wavfile
import soundfile as sf
EPS = np.finfo(float).eps
def normalize(audio, target_level=-25):
    '''Normalize the signal to the target level'''
    rms = (audio ** 2).mean() ** 0.5
    scalar = 10 ** (target_level / 20) / (rms + EPS)
    audio = audio * scalar
    return audio


def write_wav_with_normal(output_path, audio_reverb, fs):
    level_db = random.uniform(-45, -15)
    audio = normalize(audio_reverb.astype(np.int16), level_db)
    # 保存带有混响的音频
    wavfile.write(output_path, fs, audio)


def read_audio(filename):
    audio, sr = sf.read(filename)
    if sr != 16000:
        audio = sf.resample(audio, 16000)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)  # 合并多个通道
        print('多通道')
    audio = audio.flatten()
    return audio