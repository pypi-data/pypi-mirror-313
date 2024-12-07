import numpy

from gxl_ai_utils.utils import utils_file

if __name__ == '__main__':
    str_list = utils_file.load_list_file_clean(
        'E:\gengxuelong_study\server_local_adapter\gxl_work\gxl_ai_utils\eggs\knowledge_distillation\output\paraformer\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch\\am.mvn')
    # utils_file.print_list(str_list)
    res_list = []
    for i, str in enumerate(str_list):
        if i == 4 or i == 6:
            res_list.append(str.split('<LearnRateCoef> 0')[1].strip())
    utils_file.print_list(res_list)
    mean_list_str = res_list[0]
    std_list_str = res_list[1]
    mean_list = [float(i) for i in mean_list_str[1:len(mean_list_str) - 1].split()]
    std_list = [float(i) for i in std_list_str[1:len(std_list_str) - 1].split()]
    print(mean_list)
    print(std_list)
    mean = numpy.array(mean_list)
    std = numpy.array(std_list)
    mean = -1 * mean
    std = 1.0 / std
    print(mean)
    print(std)
    dic = dict(dim=560, mean=mean, std=std)
    utils_file.write_dict_to_json(dic, './mvn.json')
