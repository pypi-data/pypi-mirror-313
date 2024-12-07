import argparse
import glob
import os
import threading
import tqdm
import sys
sys.path.insert(0, '../../../')
from gxl_ai_utils.utils import utils_file

NEW2OLD_TABLE = {}
VAD_INFO_TABLE = {}
THREAD_NUM = 40


def get_vad_info_list(vad_info_txt_path):
    """
    从vad_info.txt中读取时间戳， 得到排过序的一个双层列表 [[s,e],[s,e],[s,e]...]
    :param vad_info_txt_path:
    :return:
    """

    vad_info_str_list = utils_file.load_list_file_clean(vad_info_txt_path)
    # vad_info_list = []
    # for vad_info_str in vad_info_str_list:
    #     vad_i = vad_info_str.strip().split(",")
    #     vid_i = [int(vad_i[0])*2, int(vad_i[1])*2]
    #     vad_info_list.append(vad_i)
    vad_info_list = eval(vad_info_str_list[0])
    sorted_list = sorted(vad_info_list, key=lambda x: int(x[0]))
    return sorted_list

def handle_path_new(input_new_tts_final_path, only_name=False):
    """"""
    # 郭钊版：/root/path/282492425329_CPKwq_86_6299.wav
    if only_name:
        file_name = input_new_tts_final_path
    else:
        file_name = utils_file.get_file_pure_name_from_path(input_new_tts_final_path)
    file_name_item_list = file_name.strip().split("_")
    parent_new_name = file_name_item_list[0] + "_" + file_name_item_list[1]
    index = int(file_name_item_list[2])
    millisecond_num = int(file_name_item_list[3])
    return parent_new_name, index, millisecond_num

def handle_path_old(input_new_tts_final_path, only_name=False):
    """"""
    if only_name:
        file_name = input_new_tts_final_path
    else:
        file_name = utils_file.get_file_pure_name_from_path(input_new_tts_final_path)
    file_name_item_list = file_name.strip().split("_")
    parent_new_name = file_name_item_list[0] + "_" + file_name_item_list[1]
    print("file_name_item_list: ",file_name_item_list)
    if file_name_item_list[2].startswith("VAD"):
        index = int(file_name_item_list[2][3:])  # 消掉VAD
    else:
        index = -1
    second = int(file_name_item_list[3])
    return parent_new_name, index, second


def get_true_wav_path_by_index(output_dir, parent_new_name, index, millisecond_num):
    """
    通过次序i，和音频的目录和大音频的名字，得到真实小音频的路径
    外界传来的millisecond_num只是用来判断
    :param output_dir:
    :param parent_new_name:
    :param index:
    :param millisecond_num:
    :return:
    """
    # 郭钊版:/root/path/282492425329_CPKwq_86_6299.wav
    # file_name = parent_new_name + "_" + str(index) + "_" + str(millisecond_num) + ".wav"
    file_name_rough = parent_new_name + "_" + str(index) + "_" + "*" + ".wav"
    true_wav_path_list = glob.glob(os.path.join(output_dir, file_name_rough))
    true_wav_path = true_wav_path_list[0] if len(true_wav_path_list) > 0 else None
    if true_wav_path is None:
        utils_file.logging_print(
            f"fix_path(): true_wav_path is None, parent_new_name={parent_new_name}, index={index}, millisecond_num={millisecond_num}"
        )
        return None
    _, _, duration = handle_path_old(true_wav_path)
    duration = int(duration / 1000)
    if abs(duration - millisecond_num) < 1.1:
        return true_wav_path
    else:
        utils_file.logging_print(
            f"fix_path(): abs(duration - millisecond_num) > 1={abs(duration - millisecond_num)}, 采用真实的音频地址")
        return true_wav_path


