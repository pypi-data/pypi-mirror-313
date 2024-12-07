import os

from gxl_ai_utils.utils import utils_file

input_dir = "/home/work_nfs8/xlgeng/new_workspace/Amphion/preprocessors/Emilia/input_wavs_processed"
wav_source_dir = "/home/work_nfs8/xlgeng/new_workspace/Amphion/preprocessors/Emilia/input_wavs"


def data_analysis(input_dir, wav_source_dir):
    """"""
    res_dict = {}
    res_dict['wav/type'] = ["source_time", 'valid_time', 'valid_wav_num', "valid_time_list", 'valid_time_ratio']
    separate_wav_dirs = os.listdir(input_dir)
    for separate_wav_dir in separate_wav_dirs:
        print(f'separate_wav_dir: {separate_wav_dir}')
        try:
            source_wav_path = os.path.join(wav_source_dir, separate_wav_dir + ".wav")
            sample, rate = utils_file._get_sample_count_wave(source_wav_path)
            duration_time_all = sample / rate
            print(f'{separate_wav_dir} duration time: {duration_time_all}, source_wav_path {source_wav_path}')
            separate_wav_dir_path = os.path.join(input_dir, separate_wav_dir)
            wav_child_paths = utils_file.do_listdir(separate_wav_dir_path)[1]
            duration_time_list = []
            for wav_child_path in wav_child_paths:
                if wav_child_path.endswith(".json"):
                    continue
                print(wav_child_path)
                duration_time = utils_file.do_get_wav_duration(wav_child_path)
                print(duration_time)
                duration_time_list.append(duration_time)
            wav_num = len(duration_time_list)
            all_valid_time = sum(duration_time_list)
        except Exception as e:
            print(e)
            continue
        res_dict[separate_wav_dir] = [duration_time_all, all_valid_time, wav_num, str(duration_time_list),
                                      f"{all_valid_time / duration_time_all * 100}%"]
    total_source_time = 0
    total_valid_time = 0
    total_valid_wav_num = 0
    total_valid_time_list = ""
    total_valid_time_ratio = 0
    for key, value in res_dict.items():
        if key == 'wav/type':
            continue
        total_source_time += value[0]
        total_valid_time += value[1]
        total_valid_wav_num += value[2]
        total_valid_time_ratio += float(value[4][:-1])
    total_valid_time_ratio = total_valid_time_ratio / (len(res_dict.keys())-1)
    total_valid_time_ratio = f"{total_valid_time_ratio}%"
    res_dict['total'] = [total_source_time, total_valid_time, total_valid_wav_num, str(total_valid_time_list),
                         total_valid_time_ratio]

    utils_file.write_dict_to_xlsx(res_dict, "./data_analysis.xlsx", cols_pattern=False)

if __name__ == '__main__':
    data_analysis(input_dir, wav_source_dir)

