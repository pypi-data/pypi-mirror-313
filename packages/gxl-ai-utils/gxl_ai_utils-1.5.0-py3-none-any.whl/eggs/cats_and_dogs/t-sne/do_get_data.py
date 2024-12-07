import codecs
import os

import numpy as np

from gxl_ai_utils.utils.utils_data import logging_print

from gxl_ai_utils.utils import utils_file

input_data_dir = "/home/work_nfs8/xlgeng/new_workspace/MLS2T_LLM/baseline_version/wenet_MLS2T_LLM/examples/mllibrispeech/salmonn/gxl_res"
input_total_res_path = "/home/work_nfs8/xlgeng/new_workspace/MLS2T_LLM/baseline_version/wenet_MLS2T_LLM/examples/mllibrispeech/salmonn/gxl_res/total_mean_res.scp"
res_total_item_list = []

def do_convert_str_to_float_list(str_list: str):
    """
    将字符串转换为float列表
    :param str_list:
    :return:
    """
    import ast
    # 使用ast.literal_eval将字符串转换为Python列表
    list_obj = ast.literal_eval(str_list)
    return list_obj

total_label_list = []
total_feature_list = []
def little_func(i):
    input_data_scp_path = os.path.join(input_data_dir, f"res_{i}.scp")
    line_num = 0
    label_list = []
    feature_list = []
    with open(input_data_scp_path, 'r') as f:
        for line in f:
            line = line.strip()
            items = line.split(f", device='cuda:0') ")
            label = items[0]
            label = int(label[-2]) - 1
            print(label)
            float_list = do_convert_str_to_float_list(items[1])
            print(len(float_list))
            float_array = np.array(float_list)
            float_array_mean = np.mean(float_array, axis=0)
            print(float_array_mean.shape)
            label_list.append(label)
            feature_list.append(float_array_mean)
            line_num += 1
            if line_num > 100:
                break
    total_label_list.extend(label_list)
    total_feature_list.extend(feature_list)
    label_list_array = np.array(label_list)
    feature_list_array = np.vstack(feature_list)
    print('-------- --------')
    print(label_list_array.shape)
    print(feature_list_array.shape)
    np.save(f'./label_{i}.npy', label_list_array)
    np.save(f'./feature_{i}.npy', feature_list_array)
    feature_list_array2 = np.load(f'./feature_{i}.npy')
    label_list_array2 = np.load(f'./label_{i}.npy')
    print(label_list_array2.shape)
    print(feature_list_array2.shape)

def main():
    runner = utils_file.GxlDynamicThreadPool()
    for i in range(8):
        """"""
        runner.add_task(little_func, [i])
    runner.start()

    total_label_list_array = np.array(total_label_list)
    total_feature_list_array = np.vstack(total_feature_list)
    print(total_label_list_array.shape)
    print(total_feature_list_array.shape)
    np.save(f'./total_label.npy', total_label_list_array)
    np.save(f'./total_feature.npy', total_feature_list_array)


# item_list = utils_file.do_load_item_list_from_scp(input_total_res_path)

def do_test_data():
    input_npy_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/t-sne/total_label.npy"
    label_list = np.load(input_npy_path)
    the_dict = {}
    for item in label_list:
        if item in the_dict:
            the_dict[item] += 1
        else:
            the_dict[item] = 1
    print(the_dict)

if __name__ == '__main__':
    # main()
    do_test_data()