def do_handle_wav(wav_new_path, output_dir="./"):
    """"""
    # 首先得到小段音频对应长短音频的名字。282492425329_CPKwq_86_6299.txt
    little_new_name = utils_file.get_file_pure_name_from_path(wav_new_path)
    temp_name_apart = little_new_name.strip().split("_")
    little_new_name = temp_name_apart[0] + "_" + temp_name_apart[1]
    the_old_wav_path = NEW2OLD_TABLE.get(little_new_name, None)
    if the_old_wav_path is None:
        utils_file.logging_print(
            f"do_handle_wav(): the_old_wav_path is None, little_new_name={little_new_name}"
        )
        return False
    if not os.path.exists(the_old_wav_path):
        utils_file.logging_print(
            f"do_handle_wav(): the_old_wav_path is not exist, little_new_name={little_new_name}"
        )
        return False
    long_old_clean_wav_dir = os.path.join(output_dir, "temp_long_old_clean_wav")
    utils_file.makedir_sil(long_old_clean_wav_dir)
    long_old_clean_path = os.path.join(long_old_clean_wav_dir, little_new_name + ".wav")
    if not os.path.exists(long_old_clean_path):
        # 先规范化音频
        clean_wav(the_old_wav_path, long_old_clean_path)
        # 开始切割音频
        vad_info_txt_path = VAD_INFO_TABLE.get(little_new_name, None)
        if vad_info_txt_path is None:
            utils_file.logging_print(
                f"do_handle_wav(): vad_info_txt_path is None, little_new_name={little_new_name}"
            )
            return False
        final_wav_dir = os.path.join(output_dir, "final_wav")
        utils_file.makedir_sil(final_wav_dir)
        slicing_wav(long_old_clean_path, vad_info_txt_path, final_wav_dir, little_new_name)
    else:
        utils_file.logging_print(
            f"do_handle_wav(): long_old_clean_path is exist, little_new_name={little_new_name}, 跳过该长音频的处理"
        )
    return True


def clean_wav(input_file_path, output_file_path):
    """
    将音频整理成标准格式， 16K采样， 单通道，补齐音频头
    :param input_file_path:
    :param output_file_path:
    :return:
    """
    os.system(f"ffmpeg -i '{input_file_path}' -ac 1 -ar 16000 -vn {output_file_path}")


def little_func4slicing_wav(i, vad_info, input_file_path, output_dir, wav_new_name):
    # print(vad_info)
    start_time = vad_info[0]
    end_time = vad_info[1]
    duration = int(end_time) - int(start_time)
    start_sample = int(start_time) * 16
    end_sample = int(end_time) * 16
    output_path = os.path.join(output_dir, f"{wav_new_name}_{i}_{duration}.wav")
    utils_file.do_extract_audio_segment(input_file_path, output_path, start_sample, end_sample)


def slicing_wav(input_file_path, vad_info_txt_path, output_dir, wav_new_name):
    """
    将一个音频,依据时间戳, 切分成若干小音频. 此处可以多线程并行处理
    """
    sorted_list = get_vad_info_list(vad_info_txt_path)
    thread_num = THREAD_NUM if len(sorted_list) > THREAD_NUM else len(sorted_list)
    runner = utils_file.GxlFixedThreadPool(thread_num)
    for i, vad_info in enumerate(sorted_list):
        # i = i + 1
        runner.add_thread(little_func4slicing_wav, [i, vad_info, input_file_path, output_dir, wav_new_name])
    runner.start()


def do_get_vad_scp_file(input_dir, output_dir='./'):
    """
    tts处理流程中会对每一个音频生成一个vad_info的txt文件, 我们得到一个key vad_info.txt的字典
    :param input_dir:
    :return:
    """
    vad_res_scp = utils_file.get_scp_for_wav_dir(input_dir, suffix="txt")
    utils_file.write_dict_to_scp(vad_res_scp, os.path.join(output_dir, "vad_res.scp"))


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


def do_get_final_jsonl(input_scp_path, output_dir='./'):
    """
    多线程实现
    :param input_scp_path:
    :param output_dir:
    :return:
    """
    final_dict = utils_file.load_dict_from_scp(input_scp_path)
    thread_num = 6  # 暂时不支持多线程， 多线程没法保证不同时切割同一条长音频。
    runner = utils_file.GxlDynamicThreadPool()
    little_dict_list = utils_file.do_split_dict(final_dict, thread_num)
    # lock4write = threading.Lock()
    asr_final_list_path = os.path.join(output_dir, "asr_final_list.txt")
    if os.path.exists(asr_final_list_path):
        # 此处必须， 后面逻辑是在文本末尾累加写入，一旦程序中断重新运行，如果不删原来的，
        # 就会出问题， 文件写入内容本身不占用太多时间，时间主要是在于切分以您，此处已做了
        # 防中断处理。可放心随意重新运行程序， 而不会重复工作。
        os.remove(asr_final_list_path)
    for i, little_final_dict in enumerate(little_dict_list):
        # 此处的多线程不太长成熟， 一旦多个线程同时处理同一个长音频的小音频，就会同时对该长音频的原始音频做再切割，
        # 而我们是只需要切一次， 不是多次。在切音频时仍然可以多线程， 此处无多线程也无所谓。
        runner.add_task(little_func4get_final_jsonl,
                        [i, little_final_dict, asr_final_list_path, "None", output_dir])
    runner.start()
    utils_file.logging_print("do_get_final_jsonl(): 结束")
    utils_file.logging_print('开始整合')
    asr_final_list_path_format = asr_final_list_path.replace(".txt", "")
    asr_final_path_list = glob.glob(f"{asr_final_list_path_format}*")
    res_list = []
    utils_file.print_list(asr_final_path_list)
    for asr_final_path in asr_final_path_list:
        little_dict_list = utils_file.load_dict_list_from_jsonl(asr_final_path)
        res_list.extend(little_dict_list)
    utils_file.write_dict_list_to_jsonl(res_list, asr_final_list_path)
    utils_file.logging_print('整合结束')


