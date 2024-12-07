from gxl_ai_utils.utils import utils_file
input_dir_path, output_list_file_path, suffix, recursion = utils_file.do_get_commandline_param(4)
recursion_bool = recursion=="true" or recursion=="True" or recursion=="1"
file_path_list = utils_file.do_get_list_for_wav_dir(input_dir_path,suffix=suffix,recursive=recursion_bool)
utils_file.write_list_to_file(file_path_list,output_list_file_path)
print(f'get list from dir finish, list len: {len(file_path_list)}')
