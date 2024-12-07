# 将400w条贴吧问答数据进行处理, 这个数据的特点是问句很短, 回答很长,我们只取前一句话的回答.
# 具体规则如下:
# 遇到句号,且一句话内汉字个数在60个一下,则选择它. 否则,将其过滤.
import re
import emoji
import tqdm

from gxl_ai_utils.utils import utils_file

def do_get_first_sentence(s, char_num=80):
    """
    以中文句号作为分割符
    获取长字符串中符合条件的第一句话，如果满足条件（以句号结尾且汉字个数小于80）返回这句话内容和True，否则返回空字符串和False
    """
    for index in range(len(s)):
        if s[index] == '。':
            sentence = s[:index + 1].strip()
            sentence_cleaned = do_clean_chat_text(sentence)
            chinese_count = sum(1 for char in sentence_cleaned if '\u4e00' <= char <= '\u9fff')
            if chinese_count < char_num:
                return sentence_cleaned, True
            else:
                return "", False
    total_cleaned = do_clean_chat_text(s)
    chinese_count = sum(1 for char in total_cleaned if '\u4e00' <= char <= '\u9fff')
    if chinese_count < char_num:
        return total_cleaned, True
    return "", False

def do_clean_chat_text(text):
    # 去除HTML/XML标签
    text = re.sub('<.*?>', '', text)
    # 去除圆括号内内容
    text = re.sub(r'\(.*?\)', '', text)
    # 去除方括号内内容
    text = re.sub(r'\[.*?\]', '', text)
    # 去除花括号内内容
    text = re.sub(r'\{.*?\}', '', text)
    # 去除特殊字符和符号（示例去除换行符、回车符等，可按需扩展）
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    # 去除多余的空格
    text = text.strip().replace("  ", " ")
    # 处理表情符号（将表情符号替换为空字符串）
    text = emoji.replace_emoji(text, replace='')
    # 过滤广告和无关链接（示例去除以http://或https://开头的链接，可按需扩展）
    text = re.sub('https?://\S+', '', text)

    return text


def main():
    # 加载jsonl
    jsonl_path = "/home/work_nfs15/asr_data/data/chat_data/web_text_2019_text/web_text_zh_train.json"
    dict_list = utils_file.load_dict_list_from_jsonl(jsonl_path)
    res_dict_list = []
    for dict_item in tqdm.tqdm(dict_list, total=len(dict_list)):
        key = dict_item["qid"]
        Q = dict_item["title"]
        A = dict_item["content"]
        A_first_sentence, if_exit = do_get_first_sentence(A)
        if if_exit:
            res_dict_list.append({"key": key, "Q": Q, "A": A_first_sentence})
        else:
            continue
    output_path = "/home/work_nfs15/asr_data/data/chat_data/web_text_2019_text/web_text_zh_train_by_gxl.jsonl"
    utils_file.write_dict_list_to_jsonl(res_dict_list, output_path)

if __name__ == '__main__':
    main()