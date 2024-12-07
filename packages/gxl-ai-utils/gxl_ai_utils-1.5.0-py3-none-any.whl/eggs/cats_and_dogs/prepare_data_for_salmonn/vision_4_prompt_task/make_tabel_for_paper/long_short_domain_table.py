import ast
import random
from gxl_ai_utils.utils import utils_file
from matplotlib import pyplot as plt

from Gxl2DTable import Gxl2DTable
if __name__ == '__main__':
    plt.rcParams.update({'font.size': 15})
    wer_info_table = Gxl2DTable.load_from_xlsx(
        "../xlsx_data/down_2_stage_3.xlsx",
        return_cols=True)
    data_dict = wer_info_table.dict_info
    common_list = data_dict["common"]
    short_domain_list = data_dict["short"]
    long_domain_list = data_dict["long"]
    short_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(short_domain_list)]
    long_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(long_domain_list)]
    common_messy_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(common_list)]
    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, long_list, label='long-domain', marker='o')
    plt.plot(x_values, short_list, label='short-domain', marker='s')
    plt.plot(x_values, common_messy_list, label='common', marker='^')

    # 添加标题和标签
    # plt.title('Performance improvement percentage of domain prompts compared to common prompt.')
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
    plt.savefig('./res/long_short_domain.pdf', bbox_inches='tight')


def amin():
    plt.rcParams.update({'font.size': 15})
    info_dict = utils_file.load_data_from_xlsx("../tongyi_fenxi/down2_stage3__version2/data/wer_paths2.xlsx", return_cols=False)
    # for common
    common_list = []
    type_index = 1# 2 delete, 3 insert
    for i in range(27):
        key = f"speechio_{i}"
        common_wer_path = info_dict[key][0]
        print(common_wer_path)
        res_wer = utils_file.get_wer_all_from_wer_file(common_wer_path)
        print(res_wer)
        replace_num = int(res_wer[type_index])
        common_list.append(replace_num)
    short_list = []
    for i in range(27):
        key = f"speechio_{i}"
        common_wer_path = info_dict[key][1]
        print(common_wer_path)
        res_wer = utils_file.get_wer_all_from_wer_file(common_wer_path)
        print(res_wer)
        replace_num = int(res_wer[type_index])# 2: delete 3: insert
        short_list.append(replace_num)
    long_list = []
    for i in range(27):
        key = f"speechio_{i}"
        common_wer_path = info_dict[key][2]
        print(common_wer_path)
        res_wer = utils_file.get_wer_all_from_wer_file(common_wer_path)
        print(res_wer)
        replace_num = int(res_wer[type_index])
        long_list.append(replace_num)

    # 得到提升的百分比
    messy_percent_list = [(common_list[i] - item) / common_list[i] * 100 for i, item in enumerate(long_list)]
    short_messy_list = [(common_list[i] - item) / common_list[i] * 100 for i, item in enumerate(short_list)]
    common_messy_list = [(common_list[i] - item) / common_list[i] * 100 for i, item in enumerate(common_list)]
    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, messy_percent_list, label='long-domain', marker='o')
    plt.plot(x_values, short_messy_list, label='short-domain', marker='s')
    plt.plot(x_values, common_messy_list, label='common', marker='^')

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
    plt.savefig('./res/long_short_domain_replace_errs.pdf', bbox_inches='tight')