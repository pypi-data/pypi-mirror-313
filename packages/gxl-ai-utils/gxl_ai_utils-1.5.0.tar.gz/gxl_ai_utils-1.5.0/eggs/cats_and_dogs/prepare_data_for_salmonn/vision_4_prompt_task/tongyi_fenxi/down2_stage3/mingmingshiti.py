import re

import jieba.posseg as pseg
import thulac


def extract_nouns(string_list):
    nouns = set()
    nouns_dict = {}
    for string in string_list:
        words = pseg.cut(string)
        for word, flag in words:
            if flag.startswith('n'):  # 以'n'开头的词性标记表示名词
                nouns.add(word)
                if word in nouns_dict:
                    nouns_dict[word] += 1
                else:
                    nouns_dict[word] = 1
    return nouns, nouns_dict


def convert_to_indices(s):
    result = []
    index = 0
    for word in s:
        if re.match("^[A-Za-z]*$", word):
            result.append((index,))
            index += 1
        else:
            result.append(tuple(range(index, index + len(word))))
            index += len(word)
    return result
def do_fenci(string):
        words =  pseg.cut(string)
        res = []
        for word, flag in words:
            res.append(word)
        return res, convert_to_indices(res)


thu1 = thulac.thulac(seg_only=True)  # 设置只进行分词，不进行词性标注

def do_fenci(string):
    string = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1 \2', string)
    string = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1 \2', string)
    words = thu1.cut(string, text=True)  # 进行分词
    res = words.split(' ')  # 分词结果是一个字符串，每个词之间用空格分隔，所以我们需要用split函数来将其转换为列表
    return res, convert_to_indices(res)

if __name__ == '__main__':
    test_str_list = [
        "我爱吃苹果hello嘻嘻并且喜欢和妲己一起玩耍",
        "我们一起举办了一场盛大的庆祝活动大家欢笑着共度美好时光",
        "他是一个有着丰富经验和深厚知识的专家在行业内享有很高的声誉",
    ]

    for test_str in test_str_list:
        print(test_str)
        print(do_fenci(test_str))