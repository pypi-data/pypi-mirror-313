from typing import List, TypeVar

from gxl_ai_utils.utils import utils_file

T = TypeVar('T', bound='WerInfo')


class WerInfo:
    def __init__(self, key, wer, lab_str, rec_str):
        """
        一条音频的存储单元
        :param key:
        :param wer:
        :param lab_str:
        :param rec_str:
        """
        lab_str = lab_str.replace("lab: ", '')
        rec_str = rec_str.replace("rec: ", '')
        self.key = key
        self.wer = wer
        self.lab = lab_str
        self.rec = rec_str
        self.lab_aligned_char_list = []
        self.rec_aligned_char_list = []  # 用于文本对齐
        self.words, self.words_index = [], []  # 用于分词
        self.diff_dict = {}  # 用于存储lab rec差异

    def get_lab_to_split_words(self):
        return utils_file.do_filter_for_encn(self.lab)

    def __str__(self):
        return f'{self.key} | {self.wer} | {self.lab} | {self.rec}'

    def show_info(self):
        print("-" * 100)
        print('key: ', self.key)
        print('wer: ', self.wer)
        print('lab: ', self.lab)
        print('rec: ', self.rec)
        print('lab_aligned_char_list: ', self.lab_aligned_char_list)
        print('rec_aligned_char_list: ', self.rec_aligned_char_list)
        print('words: ', self.words)
        print('words_index: ', self.words_index)
        print('diff_dict: ')
        utils_file.print_dict(self.diff_dict)
        print("-" * 100)

    @staticmethod
    def do_load_info_list_from_wer_path(wer_path):
        info_list = []
        with open(wer_path, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("utt:"):
                    key = lines[i].split()[1]
                    wer = float(lines[i + 1].split()[1])
                    lab_str = lines[i + 2].strip()
                    rec_str = lines[i + 3].strip()
                    info = WerInfo(key, wer, lab_str, rec_str)
                    info_list.append(info)
                    i += 5
                else:
                    i += 1
        return info_list

    @staticmethod
    def do_handle_info_list(info_list: List[T]):
        """"""
        from gxl_utils import do_align_lab_and_rec_to_aligned_char_list, do_fenci_for_lab_aligned_char_list, \
            do_compare_lab_rec_diff
        for info in utils_file.tqdm(info_list, desc="handling info list", total=len(info_list)):
            # 首先进行对齐
            info.lab_aligned_char_list, info.rec_aligned_char_list = do_align_lab_and_rec_to_aligned_char_list(
                info.lab, info.rec)
            # 然后进行分词
            info.words, info.words_index = do_fenci_for_lab_aligned_char_list(info.lab_aligned_char_list)
            # 最后进行比较
            info.diff_dict = do_compare_lab_rec_diff(info)

    @staticmethod
    def do_diff_analysis(info_list1: List[T], info_list2: List[T], noun_dict):
        """
        分析连个wer文件得到的info_list的差异
        :param info_list1:
        :param info_list2:
        :param noun_dict:
        :return: 提升后的词, 为提升的词,总的词数
        """
        my_res_dict = {}
        my_res_dict2 = {}
        # 得到keys
        keys = [item.key for item in info_list1]
        info_list1_dict = {item.key: item for item in info_list1}
        info_list2_dict = {item.key: item for item in info_list2}
        total_err_word = 0
        for key in utils_file.tqdm(keys, total=len(keys), desc="analysising", disable=False):
            """"""
            if not key in info_list2_dict:
                utils_file.logging_print(f'{key} not in info_list2_dict, skipping')
                continue
            info1 = info_list1_dict[key]
            info2 = info_list2_dict[key]
            diff_dict1 = info1.diff_dict
            diff_dict2 = info2.diff_dict
            if len(diff_dict1) == 0 and len(diff_dict2) == 0:
                continue
            err_word_in_1 = list(diff_dict1.keys())
            err_word_in_2 = list(diff_dict2.keys())
            for err_word in err_word_in_1:
                if err_word in noun_dict:
                    total_err_word += 1
                    if err_word in err_word_in_2:
                        err_item = {"key": key, "right": err_word, 'err_left': diff_dict1[err_word]['rec'],
                                    'err_right': diff_dict2[err_word]['rec']}
                        my_res_dict2[err_word] = {
                            "frequency": my_res_dict2[err_word]["frequency"] + 1 if err_word in my_res_dict2 else 1,
                            "errs": my_res_dict2[err_word]["errs"] + [err_item] if err_word in my_res_dict2 else [
                                err_item],
                        }
                    else:
                        err_item = {"key": key, "right": err_word, 'err_left': diff_dict1[err_word]['rec'],
                                    'err_right': err_word}
                        my_res_dict[err_word] = {
                            "frequency": my_res_dict[err_word]["frequency"] + 1 if err_word in my_res_dict else 1,
                            "errs": my_res_dict[err_word]["errs"] + [err_item] if err_word in my_res_dict else [
                                err_item],
                        }
        return my_res_dict, my_res_dict2, total_err_word
