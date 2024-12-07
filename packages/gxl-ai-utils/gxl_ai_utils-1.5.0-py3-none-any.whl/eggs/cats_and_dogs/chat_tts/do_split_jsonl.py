import argparse

import tqdm

from gxl_ai_utils.utils import utils_file

def get_parser():
    parser = argparse.ArgumentParser(description='进行大文件切割')
    parser.add_argument('--input_jsonl_path', type=str, help='输入文件路径')
    parser.add_argument('--output_dir_path', type=str, help='输出文件夹路径')
    parser.add_argument('--num_thread', type=int, default=32, help='线程数量')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_parser()
    utils_file.logging_info(args)
    input_jsonl_path = args.input_jsonl_path
    output_dir_path = args.output_dir_path
    utils_file.makedir_for_file_or_dir(output_dir_path)
    num_thread = args.num_thread
    data_list = utils_file.load_dict_list_from_jsonl(input_jsonl_path)
    data_list_list = utils_file.do_split_list(data_list, num_thread)
    for i, data_list_tmp in tqdm.tqdm(enumerate(data_list_list), total=len(data_list_list), desc='切割josnl ing'):
        output_path_tmp = utils_file.join_path(output_dir_path, f'tmp_{i}.jsonl')
        utils_file.write_dict_list_to_jsonl(data_list_tmp, output_path_tmp)


