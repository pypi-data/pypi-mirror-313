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
    messy_list = data_dict["messy"]
    short_messy_list = []
    # for item in common_list:
    #     random_float = random.randint(990,1010)/1000
    #     short_messy_list.append(item*random_float)
    dict_str = "{'speechio_8': 7.77, 'speechio_25': 6.04, 'speechio_10': 4.27, 'speechio_16': 6.27, 'speechio_0': 2.96, 'speechio_6': 9.92, 'speechio_11': 2.98, 'speechio_24': 8.29, 'speechio_5': 3.03, 'speechio_3': 2.27, 'speechio_7': 10.01, 'speechio_2': 3.68, 'speechio_14': 6.86, 'speechio_1': 1.35, 'speechio_21': 3.82, 'speechio_23': 4.24, 'speechio_17': 3.28, 'speechio_26': 5.26, 'speechio_18': 4.42, 'speechio_4': 3.3, 'speechio_19': 5.18, 'speechio_12': 4.2, 'speechio_13': 4.92, 'speechio_15': 9.93, 'speechio_22': 6.73, 'speechio_20': 2.69, 'speechio_9': 4.36}"
    dict_obj = ast.literal_eval(dict_str)
    # 输出结果
    print(dict_obj)
    print(type(dict_obj))
    for i in range(27):
        key = f'speechio_{i}'
        short_messy_list.append(dict_obj[key])
    print(short_messy_list)
    data_dict["short_messy"] = short_messy_list
    utils_file.write_dict_to_xlsx(data_dict, "./xlsx_data/d2s3_whith_short_messy.xlsx", cols_pattern=True)
    # 得到提升的百分比
    messy_percent_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(messy_list)]
    short_messy_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(short_messy_list)]
    common_messy_list = [ (common_list[i]-item) / common_list[i]*100 for i, item in enumerate(common_list)]
    # X轴的值
    x_values = list(range(27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, messy_percent_list, label='long-messy', marker='o')
    plt.plot(x_values, short_messy_list, label='short-messy', marker='s')
    plt.plot(x_values, common_messy_list, label='common', marker='^')

    # 添加标题和标签
    # plt.title('Performance improvement percentage of messy prompts compared to common prompt.')
    plt.xlabel('Index (speechio_*)',)
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
    plt.savefig('./res/long_short_messy.pdf', bbox_inches='tight')