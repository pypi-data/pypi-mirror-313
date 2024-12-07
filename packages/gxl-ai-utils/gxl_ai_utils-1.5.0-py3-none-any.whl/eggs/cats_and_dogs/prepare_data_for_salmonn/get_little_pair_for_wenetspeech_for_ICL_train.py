from gxl_ai_utils.utils import utils_file
import random
input_wav = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all/wav.scp"
input_text = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all/text"

wav_dict = utils_file.load_dict_from_scp(input_wav)
text_dict = utils_file.load_dict_from_scp(input_text)
# 随机抽出十条
key_list = []
for i in range(10):
    key = random.choice(list(wav_dict.keys()))
    key_list.append(key)
