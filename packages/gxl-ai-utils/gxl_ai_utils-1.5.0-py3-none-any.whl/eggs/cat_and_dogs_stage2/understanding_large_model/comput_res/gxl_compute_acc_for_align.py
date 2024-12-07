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

def convert_to_nearest_multiple(numbers, step=0.3):
    # 使用numpy的四舍五入功能将每个数字转换为最近的step的倍数
    return [round(num / step) * step for num in numbers]

def get_full_tag_from_str(input_str, smooth_interval=0.1):
    matches = re.findall(r'<.*?>', input_str)
    # 输出结果
    # if len(matches) == 0:
    #     return '<--no_tag-->'
    num_list = []
    for match in matches:
        try:
            # 尝试将匹配到的字符串转换为浮动数
            num_list.append(float(match[1:-1]))  # 去掉字符串的首尾字符后转换为 float
        except ValueError:
            # 如果转换失败，则将 -1 添加到 num_list
            num_list.append(-1)
    num_list = convert_to_nearest_multiple(num_list, step=smooth_interval)
    res_str = " ".join([f"{num:.6f}" for num in num_list])
    return res_str

def do_replace_tag(input_file, output_file):
    # 打开文件A并读取内容
    with open(input_file, 'r', encoding='utf-8') as file_a:
        content = file_a.read()

    # 删除文件内容中的 < 和 >
    content = content.replace('<', '').replace('>', '')
    # 将修改后的内容写入文件B
    with open(output_file, 'w', encoding='utf-8') as file_b:
        file_b.write(content)

def do_convert_to_pure_tag(input_file, output_file):
    text_dict = utils_file.load_dict_from_scp(input_file)
    new_text_dict = {}
    num_blank_tag = 0
    for key , value in text_dict.items():
        res_value = get_full_tag_from_str(value, smooth_interval=0.2)
        new_text_dict[key] =res_value
        if len(res_value) == 0:
            num_blank_tag += 1
    utils_file.logging_warning('空白时间戳的数量为：', num_blank_tag)
    output_file_blank_num = output_file + '_blank_num'
    utils_file.write_list_to_file([f'空白帧数量为{num_blank_tag}'],output_file_blank_num)
    utils_file.write_dict_to_scp(new_text_dict, output_file)

if __name__ == '__main__':
    """
    首先对识别结果进行计算，接着计算acc,
    分别存入wer文件和acc文件
    """
    parser = argparse.ArgumentParser()
    task = 'align'
    parser.add_argument('--ref_file', type=str, required=True, help='reference file, 真实的标签')
    parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file， 推理的标签')
    parser.add_argument('--output_dir', type=str, required=True, help='output dir 结果保存的目录')
    args = parser.parse_args()
    utils_file.makedir_sil(args.output_dir)
    utils_file.logging_info(f'开始计算{task}的wer')
    utils_file.do_compute_wer(args.ref_file, args.hyp_file, args.output_dir)
    utils_file.logging_info('字符错误率计算完毕，结果如下')
    res = utils_file.do_execute_shell_command(f'tail -n 8 {os.path.join(args.output_dir, "wer")}')
    print(res)

    # utils_file.logging_info(f'开始计算{task}带标签的wer')
    # acc_path = os.path.join(args.output_dir, 'wer_with_tag')
    # hyp_dict = utils_file.load_dict_from_scp(args.hyp_file)
    # ref_dict = utils_file.load_dict_from_scp(args.ref_file)
    # hyp_file_tmp = utils_file.do_get_fake_file()
    # ref_file_tmp = utils_file.do_get_fake_file()
    # do_replace_tag(args.hyp_file, hyp_file_tmp)
    # do_replace_tag(args.ref_file, ref_file_tmp)
    # output_dir_tmp = '/home/xlgeng/.cache/'
    # utils_file.do_compute_wer(ref_file_tmp, hyp_file_tmp, output_dir_tmp)
    # utils_file.copy_file(os.path.join(output_dir_tmp, 'wer'), acc_path)
    # utils_file.logging_info('字符错误率计算完毕，结果如下')
    # res = utils_file.do_execute_shell_command(f'tail -n 8 {os.path.join(args.output_dir, "wer_with_tag")}')
    # print(res)
    utils_file.logging_info(f'开始计算{task}纯标签的wer_smooth')
    acc_path = os.path.join(args.output_dir, 'wer_pure_tag_smooth')
    hyp_dict = utils_file.load_dict_from_scp(args.hyp_file)
    ref_dict = utils_file.load_dict_from_scp(args.ref_file)
    hyp_file_tmp = utils_file.do_get_fake_file()
    ref_file_tmp = utils_file.do_get_fake_file()
    do_convert_to_pure_tag(args.hyp_file, hyp_file_tmp)
    do_convert_to_pure_tag(args.ref_file, ref_file_tmp)
    output_dir_tmp = '/home/xlgeng/.cache/'
    utils_file.do_compute_wer(ref_file_tmp, hyp_file_tmp, output_dir_tmp)
    utils_file.copy_file(os.path.join(output_dir_tmp, 'wer'), acc_path)
    utils_file.logging_info('计算{task}纯标签的wer_smooth计算完毕，结果如下')
    res = utils_file.do_execute_shell_command(f'tail -n 12 {acc_path}')
    print(res)

    utils_file.logging_info('计算空时间戳的数量')











