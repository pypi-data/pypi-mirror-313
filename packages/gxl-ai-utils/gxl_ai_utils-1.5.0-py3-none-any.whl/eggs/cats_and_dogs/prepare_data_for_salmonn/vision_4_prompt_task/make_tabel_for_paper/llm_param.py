import ast
import random
from gxl_ai_utils.utils import utils_file
from matplotlib import pyplot as plt

from Gxl2DTable import Gxl2DTable
def main_1():
    plt.rcParams.update({'font.size': 15})
    # d2
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_2_stage_3.xlsx",
        return_cols=True)
    common_list_d2 = info_dict["common"]
    long_list_d2 = info_dict["messy"]
    # 得到提升的百分比
    d2s3 = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in enumerate(long_list_d2)]


    # d2s2
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_2_stage_2.xlsx",
        return_cols=True)
    common_list_d2 = info_dict["common"]
    long_list_d2 = info_dict["messy"]
    # 得到提升的百分比
    d2s2 = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in enumerate(long_list_d2)]

    common_list = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in
                             enumerate(common_list_d2)]


    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    # plt.plot(x_values, d1_long_percent_list, label='downsample-1', marker='o')
    plt.plot(x_values, d2s3, label='with', marker='s')
    plt.plot(x_values, d2s2, label='without', marker='^')
    plt.plot(x_values, common_list, label='common', marker='x')

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
    plt.show()
    # 保存图形
    # plt.savefig('./res/llm_param_messy.pdf', bbox_inches='tight')

def main_2():
    plt.rcParams.update({'font.size': 15})
    # d2
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_2_stage_3.xlsx",
        return_cols=True)
    common_list_d2 = info_dict["common"]
    long_list_d2 = info_dict["short"]
    # 得到提升的百分比
    d2s3 = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in enumerate(long_list_d2)]


    # d2s2
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_2_stage_2.xlsx",
        return_cols=True)
    common_list_d2 = info_dict["common"]
    long_list_d2 = info_dict["short"]
    # 得到提升的百分比
    d2s2 = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in enumerate(long_list_d2)]

    common_list = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in
                             enumerate(common_list_d2)]


    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    # plt.plot(x_values, d1_long_percent_list, label='downsample-1', marker='o')
    plt.plot(x_values, d2s3, label='with', marker='s')
    plt.plot(x_values, d2s2, label='without', marker='^')
    plt.plot(x_values, common_list, label='common', marker='x')

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
    plt.savefig('./res/llm_param_short.pdf', bbox_inches='tight')

if __name__ == '__main__':
    main_2()