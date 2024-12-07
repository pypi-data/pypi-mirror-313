from gxl_ai_utils.utils import utils_file
res_dict = {}
output_path = "data/desc_paths.txt"
lines = utils_file.load_list_file_clean(output_path)
lines = [item for item in lines if len(item) > 0]
for i in range(27):
    key = f'speechio_{i}'
    res_dict[key] = lines[i]

utils_file.write_dict_to_scp(res_dict, "data/desc.scp")



