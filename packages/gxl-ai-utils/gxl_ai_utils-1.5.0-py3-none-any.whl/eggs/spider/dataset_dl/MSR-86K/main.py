import glob
import os
import random
import subprocess

import tqdm

from gxl_ai_utils.utils import utils_file

input_json_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K"

language_name, _ = utils_file.do_listdir(input_json_dir, return_path=False)



# err_dict_path = './err.json'
# if os.path.exists(err_dict_path):
#     err_dict = utils_file.load_dict_from_json(err_dict_path)
# else:
#     err_dict = {}


def func_little4language(language, input_audio_dict_list, output_dir):
    """"""
    utils_file.makedir(output_dir)
    total_wav_num = len(input_audio_dict_list)
    for i, input_audio_dict in enumerate(input_audio_dict_list):
        try:
            utils_file.logging_print(f'{language} wav schedule {i}/{total_wav_num}')
            wav_name = input_audio_dict['aid']
            source_wav_path = os.path.join(output_dir, wav_name + '.mp3')
            if os.path.exists(source_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 已经存在, 跳过')
                continue
            utils_file.do_download_from_play_url(input_audio_dict['url'], output_dir, wav_name=wav_name, wav_type='mp3')
            # if not os.path.exists(source_wav_path):
            #     err_dict[input_audio_dict['aid']] = {'url': input_audio_dict['url'], 'output_dir': output_dir}
        except Exception as e:
            utils_file.logging_print(f'{e}')
            # err_dict[input_audio_dict['aid']] = {'url': input_audio_dict['url'], 'output_dir': output_dir}


def func_little4split_wav(language, wav_dict_list):
    """"""
    split_wav_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_wav/{language}"
    split_scp_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_scp/{language}"
    utils_file.makedir(split_wav_dir)
    utils_file.makedir(split_scp_dir)
    res_wav_dict_path = os.path.join(split_scp_dir, 'wav.scp')
    res_text_dict_path = os.path.join(split_scp_dir, 'text')
    res_duration_dict_path = os.path.join(split_scp_dir, 'duration.scp')
    original_wav_dict_path = os.path.join(split_scp_dir, 'origin_wav.scp')

    if os.path.exists(res_wav_dict_path) and os.path.exists(res_text_dict_path) and os.path.exists(
            res_duration_dict_path) and os.path.exists(original_wav_dict_path):
        res_wav_dict = utils_file.load_dict_from_json(res_wav_dict_path)
        res_text_dict = utils_file.load_dict_from_json(res_text_dict_path)
        res_duration_dict = utils_file.load_dict_from_json(res_duration_dict_path)
        row_wav_dict = utils_file.load_dict_from_json(original_wav_dict_path)
    else:
        res_wav_dict, res_text_dict, res_duration_dict, row_wav_dict = {}, {}, {}, {}

    row_wav_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    row_dir_language = os.path.join(row_wav_dir, language)
    row_wav_dict = utils_file.do_get_scp_for_wav_dir(row_dir_language, suffix='.mp3')
    utils_file.write_dict_to_scp(row_wav_dict, original_wav_dict_path)

    total_wav_num = len(wav_dict_list)
    for i, input_audio_dict in enumerate(wav_dict_list):
        try:
            now_time = utils_file.do_get_now_time()
            utils_file.logging_print(f'{language} wav schedule {i}/{total_wav_num}')
            wav_name = input_audio_dict['aid']
            source_wav_path = row_wav_dict[wav_name]
            if not os.path.exists(source_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 不存在,没下载, 跳过')
                continue
            input_wav_path = source_wav_path
            utils_file.logging_print('开始处理：', input_wav_path)

            normalization_wav_path = input_wav_path.replace('.mp3', '_normalization.wav')
            if os.path.exists(normalization_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} normalization_wav_path已经存在, 跳过')
                continue
            utils_file.logging_print('开始标准化')
            utils_file.do_normalization(input_wav_path, normalization_wav_path)
            utils_file.logging_print('开始分割')
            segment_list = input_audio_dict['segments']
            total_seg = len(segment_list)
            for i, segment_info_dict in enumerate(segment_list):
                utils_file.logging_print(f'input_wav: {input_wav_path}, segment schedule: {i + 1}/{total_seg}')
                sid = segment_info_dict["sid"]
                sid_name = sid + ".wav"
                begin_time = segment_info_dict["begin_time"]
                begin_time = float(begin_time)
                end_time = segment_info_dict["end_time"]
                end_time = float(end_time)
                text = segment_info_dict["text_tn"]
                utils_file.logging_print(f'{sid} {begin_time} {end_time} {text}')
                seg_wav_path = os.path.join(split_wav_dir, sid_name)
                utils_file.logging_print(f'实现如下切割-----{normalization_wav_path}->{seg_wav_path}-----------------')
                utils_file.do_extract_audio_segment(normalization_wav_path, seg_wav_path, int(begin_time * 16000),
                                                    int(end_time * 16000))
                utils_file.logging_print(f'切割完成')
                res_wav_dict[sid] = seg_wav_path
                res_text_dict[sid] = text
                res_duration_dict[sid] = end_time - begin_time

            utils_file.logging_print(f'处理完成，耗时{utils_file.do_get_elapsed_time(now_time)}s input_wav:',
                                     input_wav_path)
            if i % 100 == 0:
                utils_file.write_dict_to_json(res_wav_dict, res_wav_dict_path)
                utils_file.write_dict_to_json(res_text_dict, res_text_dict_path)
                utils_file.write_dict_to_json(res_duration_dict, res_duration_dict_path)

        except Exception as e:
            utils_file.logging_print(f'{e}')
            # err_dict[input_audio_dict['aid']] = {'url': input_audio_dict['url'], 'output_dir': output_dir}


def do_download():
    runner = utils_file.GxlDynamicProcessPool()
    root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    utils_file.makedir(root_dir)
    for language in language_name:
        input_json_dir_language = os.path.join(input_json_dir, language)
        dev_json_path = os.path.join(input_json_dir_language, 'dev.json')
        train_json_path = os.path.join(input_json_dir_language, 'train.json')
        if not os.path.exists(dev_json_path) or not os.path.exists(train_json_path):
            utils_file.logging_print(f'{language} 不存在dev.json或train.json')
            continue
        dev_json_dict = utils_file.load_dict_from_json(dev_json_path)
        train_json_dict = utils_file.load_dict_from_json(train_json_path)
        wav_dict_list = dev_json_dict['audios'] + train_json_dict['audios']
        random.shuffle(wav_dict_list)
        print(language, len(wav_dict_list))
        output_dir_language = os.path.join(root_dir, language)
        utils_file.makedir(output_dir_language)
        runner.add_thread(func_little4language, [language, wav_dict_list, output_dir_language])

    runner.start()
    utils_file.logging_print("完全下载完毕")


def do_split():
    """"""
    runner = utils_file.GxlDynamicThreadPool()
    root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    utils_file.makedir(root_dir)
    for language in language_name:
        utils_file.logging_print(language)
        input_json_dir_language = os.path.join(input_json_dir, language)
        dev_json_path = os.path.join(input_json_dir_language, 'dev.json')
        train_json_path = os.path.join(input_json_dir_language, 'train.json')
        if not os.path.exists(dev_json_path) or not os.path.exists(train_json_path):
            utils_file.logging_print(f'{language} 不存在dev.json或train.json')
            continue
        dev_json_dict = utils_file.load_dict_from_json(dev_json_path)
        train_json_dict = utils_file.load_dict_from_json(train_json_path)
        wav_dict_list = dev_json_dict['audios'] + train_json_dict['audios']
        random.shuffle(wav_dict_list)
        print(language, len(wav_dict_list))
        # func_little4split_wav(language,wav_dict_list)
        runner.add_thread(func_little4split_wav, [language, wav_dict_list])
    runner.start()


def get_sample_zip():
    """"""
    root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    utils_file.makedir(root_dir)
    res_dict = {}
    for language in language_name:
        """"""
        if language !="Thai":
            continue
        temp_res_dict = {}
        res_dict[language] = temp_res_dict
        split_wav_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_wav/{language}"
        split_scp_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/split_scp/{language}"
        row_wav_dir = f"/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav/{language}"

        row_wav_dict = utils_file.do_get_scp_for_wav_dir(row_wav_dir, suffix='.mp3')
        temp_res_dict['split_wav'] = {}
        wav_dict_path = utils_file.join_path(split_scp_dir, 'wav.scp')
        if not os.path.exists(wav_dict_path):
            utils_file.logging_print(f'{language} 不存在wav.scp')
            continue
        wav_split_dict = utils_file.load_dict_from_json(wav_dict_path)
        print(len(wav_split_dict))
        txt_split_dict = utils_file.load_dict_from_json(utils_file.join_path(split_scp_dir, 'text'))
        wav_num = 0
        for key, row_wav_path in tqdm.tqdm(row_wav_dict.items(), total=len(row_wav_dict)):
            """"""
            key1 = key + "_0000"
            if key1 not in wav_split_dict:
                continue
            for i in range(100):
                key_now = key + "_000" + str(i)
                if key_now in wav_split_dict:
                    print(key_now)
                    temp_res_dict['split_wav'][key_now] = {'wav': wav_split_dict[key_now],
                                                           'txt': txt_split_dict[key_now]}
            temp_res_dict['parent_path'] = row_wav_path
            wav_num += 1
            if wav_num > 10:
                break
        print(temp_res_dict)
    utils_file.write_dict_to_json(res_dict, './res_scp.json')


def handle_resp_scp():
    input_path = '/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/spider/dataset_dl/MSR-86K/res_scp.json'
    dict_json = utils_file.load_dict_from_json(input_path)
    output_dir_root = "/home/work_nfs8/xlgeng/new_workspace/checkpoint/a_meituan_data_demo"
    utils_file.makedir(output_dir_root)
    for language, info_dict in dict_json.items():
        print(language
              )
        print(info_dict)
        temp_root = utils_file.join_path(output_dir_root, language)
        utils_file.makedir(temp_root)
        if 'parent_path' not in info_dict:
            utils_file.logging_print(f'{language} 不存在parent_path')
            continue
        source_wav_path = info_dict['parent_path']
        new_source_wav_dir = utils_file.join_path(temp_root, 'source_wav')
        utils_file.makedir(new_source_wav_dir)
        if not os.path.exists(source_wav_path):
            utils_file.logging_print(f'{language} 不存在source_wav_path')
            continue
        utils_file.copy_file2(source_wav_path, new_source_wav_dir)
        split_dir_new = utils_file.join_path(temp_root, 'split_wav')
        split_wav_dict = info_dict['split_wav']
        for key, info_dict_split_i in split_wav_dict.items():
            wav_path_i = info_dict_split_i['wav']
            txt_str_i = info_dict_split_i['txt']
            new_wav_path = utils_file.join_path(split_dir_new, key + '.wav')
            new_txt_path = utils_file.join_path(split_dir_new, key + '.txt')
            utils_file.copy_file(wav_path_i, new_wav_path)
            utils_file.write_list_to_file([txt_str_i], new_txt_path)
    utils_file.copy_file2(input_path, output_dir_root)




def little_func(input_dir_path,language):
    """delete normal file and add filename.finish file"""
    file_path_list = glob.glob(os.path.join(input_dir_path, '*_normalization.wav'))
    utils_file.logging_print(f'input_dir_path:{input_dir_path}, file_num : {len(file_path_list)}')
    # utils_file.logging_print(file_path_list[0])
    for file_path in tqdm.tqdm(file_path_list, total=len(file_path_list), desc=f'handing {language}'):
        file_path_now = file_path.replace('_normalization', '')
        print(file_path_now)
        break
def remove_all_normal_long_wav():
    """"""
    input_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    language_name,_ = utils_file.do_listdir(input_dir, return_path=False)
    language_names = [item for item in language_name if item != 'output']
    utils_file.logging_print(f'language_name:{language_names}')
    runner = utils_file.GxlDynamicProcessPool()
    for language in language_names:
        input_dir_path = os.path.join(input_dir, language)
        runner.add_thread(little_func, [input_dir_path, language])
    runner.start()

if __name__ == '__main__':
    """"""
    # do_split()
    # do_download()
    remove_all_normal_long_wav()
