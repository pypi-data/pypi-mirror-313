import torch

from gxl_ai_utils.utils import utils_file
import pandas as pd

# 先对二倍下采用对结果进行可视化分析。表格自己得到的，主要是可视化分析
import matplotlib.pyplot as plt

from gxl_ai_utils.utils import utils_file


def get_score_dict(down, stage):
    """"""
    res1 = utils_file.load_data_from_xlsx(f'./xlsx_data/down_{down}_stage_{stage}.xlsx', return_cols=True)
    a = res1.pop("类型/数据集")
    a = [item.replace("speechio_", "") for item in a]
    print(a)
    common_list = res1['common']
    common_tensor = torch.tensor(common_list)
    res_dict = {}
    for key, value in res1.items():
        value_res = (torch.tensor(value) / common_tensor).tolist()
        print(value_res)
        res_dict[key] = value_res
    return res_dict

def get_score_dict2(input_dict):
    """"""
    # res1 = utils_file.load_data_from_xlsx(f'./xlsx_data/down_{down}_stage_{stage}.xlsx', return_cols=True)
    res1 = input_dict
    a = res1.pop("类型/数据集")
    a = [item.replace("speechio_", "") for item in a]
    print(a)
    common_list = res1['common']
    common_tensor = torch.tensor(common_list)
    res_dict = {}
    for key, value in res1.items():
        value_res = (torch.tensor(value) / common_tensor).tolist()
        print(value_res)
        res_dict[key] = value_res
    return res_dict


def do_test_1():
    dict_23 = get_score_dict(2,3)
    dict_22 = get_score_dict(2,2)
    dict_43 = get_score_dict(4,3)
    dict_42 = get_score_dict(4,2)
    dict_res = {}
    # type = "long"
    # dict_res[f'{type}_2_2'] = dict_22[type]
    # dict_res[f'{type}_4_2'] = dict_42[type]
    # dict_res['common'] = dict_22['common']
    # utils_file.plot_lines(dict_res, )
    # type = "short"
    # dict_res[f'{type}_2_2'] = dict_22[type]
    # dict_res[f'{type}_4_2'] = dict_42[type]
    # dict_res['common'] = dict_22['common']
    # utils_file.plot_lines(dict_res, )
    # type1 = "encourage"
    # type2 = "messy"
    # type3 = "repeat"
    # dict_res[f'{type1}_2_3'] = dict_23[type1]
    # dict_res[f'{type2}_2_3'] = dict_23[type2]
    # dict_res[f'{type3}_2_3'] = dict_23[type3]
    #
    # dict_res['common'] = dict_22['common']
    # utils_file.plot_lines(dict_res)
    # exit(0)

    #for dict_2_3
    dict_23 = utils_file.load_data_from_xlsx(f'./xlsx_data/down_2_stage_3.xlsx', return_cols=False)
    for key,values in dict_23.items():
        if key !="类型/数据集":
            value_new = [item/values[0] for item in values]
            dict_23[key] = value_new
    utils_file.print_dict(dict_23)
    res_list = []
    for key,values in dict_23.items():
        if key !="类型/数据集":
            if values[4]>=values[5]>=values[0]>=values[3]>=values[2]>=values[1]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key,values in dict_23.items():
        if key !="类型/数据集":
            if values[5]>=values[4]>=values[0]>=values[3]>=values[2]>=values[1]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key,values in dict_23.items():
        if key !="类型/数据集":
            if values[4]>=values[0]>=values[3]>=values[2]>=values[1]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[3] >= values[1] >= values[2]:
                res_list.append(key)
    print(res_list)
    print('------------------------------------')

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[3] and values[0] >= values[1] and values[0] >= values[2]:
                res_list.append(key)
    print(res_list)


    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[2] >= values[3] >= values[1]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[3] >= values[2] >= values[1]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[3] >= values[1] >= values[2]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[1] >= values[3] >= values[2]:
                res_list.append(key)
    print(res_list)


    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[1] >= values[2] >= values[3]:
                res_list.append(key)
    print(res_list)

    res_list = []
    for key, values in dict_23.items():
        if key != "类型/数据集":
            if values[0] >= values[2] >= values[1] >= values[3]:
                res_list.append(key)
    print(res_list)

    dict_23= utils_file.load_data_from_xlsx('./xlsx_data/down_2_stage_3.xlsx')
    x_label1 = [1,2,3,4,5,6,7,9,10,11,14,15,18,19,20,21,22,23,24]
    x_label2 = [1,4,5,18,20]
    x_label3 = [2,3,4,7,15,19,24]
    x_label4 = [6,11,22]
    x_label5 = [9,10,11,23]
    x_label6 = [8,12,13,16,17,25,26]
    for key, values in dict_23.items():
        if key != "类型/数据集":
            values_new = [values[i] for i in x_label6]
            dict_23[key] = values_new
    dict_23 = get_score_dict2(dict_23)
    utils_file.plot_lines(dict_23,x_label6, )


def do_test_2():
    dict_23 = get_score_dict(2, 3)
    dict_22 = get_score_dict(2, 2)
    dict_43 = get_score_dict(4, 3)
    dict_42 = get_score_dict(4, 2)
    dict_res = {}
    type1 = "repeat"
    type2 = "short"
    type3 = "messy"
    # dict_res[f'{type1}_4_3'] = dict_43[type1]
    dict_res[f'{type1}_2_3'] = dict_23[type1]
    dict_res[f'{type1}_2_2'] = dict_22[type1]


    dict_res['common'] = dict_23['common']
    a = list(range(24))
    # a.pop(-2)
    print(a)
    for key, values in dict_res.items():
        if key != "类型/数据集":
            values_new = [values[i] for i in a]
            dict_res[key] = values_new
    utils_file.plot_lines(dict_res,a)

if __name__ == '__main__':
    do_test_2()
    # do_test_1()