import glob
import os
import sys
import tqdm
sys.path.insert(0,'../../../../')
from gxl_ai_utils.utils import utils_file
def handle_path(input_new_tts_final_path, only_name=False):
    """"""
    # 郭钊版：/root/path/282492425329_CPKwq_86_6299.wav
    if not only_name:
        file_name = utils_file.get_file_pure_name_from_path(input_new_tts_final_path)
    else:
        file_name = input_new_tts_final_path
    file_name_item_list = file_name.strip().split("_")
    parent_new_name = file_name_item_list[0] + "_" + file_name_item_list[1]
    if file_name_item_list[2].startswith("VAD"):
        index = int(file_name_item_list[2].split("VAD")[1])
    else:
        index = int(file_name_item_list[2])
    millisecond_num = int(file_name_item_list[3])
    return parent_new_name, index, millisecond_num

def get_little_final(input_final_scp_path, output_dir):
    """从非常大的tts_final_scp中取出一小点，组成一个测试用的小的tts_final_scp文件"""
    all_dict = utils_file.load_dict_from_scp(input_final_scp_path)
    little_dict = utils_file.get_random_subdict(all_dict, 25)
    utils_file.write_dict_to_scp(little_dict, os.path.join(output_dir, f"final_scp_little.scp"))


def little_func4get_text_1(wav_scp_dict, tts_dict, text_scp_dict:dict):
    temp_text_scp_dict = {}
    for key in tqdm.tqdm(wav_scp_dict.keys(), total=len(wav_scp_dict)):
        value = tts_dict[key]
        temp_list = value.split()
        if len(temp_list) == 2:
            wav_path = temp_list[0]
            txt_path = temp_list[1]
            line_i = utils_file.load_first_row_clean(txt_path)
            if len(line_i) > 0:
                list_i = line_i.split()
                if len(list_i) >= 2:
                    key_tmp = list_i[0]
                    value = ' '.join(list_i[1:])
                    key = key.strip()
                    value = value.strip()
                    if key == key_tmp:
                        temp_text_scp_dict[key] = value
                    else:
                        utils_file.logging_print(f'error: key不相等，key：{key}, key_tmp：{key_tmp}, value:{value}')
                else:
                    utils_file.logging_print(f'error: line_i没两个item，key：{key}, line_i：{line_i}')
        else:
            utils_file.logging_print(f'error: value不是分为wav_path 和txt_path，key：{key}, value：{value}')
    text_scp_dict.update(temp_text_scp_dict)

