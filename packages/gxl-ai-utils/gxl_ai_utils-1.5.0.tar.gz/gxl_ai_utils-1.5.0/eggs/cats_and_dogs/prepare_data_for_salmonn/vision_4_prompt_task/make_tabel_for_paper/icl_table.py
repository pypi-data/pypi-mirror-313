import ast
import random
from gxl_ai_utils.utils import utils_file
from matplotlib import pyplot as plt

from Gxl2DTable import Gxl2DTable
import numpy as np
def main_1():
    plt.rcParams.update({'font.size': 15})
    icl_info_dict = utils_file.load_data_from_xlsx("./xlsx_data/ICL.xlsx", return_cols=True)
    first_10_common = icl_info_dict["前10"]
    fisrt_10_icl = icl_info_dict["前10 icl"]
    fisrt_10_icl_label = icl_info_dict["前10 icl with inference label"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]
    fisrt_10_icl_label = [item for item in fisrt_10_icl_label if not np.isnan(item)]

    first_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(fisrt_10_icl)]
    first_10_icl_label_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(fisrt_10_icl_label)]
    print(first_10_icl_percent)
    print(first_10_icl_label_percent)

    first_10_common = icl_info_dict["random10"]
    fisrt_10_icl = icl_info_dict["random10 icl"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]

    random_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(fisrt_10_icl)]
    print(random_10_icl_percent)

    first_10_common = icl_info_dict["random10-2"]
    fisrt_10_icl = icl_info_dict["random10-2 icl"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]

    random_10_icl_percent_2 = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                             enumerate(fisrt_10_icl)]
    print(random_10_icl_percent)

    common_list = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(first_10_common)]


    # X轴的值
    x_values = list(range(17,27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    # plt.plot(x_values, first_10_icl_label_percent, label='with-label', marker='o')
    # plt.plot(x_values, random_10_icl_percent, label='random-10', marker='s')
    # plt.plot(x_values, first_10_icl_percent, label='without-label', marker='^')
    plt.plot(x_values, random_10_icl_percent_2, label='random-10-2', marker='o')
    plt.plot(x_values, random_10_icl_percent, label='random-10-1', marker='s')
    plt.plot(x_values, first_10_icl_percent, label='first-10', marker='^')
    plt.plot(x_values, common_list, label='common', marker='x')

    # plt.plot(x_values, random_10_icl_percent_2, label='random-10-2', marker='o')
    # plt.plot(x_values, random_10_icl_percent, label='random-10', marker='s')
    # plt.plot(x_values, first_10_icl_percent, label='first-10', marker='^')
    # plt.plot(x_values, common_list, label='common', marker='x')

    # 添加标题和标签
    # plt.title('Performance improvement percentage of domain prompts compared to common prompt in substitution errors.')
    plt.xlabel('Index (speechio_*)')
    plt.ylabel('Value (%)')

    # 设置X轴刻度
    plt.xticks(x_values)
    plt.xticks(rotation=45)
    # 设置X轴刻度
    plt.xticks(x_values)
    # 添加图例
    plt.legend()
    plt.subplots_adjust(left=0.10, right=0.98, bottom=0.13, top=0.98)  # 调整左右边距


    # 显示网格
    plt.grid()
    # plt.show()
    # 保存图形
    plt.savefig('./res/icl_label.pdf', bbox_inches='tight')



def main_2():
    plt.rcParams.update({'font.size': 15})
    icl_info_dict = utils_file.load_data_from_xlsx("./xlsx_data/ICL.xlsx", return_cols=True)
    first_10_common = icl_info_dict["前10"]
    fisrt_10_icl = icl_info_dict["前10 icl"]
    fisrt_10_icl_label = icl_info_dict["前10 icl with inference label"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]
    fisrt_10_icl_label = [item for item in fisrt_10_icl_label if not np.isnan(item)]

    first_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                            enumerate(fisrt_10_icl)]
    first_10_icl_label_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                                  enumerate(fisrt_10_icl_label)]
    print(first_10_icl_percent)
    print(first_10_icl_label_percent)

    first_10_common = icl_info_dict["random10"]
    fisrt_10_icl = icl_info_dict["random10 icl"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]

    random_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                             enumerate(fisrt_10_icl)]
    print(random_10_icl_percent)

    first_10_common = icl_info_dict["random10-2"]
    fisrt_10_icl = icl_info_dict["random10-2 icl"]
    first_10_common = [item for item in first_10_common if not np.isnan(item)]
    fisrt_10_icl = [item for item in fisrt_10_icl if not np.isnan(item)]

    random_10_icl_percent_2 = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                               enumerate(fisrt_10_icl)]
    print(random_10_icl_percent)

    common_list = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(first_10_common)]

    # X轴的值
    x_values = list(range(17, 27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, first_10_icl_label_percent, label='with-label', marker='o')
    plt.plot(x_values, random_10_icl_percent, label='random-10', marker='s')
    plt.plot(x_values, first_10_icl_percent, label='without-label', marker='^')
    # plt.plot(x_values, random_10_icl_percent_2, label='random-10-2', marker='o')
    # plt.plot(x_values, random_10_icl_percent, label='random-10-1', marker='s')
    # plt.plot(x_values, first_10_icl_percent, label='first-10', marker='^')
    plt.plot(x_values, common_list, label='common', marker='x')

    # plt.plot(x_values, random_10_icl_percent_2, label='random-10-2', marker='o')
    # plt.plot(x_values, random_10_icl_percent, label='random-10', marker='s')
    # plt.plot(x_values, first_10_icl_percent, label='first-10', marker='^')
    # plt.plot(x_values, common_list, label='common', marker='x')

    # 添加标题和标签
    # plt.title('Performance improvement percentage of domain prompts compared to common prompt in substitution errors.')
    plt.xlabel('Index (speechio_*)')
    plt.ylabel('Value (%)')

    # 设置X轴刻度
    plt.xticks(x_values)
    plt.xticks(rotation=45)
    # 设置X轴刻度
    plt.xticks(x_values)
    # 添加图例
    plt.legend()
    plt.subplots_adjust(left=0.10, right=0.98, bottom=0.13, top=0.98)  # 调整左右边距

    # 显示网格
    plt.grid()
    # plt.show()
    # 保存图形
    plt.savefig('./res/icl_no_label.pdf', bbox_inches='tight')
