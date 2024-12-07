import argparse
import codecs
import os

import jieba
import tqdm
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu


def calculate_bleu(candidate_text: str, reference_texts: list) -> float:
    """
    计算中文对话任务的 BLEU 分数。

    参数:
        candidate_text (str): 生成的文本。
        reference_texts (list): 参考文本列表（可以有多个参考句子）。

    返回:
        float: BLEU 分数。
    """
    # 对生成文本和参考文本进行分词
    candidate_tokens = list(jieba.cut(candidate_text))
    reference_tokens = [list(jieba.cut(ref)) for ref in reference_texts]

    # 使用 nltk 的 sentence_bleu 计算 BLEU 分数
    smoothing = SmoothingFunction().method1  # 避免分数为零
    bleu_score = sentence_bleu(reference_tokens, candidate_tokens,
                               weights=(0.25, 0.25, 0.25, 0.25),  # 1-gram 到 4-gram 的权重
                               smoothing_function=smoothing)

    return bleu_score

def load_dict_from_scp(label_scp_file: str, silence: bool = False) -> dict:
    """
    得到scp文件的内容,要求key value以空格或者tab分割， 第一个为key,剩下的都是value。
    :param label_scp_file:
    :return:
    """
    res = {}
    with codecs.open(label_scp_file, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except Exception as e:
            print(e)
            return {}
        for line in lines:
            line = line.strip()
            items = line.split()
            if len(items) < 2:
                if not silence:
                    print(
                        'load_dict_from_scp;warning_gxl:, this row not conform to the regulation of scp(key content) and skip it:',
                        line)
                continue
            elif len(items) == 2:
                res[items[0].strip()] = items[1].strip()
            else:
                # logging_print(
                #     'warning_gxl:, this row not conform to the regulation of'
                #     ' scp(key content) and no skip it,第一个为key,剩下的都是value:',
                #     line)
                res[items[0].strip()] = (' '.join(items[1:])).strip()
    total_len = len(res)
    print("load_dict_from_scp()_数据总条数为:", total_len)
    return res

# 得到命令行参数, 使用parser.add_argument()方法
parser = argparse.ArgumentParser()
parser.add_argument('--ref_file', type=str, required=True, help='reference file')
parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file')
parser.add_argument('--output_file', type=str, required=True, help='output file')
args = parser.parse_args()

# 计算BLEU得分
ref_dict = load_dict_from_scp(args.ref_file)
hyp_dict = load_dict_from_scp(args.hyp_file)
os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
res_dict = {}
total_bleu_score = 0
for key, value in tqdm.tqdm(hyp_dict.items(), total=len(hyp_dict)):
    if key in ref_dict:
        ref_str = ref_dict[key]
        hyp_str = value
        bleu_score = calculate_bleu(hyp_str, [ref_str])
        res_dict[key] = bleu_score
        total_bleu_score += bleu_score
    else:
        print(f"key {key} not in ref_dict")
        continue
# 保存结果到文件
def write_dict_to_scp(dic: dict, scp_file_path: str):
    print("开始write_dict_to_scp()，数据总条数为:", len(dic))
    os.makedirs(os.path.dirname(scp_file_path), exist_ok=True)
    with codecs.open(scp_file_path, 'w', encoding='utf-8') as f:
        for k, v in dic.items():
            f.write(f"{k} {v}\n")
avg_bleu_score = total_bleu_score / len(res_dict)
print(f"平均BLEU得分为:{avg_bleu_score}")
res_dict['avg_bleu_score'] = avg_bleu_score
write_dict_to_scp(res_dict, args.output_file)