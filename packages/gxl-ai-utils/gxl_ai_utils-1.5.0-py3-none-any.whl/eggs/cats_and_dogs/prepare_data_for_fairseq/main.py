import glob
import os
import random

from tqdm import tqdm

from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool

from gxl_ai_utils.utils import utils_file, utils_data

base_path = "/home/work_nfs8/xlgeng/new_workspace/fairseq-main/examples/hubert/data_list"


def prepare_data():
    """
    将数据集转换为fairseq需要的格式
    Returns:

    """
    scp_path_list = utils_file.load_list_file_clean(
        "/home/work_nfs8/xlgeng/new_workspace/fairseq-main/examples/hubert/data_list/scp_path.txt")
    utils_file.print_list(scp_path_list)
    res_list = []
    for scp_path in scp_path_list:
        """"""
        utils_file.logging_print('开始处理: scp_path: {}'.format(scp_path))
        if not os.path.exists(scp_path):
            utils_file.logging_print("warning: scp_path not exists: {}".format(scp_path))
            continue
        dataset_name = (scp_path.split("/")[-2]).lower()
        wav_dict = utils_file.load_dict_from_scp(scp_path)
        utils_file.logging_print(f"dataset_name: {dataset_name}, lens: {len(wav_dict)}")
        # runner.add_thread(little_fun, [wav_dict, res_dict, dataset_name])
        res_list.extend(list(wav_dict.values()))

    res_file_path = "./added_data_gxl.tsv"
    random.shuffle(res_list)

    utils_file.logging_print('开始计算每个音频的采样点')
    num_thread = 100
    res_dict = {}

    def little_fun(little_list, res_dict):
        """"""
        for item in tqdm(little_list, total=len(little_list)):
            res_dict[item] = utils_data.get_sample_count(item)[0]

    res_list_list = utils_file.do_split_list(res_list, num_thread)
    thread_runner = GxlDynamicThreadPool()
    for res_list_i in res_list_list:
        thread_runner.add_thread(little_fun, [res_list_i, res_dict])
    thread_runner.start()

    utils_file.logging_print('开始写入: res_file_path: {}'.format(res_file_path))
    with open(res_file_path, "w") as f:
        f.write("/\n")
        for key, value in res_dict.items():
            f.write("{}\t{}\n".format(key, value))


def get_tsv(input_list_path, output_tsv_path, thread_num=100):
    """"""
    if isinstance(input_list_path, str):
        wav_list = utils_file.load_list_file_clean(input_list_path)
    elif isinstance(input_list_path, list):
        wav_list = input_list_path
    utils_file.logging_print('接着开始计算每个音频的采样点')
    num_thread = thread_num
    utils_file.logging_print('使用线程数: {}'.format(num_thread))
    res_dict = {}

    def little_fun(little_list, res_dict):
        """"""
        for item in tqdm(little_list, total=len(little_list)):
            res_dict[item] = utils_data.get_sample_count(item)[0]

    res_list_list = utils_file.do_split_list(wav_list, num_thread)
    thread_runner = GxlDynamicThreadPool()
    for res_list_i in res_list_list:
        thread_runner.add_thread(little_fun, [res_list_i, res_dict])
    thread_runner.start()

    utils_file.logging_print('开始写入: output_tsv_path: {}'.format(output_tsv_path))
    with open(output_tsv_path, "w") as f:
        f.write("/\n")
        for key, value in res_dict.items():
            f.write("{}\t{}\n".format(key, value))


def prepare_data_2():
    """得到全量数据的tsv和ltr"""
    data_dir_list = utils_file.load_list_file_clean(
        "./scp_path.txt")
    utils_file.logging_print('共有如下数据目录')
    utils_file.print_list(data_dir_list)
    utils_file.logging_print("对于每个数据目录，我们判断他们text wav.scp是否存在")
    for data_dir_i in data_dir_list:
        if not os.path.exists(data_dir_i):
            utils_file.logging_print("error：不存在: {}".format(data_dir_i))
            return
        wav_scp_path = os.path.join(data_dir_i, "wav.scp")
        text_path = os.path.join(data_dir_i, "text")
        if not os.path.exists(wav_scp_path):
            utils_file.logging_print("error：不存在: {}".format(wav_scp_path))
            return
        if not os.path.exists(text_path):
            utils_file.logging_print("error：不存在: {}".format(text_path))
            return
        with open(wav_scp_path, 'r') as file:
            line_count = sum(1 for line in file)
            utils_file.logging_print(f'{data_dir_i}的wav.scp行数为: {line_count}')
        with open(text_path, 'r') as file:
            line_count = sum(1 for line in file)
            utils_file.logging_print(f'{data_dir_i}的text行数为: {line_count}')

    utils_file.logging_print('判断通过')
    # utils_file.logging_print('开始处理数据, 首先合并所有的text和wav.scp')
    # big_text_dict = {}
    utils_file.logging_print('首先合并所有wav path')
    res_list = []
    for data_dir_i in data_dir_list:
        """"""
        wav_scp_path_i = os.path.join(data_dir_i, "wav.scp")
        wav_dict_i = utils_file.load_dict_from_scp(wav_scp_path_i)
        res_list.extend(list(wav_dict_i.values()))
    # res_file_path = "./added_data_and_part_wenetspeech.tsv"
    random.shuffle(res_list)
    utils_file.logging_print('开始得到10个wav_list_file，放到是个不同的节点上同时运行')
    res_list_list = utils_file.do_split_list(res_list, 10)
    for i, res_list_i in enumerate(res_list_list):
        res_file_path_i = f"./added_data_and_part_wenetspeech_{i}.list"
        utils_file.write_list_to_file(res_list_i, res_file_path_i)


