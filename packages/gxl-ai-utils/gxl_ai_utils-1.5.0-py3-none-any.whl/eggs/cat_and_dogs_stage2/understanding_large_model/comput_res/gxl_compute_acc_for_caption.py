import argparse
import os.path


from gxl_ai_utils.utils import utils_file
import re

def get_tag_from_str(input_str):
    # 使用正则表达式提取所有 <> 中的内容
    matches = re.findall(r'<.*?>', input_str)
    # 输出结果
    if len(matches)==0:
        return '<--no_tag-->'
    return matches[0].upper()


if __name__ == '__main__':
    """
    首先对识别结果进行计算，接着计算acc,
    分别存入wer文件和acc文件
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref_file', type=str, required=True, help='reference file, 真实的标签')
    parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file， 推理的标签')
    parser.add_argument('--output_dir', type=str, required=True, help='output dir 结果保存的目录')
    args = parser.parse_args()
    utils_file.makedir_sil(args.output_dir)
    utils_file.logging_info('开始计算caption正确率，wer')
    utils_file.do_compute_wer(args.ref_file, args.hyp_file, args.output_dir)
    utils_file.logging_info('字符错误率计算完毕，结果如下')
    res = utils_file.do_execute_shell_command(f'tail -n 8 {os.path.join(args.output_dir, "wer")}')
    print(res)

    utils_file.logging_info('开始计算caption正确率，acc')
    acc_path = os.path.join(args.output_dir, 'acc')
    hyp_dict = utils_file.load_dict_from_scp(args.hyp_file)
    ref_dict = utils_file.load_dict_from_scp(args.ref_file)
    tag_hyp_dict = {}
    for key, value in hyp_dict.items():
        tag_hyp_dict[key] = get_tag_from_str(value)
    tag_ref_dict = {}
    for key, value in ref_dict.items():
        tag_ref_dict[key] = get_tag_from_str(value)
    output_acc_f = open(acc_path, 'w', encoding='utf-8')
    same_num = 0
    for key, hyp_tags in tag_hyp_dict.items():
        if key not in tag_ref_dict:
            continue
        ref_tags = tag_ref_dict[key]
        # 判断标签是否相同
        if ref_tags == hyp_tags:
            if_same = True
            same_num += 1
        else:
            if_same = False

        # 向文件写入数据
        output_acc_f.write(f"key: {key}\n")
        output_acc_f.write(f"ref_tag: {ref_tags}\n")
        output_acc_f.write(f"hyp_tag: {hyp_tags}\n")
        output_acc_f.write(f"if_same: {if_same}\n")
        output_acc_f.write("\n")  # 添加空行分隔不同的条目
    output_acc_f.write(f'正确率为：{same_num / len(tag_hyp_dict)}')
    # 输出相同标签的数量
    print(f"caption的正确率为: {same_num / len(tag_hyp_dict)}")











