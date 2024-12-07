from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
from gxl_ai_utils.utils import utils_file
cache_dir = './.cache/modelscope'
os.environ['MODELSCOPE_CACHE_DIR'] = cache_dir
os.environ['MODELSCOPE_CACHE'] = cache_dir
os.environ['MODELSCOPE_MODULES_CACHE'] = cache_dir
utils_file.makedir_sil(cache_dir)

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    batch_size=64,
)


def gxl_infer():
    audio_in = 'https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/test_audio/asr_example_zh.wav'
    rec_result = inference_pipeline(audio_in=audio_in)
    print(rec_result)


if __name__ == '__main__':
    """
    hahaha
    """
    gxl_infer()
