import os

from tqdm import tqdm

from gxl_ai_utils.utils import utils_file


def little_func(tar_file_path_list, output_dir):
    """"""
    for i, tar_path in tqdm(enumerate(tar_file_path_list), total=len(tar_file_path_list)):
        utils_file.logging_print(f"处理第 {i} 个 {tar_path}")
        utils_file.do_decompression_tar(tar_path, output_dir)



if __name__ == '__main__':
    base_url = "/home/work_nfs7/tyxu/peoples_speech"
    final_tar_dir = "/home/backup_nfs5/xlgeng/data/shard_asr/peoples_speech"
    utils_file.makedir_sil(final_tar_dir)
    raw_dir = "/home/work_nfs8/xlgeng/data/raw/peoples_speech"
    utils_file.makedir_sil(raw_dir)
    all_part = ['test', 'validation']
    for part in all_part:
        temp_part = os.path.join(base_url, part)
        utils_file.logging_print(f"开始处理如下目录 {temp_part}")
        temp_raw_dir = os.path.join(raw_dir, part)
        temp_final_tar_dir = os.path.join(final_tar_dir, part)
        # 得到所有tar_path list
        tar_path_list = utils_file.get_file_path_list_for_wav_dir(temp_part, suffix=".tar", recursive=True)
        utils_file.print_list(tar_path_list)
        num_thread = 10
        runner = utils_file.GxlFixedThreadPool(num_thread)
        # for i, tar_path in enumerate(tar_path_list):
        #     utils_file.logging_print(f"处理第 {i} 个 {tar_path}")
        #     runner.add_task(utils_file.do_decompression_tar, [tar_path, temp_raw_dir])
        # runner.start()
        tar_list_list = utils_file.do_split_list(tar_path_list, num_thread)
        for tar_list_i in tar_list_list:
            runner.add_task(little_func, [tar_list_i, temp_raw_dir])
        runner.start()

        # 得到所有flac数据scp
        utils_file.logging_print("开始得到所有flac数据scp")
        flac_scp = utils_file.get_scp_for_wav_dir(temp_raw_dir, suffix=".flac", recursive=True)
        utils_file.print_dict(flac_scp)
        flac_scp_path = os.path.join(temp_raw_dir, f"wav.scp")
        utils_file.write_dict_to_scp(flac_scp, flac_scp_path)

        utils_file.logging_print(f'得到文字信息')
        json_file_path = os.path.join(temp_part, f"{part}.json")
        json_dict_list = utils_file.load_dict_list_from_jsonl(json_file_path)
        new_simplification_dict = {}
        # utils_file.print_list(json_dict_list)
        for json_dict in json_dict_list:
            # utils_file.print_list(json_dict.keys())
            json_dict = json_dict['training_data']
            label_list = json_dict['label']
            name_list = json_dict['name']
            for label, name in zip(label_list, name_list):
                name = utils_file.get_file_pure_name_from_path(name)
                new_simplification_dict[name] = label
        utils_file.print_dict(new_simplification_dict)
        text_path = os.path.join(temp_raw_dir, f"text")
        utils_file.write_dict_to_scp(new_simplification_dict, text_path)
        utils_file.do_make_shard_file(flac_scp_path, text_path, temp_final_tar_dir)





    base_url = "/home/work_nfs7/tyxu/peoples_speech/train"
    final_tar_dir = "/home/backup_nfs5/xlgeng/data/shard_asr/peoples_speech/train"
    utils_file.makedir_sil(final_tar_dir)
    raw_dir = "/home/work_nfs8/xlgeng/data/raw/peoples_speech/train"
    utils_file.makedir_sil(raw_dir)
    # all_part = ['test', 'train', 'validation']
    all_part = ['clean', 'clean_sa', 'dirty']
    for part in all_part:
        temp_part = os.path.join(base_url, part)
        utils_file.logging_print(f"开始处理如下目录 {temp_part}")
        temp_raw_dir = os.path.join(raw_dir, part)
        temp_final_tar_dir = os.path.join(final_tar_dir, part)
        # 得到所有tar_path list
        tar_path_list = utils_file.get_file_path_list_for_wav_dir(temp_part, suffix=".tar", recursive=True)
        utils_file.print_list(tar_path_list)
        num_thread = 10
        runner = utils_file.GxlFixedThreadPool(num_thread)
        # for i, tar_path in enumerate(tar_path_list):
        #     utils_file.logging_print(f"处理第 {i} 个 {tar_path}")
        #     runner.add_task(utils_file.do_decompression_tar, [tar_path, temp_raw_dir])
        # runner.start()
        tar_list_list = utils_file.do_split_list(tar_path_list, num_thread)
        for tar_list_i in tar_list_list:
            runner.add_task(little_func, [tar_list_i, temp_raw_dir])
        runner.start()

        # 得到所有flac数据scp
        utils_file.logging_print("开始得到所有flac数据scp")
        flac_scp = utils_file.get_scp_for_wav_dir(temp_raw_dir, suffix=".flac", recursive=True)
        utils_file.print_dict(flac_scp)
        flac_scp_path = os.path.join(temp_raw_dir, f"wav.scp")
        utils_file.write_dict_to_scp(flac_scp, flac_scp_path)

        utils_file.logging_print(f'得到文字信息')
        json_file_path = os.path.join(base_url, f"{part}.json")
        json_dict_list = utils_file.load_dict_list_from_jsonl(json_file_path)
        new_simplification_dict = {}
        # utils_file.print_list(json_dict_list)
        for json_dict in json_dict_list:
            # utils_file.print_list(json_dict.keys())
            json_dict = json_dict['training_data']
            label_list = json_dict['label']
            name_list = json_dict['name']
            for label, name in zip(label_list, name_list):
                name = utils_file.get_file_pure_name_from_path(name)
                new_simplification_dict[name] = label
        utils_file.print_dict(new_simplification_dict)
        text_path = os.path.join(temp_raw_dir, f"text")
        utils_file.write_dict_to_scp(new_simplification_dict, text_path)
        utils_file.do_make_shard_file(flac_scp_path, text_path, temp_final_tar_dir)