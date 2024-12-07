import os

from gxl_ai_utils.utils import utils_file


def handle():
    """"""
    data_dir = "/home/work_nfs14/xlgeng/asr_data_raw/test_data_raw/Leaderboard/datasets"
    datanames = os.listdir(data_dir)
    utils_file.print_list(datanames)
    for name in datanames:
        temp_data_dir = os.path.join(data_dir, name)
        wav_dict_path = os.path.join(temp_data_dir, 'wav.scp')
        text_dict_path = os.path.join(temp_data_dir, 'trans.txt')
        if not (os.path.exists(wav_dict_path) and os.path.exists(text_dict_path)):
            utils_file.logging_print('找不到对应的文件：', wav_dict_path, text_dict_path)
            if os.path.exists(os.path.join(temp_data_dir, 'metadata.tsv')):
                do_tsv2kaldi(os.path.join(temp_data_dir, 'metadata.tsv'), temp_data_dir)
            continue
        continue
        wav_dict = utils_file.load_dict_from_scp(wav_dict_path)
        text_dict = utils_file.load_dict_from_scp(text_dict_path)
        new_wav_dict = {}
        for key, value in wav_dict.items():
            if not value.startswith(temp_data_dir):
                new_wav_dict[key] = os.path.join(temp_data_dir, value)
            else:
                new_wav_dict[key] = value
        utils_file.write_dict_to_scp(new_wav_dict, wav_dict_path)
        utils_file.write_dict_to_scp(text_dict, os.path.join(temp_data_dir, 'text'))


def do_tsv2kaldi(tsv_path, parent_dir):
    wav_scp_path = os.path.join(parent_dir, 'wav.scp')
    text_scp_path = os.path.join(parent_dir, 'text')
    # 读取tsv文件
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        lines = tsv_file.readlines()
    wav_dict = {}
    text_dict = {}
    # 遍历tsv文件的每一行
    for i, line in enumerate(lines):
        if i == 0:
            continue
        parts = line.strip().split('\t')
        # print(parts)
        id = parts[0]
        wav_path = parts[1]
        text = parts[-1]
        if not wav_path.startswith(parent_dir):
            wav_path = os.path.join(parent_dir, wav_path)
        wav_dict[id] = wav_path
        text_dict[id] = text
    utils_file.write_dict_to_scp(wav_dict, wav_scp_path)
    utils_file.write_dict_to_scp(text_dict, text_scp_path)


def handle_2():
    data_dir = "/home/work_nfs14/xlgeng/asr_data_raw/test_data_raw/Leaderboard/datasets"
    datanames = os.listdir(data_dir)
    for name in datanames:
        temp_data_dir = os.path.join(data_dir, name)
        text_path = os.path.join(temp_data_dir, 'text')
        wav_path = os.path.join(temp_data_dir, 'wav.scp')
        data_list_path = os.path.join(temp_data_dir, 'data.list')
        if os.path.exists(text_path) and os.path.exists(wav_path):
            utils_file.do_convert_wav_text_scp_to_jsonl(wav_path, text_path, data_list_path)

def do_convert(parent_dir):
    temp_data_dir = parent_dir
    text_path = os.path.join(temp_data_dir, 'text')
    wav_path = os.path.join(temp_data_dir, 'wav.scp')
    data_list_path = os.path.join(temp_data_dir, 'data.list')
    if os.path.exists(text_path) and os.path.exists(wav_path):
        utils_file.do_convert_wav_text_scp_to_jsonl(wav_path, text_path, data_list_path)


if __name__ == '__main__':
    """"""
    do_convert('/home/work_nfs14/xlgeng/asr_data_raw/test_data_raw/Leaderboard/datasets/SPEECHIO_ASR_ZH00009')