def do_make_ltr_from_tsv_and_wav_text_scp(wav_dict_path, text_dict_path, tsv_path, output_tsv_path, output_ltr_path):
    """"""
    wav_dict = dict()
    text_dict = dict()
    tsv_list = list()
    if isinstance(wav_dict_path, str):
        wav_dict = utils_file.load_dict_from_scp(wav_dict_path)
    elif isinstance(wav_dict_path, dict):
        wav_dict = wav_dict_path
    if isinstance(text_dict_path, str):
        text_dict = utils_file.load_dict_from_scp(text_dict_path)
    elif isinstance(text_dict_path, dict):
        text_dict = text_dict_path
    if isinstance(tsv_path, str):
        tsv_list = utils_file.load_list_file_clean(tsv_path)
    elif isinstance(tsv_path, list):
        tsv_list = tsv_path
    if tsv_list[0] == "/":
        tsv_list = tsv_list[1:]
    all_info_dict = {}
    inverse_wav_dict = {v: k for k, v in wav_dict.items()}
    for tsv_i in tqdm(tsv_list, total=len(tsv_list)):
        """"""
        wav_path, sample_num = tsv_i.split()
        wav_key = inverse_wav_dict.get(wav_path, None)
        if wav_key is None:
            utils_file.logging_print(f'warning: {wav_path} not in wav_dict')
            continue
        text = text_dict.get(wav_key, None)
        if text is None:
            utils_file.logging_print(f'warning: {wav_key} not in text_dict')
            continue
        text = text.strip().replace(" ", "")
        text = " ".join(text)
        all_info_dict[tsv_i] = text
    utils_file.logging_print(f'all_info_dict: {len(all_info_dict)}')
    tsv_list_new = list(all_info_dict.keys())
    ltr_list_new = [all_info_dict[tsv_i] for tsv_i in tsv_list_new]
    tsv_list_new.insert(0, "/")
    utils_file.write_list_to_file(tsv_list_new, output_tsv_path)
    utils_file.write_list_to_file(ltr_list_new, output_ltr_path)


