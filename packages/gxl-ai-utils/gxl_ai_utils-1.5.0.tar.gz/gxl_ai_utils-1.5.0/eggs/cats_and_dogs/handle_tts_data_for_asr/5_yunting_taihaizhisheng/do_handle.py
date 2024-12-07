import argparse
import ast
import glob
import os
import sys
sys.path.insert(0,'../../../../')
sys.path.insert(0,'../')
from gxl_common_utils.common_utils import post_process
import tqdm

from gxl_ai_utils.utils import utils_file

NEW2OLD_TABLE = {}
VAD_INFO_TABLE = {}
THREAD_NUM = 40 # 切割音频的进程
IF_START_BY_0 = True  # 切割后的音频的名字的序号,是否以0起始,还是以1起始.
VAD_TYPE = 0  # 0:文件,文件内多行,每行都是i:j .. 1:文件, 格式如下:[[i,j],[i,j],[i,j]..] .. 2: str, 格式如下:[[i,j],[i,j],[i,j]..] ... 3:vad str, 格式如下:i:j i:j i:j ...
TTS_FINAL_TYPE=1  # 0:简短list型.. 1:含txt的scp型

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tts_final_scp_name", type=str)
    parser.add_argument("--asr_final_scp_name", type=str)
    parser.add_argument("--do_split", type=bool, default=False)
    args = parser.parse_args()
    return args
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
def pre_do(input_vad_info_dir,old2new_dir, final_tts_scp_path: str, output_dir: str):
    do_get_vad_scp_file(input_vad_info_dir, output_dir)
    do_get_old2new_scp_file(old2new_dir, output_dir)
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
    elif vad_type == 3:
        """
        vad str, 格式如下:
        i:j i:j i:j ...
        """
        split_list = vad_info4long_new_name.strip().split()
        vad_info_list = []
        for res in split_list:
            res_i = res.split(":")[0]
            res_j = res.split(":")[1]
            vad_info_list.append([res_i, res_j])
        sorted_list = sorted(vad_info_list, key=lambda x: int(x[0]))
    return sorted_list
def do_get_vad_scp_file(input_dir, output_dir='./'):
    """
    tts处理流程中会对每一个音频生成一个vad_info的txt文件, 我们得到一个key vad_info.txt的字典
    :param input_dir:
    :return:
    """
    if isinstance(input_dir, list):
        vad_res_dict = {}
        for input_dir_i in input_dir:
            vad_res_dict.update(utils_file.get_scp_for_wav_dir(input_dir_i, suffix="txt"))
    elif os.path.isdir(input_dir):
        vad_res_dict = utils_file.get_scp_for_wav_dir(input_dir, suffix="txt")
    else:
        res_list = utils_file.load_list_file_clean(input_dir)
        vad_res_dict = {}
        for res_line in res_list:
            wav_path = res_line.split('|')[0]
            key = utils_file.get_file_pure_name_from_path(wav_path)
            info = res_line.split('|')[1].strip()
            vad_res_dict[key] = info
    little_res_dict = utils_file.get_subdict(vad_res_dict, 0, 10)
    utils_file.logging_print("do_get_vad_scp_file(): 小字典示例:")
    utils_file.print_dict(little_res_dict)
    utils_file.write_dict_to_scp(vad_res_dict, os.path.join(output_dir, "vad_res.scp"))

def do_get_old2new_scp_file(input_dir, output_dir='./'):
    """
    这个input_dir中包含大量的old2new_*.txt文件
    :param input_dir:
    :return:
    """
    if isinstance(input_dir, list):
        old2new_path_list = input_dir
    elif os.path.isfile(input_dir):
        utils_file.logging_print("do_get_old2new_scp_file(): input_dir是文件")
        utils_file.copy_file(input_dir, os.path.join(output_dir, "old2new.scp"))
        return
    else:
        old2new_path_list = glob.glob(f"{input_dir}/old2new*.scp")

    res_dict = {}
    for old2new_path in old2new_path_list:
        old2new_dict = utils_file.load_dict_from_scp(old2new_path)
        res_dict.update(old2new_dict)
    little_res_dict = utils_file.get_subdict(res_dict, 0, 10)
    utils_file.logging_print("do_get_old2new_scp_file(): 小字典示例:")
    utils_file.print_dict(little_res_dict)
    utils_file.write_dict_to_scp(res_dict, os.path.join(output_dir, "old2new.scp"))