def little_func4get_final_jsonl(i, final_dict, asr_final_jsonl_path, lock4write, output_dir):
    asr_final_jsonl_path = asr_final_jsonl_path.replace(".txt", f"_{i}.txt")
    if os.path.exists(asr_final_jsonl_path):
        # 此处必须， 后面逻辑是在文本末尾累加写入，一旦程序中断重新运行，如果不删原来的，
        # 就会出问题， 文件写入内容本身不占用太多时间，时间主要是在于切分以您，此处已做了
        # 防中断处理。可放心随意重新运行程序， 而不会重复工作。
        os.remove(asr_final_jsonl_path)
    for key, value in tqdm.tqdm(final_dict.items(), total=len(final_dict)):
        key_list = key.strip().split(r'_')
        if len(key_list) != 4:
            print(f"len(key_list) != 4, key:{key} value:{value}")
            continue
        value_list = value.strip().split(r' ')
        if len(value_list) != 2:
            print(f"key:{key} value:{value}")
        wav_path = value_list[0]
        txt_path = value_list[1]
        txt = utils_file.load_first_row_clean(txt_path)
        if len(txt) == 0:
            print(f"txt_path文件内部无内容， key:{key} wav_path:{wav_path} txt_path:{txt_path}")
            continue
        txt = txt.strip().split("\t")[1]
        res_handle_wav = do_handle_wav(wav_path, output_dir)
        if not res_handle_wav:
            continue
        parent_new_filename, index, duration = handle_path_old(wav_path)
        if index == -1:
            continue
        asr_final_wav_dir = os.path.join(output_dir, "final_wav")
        wav_path = get_true_wav_path_by_index(asr_final_wav_dir, parent_new_filename, index, duration)
        if wav_path is None or not os.path.exists(wav_path):
            continue
        dict_i = dict(key=key, wav=wav_path, txt=txt)
        # with lock4write:
        utils_file.logging_print(f'开始写入文件:{asr_final_jsonl_path}')
        utils_file.write_single_dict_to_jsonl(dict_i, asr_final_jsonl_path)
        utils_file.logging_print(f'结束写入文件:{asr_final_jsonl_path}')
    utils_file.logging_print("little_func4get_final_jsonl(): 结束")


def main(old2new_dir, input_vad_info_dir, final_scp_path, output_dir):
    """"""
    utils_file.makedir_sil(output_dir)
    do_get_vad_scp_file(input_vad_info_dir, output_dir)
    do_get_old2new_scp_file(old2new_dir, output_dir)
    NEW2OLD_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "old2new.scp")))
    VAD_INFO_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "./vad_res.scp")))
    do_get_final_jsonl(final_scp_path,
                       output_dir=output_dir)


def split_source(input_tts_scp_path, output_dir, split_ratio=None):
    """将一个scp文件分成若干个小文件"""
    if split_ratio is None:
        split_ratio = [0.45, 0.55]
    all_dict = utils_file.load_dict_from_scp(input_tts_scp_path)
    total_ratio = sum(split_ratio)
    if total_ratio != 1.0:
        raise ValueError("Ratios should add up to 1.0")
    start = 0
    for i, ratio in enumerate(split_ratio):
        end = start + int(len(all_dict) * ratio)
        dict_i = utils_file.get_subdict(all_dict, start, end)
        start = end
        utils_file.write_dict_to_scp(dict_i, os.path.join(output_dir, f"final_scp_part_{i}.scp"))


