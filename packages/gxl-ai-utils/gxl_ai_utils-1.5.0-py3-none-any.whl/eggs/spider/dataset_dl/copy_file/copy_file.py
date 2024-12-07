import os.path

from gxl_ai_utils.utils import utils_file


def copy_file():
    source_dir = "/mnt/disk1/yhdai/data_zipformer/batch03"
    output_dir = "/mnt/tencent/mnt/disk1/yhdai/data_zipformer/batch03"
    file_names_list = [
        'ximalaya_shenghuo_2.tar.gz',
        "wjtian_xmly2T_xuanyi_925h.tar.gz",
        "wjtian_xmly2T_renwen_3038h.tar.gz",
        "wjtian_lishi_2500h.tar.gz",
        "ximalaya_lishi_10T-1.tar.gz",
        "ximalaya_lishi_10T-0.tar.gz",
        "ximalaya_redian_2T.tar.gz",
        "zhguo_xmly2T_child_1350h.tar.gz",
    ]
    res_list = []
    for file_name in file_names_list:
        utils_file.logging_print(f'handling {file_name}')
        source_file_path_i = os.path.join(source_dir, file_name)
        output_file_path_i = os.path.join(output_dir, file_name)
        command_str = f'my_cp {source_file_path_i} {output_file_path_i}'
        res_list.append(command_str)
    utils_file.write_list_to_file(res_list, './run.sh')
if __name__ == '__main__':
    copy_file()