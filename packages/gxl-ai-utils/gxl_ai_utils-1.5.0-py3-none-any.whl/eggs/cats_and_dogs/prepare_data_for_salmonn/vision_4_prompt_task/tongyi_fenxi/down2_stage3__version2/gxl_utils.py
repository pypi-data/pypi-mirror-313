import re
import sys
import unicodedata
from typing import List

import tqdm

from gxl_ai_utils.utils import utils_file
from Gxl2DTable import Gxl2DTable
def _characterize(string):
    """
    把一句话切分冲单元序列, 音频单词和汉字均是单元
    :param string:
    :return:
    """
    spacelist = [' ', '\t', '\r', '\n']
    puncts = [
        '!', ',', '?', '、', '。', '！', '，', '；', '？', '：', '「', '」', '︰', '『', '』',
        '《', '》'
    ]
    res = []
    i = 0
    while i < len(string):
        char = string[i]
        if char in puncts:
            i += 1
            continue
        cat1 = unicodedata.category(char)
        # https://unicodebook.readthedocs.io/unicode.html#unicode-categories
        if cat1 == 'Zs' or cat1 == 'Cn' or char in spacelist:  # space or not assigned
            i += 1
            continue
        if cat1 == 'Lo':  # letter-other
            res.append(char)
            i += 1
        else:
            # some input looks like: <unk><noise>, we want to separate it to two words.
            sep = ' '
            if char == '<': sep = '>'
            j = i + 1
            while j < len(string):
                c = string[j]
                if ord(c) >= 128 or (c in spacelist) or (c == sep):
                    break
                j += 1
            if j < len(string) and string[j] == '>':
                j += 1
            res.append(string[i:j])
            i = j
    return res


class _Calculator:

    def __init__(self):
        self.data = {}
        self.space = []
        self.cost = {}
        self.cost['cor'] = 0
        self.cost['sub'] = 1
        self.cost['del'] = 1
        self.cost['ins'] = 1

    def calculate(self, lab, rec):
        # Initialization
        lab.insert(0, '')
        rec.insert(0, '')
        while len(self.space) < len(lab):
            self.space.append([])
        for row in self.space:
            for element in row:
                element['dist'] = 0
                element['error'] = 'non'
            while len(row) < len(rec):
                row.append({'dist': 0, 'error': 'non'})
        for i in range(len(lab)):
            self.space[i][0]['dist'] = i
            self.space[i][0]['error'] = 'del'
        for j in range(len(rec)):
            self.space[0][j]['dist'] = j
            self.space[0][j]['error'] = 'ins'
        self.space[0][0]['error'] = 'non'
        for token in lab:
            if token not in self.data and len(token) > 0:
                self.data[token] = {
                    'all': 0,
                    'cor': 0,
                    'sub': 0,
                    'ins': 0,
                    'del': 0
                }
        for token in rec:
            if token not in self.data and len(token) > 0:
                self.data[token] = {
                    'all': 0,
                    'cor': 0,
                    'sub': 0,
                    'ins': 0,
                    'del': 0
                }
        # Computing edit distance
        for i, lab_token in enumerate(lab):
            for j, rec_token in enumerate(rec):
                if i == 0 or j == 0:
                    continue
                min_dist = sys.maxsize
                min_error = 'none'
                dist = self.space[i - 1][j]['dist'] + self.cost['del']
                error = 'del'
                if dist < min_dist:
                    min_dist = dist
                    min_error = error
                dist = self.space[i][j - 1]['dist'] + self.cost['ins']
                error = 'ins'
                if dist < min_dist:
                    min_dist = dist
                    min_error = error
                if lab_token == rec_token:
                    dist = self.space[i - 1][j - 1]['dist'] + self.cost['cor']
                    error = 'cor'
                else:
                    dist = self.space[i - 1][j - 1]['dist'] + self.cost['sub']
                    error = 'sub'
                if dist < min_dist:
                    min_dist = dist
                    min_error = error
                self.space[i][j]['dist'] = min_dist
                self.space[i][j]['error'] = min_error
        # Tracing back
        result = {
            'lab': [],
            'rec': [],
            'all': 0,
            'cor': 0,
            'sub': 0,
            'ins': 0,
            'del': 0
        }
        i = len(lab) - 1
        j = len(rec) - 1
        while True:
            if self.space[i][j]['error'] == 'cor':  # correct
                if len(lab[i]) > 0:
                    self.data[lab[i]]['all'] = self.data[lab[i]]['all'] + 1
                    self.data[lab[i]]['cor'] = self.data[lab[i]]['cor'] + 1
                    result['all'] = result['all'] + 1
                    result['cor'] = result['cor'] + 1
                result['lab'].insert(0, lab[i])
                result['rec'].insert(0, rec[j])
                i = i - 1
                j = j - 1
            elif self.space[i][j]['error'] == 'sub':  # substitution
                if len(lab[i]) > 0:
                    self.data[lab[i]]['all'] = self.data[lab[i]]['all'] + 1
                    self.data[lab[i]]['sub'] = self.data[lab[i]]['sub'] + 1
                    result['all'] = result['all'] + 1
                    result['sub'] = result['sub'] + 1
                result['lab'].insert(0, lab[i])
                result['rec'].insert(0, rec[j])
                i = i - 1
                j = j - 1
            elif self.space[i][j]['error'] == 'del':  # deletion
                if len(lab[i]) > 0:
                    self.data[lab[i]]['all'] = self.data[lab[i]]['all'] + 1
                    self.data[lab[i]]['del'] = self.data[lab[i]]['del'] + 1
                    result['all'] = result['all'] + 1
                    result['del'] = result['del'] + 1
                result['lab'].insert(0, lab[i])
                result['rec'].insert(0, "")
                i = i - 1
            elif self.space[i][j]['error'] == 'ins':  # insertion
                if len(rec[j]) > 0:
                    self.data[rec[j]]['ins'] = self.data[rec[j]]['ins'] + 1
                    result['ins'] = result['ins'] + 1
                result['lab'].insert(0, "")
                result['rec'].insert(0, rec[j])
                j = j - 1
            elif self.space[i][j]['error'] == 'non':  # starting point
                break
            else:  # shouldn't reach here
                print(
                    'this should not happen , i = {i} , j = {j} , error = {error}'
                    .format(i=i, j=j, error=self.space[i][j]['error']))
        return result


