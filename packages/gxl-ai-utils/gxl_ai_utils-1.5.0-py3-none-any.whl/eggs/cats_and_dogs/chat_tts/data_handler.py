import re

from tqdm import tqdm

from gxl_ai_utils.utils import utils_file

input_path = "/home/work_nfs8/xlgeng/new_workspace/checkpoint/download/xiaohuangji50w_nofenci.conv"


lines_all = utils_file.load_list_file_clean(input_path)
lines_num = len(lines_all)
print(lines_num)
index = 0
res_data = []
now_str = "Q: "
for line in tqdm(lines_all[:int(lines_num / 20)]):
    if line == "E":
        index += 1
        continue
    line = line.strip().replace("M ", "")
    if index == 1:
        now_str += line
        now_str += " A: "
        index +=1
        continue
    if index == 2:
        now_str += line
        res_data.append(now_str)
        index = 0
        now_str = "Q: "
        continue

utils_file.print_list(res_data[:10])


def get_QA(line):
    items = line.split("A: ")
    Q = items[0].replace("Q: ", "").replace(" ","").strip()
    A = items[1].replace(" ", "").strip()
    return Q, A

def has_letters(string):
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(string))


utils_file.logging_print("filtering")
res_data_new = []
for line in tqdm(res_data):
    Q, A = get_QA(line)
    Q = Q.strip()
    A = A.strip()
    if len(Q) > 30 or len(Q) < 7:
        continue
    if len(A) > 30 or len(A) < 7:
        continue
    if has_letters(Q) or has_letters(A):
        print(Q,A )
        continue
    lines = f'Q: {Q} A: {A}'
    res_data_new.append(lines)

utils_file.print_list(res_data_new[:10])
utils_file.logging_limit_print(len(res_data_new))

utils_file.write_list_to_file(res_data_new, "./xiaohuangji50w_nofenci.all")
dict_list = []
keys = []
for line in tqdm(res_data_new):
    Q, A = get_QA(line)
    key = utils_file.do_generate_random_num(20)
    while key in keys:
        key = utils_file.do_generate_random_num(20)
    keys.append(key)
    dict_i = {"key": key, "Q": Q, "A": A}
    dict_list.append(dict_i)
utils_file.write_dict_list_to_jsonl(dict_list, "./xiaohuangji50w_nofenci.josnl")


