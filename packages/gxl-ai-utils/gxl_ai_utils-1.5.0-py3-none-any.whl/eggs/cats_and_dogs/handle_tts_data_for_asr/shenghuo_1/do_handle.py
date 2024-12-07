import argparse
import ast
import glob
import os

import tqdm
import sys
sys.path.insert(0,'../../../../')
from gxl_ai_utils.utils import utils_file

NEW2OLD_TABLE = {}
VAD_INFO_TABLE = {}
THREAD_NUM = 40
IF_START_BY_0 = True  # 切割后的音频的名字的序号,是否以0起始,还是以1起始.
VAD_TYPE = 1


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tts_final_scp_name", type=str)
    parser.add_argument("--asr_final_scp_name", type=str)
    parser.add_argument("--do_split", type=bool, default=False)
    args = parser.parse_args()
    return args


def pre_do(final_tts_scp_path: str, output_dir: str):
    utils_file.logging_print('首先切分tts_final.scp,切分为6个')
    # final_tts_dict = utils_file.load_dict_from_scp(final_tts_scp_path)
    # tts_dict_list = utils_file.do_split_dict(final_tts_dict, 6)
    # for i, tts_dict in enumerate(tts_dict_list):
    #     i = i + 1
    #     utils_file.write_dict_to_scp(tts_dict, os.path.join(output_dir, f"tts_final_{i}.scp"))
    final_tts_list = utils_file.load_list_file_clean(final_tts_scp_path)
    list_list = utils_file.do_split_list(final_tts_list, 6)
    for i, list in enumerate(list_list):
        i = i + 1
        utils_file.write_list_to_file(list, os.path.join(output_dir, f"tts_final_{i}.scp"))

def do_handle_wav(long_wav_new_name, output_dir="./"):
    """
    处理一个长音频. 传入该长音频的new_name, 然后对其进行clean和切割.
    :param long_wav_new_name:
    :param output_dir:
    :return:
    """
    global NEW2OLD_TABLE, VAD_INFO_TABLE, THREAD_NUM
    the_old_wav_path = NEW2OLD_TABLE.get(long_wav_new_name, None)
    if the_old_wav_path is None:
        utils_file.logging_print(
            f"do_handle_wav(): old2new字典中不包含如下new_name的映射, long_wav_new_name={long_wav_new_name}"
        )
        return False
    if not os.path.exists(the_old_wav_path):
        utils_file.logging_print(
            f"do_handle_wav(): the_old_wav_path is not exist, long_wav_new_name:{long_wav_new_name},the_old_wav_path:{the_old_wav_path}"
        )
        return False
    long_old_clean_wav_dir = os.path.join(output_dir, "temp_long_old_clean_wav")
    utils_file.makedir_sil(long_old_clean_wav_dir)
    long_clean_path = os.path.join(long_old_clean_wav_dir, long_wav_new_name + ".wav")
    if not os.path.exists(long_clean_path):
        # 先规范化音频
        utils_file.do_clean_wav(the_old_wav_path, long_clean_path)
        # 开始切割音频
        vad_info4long_new_name = VAD_INFO_TABLE.get(long_wav_new_name, None)
        if vad_info4long_new_name is None:
            utils_file.logging_print(
                f"do_handle_wav(): vad_table不包含如下new_name的映射, long_wav_new_name={long_wav_new_name}"
            )
            return False
        final_wav_dir = os.path.join(output_dir, "final_wav")
        utils_file.makedir_sil(final_wav_dir)
        slicing_wav(long_clean_path, vad_info4long_new_name, final_wav_dir, long_wav_new_name, THREAD_NUM)
    else:
        utils_file.logging_print(
            f"do_handle_wav(): long_old_clean_path is exist, long_wav_new_name={long_wav_new_name}, 跳过该长音频的处理"
        )
    return True


def slicing_wav(input_file_path, vad_info4long_new_name, output_dir, wav_new_name, thread_num=40):
    """
    将一个音频,依据时间戳, 切分成若干小音频. 此处可以多线程并行处理
    """
    global IF_START_BY_0, VAD_TYPE
    sorted_list = get_vad_info_list(vad_info4long_new_name, VAD_TYPE)
    thread_num = thread_num if len(sorted_list) > thread_num else len(sorted_list)
    runner = utils_file.GxlFixedThreadPool(thread_num)
    for i, vad_info in enumerate(sorted_list):
        if IF_START_BY_0:
            i = i
        else:
            i = i + 1
        runner.add_thread(little_func4slicing_wav, [i, vad_info, input_file_path, output_dir, wav_new_name])
    runner.start()


