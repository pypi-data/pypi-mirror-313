import tqdm

from gxl_ai_utils.utils import utils_file
"""
从jsonl中提取问题的text.scp
"""
full_jsonl_path = "/home/node54_tmpdata/xlgeng/chat_data/gxl_all_chat_text.jsonl"
dict_list = utils_file.load_dict_list_from_jsonl(full_jsonl_path)
test_text_scp_path = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/text"
test_dict = utils_file.load_dict_from_scp(test_text_scp_path)
new_test_dict = {}
for key, value in test_dict.items():
    new_key = key.replace(".mp3","")
    new_test_dict[new_key] = value

res_question_dict = {}
for item in tqdm.tqdm(dict_list, desc='processing', total=len(dict_list)):
    key = item['key']
    if key in new_test_dict:
        key_with_mp3 = key + ".mp3"
        res_question_dict[key_with_mp3] = item['Q']

output_file = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/text_Q"
utils_file.write_dict_to_scp(res_question_dict, output_file)