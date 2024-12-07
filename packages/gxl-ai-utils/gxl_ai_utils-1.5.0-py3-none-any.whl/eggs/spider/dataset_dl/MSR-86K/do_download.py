import os

from gxl_ai_utils.utils import utils_file


def func_little4language(language, wav_info_list_i, output_dir):
    """"""
    utils_file.makedir(output_dir)
    total_wav_num = len(wav_info_list_i)
    for i, input_audio_dict in enumerate(wav_info_list_i):
        try:
            utils_file.logging_print(f'{language} wav schedule {i}/{total_wav_num}')
            wav_name = input_audio_dict['aid']
            source_wav_path = os.path.join(output_dir, wav_name + '.mp3')
            if os.path.exists(source_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 已经存在, 跳过')
                continue
            utils_file.do_download_from_play_url(input_audio_dict['url'], output_dir, wav_name=wav_name, wav_type='mp3')
        except Exception as e:
            utils_file.logging_print(f'{e}')


def do_download(language):
    root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
    input_json_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K"
    utils_file.makedir(root_dir)
    input_json_dir_language = os.path.join(input_json_dir, language)
    dev_json_path = os.path.join(input_json_dir_language, 'dev.json')
    train_json_path = os.path.join(input_json_dir_language, 'train.json')
    if not os.path.exists(dev_json_path) or not os.path.exists(train_json_path):
        utils_file.logging_print(f'{language} 不存在dev.json或train.json')
        return
    dev_json_dict = utils_file.load_dict_from_json(dev_json_path)
    train_json_dict = utils_file.load_dict_from_json(train_json_path)
    wav_dict_list = dev_json_dict['audios'] + train_json_dict['audios']
    print(language, len(wav_dict_list))
    output_dir_language = os.path.join(root_dir, language)
    utils_file.makedir(output_dir_language)
    # 通过wav_dict_list得到应该下载的wav_info_dict_list
    should_wav_dict_list = []
    has_download_num = 0
    for i, input_audio_dict in enumerate(wav_dict_list):
        wav_name = input_audio_dict['aid']
        source_wav_path = os.path.join(output_dir_language, wav_name + '.mp3')
        if os.path.exists(source_wav_path):
            has_download_num += 1
            continue
        should_wav_dict_list.append(input_audio_dict)
    utils_file.logging_limit_print(
        f'{language} 已经下载{has_download_num}/{len(wav_dict_list)}, 剩余{len(should_wav_dict_list)}去下载')
    num_thread = 32
    list_list = utils_file.do_split_list(should_wav_dict_list, num_thread)
    runner = utils_file.GxlDynamicProcessPool()
    for i, wav_info_list_i in enumerate(list_list):
        runner.add_thread(func_little4language, [language, wav_info_list_i, output_dir_language])
    runner.start()
    utils_file.logging_print("完全下载完毕")


def main():
    language = "Thai"
    utils_file.logging_print(language)
    do_download(language)


if __name__ == '__main__':
    main()