_calculator = _Calculator()


def do_align_lab_and_rec_to_aligned_char_list(lab_str, rec_str):
    """
    对齐lab和rec
    传入原生的str,空格的多少无所谓,只要英文单词之前有空格就行,英文与中文之间也无所谓
    :param lab_str:
    :param rec_str:
    :return:
    """
    lab_uni_list = _characterize(lab_str)
    rec_uni_list = _characterize(rec_str)
    res = _calculator.calculate(lab_uni_list, rec_uni_list)
    lab_list = res['lab']
    rec_list = res['rec']
    lab_list = [item if item != '' else '[]' for item in lab_list]
    rec_list = [item if item != '' else '[]' for item in rec_list]
    return lab_list, rec_list


def do_fenci_for_lab_aligned_char_list(lab_aligned_char_list, fenci_type='jieba'):
    """
    输入lab_aligned_char_list,
    输出每个词对应的index
    :param lab_aligned_char_list:
    :return:
    """
    char_available_list = [item for item in lab_aligned_char_list if item != '[]']
    str_represent = ' '.join(char_available_list)
    # 去除汉字之间的空格
    str_represent = re.sub(r'\s+([\u4e00-\u9fa5])', r'\1', str_represent)
    if fenci_type == 'jieba':
        words_list = utils_file.do_fenci(str_represent, fenci_obj_type='jieba', )
    elif fenci_type == 'thulac':
        words_list = utils_file.do_fenci(str_represent, fenci_obj_type='thulac', )
    else:
        raise ValueError('fenci_type should be jieba or thulac')
    word_indices = []
    index = 0
    for word_i in words_list:
        word_indices.append(index)
        if utils_file.do_judge_str_is_all_english(word_i):
            index += 1
        else:
            index += len(word_i)
        while index < len(lab_aligned_char_list) and lab_aligned_char_list[index] == '[]':
            index += 1
    res_index_list = []
    for i in range(len(word_indices)):
        index_now = word_indices[i]
        index_next = word_indices[i + 1] if i < len(word_indices) - 1 else len(lab_aligned_char_list)
        res_index_list.append(list(range(index_now, index_next)))
    return words_list, res_index_list


def _get_word_index_by_char_index(char_index, words_index_list):
    for i, word_list in enumerate(words_index_list):
        if char_index in word_list:
            return i
    return -1

def get_wer_path_table(wer_path_info_path)-> Gxl2DTable:
    """
    从wer_path_dict 中得到每个speechio的wer_path
    """
    wer_path_info_path = wer_path_info_path
    # dict_temp1 = {'speechio': ['common', 'short', 'long', 'repeat', 'messy', 'encourage']}
    # dict_temp2 = utils_file.load_dict_from_json(wer_path_info_path)
    # dict_temp1.update(dict_temp2)

    wer_table = Gxl2DTable.load_from_json(wer_path_info_path)
    return wer_table

from WerInfo_Object import WerInfo