def get_ltr_for_added():
    """"""
    utils_file.logging_print('开始得到ltr文件')
    utils_file.logging_print('首先合并所有的小tsv')
    tsv_i_path_list = glob.glob("./added_data_and_part_wenetspeech_*.tsv")
    utils_file.print_list(tsv_i_path_list)
    all_info_list = []
    for tsv_i_path in tsv_i_path_list:
        """"""
        utils_file.logging_print('开始处理: tsv_i_path: {}'.format(tsv_i_path))
        with open(tsv_i_path, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            if lines[0] == "/":
                lines = lines[1:]
            all_info_list.extend(lines)
    random.shuffle(all_info_list)
    all_info_list.insert(0, "/")
    utils_file.write_list_to_file(all_info_list, "./added_data_and_part_wenetspeech.tsv")
    utils_file.logging_print('得到合并的tsv完成')

    utils_file.logging_print('开始得到总的wav_dict和text_dict')
    data_dir_list = utils_file.load_list_file_clean(
        "./scp_path.txt")
    wav_dict = {}
    text_dict = {}
    for data_dir_i in data_dir_list:
        if not os.path.exists(data_dir_i):
            utils_file.logging_print("error：不存在: {}".format(data_dir_i))
            return
        wav_scp_path = os.path.join(data_dir_i, "wav.scp")
        text_path = os.path.join(data_dir_i, "text")
        if not os.path.exists(wav_scp_path):
            utils_file.logging_print("error：不存在: {}".format(wav_scp_path))
            return
        if not os.path.exists(text_path):
            utils_file.logging_print("error：不存在: {}".format(text_path))
            return
        with open(wav_scp_path, 'r') as file:
            first_line = file.readline()
            first_wav_path = first_line.split()[1]
            if not os.path.exists(first_wav_path):
                utils_file.logging_print("error：音频位置不存在: {}".format(first_wav_path))
                return
        with open(wav_scp_path, 'r') as file:
            line_count = sum(1 for line in file)
            utils_file.logging_print(f'{data_dir_i}的wav.scp行数为: {line_count}')
        with open(text_path, 'r') as file:
            line_count = sum(1 for line in file)
            utils_file.logging_print(f'{data_dir_i}的text行数为: {line_count}')
        wav_dict_i = utils_file.load_dict_from_scp(wav_scp_path)
        text_dict_i = utils_file.load_dict_from_scp(text_path)
        wav_dict.update(wav_dict_i)
        text_dict.update(text_dict_i)

    utils_file.logging_print('判断通过')
    utils_file.logging_print(f"得到了wav_dict:{len(wav_dict)}, text_dict:{len(text_dict)}")
    do_make_ltr_from_tsv_and_wav_text_scp(wav_dict, text_dict, "./added_data_and_part_wenetspeech.tsv",
                                          "./added_data_and_part_wenetspeech_final.tsv",
                                          "./added_data_and_part_wenetspeech.ltr")

def get_ltr_for_trainl():
    """"""
    input_tsv = '/home/work_nfs9/lhli/dialect/data/wenetspeech/wenetspeech.tsv'
    wav_dict_path = "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/train_l/wav.scp"
    text_dict_path = "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/train_l/text"
    wav_dict = utils_file.load_dict_from_scp(wav_dict_path)
    text_dict = utils_file.load_dict_from_scp(text_dict_path)
    wav_dict = {k: v.replace('/home/work_nfs6/disk2/ASR_data/wav/train_l', '/home/38_data/ASR_data/wav/train_l') for
                k, v in tqdm(wav_dict.items(), total=len(wav_dict))}

    do_make_ltr_from_tsv_and_wav_text_scp(wav_dict, text_dict, input_tsv, "./trainl_final.tsv", "./trainl.ltr")


def add_2_tsv_and_ltr(i_tsv_path, i_ltr_path, j_tsv_path, j_ltr_path):
    i_tsv_list = utils_file.load_list_file_clean(i_tsv_path)
    if i_tsv_list[0] == "/":
        i_tsv_list = i_tsv_list[1:]
    i_ltr_list = utils_file.load_list_file_clean(i_ltr_path)

    j_tsv_list = utils_file.load_list_file_clean(j_tsv_path)
    if j_tsv_list[0] == "/":
        j_tsv_list = j_tsv_list[1:]

    j_ltr_list = utils_file.load_list_file_clean(j_ltr_path)
    tsv_list = i_tsv_list + j_tsv_list
    ltr_list = i_ltr_list + j_ltr_list
    if len(tsv_list) != len(ltr_list):
        utils_file.logging_print(f"error: len(tsv_list):{len(tsv_list)} != len(ltr_list):{len(ltr_list)}")
        return
    index_list = list(range(len(tsv_list)))
    random.shuffle(index_list)
    tsv_list = [tsv_list[i] for i in index_list]
    ltr_list = [ltr_list[i] for i in index_list]
    tsv_list.insert(0, "/")
    utils_file.write_list_to_file(tsv_list, "./final.tsv")
    utils_file.write_list_to_file(ltr_list, "./final.ltr")


def get_tsv_ltr_from_wav_text(wav_dict_path, text_dict_path, tsv_path, ltr_path):
    """"""
    wav_dict = utils_file.load_dict_from_scp(wav_dict_path)
    text_dict = utils_file.load_dict_from_scp(text_dict_path)
    wav_path_list = list(wav_dict.values())
    get_tsv(wav_path_list, tsv_path, 100)
    do_make_ltr_from_tsv_and_wav_text_scp(wav_dict, text_dict, tsv_path, tsv_path, ltr_path)



if __name__ == '__main__':
    # get_ltr_for_trainl()
    # add_2_tsv_and_ltr("./trainl_final.tsv",
    #                   "./trainl.ltr",
    #                   "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_fairseq/added_data_and_part_wenetspeech_final.tsv",
    #                   "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_fairseq/added_data_and_part_wenetspeech.ltr")
    # path_list = utils_file.load_list_file_clean('./final.tsv')
    # path_list.insert(0, '/')
    # utils_file.write_list_to_file(path_list, './final.tsv')
    get_tsv_ltr_from_wav_text("/home/backup_nfs2/nfs1_data/data_aishell/transcript/dev/wav.scp","/home/backup_nfs2/nfs1_data/data_aishell/transcript/dev/text", "./dev.tsv", "./dev.ltr")
    # i = 0
    # input_list_path = f"./added_data_and_part_wenetspeech_{i}.list"
    # input_list = utils_file.load_list_file_clean(input_list_path)
    # input_list_list = utils_file.do_split_list(input_list, 2)
    # for i, input_list_i in enumerate(input_list_list):
    #     utils_file.write_list_to_file(input_list_i, f"./added_data_and_part_wenetspeech_2_{i}.list")
    # input_list_path = f"./added_data_and_part_wenetspeech_2_{i}.list"
    # output_tsv_path = f"./added_data_and_part_wenetspeech_2_{i}.tsv"
    # get_tsv(input_list_path, output_tsv_path, thread_num=100)
