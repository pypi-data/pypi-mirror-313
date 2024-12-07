from matplotlib import pyplot as plt

from gxl_ai_utils.utils import utils_file


def main():
    """
    统计喜马拉雅音频下载的数量，并绘制成柱状图
    :return:
    """
    res_dic = {}
    with open('gxl.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
            items = line.strip().split(' ')
            res_dic[items[-1].strip()] = int(items[0].strip())
    with open('gxl2.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
            items = line.strip().split(' ')
            if items[-1].strip() not in res_dic:
                res_dic[items[-1].strip()] = int(items[0].strip())
            else:
                res_dic[items[-1].strip()] = int(res_dic[items[-1].strip()]) + int(items[0].strip())
    print(res_dic)
    utils_file.write_dict_to_json(res_dic, './res.json')
    items_list = list(res_dic.items())
    items_list.sort(key=lambda x: x[1])
    print(items_list)
    x_labels = [x for x, y in items_list]
    y_labels = [y for x, y in items_list]
    print(x_labels)
    new_labels = []
    for l in x_labels:
        if len(l) > 2:
            l = l[:2] + '\n' + l[2:]
        new_labels.append(l)
    print(y_labels)
    # x = ['A', 'B', 'C', 'D', 'E']  # x轴的标签
    # y = [10, 20, 15, 25, 30]  # y轴的数值
    total = 0
    for y in y_labels:
        total += y
    # 创建一个图形对象
    fig = plt.figure()

    # 在图形对象上添加一个子图
    ax = fig.add_subplot(111)

    # 在子图上绘制柱状图
    rects = ax.bar(new_labels, y_labels, color='blue', width=0.8)

    # 在每个柱子的顶部添加数值标签
    for rect in rects:
        height = rect.get_height()  # 获取柱子的高度
        x_pos = rect.get_x() + rect.get_width() / 2  # 获取柱子的中心位置
        y_pos = height + 0.5  # 获取文本标签的纵坐标位置，偏移量为0.5
        label = f'{height:.0f}'  # 获取文本标签的内容，保留一位小数
        ax.text(x_pos, y_pos, label, ha='center', va='bottom', fontsize=12)  # 添加文本标签

    # 设置x轴和y轴的标签
    ax.set_xlabel('Category')
    ax.set_ylabel('Value/GB')

    # 设置图形的标题
    ax.set_title(f'每个目录的大小，总大小：{total}GB')

    # 保存图形为图片，格式为png，分辨率为300dpi
    fig.savefig('bar_chart.png', format='png', dpi=600)


if __name__ == '__main__':
    main()