def solution(final_tts_scp_path, output_dir, old2new_dir, input_vad_info_dir):
    utils_file.logging_print('首先从命令行中拿到要处理的tts_final.scp的子集')
    args = get_args()
    if args.do_split:
        utils_file.logging_print('开始do_split')
        pre_do(input_vad_info_dir,old2new_dir,final_tts_scp_path, output_dir)
        utils_file.logging_print('do_split完成, 直接return')
        return
    tts_scp_path = os.path.join(output_dir, args.tts_final_scp_name)
    asr_final_path = os.path.join(output_dir, args.asr_final_scp_name)
    if os.path.exists(asr_final_path):
        utils_file.logging_print('asr_scp_path已经存在，直接删除')
        os.remove(asr_final_path)
    utils_file.logging_print('拿到成功\n')

    utils_file.logging_print('加载vad和old2new的信息,从而在output目录下得到vad_res.scp和old2new.scp,这一步基本是不用变动的,然后将dict信息加载到全局变量中')
    utils_file.makedir_sil(output_dir)
    NEW2OLD_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "old2new.scp")))
    VAD_INFO_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "vad_res.scp")))
    utils_file.logging_print('加载vad和old2new的信息完成\n')

    utils_file.logging_print('获取tts_scp对应的长音频的新名字列表')
    long_wav_new_names_list = []
    if TTS_FINAL_TYPE == 0:
        wav_path_list = utils_file.load_list_file_clean(tts_scp_path)
        for wav_path in tqdm.tqdm(wav_path_list, total=len(wav_path_list)):
            long_wav_new_name, _, _ = handle_path(wav_path, only_name=False)
            long_wav_new_names_list.append(long_wav_new_name)
    elif TTS_FINAL_TYPE == 1:
        tts_dict = utils_file.load_dict_from_scp(tts_scp_path)
        for key in tqdm.tqdm(tts_dict.keys(), total=len(tts_dict)):
            long_wav_new_name, _, _ = handle_path(key, only_name=True)
            long_wav_new_names_list.append(long_wav_new_name)
    long_wav_new_names_list = list(set(long_wav_new_names_list))
    utils_file.logging_print('获取tts_scp对应的长音频的新名字列表完成,其一共有:', len(long_wav_new_names_list), '\n')

    utils_file.logging_print('开始验证vad信息和old2new信息是否全面,从而得到最终真正能处理的长音频的新名字列表,以及他的数量')
    final_long_wav_new_names_list = []
    for long_wav_new_name in tqdm.tqdm(long_wav_new_names_list, total=len(long_wav_new_names_list)):
        if long_wav_new_name in VAD_INFO_TABLE and long_wav_new_name in NEW2OLD_TABLE:
            final_long_wav_new_names_list.append(long_wav_new_name)
        else:
            utils_file.logging_print(
                f"这个长音频 验证vad信息和old2new信息是否全面失败: long_wav_new_name={long_wav_new_name}"
            )
            if not (long_wav_new_name in VAD_INFO_TABLE):
                utils_file.logging_print(f"vad_info表中不包含该音频")
            if not (long_wav_new_name in NEW2OLD_TABLE):
                utils_file.logging_print(f"new2old表中不包含该音频")
    utils_file.logging_print('验证vad信息和old2new信息是否全面完成,其一共有:', len(final_long_wav_new_names_list), '\n')
    long_wav_new_names_list = final_long_wav_new_names_list



    utils_file.logging_print("开始逐条长音频得处理")
    for long_wav_new_name in tqdm.tqdm(long_wav_new_names_list, total=len(long_wav_new_names_list)):
        do_handle_wav(long_wav_new_name, output_dir)
    utils_file.logging_print('完全切割完毕')
    return
    #  ------------------后处理-----------------------------



if __name__ == '__main__':
    output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/yunting_taihaizhisheng"
    utils_file.makedir_for_file_or_dir(output_dir)
    old2new_dir = "/home/work_nfs8/ypjiang/data_process/yunting/台海之声/*_info/init_lists"
    vad_info_dir = "/home/work_nfs8/ypjiang/data_process/yunting/台海之声/*_info/vad_info"
    # text_dir = "/home/work_nfs6/tlzuo/data_handle/lists/5txts"
    final_tts_scp_path = "/home/work_nfs8/ypjiang/data_process/yunting/台海之声/final.scp"

    # utils_file.logging_print('开始一些专属的特殊处理')
    # directories = glob.glob('/home/work_nfs8/ypjiang/data_process/yunting/台海之声/*_info')
    # # 打印匹配到的目录
    # print(directories)
    # old2new_res_list = []
    # for directory in directories:
    #     temp_parent_dir = os.path.join(directory, 'init_lists')
    #     old2new_path_list_temp = glob.glob(os.path.join(temp_parent_dir, 'old2new*.scp'))
    #     old2new_res_list.extend(old2new_path_list_temp)
    # old2new_dir = old2new_res_list
    # utils_file.print_list(old2new_dir)
    #
    # vad_dir_list = []
    # for directory in directories:
    #     temp_parent_dir = os.path.join(directory, 'vad_info')
    #     vad_dir_list.append(temp_parent_dir)
    # vad_info_dir= vad_dir_list
    # utils_file.print_list(vad_info_dir)

    # solution(final_tts_scp_path, output_dir, old2new_dir, vad_info_dir)
    sys.path.insert(0, '../')
    from gxl_common_utils.common_utils import post_process
    shard_output_dir = "/home/work_nfs9/xlgeng/asr_data_shard/pachong_data/5_yunting_taihaizhisheng/"
    post_process(output_dir, final_tts_scp_path, shard_output_dir, TTS_FINAL_TYPE=TTS_FINAL_TYPE)