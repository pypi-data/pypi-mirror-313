
from gxl_ai_utils.utils import utils_file


def do_get_formatted_datalist_for_chat_task(input_wav, input_text, dataset_name):
    """
    这个函是为了给实验室理解大模型任务中要用到的数据生成标准格式的data.list
    标准格式:
      {
  "task": task_tag, # 如 "<TRANSCRIBE>"
  "key":  utt_id, # 如 "IC0001W0007"
  "wav": wav_path, # 如 "/home/backup_nfs/data-ASR/AIShell2/AISHELL-2/iOS/data/wav/C0001/IC0001W0007.wav"
  "txt": text, # 如 "天安门"
  "lang": language, # 如 "<CN>"
  "speaker": speaker_tag, # 如 "spk001"
  "emotion": emotion等分类标签 # 如 "<HAPPY>"
  "gender": 性别标签 # 如 "<MALE>"
  "extra":{class:"label", "duration": wav_length# 单位s，如2.05125，表示2.05秒}
  }

    :param input_text:
    :param input_wav:
    :return:
    """
    if not isinstance(input_wav, dict):
        assert isinstance(input_wav, str)
        input_wav = utils_file.load_dict_from_scp(input_wav)
    if not isinstance(input_text, dict):
        assert isinstance(input_text, str)
        input_text = utils_file.load_dict_from_scp(input_text)
    task_tag = "<S2TCHAT>"
    lang = "<CN>"
    speaker = "<NONE>"
    emotion  = "NEUTRAL"
    gender = "<NONE>"
    res_list = []
    for key, wav_path in utils_file.tqdm(input_wav.items(), desc="Generating formatted data.list for ASR task", total=len(input_wav)):
        # txt = input_text[key]  # 别忘了key值的对应性
        if key not in input_text:
            utils_file.logging_warning("Warning: {} not in input_text".format(key))
            continue
        txt = input_text[key]
        duration = 0
        try:
            duration = utils_file.do_get_wav_duration(wav_path)
        except:
            try:
                samples, rt = utils_file._get_sample_count_torchaudio(wav_path)
                duration = samples / rt
            except:
                # utils_file.logging_print('Error in getting duration of wav file: {}'.format(wav_path))
                duration = 0
        extra = {"duration": duration, "dataset": dataset_name}
        item_dict = {"task": task_tag, "key": key, "wav": wav_path,"txt": txt, "lang": lang, "speaker": speaker, "emotion": emotion, "gender": gender, "extra": extra}
        res_list.append(item_dict)
    return res_list

input_origin_data_jsonl = "/home/work_nfs15/asr_data/data/chat_data/web_text_2019_text/train_20W_3.jsonl"
origin_wav_dir_path = "/home/work_nfs15/asr_data/data/chat_data/web_text_2019_text/train_20W_3_wav"
# 分布得到wav_dict 和 text_dict
wav_dict = utils_file.get_scp_for_wav_dir(origin_wav_dir_path,suffix=".wav")
# print(len(wav_dict))
# little_wav_dict = utils_file.get_subdict(wav_dict, 0, 10)
# utils_file.print_dict(little_wav_dict)
text_dict = {}
info_dict_list = utils_file.load_dict_list_from_jsonl(input_origin_data_jsonl)
for item in utils_file.tqdm(info_dict_list, desc="Generating text dict from jsonl"):
    key = str(item["key"])
    text_dict[key] = item['A']

#     if key in text_dict:
#         print('出现key值重复','老值：',text_dict[key],'新值：',f'{item["Q"]} {item["A"]}')
#     text_dict[item["key"]] = f'{item["Q"]} {item["A"]}'
# tittle_text_dict = {key: text_dict[key] for index, key in enumerate(text_dict) if index < 10}
# utils_file.print_dict(tittle_text_dict)

# check key 是否相同
# eq_num = 0
# neq_num = 0
# for key in wav_dict.keys():
#     if key in text_dict:
#         eq_num += 1
#     else:
#         neq_num +=1
# print("eq_num:",eq_num)
# print("neq_num" , neq_num)


# 得到data.list
data_list_path = "/home/work_nfs15/asr_data/data/chat_data/web_text_2019_text/common_format/train_20W_3/data.list"
res_dict_list = do_get_formatted_datalist_for_chat_task(wav_dict, text_dict, "web_text_2019__text_train_20W_3")
utils_file.write_dict_list_to_jsonl(res_dict_list, data_list_path)
shard_dir = "/home/node54_tmpdata/xlgeng/chat_data/web_text_2019_text/common_format/train_20W_3/shards"
from make_shard_for_common_format import make_shards
make_shards(data_list_path, shard_dir)


