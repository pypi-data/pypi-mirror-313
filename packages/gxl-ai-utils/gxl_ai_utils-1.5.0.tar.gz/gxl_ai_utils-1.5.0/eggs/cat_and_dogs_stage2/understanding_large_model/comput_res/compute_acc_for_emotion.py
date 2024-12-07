import argparse
import json

from gxl_ai_utils.utils import utils_file
from sklearn.metrics import classification_report, accuracy_score, recall_score

def evaluate_emotion_prediction(list_file_path, text_file_path):
    """
    评估情感预测的性能，包括 Weighted Accuracy (WA), Unweighted Accuracy (UA), 和 Weighted F1 (WF1)。
    同时处理没有预测标签的样本，并统计未找到预测标签的数量。

    参数:
        list_file_path (str): data.list 文件的路径。
        text_file_path (str): text.txt 文件的路径。

    返回:
        dict: 包含 WA, UA, WF1 的计算结果和未找到预测标签的样本数量。
    """
    # 读取 data.list 文件
    with open(list_file_path, "r") as f:
        data_list = [json.loads(line.strip()) for line in f]

    # 读取 text.txt 文件
    with open(text_file_path, "r") as f:
        text_data = [line.strip().split("\t") for line in f]

    # 构造预测字典
    pred_dict = {}
    for line in text_data:
        if len(line) > 1 and "<" in line[1] and ">" in line[1]:
            pred_label = line[1].split("<")[-1].split(">")[0].upper()
            pred_dict[line[0]] = pred_label
        else:
            # 打印无效行的 key（如果存在）
            key = line[0] if len(line) > 0 else "UNKNOWN"
            print(f"Skipping invalid key: {key}")

    # 提取原始标签和预测标签
    y_true = []
    y_pred = []
    missing_keys = 0  # 统计没有预测标签的样本数量

    for entry in data_list:
        key = entry["key"]
        if key in pred_dict:
            y_true.append(entry["emotion"])
            y_pred.append(pred_dict[key])
        else:
            # 如果没有预测标签，统计并跳过
            missing_keys += 1

    if not y_true or not y_pred:
        raise ValueError("No valid predictions found. Check the input files.")

    # 计算 Weighted Accuracy (WA)
    wa = accuracy_score(y_true, y_pred)

    # 计算 Unweighted Accuracy (UA)
    ua = recall_score(y_true, y_pred, average="macro")
    unique_emotions = set(y_true)
    # ua = sum(
    #     accuracy_score(
    #         [true for true, pred in zip(y_true, y_pred) if true == emotion],
    #         [pred for true, pred in zip(y_true, y_pred) if true == emotion],
    #     )
    #     for emotion in unique_emotions
    # ) / len(unique_emotions)

    # 计算 Weighted F1 (WF1)
    report = classification_report(
        y_true, y_pred, labels=list(unique_emotions), output_dict=True
    )
    wf1 = sum(
        report[emotion]["f1-score"] * (y_true.count(emotion) / len(y_true))
        for emotion in unique_emotions if emotion in report
    )

    return {"WA": wa, "UA": ua, "WF1": wf1, "missing_keys": missing_keys}

# 主函数
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--ref_file', type=str, required=True, help='reference file, 真实的标签')
    parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file， 推理的标签')
    parser.add_argument('--output_file', type=str, required=True, help='output file')
    args = parser.parse_args()

    # 用户输入文件路径
    list_file_path = "/home/work_nfs11/zxzhao/emotion.list"
    # text_file_path = "/home/work_nfs11/zxzhao/text"
    text_file_path = args.hyp_file

    # 调用函数并输出结果
    try:
        results = evaluate_emotion_prediction(list_file_path, text_file_path)
        print(f"Weighted Accuracy (WA): {results['WA']:.4f}")
        print(f"Unweighted Accuracy (UA): {results['UA']:.4f}")
        print(f"Weighted F1 (WF1): {results['WF1']:.4f}")
        print(f"未找到预测标签的样本数量: {results['missing_keys']}")
        res_list = [f"Weighted Accuracy (WA): {results['WA']:.4f}", f"Unweighted Accuracy (UA): {results['UA']:.4f}",
                    f"Weighted F1 (WF1): {results['WF1']:.4f}", f"未找到预测标签的样本数量: {results['missing_keys']}"]
        utils_file.write_list_to_file(res_list, args.output_file)
    except Exception as e:
        print(f"发生错误：{e}")