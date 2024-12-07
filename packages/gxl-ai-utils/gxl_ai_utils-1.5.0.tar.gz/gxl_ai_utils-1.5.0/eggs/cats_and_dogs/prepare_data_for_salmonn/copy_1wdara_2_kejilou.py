from gxl_ai_utils.utils import utils_file


input_data_list_path = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/data_list/gxl_all_new_wenetspeech_fix.list"
path_list = utils_file.load_list_file_clean(input_data_list_path)

utils_file.logging_print("path_list len: {}".format(len(path_list)))
def little_func(path_list, output_root_dir):
    for path_i in utils_file.tqdm(path_list):
        """"""