def get_vad_info_list(vad_info4long_new_name, vad_type=0):
    """
    处理vad_info4long_new_name, 得到排过序的一个双层列表 [[s,e],[s,e],[s,e]...]
    :param vad_info_txt_path:
    :return:
    """
    sorted_list = []
    if vad_type == 0:
        """
        vad文件, 格式如下:
        i,j
        i,j
        i,j     
        """
        vad_info_str_list = utils_file.load_list_file_clean(vad_info4long_new_name)
        vad_info_list = []
        for vad_info_str in vad_info_str_list:
            vad_i = vad_info_str.strip().split(",")
            vad_info_list.append(vad_i)
        sorted_list = sorted(vad_info_list, key=lambda x: int(x[0]))
    elif vad_type == 1:
        """
        vad 文件, 格式如下:
        [[i,j],[i,j],[i,j]..]
        """
        str_one_line = utils_file.load_first_row_clean(vad_info4long_new_name)
        vad_info_list = ast.literal_eval(str_one_line)
        sorted_list = sorted(vad_info_list, key=lambda x: int(x[0]))
    elif vad_type == 2:
        """
        vad str, 格式如下:
        [[i,j],[i,j],[i,j]..]
        """
        # str_one_line = utils_file.load_first_row_clean(vad_info4long_new_name)
        vad_info_list = ast.literal_eval(vad_info4long_new_name)
        sorted_list = sorted(vad_info_list, key=lambda x: int(x[0]))

    return sorted_list


def little_func4slicing_wav(i, vad_info, input_file_path, output_dir, wav_new_name):
    """

    :param i:
    :param vad_info:  [i,j], 毫秒数
    :param input_file_path:
    :param output_dir:
    :param wav_new_name:
    :return:
    """
    start_time = vad_info[0]
    end_time = vad_info[1]
    duration = int(end_time) - int(start_time)
    start_sample = int(start_time) * 16
    end_sample = int(end_time) * 16
    output_path = os.path.join(output_dir, f"{wav_new_name}_{i}_{duration}.wav")
    utils_file.do_extract_audio_segment(input_file_path, output_path, start_sample, end_sample)


def solution(final_tts_scp_path, output_dir, old2new_dir, input_vad_info_dir):
    utils_file.logging_print('首先从命令行中拿到要处理的tts_final.scp的子集')
    args = get_args()
    if args.do_split:
        utils_file.logging_print('开始do_split')
        pre_do(final_tts_scp_path, output_dir)
        utils_file.logging_print('do_split完成, 直接return')
        return
    tts_scp_path = os.path.join(output_dir, args.tts_final_scp_name)
    asr_final_path = os.path.join(output_dir, args.asr_final_scp_name)
    if os.path.exists(asr_final_path):
        utils_file.logging_print('asr_scp_path已经存在，直接删除')
        os.remove(asr_final_path)
    utils_file.logging_print('加载vad和old2new的信息')
    utils_file.makedir_sil(output_dir)
    do_get_vad_scp_file(input_vad_info_dir, output_dir)
    do_get_old2new_scp_file(old2new_dir, output_dir)
    NEW2OLD_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "old2new.scp")))
    VAD_INFO_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "vad_res.scp")))

    utils_file.logging_print('获取tts_scp对应的长音频的新名字列表')
    # tts_dict = utils_file.load_dict_from_scp(tts_scp_path)
    wav_path_list = utils_file.load_list_file_clean(tts_scp_path)
    long_wav_new_names_list = []
    # for key in tqdm.tqdm(tts_dict.keys(), total=len(tts_dict)):
    #     long_wav_new_name, _, _ = handle_path(key, only_name=True)
    #     long_wav_new_names_list.append(long_wav_new_name)
    for wav_path in tqdm.tqdm(wav_path_list, total=len(wav_path_list)):
        long_wav_new_name, _, _ = handle_path(wav_path, only_name=False)
        long_wav_new_names_list.append(long_wav_new_name)
    long_wav_new_names_list = list(set(long_wav_new_names_list))

    utils_file.logging_print("开始逐条长音频得处理")
    for long_wav_new_name in tqdm.tqdm(long_wav_new_names_list, total=len(long_wav_new_names_list)):
        do_handle_wav(long_wav_new_name, output_dir)
    utils_file.logging_print('完全切割完毕')
    return
    #  ------------------后处理-----------------------------

