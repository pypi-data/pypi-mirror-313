import glob
import os
import random
import shutil
import sys

import tqdm

sys.path.insert(0, '/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils')
from gxl_ai_utils.utils import utils_file


def do_get_all_shard_list_for_data4w():
    """"""
    input_dir = '/home/41_data/data4w/shard_1'
    output_dir = '/home/work_nfs6/xlgeng/gxl_data/asr_data_shard_list'
    utils_file.makedir_sil(output_dir)
    # 得到一级子目录
    all_child_dir = os.listdir(input_dir)
    print(all_child_dir)
    for child_dir in tqdm.tqdm(all_child_dir, total=len(all_child_dir)):
        now_dir = utils_file.join_path(input_dir, child_dir)
        tar_list = glob.glob(os.path.join(now_dir, '*.tar'))
        output_path = utils_file.join_path(output_dir, child_dir, 'shard_list.txt')
        utils_file.write_list_to_file(tar_list, output_path)


def do_get_all_raw_list_for_data4w():
    """"""
    input_dir = '/home/work_nfs5_ssd/hfxue/gxl_data/data4w/source_1'
    output_dir = '/home/work_nfs6/xlgeng/gxl_data/asr_data_raw_list'
    utils_file.makedir_sil(output_dir)
    # 得到一级子目录
    all_child_dir = os.listdir(input_dir)
    print(all_child_dir)
    for child_dir in tqdm.tqdm(all_child_dir, total=len(all_child_dir)):
        now_dir = utils_file.join_path(input_dir, child_dir)
        print(now_dir)
        wav_scp_path = os.path.join(now_dir, 'wav.scp')
        text_path = os.path.join(now_dir, 'text')
        if os.path.exists(wav_scp_path) and os.path.exists(text_path):
            output_path = utils_file.join_path(output_dir, child_dir, 'gxl_data.list')
            utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_path, text_path, output_path)
        else:
            print(f'{wav_scp_path} or {text_path} do not exist')


def cut_train_test():
    input_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/gxl_data/asr_data_shard/shard.list"
    all_list = utils_file.load_list_file_clean(input_path)
    train_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/gxl_data/asr_data_shard/train.list"
    test_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/gxl_data/asr_data_shard/test.list"
    dev_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/gxl_data/asr_data_shard/dev.list"
    train_list = all_list[:int(len(all_list) * 0.8)]
    test_list = all_list[int(len(all_list) * 0.8):int(len(all_list) * 0.9)]
    dev_list = all_list[int(len(all_list) * 0.9):]
    utils_file.write_list_to_file(train_list, train_path)
    utils_file.write_list_to_file(test_list, test_path)
    utils_file.write_list_to_file(dev_list, dev_path)


def train_aslp_data():
    list_path_1 = "/home/work_nfs6/xlgeng/data/asr_data_shard_list/ASRU700/shard_list.txt"
    list_path_2 = "/home/work_nfs6/xlgeng/data/asr_data_shard_list/LibriSpeech/shard_list.txt"
    list_path_3 = "/home/work_nfs6/xlgeng/data/asr_data_shard_list/AISHELL-2/shard_list.txt"
    # output_dir = '/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/gxl_data/asr_data_shard'
    # utils_file.makedir_sil(output_dir)
    list_1 = utils_file.load_list_file_clean(list_path_1)
    list_2 = glob.glob('/home/local_data/hwang/huawei_cn_en/en/librispeech/*.tar')
    list_3 = utils_file.load_list_file_clean(list_path_3)
    list_1.extend(list_2)
    list_1.extend(list_3)
    random.shuffle(list_1)
    output_dir = "/home/work_nfs7/xlgeng/new_workspace/wenet_gxl_en_cn/examples/aishell/en_cn/data_list"
    utils_file.write_list_to_file(list_1, os.path.join(output_dir, '3000h_data.shards'))
    # utils_file.print_list(utils_file.load_list_file_clean(list_path_1))
    # utils_file.print_list(utils_file.load_list_file_clean(list_path_2))
    # utils_file.print_list(utils_file.load_list_file_clean(list_path_3))


def get_text_for_test():
    input_path = "/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/kd_model/gxl_data/AISHELL-2"
    test_list = utils_file.load_dict_list_from_jsonl(os.path.join(input_path, 'test.list'))
    text_dict = {}
    for item in test_list:
        key = item['key']
        text = item['txt']
        text_dict[key] = text
    utils_file.write_dict_to_scp(text_dict, os.path.join(input_path, 'test.text'))


def get_test_files_for_asru():
    aslp_data = utils_file.AslpDataset()
    info_1 = aslp_data.get_path_info_by_key_or_id(65)
    wav_scp_file = info_1['wav_scp']
    text_file = info_1['text']
    data_list = utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_file, text_file)
    random.shuffle(data_list)
    test_list = data_list[:int(len(data_list) * 0.1)]
    utils_file.write_dict_list_to_jsonl(test_list,
                                        '/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/gxl_data/asru_test.list')
    text_dict = {}
    for item in test_list:
        key = item['key']
        text = item['txt']
        text_dict[key] = text
    utils_file.write_dict_to_scp(text_dict,
                                 '/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/gxl_data/asru_test_text')


