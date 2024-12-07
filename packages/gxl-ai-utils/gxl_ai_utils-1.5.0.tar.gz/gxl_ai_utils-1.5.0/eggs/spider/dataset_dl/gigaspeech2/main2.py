import os
import random

import tqdm
import webdataset as wds
from huggingface_hub import HfFileSystem, get_token, hf_hub_url
from gxl_ai_utils.utils import utils_file


def get_url_to_wget():
    fs = HfFileSystem()
    files = [fs.resolve_path(path) for path in fs.glob("hf://datasets/speechcolab/gigaspeech2/**/train/*.tar.gz")]
    urls = [hf_hub_url(file.repo_id, file.path_in_repo, repo_type="dataset") for file in files]
    res_dict = {}
    output_path = './data/url.scp'
    for i, url in enumerate(urls):
        filename = url.split("/")[-1]
        language_name = url.split("/")[-3]
        print(url)
        print(filename)
        print(language_name)
        res_dict[f'{i}'] = f'{url} {filename} {language_name}'
    utils_file.write_dict_to_scp(res_dict, output_path)
    return res_dict


def little_func_for_download(input_res_dict, local_dir):
    for key, value in tqdm.tqdm(input_res_dict.items(), desc="download", total=len(input_res_dict)):
        url, filename, language_name = value.split()
        if language_name != 'th':
            utils_file.logging_print(f"{language_name} is not th, 跳过")
            continue
        output_dir_temp = os.path.join(local_dir, language_name)
        os.makedirs(output_dir_temp, exist_ok=True)
        output_path = os.path.join(str(output_dir_temp), filename)
        file_size_num = utils_file.get_file_size(output_path)# 单位：MB
        if os.path.exists(output_path) and file_size_num > 3*1024:
            utils_file.logging_print(f"{filename} is already downloaded, 跳过")
            continue
        os.system(f"wget {url} -O {output_path}")


if __name__ == "__main__":
    res_dict = get_url_to_wget()
    local_dir = "/home/work_nfs10/xlgeng/data/gigaspeech2/train"
    os.makedirs(local_dir, exist_ok=True)
    thread = 10
    items_list = list(res_dict.items())
    random.shuffle(items_list)
    new_res_dict = {key: value for key, value in items_list}
    res_dict_list = utils_file.do_split_dict(new_res_dict, thread)
    runner = utils_file.GxlDynamicProcessPool()
    for res_dict_i in res_dict_list:
        runner.add_thread(little_func_for_download, [res_dict_i, local_dir])
    runner.run()


