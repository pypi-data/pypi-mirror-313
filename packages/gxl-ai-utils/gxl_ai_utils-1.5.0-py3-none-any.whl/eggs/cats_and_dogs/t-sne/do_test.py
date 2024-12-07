import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn import datasets
from sklearn.manifold import TSNE


# 加载数据
def get_data():
    """
    :return: 数据集、标签、样本数量、特征数量
    """
    digits = datasets.load_digits(n_class=10)
    data = digits.data  # 图片特征
    label = digits.target  # 图片标签
    n_samples, n_features = data.shape  # 数据集的形状
    return data, label, n_samples, n_features
def get_my_data():
    input_label_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/t-sne/total_label.npy"
    input_feature_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/t-sne/total_feature.npy"
    label = np.load(input_label_path)
    feature = np.load(input_feature_path)
    return feature, label, feature.shape[0], feature.shape[1]

# 对样本进行预处理并画图
def plot_embedding2(data, label, title):
    """
    :param data:数据集
    :param label:样本标签
    :param title:图像标题
    :return:图像
    """
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)  # 对数据进行归一化处理
    fig = plt.figure()  # 创建图形实例
    ax = plt.subplot(111)  # 创建子图
    # 遍历所有样本
    for i in range(data.shape[0]):
        # 在图中为每个数据点画出标签
        plt.text(data[i, 0], data[i, 1], str(label[i]), color=plt.cm.Set1(label[i] / 10),
                 fontdict={'weight': 'bold', 'size': 7})
    plt.xticks()  # 指定坐标的刻度
    plt.yticks()
    plt.title(title, fontsize=14)
    # 返回值
    return fig


def plot_embedding(data, label, title):
    """
    :param data: 数据集
    :param label: 样本标签
    :param title: 图像标题
    :return: 图像
    """
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)  # 对数据进行归一化处理
    fig = plt.figure()  # 创建图形实例
    ax = plt.subplot(111)  # 创建子图
    # 遍历所有样本
    for i in range(data.shape[0]):
        # 在图中为每个数据点画出圆点
        ax.scatter(data[i, 0], data[i, 1], color=plt.cm.Set1(label[i] / 10), marker='o', s=5)

    plt.xticks([])  # 隐藏x轴刻度
    plt.yticks([])  # 隐藏y轴刻度
    plt.title(title, fontsize=14)
    mls_dict = {"dutch": 0, "french": 1, "italian": 2, "portuguese": 3, "english": 4, "german": 5, "polish": 6,
                "spanish": 7}
    id_to_mls = {str(v): k for k, v in mls_dict.items()}

    # 创建边角栏
    legend_elements = []
    unique_labels = np.unique(label)
    for lbl in unique_labels:
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label=id_to_mls[str(lbl)],
                                      markerfacecolor=plt.cm.Set1(lbl / 10), markersize=8))
    ax.legend(handles=legend_elements, loc='upper right')

    # 返回值
    return fig


# 主函数，执行t-SNE降维
def main():
    data, label, n_samples, n_features = get_my_data()  # 调用函数，获取数据集信息
    print(data.shape)
    print(label.shape)
    return
    print('Starting compute t-SNE Embedding...')
    ts = TSNE(n_components=2, init='pca', random_state=0)
    # t-SNE降维
    reslut = ts.fit_transform(data)
    print(reslut.shape)
    print(label.shape)
    # 调用函数，绘制图像
    fig = plot_embedding(reslut, label, 't-SNE Embedding of Baseline Model')
    # 显示图像
    plt.savefig('./image1.png')


# 主函数
if __name__ == '__main__':
    main()
