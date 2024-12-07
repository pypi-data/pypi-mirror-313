import math



def show_image_for_arrays(image_arrays, text_labels, col_num=5):
    """展示数组形式的图片"""
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    num = len(image_arrays)
    row_num = math.ceil(num / col_num)
    plt.figure(figsize=(20, 6 * row_num))
    for i in range(1, num + 1):
        plt.subplot(row_num, col_num, i)
        plt.imshow(image_arrays[i - 1])
        plt.xticks([])
        plt.yticks([])
        plt.title(text_labels[i - 1])
    plt.subplots_adjust(hspace=0, wspace=0)  # 调整子图间距
    plt.show()


def show_hist(data, bins=50):
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    """
    绘制直方图
    gxl_data:必选参数，绘图数据
    bins:直方图的长条形数目，可选项，默认为10
    facecolor:长条形的颜色
    edgecolor:长条形边框的颜色
    alpha:透明度
    """
    plt.hist(data, bins=bins, facecolor="blue", edgecolor="black", alpha=0.7)
    # 显示横轴标签
    plt.xlabel("区间")
    # 显示纵轴标签
    plt.ylabel("频数/频率")
    # 显示图标题
    plt.title("频数/频率分布直方图")
    plt.show()


def show_lines(x, y):
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    plt.plot(x, y)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    plt.show()


def show_func(func: callable, x_min=-3, x_max=3):
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    x = np.arange(x_min, x_max, 0.01)
    y = func(x)
    show_lines(x, y)
