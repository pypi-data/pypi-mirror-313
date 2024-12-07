from gxl_ai_utils.utils import utils_file
import os


def get_data_from_first_dir(input_dir_path, res_dict):
    dataset_name_list = os.listdir(input_dir_path)
    for dataset_name in dataset_name_list:
        temp_wer_path = os.path.join(input_dir_path, dataset_name, "wer")
        if not os.path.exists(temp_wer_path):
            utils_file.logging_print(f'{temp_wer_path} not exists, not handle it')
            continue
        if not "speechio" in dataset_name:
            utils_file.logging_print(f'{dataset_name} not speechio, not handle it')
            continue
        wer_num = utils_file.get_wer_from_wer_file(temp_wer_path)
        res_dict[dataset_name] = wer_num
    print(res_dict)
    print(list(res_dict.values()))
#
# if __name__ == '__main__':
#     info_dict = utils_file.load_data_from_xlsx("/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn/vision_4_prompt_task/tongyi_fenxi/down2_stage3__version2/data/wer_paths2.xlsx", return_cols=False)
#     # for common
#     for i in range(27):
#         key = f"speechio_{i}"
#         common_wer_path = info_dict[key][0]
#         print(common_wer_path)
#         res_wer = utils_file.get_wer_all_from_wer_file(common_wer_path)
#     # get_data_from_first_dir("./", res_dict={})


def get_all_parttern_from_root_dir(root_dir,pt_name, down_num=4, stage=2):
    """"""
    # root_dir = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v16/5_epoch"
    dir_path_list, _ = utils_file.do_listdir(root_dir)
    pattern_list = [
        "common",
        "short",
        "long",
        # "repeat",
        # "encourage",
        # "messy"
    ]
    dataset_list = [f"speechio_{i}" for i in range(27)]
    final_res_dict = {"类型/数据集": dataset_list}
    for pattern in pattern_list:
        print(pattern)
        res_dict4pattern = {}
        for dir_path in dir_path_list:
            print(dir_path)
            if not pt_name in dir_path:
                utils_file.logging_print(f'{dir_path} not {pt_name}, not handle it')
                continue
            if pattern in dir_path:
                get_data_from_first_dir(dir_path, res_dict4pattern)
            else:
                utils_file.logging_print(f'{pattern} not {dir_path}, not handle it')
                continue
        res_list = []
        for dataset in dataset_list:
            if dataset in res_dict4pattern:
                res_list.append(res_dict4pattern[dataset])
            else:
                res_list.append(-1)
        final_res_dict[pattern] = res_list
    utils_file.write_dict_to_json(final_res_dict, f"./xlsx_data/down_{down_num}_stage_{stage}.json")
    utils_file.write_dict_to_xlsx(final_res_dict, f"./xlsx_data/down_{down_num}_stage_{stage}.xlsx")


if __name__ == '__main__':
    # root_dir = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v16/5_epoch"
    # down_num = 4
    # stage_num = 3
    # pt_name= "epoch_0"
    # root_dir = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v16/3_epoch/test_step_29988/speechio"
    # down_num = 4
    # stage_num = 2
    # pt_name = "step_29988"
    # get_all_parttern_from_root_dir(root_dir,pt_name, down_num, stage_num)
    root_dir = "/home/work_nfs15/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v17/5_epoch/test_epoch_0/speechio"
    down_num = 8
    stage_num = 3
    pt_name = "epoch_0"
    get_all_parttern_from_root_dir(root_dir,pt_name, down_num, stage_num)