def post_process(output_dir,tts_final_path):
    utils_file.logging_print('开始后处理')
    # 这里的tts final_path 只是处理后的wav_list了，没了text信息
    tts_wav_path_list = utils_file.load_list_file_clean(tts_final_path)
    tts_dict = {}
    for tts_wav_path in tts_wav_path_list:
        key = utils_file.get_file_pure_name_from_path(tts_wav_path)
        tts_dict[key] = tts_wav_path
    little_dict = utils_file.get_subdict(tts_dict, 0, 10)
    utils_file.print_dict(little_dict)
    utils_file.logging_print('首先弄清楚asr wav和tts wav的对应关系')
    asr_wav_dir = os.path.join(output_dir, 'final_wav')
    utils_file.logging_print('开始得到总的切割音频：')
    # split_wav_big_dict = utils_file.get_scp_for_wav_dir(asr_wav_dir)
    split_wav_big_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'split_wav_big.scp'))
    little_split_dict = utils_file.get_subdict(split_wav_big_dict, 0, 10)
    utils_file.print_dict(little_split_dict)
    utils_file.logging_print('得到总的切割音频：完成,总的切割音频数为：', len(split_wav_big_dict))
    # utils_file.write_dict_to_scp(split_wav_big_dict, os.path.join(output_dir, 'split_wav_big.scp'))
    utils_file.logging_print('然后验证一下和tts wav的key关系')
    utils_file.logging_print('开始变换split_dict的key')
    new_split_dict = {}
    for key, value in split_wav_big_dict.items():
        name, i, d = handle_path(key, only_name=True)
        new_key = f"{name}_VAD{i}_{int(float(d)/1000)+1}"
        new_split_dict[new_key] = value
    little_dict = utils_file.get_subdict(new_split_dict, 0, 10)
    utils_file.print_dict(little_dict)
    num = 10
    for key, value in tts_dict.items():
        long_new_name, index, duration = handle_path(key, only_name=True)
        # key_new = f"{long_new_name}_{index}"
        if key in new_split_dict:
            utils_file.logging_print('-----------')
            utils_file.logging_print(f'tts key：{key}, value：{value}')
            utils_file.logging_print(f'asr key：{key}, value：{new_split_dict[key]}')
            utils_file.logging_print('-----------')
            utils_file.logging_print('\n')
            num -= 1
            if num < 0:
                break
    num = 0
    for key, value in tts_dict.items():
        long_new_name, index, duration = handle_path(key, only_name=True)
        # key_new = f"{long_new_name}_{index}"
        if key in new_split_dict:
           num +=1
    utils_file.logging_print("验证一下tts wav和asr wav的key关系：验证成功完成， key值可以直接完全对应")
    utils_file.logging_print(f'tts_final覆盖率为：{num / len(tts_dict)}')

    utils_file.logging_print('开始得到wav.scp')
    wav_scp_dict = {}
    for key, value in tts_dict.items():
        long_new_name, index, duration = handle_path(key, only_name=True)
        # key_new = f"{long_new_name}_{index}"
        if key in new_split_dict:
            wav_scp_dict[key] = new_split_dict[key]
    utils_file.write_dict_to_scp(wav_scp_dict, os.path.join(output_dir, 'wav.scp'))
    utils_file.logging_print('得到wav.scp：完成, 长度为：', len(wav_scp_dict))
    # return
    utils_file.logging_print('开始得到text.scp')
    text_dir = "/home/work_nfs8/kxxia/data/score1/asr"
    text_scp_dict = utils_file.get_scp_for_wav_dir(text_dir,suffix='.txt')
    little_dict = utils_file.get_subdict(text_scp_dict, 0, 10)
    utils_file.print_dict(little_dict)
    utils_file.logging_print(f'text_scp_dict长度为：{len(text_scp_dict)}')
    new_text_scp_dict = {}
    for key, value in text_scp_dict.items():
        if key in wav_scp_dict:
            new_text_scp_dict[key] = value
    utils_file.write_dict_to_scp(new_text_scp_dict, os.path.join(output_dir, 'text_old'))
    return



def do_get_vad_scp_file(input_dir, output_dir='./'):
    """
    tts处理流程中会对每一个音频生成一个vad_info的txt文件, 我们得到一个key vad_info.txt的字典
    :param input_dir:
    :return:
    """
    vad_res_dict = utils_file.get_scp_for_wav_dir(input_dir, suffix="txt")
    little_res_dict = utils_file.get_subdict(vad_res_dict, 0, 10)
    utils_file.logging_print("do_get_vad_scp_file(): 小字典示例:")
    utils_file.print_dict(little_res_dict)
    utils_file.write_dict_to_scp(vad_res_dict, os.path.join(output_dir, "vad_res.scp"))


