# 该文件用于计算仅时间戳token正确率
import argparse



def validate_format_and_length(lab, rec):
    # 检查两个列表的长度是否相同
    if len(lab) != len(rec):
        return False

    # 检查每个列表的长度是否能被3整除
    if len(lab) % 3 != 0:
        return False

    # 验证每组的格式
    for i in range(0, len(lab), 3):
        group_lab = lab[i:i + 3]
        group_rec = rec[i:i + 3]

        # 每组的第一个和第三个元素应该是时间戳格式
        if not (group_lab[0].startswith('<') and group_lab[0].endswith('>') and
                group_lab[2].startswith('<') and group_lab[2].endswith('>')):
            return False

        if not (group_rec[0].startswith('<') and group_rec[0].endswith('>') and
                group_rec[2].startswith('<') and group_rec[2].endswith('>')):
            return False

        # 每组的第二个元素应该是字符串并且不是时间戳格式
        if (group_lab[1].startswith('<') and group_lab[1].endswith('>')):
            return False

        if (group_rec[1].startswith('<') and group_rec[1].endswith('>')):
            return False

    return True


def calculate_wer_timestamps(lab_timestamps, rec_timestamps, threshold):
    n = len(lab_timestamps)
    m = 0

    for lab_item, rec_item in zip(lab_timestamps, rec_timestamps):
        lab_time = float(lab_item[1:-1])
        rec_time = float(rec_item[1:-1])
        diff = abs(lab_time - rec_time)
        if diff >= threshold:
            m += 1

    wer = m / n
    return wer


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

from gxl_ai_utils.utils import utils_file
def process_files(lab_file_path, rec_file_path, threshold):
    # lab_lines = read_file(lab_file_path)
    # rec_lines = read_file(rec_file_path)
    lab_dict= utils_file.load_dict_from_scp(lab_file_path)
    rec_dict= utils_file.load_dict_from_scp(rec_file_path)
    dict_list = []
    for key, value in lab_dict.items():
        if key not in rec_dict:
            continue
        dict_list.append({'key': key, 'ref': value, 'hyp': rec_dict[key]})
    all_num = len(dict_list)
    print(f'all_num: {all_num}')

    all_lab_timestamps = []
    all_rec_timestamps = []
    error_num = 0 # 不是标准格式的数量
    # for lab_line, rec_line in zip(lab_lines, rec_lines):
    for dict_item in dict_list:
        # lab_data = lab_line.strip().split('\t')[1].split()
        # rec_data = rec_line.strip().split('\t')[1].split()
        lab_data = dict_item['ref'].split()
        rec_data = dict_item['hyp'].split()

        if validate_format_and_length(lab_data, rec_data):
            lab_timestamps = [(lab_data[i], lab_data[i + 2]) for i in range(0, len(lab_data), 3)]
            rec_timestamps = [(rec_data[i], rec_data[i + 2]) for i in range(0, len(rec_data), 3)]

            lab_timestamps = [item for sublist in lab_timestamps for item in list(sublist)]
            rec_timestamps = [item for sublist in rec_timestamps for item in list(sublist)]

            all_lab_timestamps.extend(lab_timestamps)
            all_rec_timestamps.extend(rec_timestamps)
        else:
            error_num += 1
    print(all_lab_timestamps)
    print(all_rec_timestamps)
    print(f'error_num : {error_num}')
    if all_lab_timestamps and all_rec_timestamps:
        total_wer = calculate_wer_timestamps(all_lab_timestamps, all_rec_timestamps, threshold)
        return total_wer, all_num, error_num


# 得到命令行参数, 使用parser.add_argument()方法
parser = argparse.ArgumentParser()
parser.add_argument('--ref_file', type=str, required=True, help='reference file, 真实的标签')
parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file， 推理的标签')
parser.add_argument('--output_file', type=str, required=True, help='output file')
args = parser.parse_args()


# 示例文件路径
# lab_file_path = '/home/work_nfs16/znlin/align_task_process/code/egs/ter/hyp'
# rec_file_path = '/home/work_nfs16/znlin/align_task_process/code/egs/ter/ref'
lab_file_path = args.ref_file
rec_file_path = args.hyp_file
output_path = args.output_file
threshold = 0.05

# 处理文件并输出结果
total_wer, all_num, error_num = process_files(lab_file_path, rec_file_path, threshold)

res_list = []
if total_wer is not None:
    print(f"Total WER: {total_wer}")
    res_list.append(f"Total WER: {total_wer}")
    print(f'error num: {error_num}, all num: {all_num}')
    res_list.append(f'error num: {error_num}, all num:{all_num}')
else:
    print("No valid data to compute WER.")