import ast
import random
from gxl_ai_utils.utils import utils_file
from matplotlib import pyplot as plt

from Gxl2DTable import Gxl2DTable
if __name__ == '__main__':
    # d2
    type_name='long'
    plt.rcParams.update({'font.size': 15})
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_2_stage_3.xlsx",
        return_cols=True)
    common_list_d2 = info_dict["common"]
    long_list_d2 = info_dict[type_name]
    # 得到提升的百分比
    d2_long_percent_list = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in enumerate(long_list_d2)]
    print(d2_long_percent_list)

    # d1 ,,speechio5 12 22数据等待中
    # info_dict = utils_file.load_data_from_xlsx(
    #     "../xlsx_data/down_1_stage_3.xlsx",
    #     return_cols=True)
    # common_list_d1 = info_dict["common"]
    # long_list_d1 = info_dict["short"]
    # # 得到提升的百分比
    # d1_long_percent_list = [(common_list_d1[i] - item) / common_list_d1[i] * 100 for i, item in
    #                          enumerate(long_list_d1)]
    # print(d1_long_percent_list)


    # d4
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_4_stage_3.xlsx",
        return_cols=True)
    common_list_d4 = info_dict["common"]
    long_list_d4 = info_dict[type_name]
    # 得到提升的百分比
    d4_long_percent_list = [(common_list_d4[i] - item) / common_list_d4[i] * 100 for i, item in
                             enumerate(long_list_d4)]
    print(d4_long_percent_list)


    # d8
    info_dict = utils_file.load_data_from_xlsx(
        "../xlsx_data/down_8_stage_3.xlsx",
        return_cols=True)
    common_list_d8 = info_dict["common"]
    long_list_d8 = info_dict[type_name]
    # 得到提升的百分比
    d8_long_percent_list = [(common_list_d8[i] - item) / common_list_d8[i] * 100 for i, item in
                             enumerate(long_list_d8)]
    print(d8_long_percent_list)

    common_list = [(common_list_d2[i] - item) / common_list_d2[i] * 100 for i, item in
                             enumerate(common_list_d2)]



    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    # plt.plot(x_values, d1_long_percent_list, label='downsample-1', marker='o')
    plt.plot(x_values, d2_long_percent_list, label='downsample-2', marker='s')
    plt.plot(x_values, d4_long_percent_list, label='downsample-4', marker='^')
    plt.plot(x_values, d8_long_percent_list, label='downsample-8', marker='*')
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

    plt.grid()
    # plt.show()
    # 保存图形
    if type_name != 'messy':
        plt.savefig(f'./res/{type_name}-domain-downsample.pdf', bbox_inches='tight')
    else:
        plt.savefig('./res/long-messy-downsample.pdf', bbox_inches='tight')