def do_get_old2new_scp_file(input_dir, output_dir='./'):
    """
    这个input_dir中包含大量的old2new_*.txt文件, 我们得到一个key old2new.txt的字典
    :param input_dir:
    :return:
    """
    if os.path.isfile(input_dir):
        utils_file.logging_print("do_get_old2new_scp_file(): input_dir是文件")
        utils_file.copy_file(input_dir, os.path.join(output_dir, "old2new.scp"))
        return
    old2new_path_list = glob.glob(f"{input_dir}/old2new*.scp")
    res_dict = {}
    for old2new_path in old2new_path_list:
        old2new_dict = utils_file.load_dict_from_scp(old2new_path)
        res_dict.update(old2new_dict)
    little_res_dict = utils_file.get_subdict(res_dict, 0, 10)
    utils_file.logging_print("do_get_old2new_scp_file(): 小字典示例:")
    utils_file.print_dict(little_res_dict)
    utils_file.write_dict_to_scp(res_dict, os.path.join(output_dir, "old2new.scp"))


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


def final_handle(output_dir):
    """"""
    text_file_list = glob.glob(os.path.join(output_dir, "*.text"))
    text_dict_all = {}
    for text_file in text_file_list:
        text_dict = utils_file.load_dict_from_scp(text_file)
        text_dict_all.update(text_dict)
    utils_file.write_dict_to_scp(text_dict_all, os.path.join(output_dir, "all.text"))
    wavscp_file_list = glob.glob(os.path.join(output_dir, "*_wav.scp"))
    wav_dict_all = {}
    for wavscp_file in wavscp_file_list:
        wav_dict = utils_file.load_dict_from_scp(wavscp_file)
        wav_dict_all.update(wav_dict)
    utils_file.write_dict_to_scp(text_dict_all, os.path.join(output_dir, "all_wav.scp"))
    utils_file.do_convert_wav_text_scp_to_jsonl(os.path.join(output_dir, "all_wav.scp"),
                                                os.path.join(output_dir, "all.text"),
                                                os.path.join(output_dir, "all.list"))


def get_little_final(input_final_scp_path, output_dir):
    """从非常大的tts_final_scp中取出一小点，组成一个测试用的小的tts_final_scp文件"""
    all_dict = utils_file.load_dict_from_scp(input_final_scp_path)
    little_dict = utils_file.get_random_subdict(all_dict, 25)
    utils_file.write_dict_to_scp(little_dict, os.path.join(output_dir, f"final_scp_little.scp"))


if __name__ == '__main__':
    output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/ximalaya_shenghuo_10T_1"
    # output_dir = './output/ximalaya_shenghuo_10T_1/'
    utils_file.makedir_for_file_or_dir(output_dir)
    input_vad_info_dir = "/home/work_nfs8/kxxia/data/vad_result1"
    # 表格里写的如果不是dir,而是成品scp文件， 就把scp文件的路径传入即可
    old2new_dir = "/home/node36_data/kxxia/life/list/init_lists"
    final_tts_scp_path = "/home/work_nfs8/kxxia/data/score1/final.scp"
    # get_little_final(final_tts_scp_path, output_dir)
    # final_tts_scp_path = os.path.join(output_dir, "final_scp_little.scp")
    # post_process( output_dir, final_tts_scp_path)
    def little_func(input_text_dict, res_text_dict):
        for key, path in tqdm.tqdm(input_text_dict.items(), total=len(input_text_dict)):
            text = utils_file.load_first_row_clean(path)
            if len(text) > 0:
                text = text.strip().split()[-1]
                text = utils_file.do_filter(text)
                res_text_dict[key] = text

    # text_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, "text_old"))
    # new_text_dict = {}
    # text_dict_list = utils_file.do_split_dict(text_dict, 100)
    # runner = utils_file.GxlDynamicThreadPool()
    # for text_dict_i in text_dict_list:
    #     runner.add_task(little_func, [text_dict_i, new_text_dict])
    # runner.start()
    # utils_file.write_dict_to_scp(new_text_dict, os.path.join(output_dir, "text"))
    # utils_file.write_dict_to_scp(text_dict, os.path.join(output_dir, "text_old"))
    shard_output_dir = "/home/work_nfs14/xlgeng/asr_data_shard/pachong_data/shenghuo_1/"
    utils_file.do_make_shard_file(os.path.join(output_dir, "wav.scp"), os.path.join(output_dir, "text"),
                                  shard_output_dir, num_threads=50)