def make_all_data_for_en_cn():
    """"""
    dataset_obj = utils_file.AslpDataset()
    dataset_obj.print_all_keys()
    dataset_obj.print_all_data()
    dataset_obj.search('ai')

def from_from_list_get_wav_scp():
    """"""
    dict_list = utils_file.load_dict_list_from_jsonl('/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/data/asru_test.list')
    wav_dict = {}
    for item in dict_list:
        wav_dict[item['key']] = item['wav']
    utils_file.write_dict_to_scp(wav_dict, '/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/data/asru_test.scp')


def clean_data_from_41node():
    """"""
    input_dir = "/home/local_data/data4w/shard_1"
    input_dir = "/home/41_data/data4w/shard_1"
    dataset_names = os.listdir(input_dir)
    print(len(dataset_names))
    # utils_file.print_list(dataset_names)
    dataset_dict = {}
    for dataset_name in dataset_names:
        dataset_dict[dataset_name.lower()] = dataset_name
    # utils_file.print_list(dataset_names)
    cn_1_dataset_names = os.listdir("/home/local_data/hwang/huawei_cn_en/cn")
    cn_1_dict = {}
    for cn_0_dataset_name in cn_1_dataset_names:
        cn_1_dict[cn_0_dataset_name.lower()] = cn_0_dataset_name
    cn_2_dataset_names = os.listdir("/home/local_data/hwang/huawei_cn_en/cn2")
    cn_2_dict = {}
    for cn_0_dataset_name in cn_2_dataset_names:
        cn_2_dict[cn_0_dataset_name.lower()] = cn_0_dataset_name
    en_dataset_names = os.listdir("/home/local_data/hwang/huawei_cn_en/en")
    en_dict = {}
    for en_dataset_name in en_dataset_names:
        en_dict[en_dataset_name.lower()] = en_dataset_name
    mix_dataset_names = os.listdir("/home/local_data/hwang/huawei_cn_en/mix")
    mix_dict = {}
    for mix_dataset_name in mix_dataset_names:
        mix_dict[mix_dataset_name.lower()] = mix_dataset_name

    removed_list = []
    for k, v in dataset_dict.items():
        if k in cn_1_dict:
            item_dict = dict(sn=v, tn=cn_1_dict[k], wh='c1')
            removed_list.append(item_dict)
        elif k in cn_2_dict:
            item_dict = dict(sn=v, tn=cn_2_dict[k], wh='c2')
            removed_list.append(item_dict)
        elif k in en_dict:
            item_dict = dict(sn=v, tn=en_dict[k], wh='e')
            removed_list.append(item_dict)
        elif k in mix_dict:
            item_dict = dict(sn=v, tn=mix_dict[k], wh='mix')
            removed_list.append(item_dict)

    utils_file.print_list(removed_list)

    print('开始删除文件')
    for item in tqdm.tqdm(removed_list, desc='删除文件', total=len(removed_list)):
        input_path = os.path.join(input_dir, item['sn'])
        print(input_path)
        shutil.rmtree(input_path)


def get_tiny_test():
    """"""

def add_other_wenetspeech_to_base_and_all():
    """"""
    trainl_dir = "/home/41_data/data4w/shard_1/train_l"
    trainl_list = glob.glob(os.path.join(trainl_dir, '*.tar'))
    gxl_base_path = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_en_cn/examples/aishell/en_cn/data_list/big_data/gxl_base.txt"
    gxl_base_path_o = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_en_cn/examples/aishell/en_cn/data_list/big_data/gxl_base_2.txt"
    gxl_all_path = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_en_cn/examples/aishell/en_cn/data_list/big_data/gxl_all_2.txt"
    gxl_all_path_o = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_en_cn/examples/aishell/en_cn/data_list/big_data/gxl_all_3.txt"
    utils_file.logging_print('开始结合base')
    base_list = utils_file.load_list_file_clean(gxl_base_path)
    base_list.extend(trainl_list)
    random.shuffle(base_list)
    utils_file.write_list_to_file(base_list, gxl_base_path_o)
    utils_file.logging_print('开始结合all')
    all_list = utils_file.load_list_file_clean(gxl_all_path)
    all_list.extend(trainl_list)
    random.shuffle(all_list)
    utils_file.write_list_to_file(all_list, gxl_all_path_o)

if __name__ == '__main__':
    """"""
    print('哈哈哈')
    add_other_wenetspeech_to_base_and_all()
    # do_get_all_shard_list_for_data4w()
    # do_get_all_raw_list_for_data4w()
    # cut_train_test()
    # get_text_for_test()
    # train_aslp_data()
    # get_test_files_for_asru()
    # make_all_data_for_en_cn()
    # from_from_list_get_wav_scp()
    # clean_data_from_41node()
    # train_aslp_data()