def get_little_final(input_final_scp_path, output_dir):
    """从非常大的tts_final_scp中取出一小点，组成一个测试用的小的tts_final_scp文件"""
    all_dict = utils_file.load_dict_from_scp(input_final_scp_path)
    little_dict = utils_file.get_random_subdict(all_dict, 24)
    utils_file.write_dict_to_scp(little_dict, os.path.join(output_dir, f"final_scp_little.scp"))


def fix_old2new_file():
    """
    将2T的old2new.scp进行修复
    :return:
    """
    old_scp_path = "/home/node39_data2/zhguo/data_hot_topic/list/init_lists/old2new.scp"
    old_dict = utils_file.load_dict_from_scp(old_scp_path)
    new_dict = {}
    for key, value in tqdm.tqdm(old_dict.items(), total=len(old_dict)):
        value = value.replace("/home/work_nfs6/xlgeng/data/pachong_ximalaya_2/wav_files/",
                              "/home/node36_data/ximalaya_2T/")
        new_dict[key] = value
    new_scp_path = "/home/node36_data/xlgeng/asr_data_from_pachong/xmly2T_hot_point_old2new.scp"
    utils_file.write_dict_to_scp(new_dict, new_scp_path)

    old_scp_path = "/home/backup_nfs5/zhguo/audio_drama/list/init_lists/old2new.scp"
    old_dict = utils_file.load_dict_from_scp(old_scp_path)
    new_dict = {}
    for key, value in tqdm.tqdm(old_dict.items(), total=len(old_dict)):
        value = value.replace("/home/work_nfs6/xlgeng/data/pachong_ximalaya_2/wav_files/",
                              "/home/node36_data/ximalaya_2T/")
        new_dict[key] = value
    new_scp_path = "/home/node36_data/xlgeng/asr_data_from_pachong/xmly2T_radio_drama_old2new.scp"
    utils_file.write_dict_to_scp(new_dict, new_scp_path)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tts_final_scp_path", type=str)
    parser.add_argument("--asr_final_scp_path", type=str)
    parser.add_argument("--do_split", type=bool, default=False)
    args = parser.parse_args()
    return args


def pre_do(final_tts_scp_path: str, output_dir: str):
    utils_file.logging_print('首先切分tts_final.scp,切分为6个')
    # output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/ximalaya_lishi_10T"
    # final_tts_scp_path = "/home/work_nfs8/lhma/double_check_lists/zhguo_lishi_part0_3700h.scp"
    final_tts_dict = utils_file.load_dict_from_scp(final_tts_scp_path)
    tts_dict_list = utils_file.do_split_dict(final_tts_dict, 6)
    for i, tts_dict in enumerate(tts_dict_list):
        i = i + 1
        utils_file.write_dict_to_scp(tts_dict, os.path.join(output_dir, f"tts_final_{i}.scp"))


def do_handle_wav_2(long_wav_new_name, output_dir="./"):
    """"""
    global NEW2OLD_TABLE, VAD_INFO_TABLE
    the_old_wav_path = NEW2OLD_TABLE.get(long_wav_new_name, None)
    if the_old_wav_path is None:
        utils_file.logging_print(
            f"do_handle_wav(): the_old_wav_path is None, long_wav_new_name={long_wav_new_name}"
        )
        return False
    if not os.path.exists(the_old_wav_path):
        utils_file.logging_print(
            f"do_handle_wav(): the_old_wav_path is not exist, long_wav_new_name={long_wav_new_name}"
        )
        return False
    long_old_clean_wav_dir = os.path.join(output_dir, "temp_long_old_clean_wav")
    utils_file.makedir_sil(long_old_clean_wav_dir)
    long_clean_path = os.path.join(long_old_clean_wav_dir, long_wav_new_name + ".wav")
    if not os.path.exists(long_clean_path):
        # 先规范化音频
        clean_wav(the_old_wav_path, long_clean_path)
        # 开始切割音频
        vad_info_txt_path = VAD_INFO_TABLE.get(long_wav_new_name, None)
        if vad_info_txt_path is None:
            utils_file.logging_print(
                f"do_handle_wav(): vad_info_txt_path is None, long_wav_new_name={long_wav_new_name}"
            )
            return False
        final_wav_dir = os.path.join(output_dir, "final_wav")
        utils_file.makedir_sil(final_wav_dir)
        slicing_wav(long_clean_path, vad_info_txt_path, final_wav_dir, long_wav_new_name)
    else:
        utils_file.logging_print(
            f"do_handle_wav(): long_old_clean_path is exist, long_wav_new_name={long_wav_new_name}, 跳过该长音频的处理"
        )
    return True


