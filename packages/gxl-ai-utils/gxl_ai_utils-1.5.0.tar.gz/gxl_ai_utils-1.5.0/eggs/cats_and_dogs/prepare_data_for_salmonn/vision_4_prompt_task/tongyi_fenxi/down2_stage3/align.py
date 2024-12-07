import re
import sys
import unicodedata
from itertools import zip_longest


# def do_align(lab,rec):
#     lab_list = lab.split()
#     rec_list = rec.split()
#
#     aligned = list(zip_longest(lab_list, rec_list, fillvalue='[]'))
#
#     lab_aligned = [i[0] for i in aligned]
#     rec_aligned = [i[1] for i in aligned]
#
#     return lab_aligned, rec_aligned

def do_align_old(lab, rec):
    # 进行严格对齐
    lab = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1 \2', lab)
    rec = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1 \2', rec)
    lab_list = re.split(r'(\s+)', lab)
    rec_list = re.split(r'(\s+)', rec)
    if lab_list[-1] == "":
        lab_list.pop()
    if rec_list[-1] == "":
        rec_list.pop()
    if lab_list[0] == "":
        lab_list.pop(0)
    if rec_list[0] == "":
        rec_list.pop(0)

    if lab_list[-1] == "   ":
        lab_list[-1] = '[]'
    if rec_list[-1] == "   ":
        rec_list[-1] = '[]'

    lab_list = [x for x in lab_list if x != " "]
    rec_list = [x for x in rec_list if x != " "]
    lab_list = [x if x != "    " else "[]" for x in lab_list]
    rec_list = [x if x != "    " else "[]" for x in rec_list]
    lab_list = [x for x in lab_list if x.strip() != ""]
    rec_list = [x for x in rec_list if x.strip() != ""]
    # 对齐字符串长度
    if len(lab_list) > len(rec_list):
        while (len(lab_list) > len(rec_list)):
            rec_list.append("[]")
    elif len(lab_list) < len(rec_list):
        while (len(lab_list) < len(rec_list)):
            lab_list.append("[]")
    return lab_list, rec_list


spacelist = [' ', '\t', '\r', '\n']
puncts = [
    '!', ',', '?', '、', '。', '！', '，', '；', '？', '：', '「', '」', '︰', '『', '』',
    '《', '》'
]


def characterize(string):
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


def stripoff_tags(x):
    if not x: return ''
    chars = []
    i = 0
    T = len(x)
    while i < T:
        if x[i] == '<':
            while i < T and x[i] != '>':
                i += 1
            i += 1
        else:
            chars.append(x[i])
            i += 1
    return ''.join(chars)


class Calculator:

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
        lab_list = result['lab']
        rec_list = result['rec']
        lab_list = [x if x != "" else "[]" for x in lab_list]
        rec_list = [x if x != "" else "[]" for x in rec_list]
        return lab_list, rec_list

calculator = Calculator()

def do_align(lab, rec):
    """"""
    lab = characterize(lab)
    rec = characterize(rec)
    return calculator.calculate(lab, rec)

if __name__ == '__main__':
    # 示例输入
    lab = "但 是 从 尺 寸 来 讲 呢 往 往 呢 就 这 个 尺 寸 一 有 呃 一 个 城 市 都 是 大 于 啊 一 般 欧 洲 的 一 个 国 家 的   "
    rec = "但 是 从 尺 寸 来 讲 呢 往 往 呢 就 这 个 尺 寸 已 有 的 一 个 城    都 是 大 于 呃 一 般 欧 洲 的 一 个 国 家 的 啊"
    lab_list, rec_list = do_align(lab, rec)
    print("对齐后的 lab list：", lab_list)
    print("对齐后的 rec list：", rec_list)
    lab = "HELLO    大 家 好"
    rec = "哈    喽 大 家 好"
    lab_list, rec_list = do_align(lab, rec)
    print("对齐后的 lab list：", lab_list)
    print("对齐后的 rec list：", rec_list)