def do_extract_nouns_jieba(common_info_list:List["WerInfo"]):
    import jieba.posseg as pseg
    nouns = set()
    nouns_dict = {}
    for info in  tqdm.tqdm(common_info_list, desc="extract nouns", total=len(common_info_list)):
        string = info.get_lab_to_split_words()
        words = pseg.cut(string)
        for word, flag in words:
            if flag.startswith('n'):  # 以'n'开头的词性标记表示名词
                nouns.add(word)
                if word in nouns_dict:
                    nouns_dict[word] += 1
                else:
                    nouns_dict[word] = 1
    return nouns, nouns_dict

from typing import List, Set, Dict

def do_extract_nouns_thulac(common_info_list: List["WerInfo"]) -> (Set[str], Dict[str, int]):
    import thulac
    thu1 = thulac.thulac(seg_only=False)  # 初始化THULAC，seg_only=False表示进行分词和词性标注
    nouns = set()
    nouns_dict = {}

    for info in tqdm.tqdm(common_info_list, desc="extract nouns", total=len(common_info_list)):
        string = info.get_lab_to_split_words()
        words = thu1.cut(string, text=True)  # 进行分词和词性标注
        for item in words.split():
            word, flag = item.split('_')
            if flag.startswith('n'):  # 以'n'开头的词性标记表示名词
                nouns.add(word)
                if word in nouns_dict:
                    nouns_dict[word] += 1
                else:
                    nouns_dict[word] = 1

    return nouns, nouns_dict

def do_compare_lab_rec_diff(info: "WerInfo", lab_aligned_char_list=None, rec_aligned_char_list=None, words_list=None, words_index_list=None):
    res_dict = {}
    if info is not None:
        lab_aligned_char_list, rec_aligned_char_list = info.lab_aligned_char_list, info.rec_aligned_char_list
        if len(lab_aligned_char_list) != len(rec_aligned_char_list):
            print("rec_aligned_char_list 和 rec_aligned_char_list 长度不一致")
            print(lab_aligned_char_list)
            print(rec_aligned_char_list)
            exit(0)
        words_list, words_index_list = info.words, info.words_index
    else:
        lab_aligned_char_list = lab_aligned_char_list
        rec_aligned_char_list = rec_aligned_char_list
        words_list = words_list
        words_index_list = words_index_list

    for i in range(len(lab_aligned_char_list)):
        if lab_aligned_char_list[i] != rec_aligned_char_list[i]:
            word_index = _get_word_index_by_char_index(i, words_index_list)
            word_involved = words_list[word_index]
            if word_involved in res_dict:
                continue
            word_indexs_involved = words_index_list[word_index]
            try:
                word_chars_lab = [lab_aligned_char_list[i] for i in word_indexs_involved]
                word_chars_rec = [rec_aligned_char_list[i] for i in word_indexs_involved]
            except:
                print(word_indexs_involved)
                info.show_info()
                continue
            word_lab = " ".join(word_chars_lab)
            word_lab = utils_file.do_filter_for_encn(word_lab)
            word_rec = " ".join(word_chars_rec)
            word_rec = utils_file.do_filter_for_encn(word_rec)
            if '[]' in word_chars_lab:
                tag = "insert"
            elif '[]' in word_chars_rec:
                tag = "delete"
            else:
                tag = "replace"
            res_dict[word_involved] = {
                "lab": word_lab,
                "rec": word_rec,
                "tag": tag,
            }
    return res_dict


if __name__ == '__main__':  # test code
    """"""
    # 测试对齐
    lab = "整 个 儿 把 蒋 昭 儿 吊 到 里 头hello xi 好 了  妲己和王昭君也来了 上官婉儿也不错"
    rec = "整 个    把 勋 章 掉    到 里 头 了 hi 我 更 好 了 xiao  wen 妲己和耿雪龙也来了 闸阀是的也不粗"
    lab_list, rec_list = do_align_lab_and_rec_to_aligned_char_list(lab, rec)
    print(lab_list)
    print(rec_list)
    # 测试分词
    word, word_indexs = do_fenci_for_lab_aligned_char_list(lab_list)
    print(word)
    print(word_indexs)
    # 测试差异提取
    res = do_compare_lab_rec_diff(None, lab_list, rec_list, word, word_indexs)
    print(res)

    # 测试对齐
    lab = "全 国 居 民 消 费 价 格 指 数 C   P I 同 比 上 涨 百 分 之 二 点 儿 三"
    rec = " 全 国 居 民 消 费 价 格 指 数 CPI     同 比 上 涨 百 分 之 二 点    三"
    lab_list, rec_list = do_align_lab_and_rec_to_aligned_char_list(lab, rec)
    print(lab_list)
    print(rec_list)
    # 测试分词
    word, word_indexs = do_fenci_for_lab_aligned_char_list(lab_list)
    print(word)
    print(word_indexs)
    # 测试差异提取
    res = do_compare_lab_rec_diff(None, lab_list, rec_list, word, word_indexs)
    print(res)

