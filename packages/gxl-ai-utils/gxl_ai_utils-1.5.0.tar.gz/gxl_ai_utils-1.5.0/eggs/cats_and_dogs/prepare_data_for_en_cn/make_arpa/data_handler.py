import os

from tqdm import tqdm

from gxl_ai_utils.utils import utils_file


def make_words_line_file():
    """"""
    output_dir = './data_res'
    utils_file.makedir_sil(output_dir)
    input_words_path = "/home/work_nfs4_ssd/yhliang/LanguageModel/lang/lang_test616_mix0.1_pruned_5e-11/words.txt"
    lines = utils_file.load_list_file_clean(input_words_path)
    res_list = []
    for i, line in tqdm(enumerate(lines), total=len(lines)):
        if i == 0:
            continue
        item = line.strip().split()[0]
        res_list.append(item)
    output_path = os.path.join(output_dir, 'words_lines.txt')
    utils_file.write_list_to_file(res_list, output_path)


if __name__ == '__main__':
    make_words_line_file()
