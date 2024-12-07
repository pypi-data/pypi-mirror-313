import tqdm

from gxl_ai_utils.utils import utils_file

def little_func(input_dict, res_dict, output_dir):
    temp_res_dict = {}
    for k, wav_path in tqdm.tqdm(input_dict.items(), total=len(input_dict), desc=f"移动音频中"):
        output_wav_path = f"{output_dir}/{k}.npy"
        utils_file.copy_file(wav_path, output_wav_path, use_shell=True)
        temp_res_dict[k] = output_wav_path
    res_dict.update(temp_res_dict)



def get_wav_file():
    intput_dir = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_codec_asr/output2"
    partition = ['train', 'dev', 'test']
    for p in partition:
        output_wav_dir = f"{intput_dir}/{p}/wav"
        input_data_path = f"{intput_dir}/{p}/wav_old.scp"
        wav_path_dict = utils_file.load_dict_from_scp(input_data_path)
        utils_file.write_dict_to_scp(wav_path_dict, f"{intput_dir}/{p}/wav_old.scp")
        new_wav_dict = {}
        dict_list = utils_file.do_split_dict(wav_path_dict, 45)
        runner = utils_file.GxlDynamicThreadPool()
        for dict_i in dict_list:
            runner.add_task(little_func, [dict_i, new_wav_dict, output_wav_dir])
        runner.start()
        utils_file.write_dict_to_scp(new_wav_dict, f"{intput_dir}/{p}/wav.scp")
        utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_file_path=f"{intput_dir}/{p}/wav.scp",
                                                    text_scp_file_path=f"{intput_dir}/{p}/text",
                                                    target_jsonl_file_path=f"{intput_dir}/{p}/data.list")

if __name__ == '__main__':
    get_wav_file()