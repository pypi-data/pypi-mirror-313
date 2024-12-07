from gxl_ai_utils.utils import utils_file
from matplotlib import pyplot as plt

def main_first_10():
    """
    12 icl lack,, 11 icl_label fake: "speechio_11": 24.24,
    :return:
    """
    plt.rcParams.update({'font.size': 15})
    data_dict = utils_file.load_dict_from_json('./json_data/first_10_res_dict.json')
    common_list = []
    icl_list = []
    icl_with_label_list = []
    for i in range(27):
        key = f'speechio_{i}'
        common_list.append(data_dict['common'][key])
        icl_list.append(data_dict['icl'][key])
        icl_with_label_list.append(data_dict['icl_with_label'][key])
    first_10_common = common_list
    fisrt_10_icl = icl_list
    fisrt_10_icl_label = icl_with_label_list
    first_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                            enumerate(fisrt_10_icl)]
    first_10_icl_label_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                                  enumerate(fisrt_10_icl_label)]
    print(first_10_icl_percent)
    print(first_10_icl_label_percent)
    common_list = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(first_10_common)]
    print(common_list)

    # X轴的值
    x_values = list(range(0, 27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, first_10_icl_label_percent, label='with-label', marker='o')
    plt.plot(x_values, first_10_icl_percent, label='without-label', marker='^')
    plt.plot(x_values, common_list, label='common', marker='x')

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
    plt.savefig('./res/icl_label.pdf', bbox_inches='tight')

def main_random_10():
    """
    12 icl lack,, random2
    11 12 icl lack random1
    :return:
    """
    plt.rcParams.update({'font.size': 15})
    data_dict = utils_file.load_dict_from_json('./json_data/random10_res_dict.json')
    data_dict2 = utils_file.load_dict_from_json('./json_data/random10-2_res_dict.json')
    data_dict3 = utils_file.load_dict_from_json('./json_data/first_10_res_dict.json')
    common_list = []
    icl_list = []
    icl_list_2 = []
    common_list_2 = []
    icl_list_3 = []
    common_list_3 = []
    # icl_with_label_list = []
    for i in range(27):
        key = f'speechio_{i}'
        common_list.append(data_dict['common'][key])
        icl_list.append(data_dict['icl'][key])
        icl_list_2.append(data_dict2['icl'][key])
        common_list_2.append(data_dict2['common'][key])
        icl_list_3.append(data_dict3['icl'][key])
        common_list_3.append(data_dict3['common'][key])
    first_10_common = common_list
    fisrt_10_icl = icl_list
    # fisrt_10_icl_label = icl_with_label_list
    first_10_icl_percent = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in
                            enumerate(fisrt_10_icl)]
    icl_2_percent = [(common_list_2[i] - item) / common_list_2[i] * 100 for i, item in enumerate(icl_list_2)]
    icl_3_percent = [(common_list_3[i] - item) / common_list_3[i] * 100 for i, item in enumerate(icl_list_3)]
    print(first_10_icl_percent)
    print(icl_2_percent)
    # print(first_10_icl_label_percent)
    common_list = [(first_10_common[i] - item) / first_10_common[i] * 100 for i, item in enumerate(first_10_common)]
    print(common_list)

    # X轴的值
    x_values = list(range(0, 27))

    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, icl_2_percent, label='random-10-2', marker='o')
    plt.plot(x_values, first_10_icl_percent, label='random-10', marker='^')
    plt.plot(x_values, icl_3_percent, label='first-10', marker='s')
    plt.plot(x_values, common_list, label='common', marker='x')

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
    plt.savefig('./res/icl_no_label.pdf', bbox_inches='tight')
if __name__ == '__main__':
    main_first_10()
    main_random_10()