def post_process(output_dir,tts_final_path,shard_output_dir, text_dir=None, TTS_FINAL_TYPE=0):
    utils_file.logging_print('耿雪龙： 通用后处理函数')
    utils_file.logging_print('开始后处理')
    # 这里的tts final_path 只是处理后的wav_list了，没了text信息
    utils_file.logging_print('开始得到tts_wav_dict')
    if TTS_FINAL_TYPE == 0:
        tts_wav_path_list = utils_file.load_list_file_clean(tts_final_path)
        tts_dict = {}
        for tts_wav_path in tts_wav_path_list:
            key = utils_file.get_file_pure_name_from_path(tts_wav_path)
            tts_dict[key] = tts_wav_path
        little_dict = utils_file.get_subdict(tts_dict, 0, 10)
        utils_file.print_dict(little_dict)
    elif TTS_FINAL_TYPE == 1:
        tts_dict = utils_file.load_dict_from_scp(tts_final_path)
        little_dict = utils_file.get_subdict(tts_dict, 0, 10)
        utils_file.print_dict(little_dict)
    else:
        tts_dict = {}
    utils_file.logging_print('得到tts_wav_dict成功,总的tts_wav_dict数为：', len(tts_dict))

    utils_file.logging_print('开始得到总的切割音频的wav_dict：')
    if os.path.exists(os.path.join(output_dir, 'split_wav_big.scp')):
        split_wav_big_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'split_wav_big.scp'))
    else:
        asr_wav_dir = os.path.join(output_dir, 'final_wav')
        split_wav_big_dict = utils_file.get_scp_for_wav_dir(asr_wav_dir)
        utils_file.write_dict_to_scp(split_wav_big_dict, os.path.join(output_dir, 'split_wav_big.scp'))
    little_split_dict = utils_file.get_subdict(split_wav_big_dict, 0, 10)
    utils_file.print_dict(little_split_dict)
    utils_file.logging_print('得到总的切割音频：完成,总的切割音频数为：', len(split_wav_big_dict))

    utils_file.logging_print('然后验证一下和tts wav的key关系')

    tmp_key = list(tts_dict.keys())[0]
    if 'VAD' in tmp_key:
        utils_file.logging_print('含有VAD的key风格,重新设计split_wav_dict的key')
        new_split_dict = {}
        for key, value in split_wav_big_dict.items():
            name, i, d = handle_path(key, only_name=True)
            duration = int(d/1000) + 1
            new_key = f"{name}_VAD{i}_{duration}"
            new_split_dict[new_key] = value
        little_dict = utils_file.get_subdict(new_split_dict, 0, 10)
        utils_file.print_dict(little_dict)
        split_wav_big_dict = new_split_dict

    num = 10
    for key, value in tts_dict.items():
        long_new_name, index, duration = handle_path(key, only_name=True)
        # key_new = f"{long_new_name}_{index}"
        if key in split_wav_big_dict:
            utils_file.logging_print('-----------')
            utils_file.logging_print(f'tts key：{key}, value：{value}')
            utils_file.logging_print(f'asr key：{key}, value：{split_wav_big_dict[key]}')
            utils_file.logging_print('-----------')
            utils_file.logging_print('\n')
            num -= 1
            if num < 0:
                break
    is_verify = num < 0
    utils_file.logging_print(f"验证一下tts wav和asr wav的key关系：验证完成,验证结果为:{is_verify}")

    utils_file.logging_print('如果验证成功，那么就计算覆盖率')
    if is_verify:
        num = 0
        for key, value in tts_dict.items():
            long_new_name, index, duration = handle_path(key, only_name=True)
            # key_new = f"{long_new_name}_{index}"
            if key in split_wav_big_dict:
                num += 1
        utils_file.logging_print(f'tts_final覆盖率为：{num / len(tts_dict)}')

    if not is_verify:
        return
    utils_file.logging_print('开始得到wav.scp')
    if os.path.exists(os.path.join(output_dir, 'wav.scp')):
        wav_scp_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'wav.scp'))
    else:
        wav_scp_dict = {}
        for key, value in tts_dict.items():
            # long_new_name, index, duration = handle_path(key, only_name=True)
            # key_new = f"{long_new_name}_{index}"
            if key in split_wav_big_dict:
                wav_scp_dict[key] = split_wav_big_dict[key]
        utils_file.write_dict_to_scp(wav_scp_dict, os.path.join(output_dir, 'wav.scp'))
    utils_file.logging_print('得到wav.scp：完成, 长度为：', len(wav_scp_dict))

    utils_file.logging_print(f'开始得到text.scp， TTS_FINAL_TYPE：{TTS_FINAL_TYPE}')
    text_scp_dict = {}
    if os.path.exists(os.path.join(output_dir, 'text_with_punctuation')):
        utils_file.logging_print('text_with_punctuation已存在，不用做任何事')
    else:
        if TTS_FINAL_TYPE == 0:
            temp_txt_file_dict = {}
            txt_file_list = glob.glob(str(os.path.join(text_dir, '*.txt')))
            for txt_file in tqdm.tqdm(txt_file_list, total=len(txt_file_list)):
                key = utils_file.get_file_pure_name_from_path(txt_file)
                temp_txt_file_dict[key] = txt_file
            for key in tqdm.tqdm(wav_scp_dict.keys(), total=len(wav_scp_dict)):
                if key in temp_txt_file_dict:
                    txt_file = temp_txt_file_dict[key]
                    line_i = utils_file.load_first_row_clean(txt_file)
                    if len(line_i) > 0:
                        list_i = line_i.split()
                        if len(list_i) >= 2:
                            key_tmp = list_i[0]
                            value = ' '.join(list_i[1:])
                            key = key.strip()
                            value = value.strip()
                            if key == key_tmp:
                                text_scp_dict[key] = value
                            else:
                                utils_file.logging_print(f'error: key不相等，key：{key}, key_tmp：{key_tmp}, value:{value}')
                        else:
                            utils_file.logging_print(f'error: line_i没两个item，key：{key}, line_i：{line_i}')
        elif TTS_FINAL_TYPE == 1:
            num_thread = 20
            runner = utils_file.GxlDynamicThreadPool()
            wav_scp_dict_list = utils_file.do_split_dict(wav_scp_dict, num_thread)
            for wav_scp_dict_i in wav_scp_dict_list:
                runner.add_thread(little_func4get_text_1, [wav_scp_dict_i,tts_dict, text_scp_dict])
            runner.start()
        utils_file.write_dict_to_scp(text_scp_dict, os.path.join(output_dir, 'text_with_punctuation'))
        utils_file.logging_print(f'text_scp得到完成,text_scp_dict长度为：{len(text_scp_dict)}')

    utils_file.logging_print('开始为text清除标点')
    if os.path.exists( os.path.join(output_dir, 'text')):
        utils_file.logging_print('text已存在，不用做任何事')
        pass
    else:
        text_with_punctuation_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'text_with_punctuation'))
        text_no_punctuation_dict = {}
        for key, value in text_with_punctuation_dict.items():
            text_no_punctuation_dict[key] = utils_file.do_filter(value)
        utils_file.write_dict_to_scp(text_no_punctuation_dict, os.path.join(output_dir, 'text'))
    utils_file.logging_print('清除标点完成,len: ', len(text_no_punctuation_dict))

    utils_file.logging_print('开始打shard包')
    utils_file.do_make_shard_file(os.path.join(output_dir, "wav.scp"), os.path.join(output_dir, "text"),
                                  shard_output_dir, num_threads=50)
    utils_file.logging_print('打shard包完成')

