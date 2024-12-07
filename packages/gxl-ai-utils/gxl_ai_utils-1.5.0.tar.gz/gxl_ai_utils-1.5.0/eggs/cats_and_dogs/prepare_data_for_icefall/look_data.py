from gxl_ai_utils.utils import utils_file

input_jsonl_path = "/mnt/disk1/yhdai/data_zipformer/batch01/aishell1/fbank/modified_cuts_train.jsonl"
data_list = utils_file.load_dict_list_from_jsonl(input_jsonl_path)
duration = 0
for data in utils_file.tqdm(data_list, total=len(data_list)):
    duration += data["duration"]
print(duration)