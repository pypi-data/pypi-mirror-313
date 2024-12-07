import os

from gxl_ai_utils.utils import utils_file

input_train_list_path = "/home/work_nfs14/yhdai/data_shard/chattts/01/shards_list.txt"
input_cv_list_path = "/home/work_nfs14/yhdai/data_shard/chattts/cv/shards_list.txt"
output_dir = "/home/work_nfs15/xlgeng/data/data_shards/chat_wav_data"
# train
output_dir_train = os.path.join(output_dir, "train")
utils_file.makedir_sil(output_dir_train)
new_list_path = os.path.join(output_dir_train, "shards_list.txt")
path_list = utils_file.load_list_file_clean(input_train_list_path)
new_path_list = []
for path in path_list:
    new_path_i = utils_file.do_replace_dir(path, output_dir_train)
    utils_file.copy_file(path, new_path_i)
    new_path_list.append(new_path_i)
utils_file.write_list_to_file(new_path_list, new_list_path)

# cv
output_dir_train = os.path.join(output_dir, "cv")
utils_file.makedir_sil(output_dir_train)
new_list_path = os.path.join(output_dir_train, "shards_list.txt")
path_list = utils_file.load_list_file_clean(input_cv_list_path)
new_path_list = []
for path in path_list:
    new_path_i = utils_file.do_replace_dir(path, output_dir_train)
    utils_file.copy_file(path, new_path_i)
    new_path_list.append(new_path_i)
utils_file.write_list_to_file(new_path_list, new_list_path)





