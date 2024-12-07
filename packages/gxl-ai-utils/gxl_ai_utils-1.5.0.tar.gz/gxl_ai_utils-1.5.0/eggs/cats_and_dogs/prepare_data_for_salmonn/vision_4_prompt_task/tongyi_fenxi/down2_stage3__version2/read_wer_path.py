import os

from gxl_ai_utils.utils import utils_file


def read_wer_path():
    """"""
    # down4stage2
    d = 8
    s = 3
    output_dir = f"./data/wer_paths_store_d{d}s{s}"
    wer_path_dir = "/home/work_nfs15/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v17/5_epoch/test_epoch_0/speechio"
    types, _ = utils_file.do_listdir(wer_path_dir, return_path=False)
    types_dict = {item.replace('_prompt', ''): os.path.join(wer_path_dir, item) for item in types}
    print(types_dict)
    type_list = ['common', 'short', 'long', 'repeat', 'messy', 'encourage']
    res_dict = {"speechio": type_list}
    for i in range(27):
        dataset_name = 'speechio_' + str(i)
        res_dict[dataset_name] = []
        for type_i in type_list:
            wer_dir_i = types_dict[type_i]
            wer_path_i = os.path.join(wer_dir_i, dataset_name, 'wer')
            output_wer_path_i = os.path.join(output_dir, type_i, dataset_name, 'wer.txt')
            utils_file.makedir_for_file(output_wer_path_i)
            utils_file.copy_file(wer_path_i, output_wer_path_i, use_shell=True)
            if os.path.exists(wer_path_i):
                res_dict[dataset_name].append(output_wer_path_i)
    utils_file.write_dict_to_json(res_dict, f"./data/wer_path_d{d}s{s}.json")
    utils_file.write_dict_to_xlsx(res_dict, f"./data/wer_paths_d{d}s{s}.xlsx", cols_pattern=False)


def read_wer_path_2():
    # down4stage3
    wer_path_dir = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v16/5_epoch"
    output_dir = "./data/wer_paths_store_d4s3"
    type_list = ['common', 'short', 'long', 'repeat', 'messy', 'encourage']
    res_dict = {"speechio": type_list}
    for i in range(27):
        key = f'speechio_{i}'
        res_dict[key] = []
    child_dir_path_list, _ = utils_file.do_listdir(wer_path_dir)
    for type_i in type_list:
        for child_dir_path in child_dir_path_list:
            if not child_dir_path.endswith('/'):
                child_dir_path = child_dir_path + '/'
            if f"{type_i}" in child_dir_path and "test_epoch_0" in child_dir_path:
                speechio_dir_list, _ = utils_file.do_listdir(child_dir_path)
                for i in range(27):
                    key = f'speechio_{i}'
                    for speechio_dir_i in speechio_dir_list:
                        if not speechio_dir_i.endswith('/'):
                            speechio_dir_i = speechio_dir_i + '/'
                        if f'{key}/' in speechio_dir_i:
                            wer_path_i = os.path.join(speechio_dir_i, 'wer')
                            output_wer_path_i = os.path.join(output_dir, type_i, key, 'wer.txt')
                            utils_file.makedir_for_file(output_wer_path_i)
                            utils_file.copy_file(wer_path_i, output_wer_path_i, use_shell=True)
                            if os.path.exists(wer_path_i):
                                res_dict[key].append(output_wer_path_i)

    utils_file.write_dict_to_json(res_dict, "./data/wer_path_d4s3.json")


if __name__ == '__main__':
    read_wer_path()

