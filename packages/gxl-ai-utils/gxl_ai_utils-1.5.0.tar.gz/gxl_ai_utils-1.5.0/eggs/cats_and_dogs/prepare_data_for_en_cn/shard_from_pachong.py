import os.path

from gxl_ai_utils.utils import utils_file


def do_handle():
    """"""
    data_dir = "/home/work_nfs14/xlgeng/asr_data_shard/pachong_data"
    data_names = ['shangye_caijing_3', 'shangye_caijing_2', 'shangye_caijing_4','shenghuo_2']
    all_list = []
    for data_name in data_names:
        temp_path = os.path.join(data_dir, data_name,'shards_list.txt')
        temp_list = utils_file.load_list_file_clean(temp_path)
        all_list.extend(temp_list)
    utils_file.write_list_to_file(all_list, os.path.join(data_dir, 'all_shards_list_2.txt'))
def do_handle_2():
    """"""
    data_dir = "/home/work_nfs14/xlgeng/asr_data_shard/pachong_data"
    data_names = ['4_lizhi_jiankang', '5_yunting_taihaizhisheng', '6_yunting_zhongguozhisheng','8_liukai_chuantongguoxue','shenghuo_1']
    all_list = []
    for data_name in data_names:
        temp_path = os.path.join(data_dir, data_name,'shards_list.txt')
        temp_list = utils_file.load_list_file_clean(temp_path)
        all_list.extend(temp_list)
    utils_file.write_list_to_file(all_list, os.path.join(data_dir, 'all_shards_list_3.txt'))

if __name__ == '__main__':
    do_handle_2()