import os

import tqdm

from gxl_ai_utils.utils import utils_file


def split_wav_little_func(big_wav_dict, row_wav_dict, language, split_wav_dir, split_scp_dir):
    print('进入split_wav_little_func')
    res_wav_dict = {}
    res_text_dict = {}
    res_duration_dict = {}
    total_wav_num = len(row_wav_dict)
    i = 0
    for aid, source_wav_path in row_wav_dict.items():
        """"""
        try:
            input_audio_dict = big_wav_dict[aid]
            utils_file.logging_print(f'{language} wav schedule {i}/{total_wav_num}')
            if not os.path.exists(source_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 不存在,没下载, 跳过')
                continue
            finish_file_path = source_wav_path.replace(".mp3", ".split.finish")
            if os.path.exists(finish_file_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 已经完成, 跳过')
                continue
            utils_file.logging_print('开始处理：', source_wav_path)
            normal_wav_path = source_wav_path.replace(".mp3", "_normal.wav")
            if not os.path.exists(normal_wav_path):
                utils_file.do_normalization(source_wav_path, normal_wav_path)
            else:
                utils_file.logging_print(f'normal file存在,跳过normal步骤')
            segment_list = input_audio_dict['segments']
            total_seg = len(segment_list)
            for j, segment_info_dict in enumerate(segment_list):
                utils_file.logging_print(f'wav schedule {i}/{total_wav_num}, segment schedule: {j + 1}/{total_seg}')
                sid = segment_info_dict["sid"]
                sid_name = sid + ".wav"
                begin_time = segment_info_dict["begin_time"]
                begin_time = float(begin_time)
                end_time = segment_info_dict["end_time"]
                end_time = float(end_time)
                text = segment_info_dict["text_tn"]
                utils_file.logging_print(f'{sid} {begin_time} {end_time} {text}')
                seg_wav_path = os.path.join(split_wav_dir, sid_name)
                sample_rate = 16000
                utils_file.do_extract_audio_segment(normal_wav_path, seg_wav_path, int(begin_time * sample_rate),
                                                    int(end_time * sample_rate))
                res_wav_dict[sid] = seg_wav_path
                res_text_dict[sid] = text
                res_duration_dict[sid] = end_time - begin_time
            utils_file.remove_file(normal_wav_path)
            utils_file.write_list_to_file([],finish_file_path)
        except Exception as e:
            utils_file.logging_print(f'{e}')
        i += 1
    utils_file.write_dict_to_scp(res_wav_dict, os.path.join(split_scp_dir, 'wav.scp'))
    utils_file.write_dict_to_scp(res_text_dict, os.path.join(split_scp_dir, 'text'))
    utils_file.write_dict_to_scp(res_duration_dict, os.path.join(split_scp_dir, 'duration.scp'))
def split_wav(language, wav_dict_list):
    """"""
    split_wav_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_wav_new/{language}"
    split_scp_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_scp_new/{language}"
    utils_file.makedir(split_wav_dir)
    utils_file.makedir(split_scp_dir)

    original_wav_dict_path = os.path.join(split_scp_dir, 'origin_wav.scp')
    row_wav_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    row_dir_language = os.path.join(row_wav_dir, language)
    row_wav_dict = utils_file.do_get_scp_for_wav_dir(row_dir_language, suffix='.mp3')
    utils_file.write_dict_to_scp(row_wav_dict, original_wav_dict_path)
    utils_file.logging_print(f"{language}:  now original_wav num: {len(row_wav_dict)}, should original_wav num: {len(wav_dict_list)}")
    big_wav_dict = {}
    for dict_item in tqdm.tqdm(wav_dict_list, desc=f"{language}_big_dict", total=len(wav_dict_list)):
        big_wav_dict[dict_item['aid']] = dict_item

    num_thread = 32
    runner = utils_file.GxlDynamicProcessPool()
    row_wav_dict_list = utils_file.do_split_dict(row_wav_dict, num_thread)
    index = 0
    for row_wav_dict_i in row_wav_dict_list:
        split_scp_dir_i = os.path.join(split_scp_dir, f'split_{index}')
        split_wav_dir_i = os.path.join(split_wav_dir, f'split_{index}')
        utils_file.makedir(split_scp_dir_i)
        utils_file.makedir(split_wav_dir_i)
        runner.add_task(split_wav_little_func, [big_wav_dict, row_wav_dict_i, language, split_wav_dir_i, split_scp_dir_i])
        index += 1
    runner.run()


def main():
    """"""
    root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    utils_file.makedir(root_dir)
    language = "Thai"
    utils_file.logging_print(language)
    input_json_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K"
    input_json_dir_language = os.path.join(input_json_dir, language)
    dev_json_path = os.path.join(input_json_dir_language, 'dev.json')
    train_json_path = os.path.join(input_json_dir_language, 'train.json')
    if not os.path.exists(dev_json_path) or not os.path.exists(train_json_path):
        utils_file.logging_print(f'{language} 不存在dev.json或train.json')
        return
    dev_json_dict = utils_file.load_dict_from_json(dev_json_path)
    train_json_dict = utils_file.load_dict_from_json(train_json_path)
    wav_dict_list = dev_json_dict['audios'] + train_json_dict['audios']
    split_wav(language, wav_dict_list)

if __name__ == '__main__':
    main()