def solution_2(output_dir, old2new_dir, input_vad_info_dir):
    # utils_file.logging_print('首先从命令行中拿到要处理的tts_final.scp的子集')
    args = get_args()
    if args.do_split:
        utils_file.logging_print('开始do_split')
        pre_do(final_tts_scp_path, output_dir)
        utils_file.logging_print('do_split完成, 直接return')
        return
    tts_scp_path = os.path.join(output_dir, args.tts_final_scp_path)
    asr_scp_path = os.path.join(output_dir, args.asr_final_scp_path)
    if os.path.exists(asr_scp_path):
        utils_file.logging_print('asr_scp_path已经存在，直接删除')
        os.remove(asr_scp_path)
    utils_file.logging_print('加载vad和old2new的信息')
    utils_file.makedir_sil(output_dir)
    do_get_vad_scp_file(input_vad_info_dir, output_dir)
    do_get_old2new_scp_file(old2new_dir, output_dir)
    NEW2OLD_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "old2new.scp")))
    VAD_INFO_TABLE.update(utils_file.load_dict_from_scp(os.path.join(output_dir, "./vad_res.scp")))
    utils_file.logging_print('获取tts_scp对应的长音频的新名字列表')
    tts_dict = utils_file.load_dict_from_scp(tts_scp_path)
    long_wav_new_names_list = []
    for key in tqdm.tqdm(tts_dict.keys(), total=len(tts_dict)):
        key_list = key.strip().split(r'_')
        if len(key_list) != 4:
            continue
        long_wav_new_name, _, _ = handle_path_old(key, only_name=True)
        long_wav_new_names_list.append(long_wav_new_name)
    long_wav_new_names_list = list(set(long_wav_new_names_list))
    utils_file.logging_print("开始逐条长音频得处理")
    for long_wav_new_name in tqdm.tqdm(long_wav_new_names_list, total=len(long_wav_new_names_list)):
        do_handle_wav(long_wav_new_name, output_dir)
    utils_file.logging_print("开始逐tts_final条映射到asr_final")
    for key, value in tqdm.tqdm(tts_dict.items(), total=len(tts_dict)):
        key_list = key.strip().split(r'_')
        if len(key_list) != 4:
            continue
        value_list = value.strip().split(r' ')
        if len(value_list) != 2:
            utils_file.logging_print(f"key:{key} value:{value},len(value_list) != 2")
        wav_path = value_list[0]
        txt_path = value_list[1]
        txt = utils_file.load_first_row_clean(txt_path)
        if len(txt) == 0:
            utils_file.logging_print(f"txt_path文件内部无内容， key:{key} wav_path:{wav_path} txt_path:{txt_path}")
            continue
        txt = txt.strip().split("\t")[1]
        parent_new_filename, index, duration = handle_path_old(wav_path)
        if index == -1:
            continue
        asr_final_wav_dir = os.path.join(output_dir, "final_wav")
        wav_path = get_true_wav_path_by_index(asr_final_wav_dir, parent_new_filename, index, duration)
        if wav_path is None or not os.path.exists(wav_path):
            continue
        dict_i = dict(key=key, wav=wav_path, txt=txt)
        utils_file.write_single_dict_to_jsonl(dict_i, asr_scp_path)
    utils_file.logging_print("处理完毕")


def get_new_key(key):
    """"""
    key_list = key.split('_')
    if len(key_list) != 4:
        utils_file.logging_print(f'key_list长度不为4，key:{key}')
        return "error"
    if key_list[2].startswith('VAD'):
        key_list[2] = key_list[2][3:]
    return '_'.join(key_list[0:3])


