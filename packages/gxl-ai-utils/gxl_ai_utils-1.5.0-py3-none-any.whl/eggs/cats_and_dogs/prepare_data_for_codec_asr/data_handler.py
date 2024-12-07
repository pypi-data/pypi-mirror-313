import os.path

import tqdm

from gxl_ai_utils.utils import utils_file


def data_handler():
    input_data_path = "/home/node40_data2/dkguo/1500w_0328_text.lst"
    lines_data = utils_file.load_list_file_clean(input_data_path)
    lines_data = utils_file.do_get_random_sublist(lines_data, 500000)
    res_dict_list = []
    for line in tqdm.tqdm(lines_data, total=len(lines_data)):
        items = line.strip().split('|')
        key = items[0]
        token_list_path = items[1]
        text = items[-1]
        text = utils_file.do_filter(text)
        temp_dict = dict(
            key=key,
            wav=token_list_path,
            txt=text
        )
        res_dict_list.append(temp_dict)
    timer = utils_file.GxlTimer()
    timer.start()
    utils_file.write_dict_list_to_jsonl(res_dict_list, "./output/1500w_0328_text.jsonl")
    timer.stop_halfway()


def data_handler_2():
    input_jsonl_path = "./output/1500w_0328_text.jsonl"
    all_list = utils_file.load_list_file_clean(input_jsonl_path)
    train_list = all_list[:int(len(all_list) * 0.9)]
    dev_list = all_list[int(len(all_list) * 0.9):int(len(all_list) * 0.93)]
    test_list = all_list[int(len(all_list) * 0.93):]
    utils_file.write_list_to_file(train_list, "./output2/train/1500w_0328_text.list")
    utils_file.write_list_to_file(dev_list, "./output2/dev/1500w_0328_text.list")
    utils_file.write_list_to_file(test_list, "./output2/test/1500w_0328_text.list")
    for partition in ["train", "dev", "test"]:
        input_data_path = f"./output2/{partition}/1500w_0328_text.list"
        utils_file.do_convert_jsonl_to_wav_text_scp(input_data_path, f"./output2/{partition}/wav.scp",
                                                    f"./output2/{partition}/text")


def data_handler_3():
    input_text_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_codec_asr/output2/train/text"
    utils_file.do_convert_text2chars_dict(input_text_path, "./output2/train/chars.dict")


def data_handler_4():
    for partition in ["train", "dev", "test"]:
        input_dir = f"/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_codec_asr/output2/{partition}"
        utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_file_path=os.path.join(input_dir, "wav.scp"),
                                                    text_scp_file_path=os.path.join(input_dir, "text"),
                                                    target_jsonl_file_path=os.path.join(input_dir, "data.list"))


if __name__ == '__main__':
    data_handler()
    data_handler_2()
    data_handler_3()
    data_handler_4()
