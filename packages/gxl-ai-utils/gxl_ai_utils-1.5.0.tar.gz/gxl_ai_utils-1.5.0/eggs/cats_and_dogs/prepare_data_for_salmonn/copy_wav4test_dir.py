from gxl_ai_utils.utils import utils_file
import os
import tqdm

test_dir = "/home/work_nfs8/xlgeng/data/scp_test"

dataset_names = os.listdir(test_dir)
def little_func(dataset_name):
    dataset_path = os.path.join(test_dir, dataset_name)
    wav_scp_path = os.path.join(dataset_path, "wav.scp")
    if not os.path.exists(wav_scp_path):
        return
    wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
    wav_output_dir = os.path.join(dataset_path, "wav")
    utils_file.makedir_sil(wav_output_dir)
    new_wav_dict = {}
    for key in tqdm.tqdm(wav_dict.keys()):
        wav_path = wav_dict[key]
        new_wav_path = os.path.join(wav_output_dir, os.path.basename(wav_path))
        new_wav_dict[key] = new_wav_path
        utils_file.copy_file(wav_path, new_wav_path, use_shell=True)
    utils_file.write_dict_to_scp(new_wav_dict, wav_scp_path)
    utils_file.write_dict_to_scp(wav_dict, os.path.join(dataset_path, "wav_old.scp"))
    utils_file.do_convert_wav_text_scp_to_jsonl(os.path.join(dataset_path, "wav.scp"),os.path.join(dataset_path, "text"), os.path.join(dataset_path, "data.list"))

runner = utils_file.GxlDynamicThreadPool()
for dataset_name in dataset_names:
    runner.add_thread(little_func, [dataset_name])

runner.start()
