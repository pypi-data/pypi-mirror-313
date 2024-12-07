import os

import tqdm

from gxl_ai_utils.utils import utils_file
def do_prepare_data_for_format():
    """"""
    cv_wav_dict = {}
    cv_text_dict = {}
    train_wav_dict = {}
    train_text_dict = {}
    output_dir = './data_scp'

    input_dir = "/home/work_nfs13/yhdai/data/chat_llm/data_raw"
    dir_name_list,_ = utils_file.do_listdir(input_dir, return_path=False)
    for dir_name in dir_name_list:
        print(dir_name)
        if dir_name == 'cv':
            item_wav_scp_path = os.path.join(input_dir, dir_name, 'wav.scp')
            item_text_path = os.path.join(input_dir, dir_name, 'text')
            output_wav_path =  os.path.join(output_dir, 'dev', 'wav.scp')
            output_text_path = os.path.join(output_dir, 'dev', 'text')
            output_data_list_path = os.path.join(output_dir, 'dev', 'data.list')
            utils_file.copy_file(item_wav_scp_path, output_wav_path)
            utils_file.copy_file(item_text_path, output_text_path)
            utils_file.do_convert_wav_text_scp_to_jsonl(item_wav_scp_path, item_text_path, output_data_list_path)
        else:
            item_wav_scp_path = os.path.join(input_dir, dir_name, 'wav.scp')
            item_text_path = os.path.join(input_dir, dir_name, 'text')
            if not os.path.exists(item_wav_scp_path) or  not os.path.exists(item_text_path):
                print(f'{item_wav_scp_path} or {item_text_path} not exist')
                continue
            train_wav_dict.update(utils_file.load_dict_from_scp(item_wav_scp_path))
            train_text_dict.update(utils_file.load_dict_from_scp(item_text_path))

    output_wav_path =  os.path.join(output_dir, 'train', 'wav.scp')
    output_text_path = os.path.join(output_dir, 'train', 'text')
    output_data_list_path = os.path.join(output_dir, 'train', 'data.list')
    utils_file.write_dict_to_scp(train_wav_dict, output_wav_path)
    utils_file.write_dict_to_scp(train_text_dict, output_text_path)
    utils_file.do_convert_wav_text_scp_to_jsonl(output_wav_path, output_text_path, output_data_list_path)
    # handle data.list
    for partition in ['dev','train']:
        data_list_path = os.path.join(output_dir, partition, 'data.list')
        output_list_path = os.path.join(output_dir, partition, 'data_full.list')
        dict_list = utils_file.load_dict_list_from_jsonl(data_list_path)
        new_dict_list = []
        for dict_item in tqdm.tqdm(dict_list, total=len(dict_list)):
            """"""
            dict_item['task']="<S2TCHAT>"
            dict_item['duration'] = utils_file.do_get_wav_duration(dict_item['wav'])
            dict_item['lang'] = "<CN>"
            dict_item['speaker'] = "<NONE>"
            dict_item['emotion'] = "<NONE>"
            dict_item['gender'] = "<NONE>"
            dict_item['extra'] = {}
            new_dict_list.append(dict_item)
        utils_file.write_dict_list_to_jsonl(new_dict_list, output_list_path)


def change_data_list_for_format():
    """"""
    for partition in ['dev','train']:
        data_list_path = os.path.join('./data_scp', partition, 'data_full.list')
        output_list_path = os.path.join('./data_scp', partition, 'data_chat.list')
        dict_list = utils_file.load_dict_list_from_jsonl(data_list_path)
        new_dict_list = []
        for dict_item in tqdm.tqdm(dict_list, total=len(dict_list)):
            """"""
            new_dict_item = {}
            new_dict_item['task'] = "<S2TCHAT>"
            new_dict_item['key'] = dict_item['key']
            new_dict_item['wav'] = dict_item['wav']
            new_dict_item['txt'] = dict_item['txt']
            dict_item['lang'] = "<CN>"
            dict_item['speaker'] = "<NONE>"
            dict_item['emotion'] = "<NONE>"
            dict_item['gender'] = "<NONE>"
            new_dict_item['extra'] = {'duration': dict_item['duration'], 'dataset': 'chat_200h'}
            new_dict_list.append(new_dict_item)
        utils_file.write_dict_list_to_jsonl(new_dict_list, output_list_path)
def compute_time_duration():
    output_dir = './data_scp'
    for partition in ['dev','train']:
        output_list_path = os.path.join(output_dir, partition, 'data_full.list')
        duration_sum = 0
        dict_list = utils_file.load_dict_list_from_jsonl(output_list_path)
        for dict_item in tqdm.tqdm(dict_list, total=len(dict_list)):
            duration_sum += dict_item['duration']
        print(f'{partition} duration_sum: {duration_sum/3600}h')


if __name__ == '__main__':
    """"""
    change_data_list_for_format()
    # compute_time_duration()