def final_handle():
    """"""
    output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/ximalaya_redian_2T"
    final_tts_scp_path = "/home/work_nfs8/lhma/double_check_lists/zhguo_xmly2T_redian_950h.scp"
    tts_dict = utils_file.load_dict_from_scp(final_tts_scp_path)
    utils_file.logging_print('开始得到all.text')
    text_dict = {}
    for key, value in tqdm.tqdm(tts_dict.items(), total=len(tts_dict)):
        value_list = value.strip().split(r' ')
        if len(value_list) != 2:
            utils_file.logging_print(f"key:{key} value:{value},len(value_list) != 2")
        wav_path = value_list[0]
        txt_path = value_list[1]
        if not os.path.exists(txt_path):
            utils_file.logging_print(f"txt_path文件不存在， key:{key} wav_path:{wav_path} txt_path:{txt_path}")
            continue
        txt = utils_file.load_first_row_clean(txt_path)
        if len(txt) == 0:
            utils_file.logging_print(f"txt_path文件内部无内容， key:{key} wav_path:{wav_path} txt_path:{txt_path}")
            continue
        txt = txt.strip().split("\t")[1]
        key = get_new_key(key)
        if key == "error":
            continue
        text_dict[key] = txt
    utils_file.write_dict_to_scp(text_dict, os.path.join(output_dir, "all.text"))

    utils_file.logging_print('开始得到all_wav.scp')
    wav_dict = utils_file.get_scp_for_wav_dir(os.path.join(output_dir, "final_wav"))
    wav_dict_with_new_key = {}
    utils_file.logging_print('为wav_dcit更换新的key')
    for key, value in tqdm.tqdm(wav_dict.items(), total=len(wav_dict)):
        new_key = get_new_key(key)
        if new_key == "error":
            continue
        wav_dict_with_new_key[new_key] = value
    utils_file.write_dict_to_scp(wav_dict_with_new_key, os.path.join(output_dir, "all_wav.scp"))
    utils_file.do_convert_wav_text_scp_to_jsonl(os.path.join(output_dir, "all_wav.scp"), os.path.join(output_dir, "all.text"), os.path.join(output_dir, "all.list"))


def copy_file_to_nfs():
    """"""
    source_list_path = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/ximalaya_redian_2T/all.list"
    dict_list = utils_file.load_dict_list_from_jsonl(source_list_path)
    target_dir = "/home/work_nfs14/xlgeng/asr_data_from_pachong/ximalaya_redian_2T"
    utils_file.makedir_sil(target_dir)
    runner = utils_file.GxlFixedThreadPool(50)
    utils_file.logging_print('得到wav path list')
    wav_path_list = []
    for item in tqdm.tqdm(dict_list):
        wav_path = item['wav']
        wav_path_list.append(wav_path)
    runner.map(utils_file.copy_file2, wav_path_list, {"target_dir": target_dir})
    runner.start()

if __name__ == '__main__':
    # output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/xmly10T-history-0/mcshao"
    # # output_dir ='./'
    # input_vad_info_dir = "/home/node36_data/zhguo/history_10T/part_0/vad/txts"
    # # 表格里写的如果不是dir,而是成品scp文件， 就把scp文件的路径传入即可
    # old2new_dir = "/home/node36_data/zhguo/history_10T/part_0/list/init_lists/"
    # final_tts_scp_path = "/home/work_nfs10/mcshao/TTS-ASR-PROCESS/Splited_source/aa/final_scp_part_0.scp"
    # main(old2new_dir, input_vad_info_dir, final_tts_scp_path, output_dir)
    # # split_source(final_tts_scp_path, './')
    # # get_little_final(final_tts_scp_path, './')
    # output_dir = './'
    output_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/ximalaya_redian_2T"

    # input_vad_info_dir = "/home/node36_data/zhguo/history_10T/part_0/vad/txts"
    input_vad_info_dir = "/home/node39_data2/zhguo/data_hot_topic/lists/vad_result"
    # input_vad_info_dir = "/home/node36_data/zhguo/audio_drama/vad/txts"

    # 表格里写的如果不是dir,而是成品scp文件， 就把scp文件的路径传入即可
    # old2new_dir = "/home/node36_data/zhguo/history_10T/part_0/list/init_lists"
    old2new_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/xmly2T_hot_point_old2new.scp"
    # old2new_dir = "/home/node36_data/xlgeng/asr_data_from_pachong/xmly2T_radio_drama_old2new.scp"

    # final_tts_scp_path = "/home/work_nfs8/lhma/double_check_lists/zhguo_lishi_part0_3700h.scp"
    final_tts_scp_path = "/home/work_nfs8/lhma/double_check_lists/zhguo_xmly2T_redian_950h.scp"
    # final_tts_scp_path = "/home/work_nfs8/lhma/double_check_lists/zhguo_xmly2T_guangbojv_1550h.scp"

    # get_little_final(final_tts_scp_path, './')
    # final_tts_scp_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/handle_tts_data_for_asr/final_scp_little.scp"
    # main(old2new_dir, input_vad_info_dir, final_tts_scp_path, output_dir)
    # solution_2(output_dir, old2new_dir, input_vad_info_dir)
    copy_file_to_nfs()
