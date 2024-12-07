import os.path

from gxl_ai_utils.utils import utils_file

def fun_little(path_list, output_dir):
    """"""
    for path in utils_file.tqdm(path_list, total=len(path_list)):
        output_path = utils_file.do_replace_dir(path, output_dir)
        utils_file.copy_file(path, output_path, use_shell=True)


def copy_speechio():
    """"""
    input_dir_path = "/home/work_nfs8/xlgeng/data/scp_test"
    output_dir_path = "/home/work_nfs15/xlgeng/data/scp_test"
    dir_path_list, file_path_list = utils_file.do_listdir(input_dir_path)
    for dir_path in dir_path_list:
        if "speechio" not in dir_path:
            utils_file.logging_print(f'handle {dir_path}')
            new_speechio_dir_path = utils_file.do_replace_dir(dir_path, output_dir_path)
            utils_file.makedir(new_speechio_dir_path)
            dir_path_list_i, file_path_list_i = utils_file.do_listdir(dir_path)
            fun_little(file_path_list_i, new_speechio_dir_path)
            old_wav_dir = utils_file.join_path(dir_path, "wav")
            new_wav_dir = utils_file.join_path(new_speechio_dir_path, "wav")
            utils_file.makedir(new_wav_dir)
            _, wav_path_i = utils_file.do_listdir(old_wav_dir)
            num_thread = 18
            runner = utils_file.GxlDynamicThreadPool()
            list_list = utils_file.do_split_list(wav_path_i, num_thread)
            for list_i in list_list:
                runner.add_thread(fun_little, [list_i, new_wav_dir])
            runner.start()

def get_scp_speechio():
    input_dir = "/home/work_nfs15/xlgeng/data/scp_test"
    dir_path_list, file_path_list = utils_file.do_listdir(input_dir)
    for dir_path in dir_path_list:
        if "speechio" in dir_path:
            utils_file.logging_print(f"handle {dir_path}")
            wav_scp_path = utils_file.join_path(dir_path, "wav.scp")
            data_list_path = utils_file.join_path(dir_path, "data.list")
            text_path = utils_file.join_path(dir_path, "text")
            utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_path,text_path,data_list_path)




if __name__ == '__main__':
    get_scp_speechio()
