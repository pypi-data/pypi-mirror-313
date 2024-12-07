import torch

from gxl_ai_utils.utils import utils_data


def do_test_namespaceObj():
    """"""
    dic = {'a': 1, 'b': 2}
    namespaceObj = utils_data.do_dict2simpleNamespaceObj(dic)
    print(namespaceObj.a)
    print(namespaceObj.b)
    # print(namespaceObj.c)
    namespaceObj.a = 'gxl'
    print(namespaceObj.a)


def do_test_tensor():
    # 创建一个示例张量
    tensor = torch.randn((10, 20, 3))
    print(tensor.shape)
    # 复制前5个时间步的内容为原来的3倍
    a_temp = tensor[:, :5, :].repeat(1, 3, 1)
    # 复制后面每个时间步的内容为原来的2倍
    b_temp = tensor[:, 5:, :].repeat(1, 2, 1)
    tensor = torch.cat([a_temp, b_temp], dim=1)
    print(tensor.shape)


if __name__ == '__main__':
    do_test_tensor()
