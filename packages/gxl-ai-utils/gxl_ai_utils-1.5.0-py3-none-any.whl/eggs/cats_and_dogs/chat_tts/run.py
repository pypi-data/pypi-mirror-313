import ChatTTS
import torch
import torchaudio


from gxl_ai_utils.utils import utils_file
chat = ChatTTS.Chat()
chat.load(compile=False) # Set to True for better performance
OUTPUT_DIR='/home/work_nfs15/asr_data/data/chat_data/wav'
def main(texts, keys):
    batch_size = 5
    wavs = chat.infer(texts)
    for i in range(len(wavs)):
        """
        In some versions of torchaudio, the first line works but in other versions, so does the second line.
        """
        try:
            torchaudio.save(f"{OUTPUT_DIR}/{keys[i]}.wav", torch.from_numpy(wavs[i]).unsqueeze(0), 24000)
        except:
            torchaudio.save(f"{OUTPUT_DIR}/{keys[i]}.wav", torch.from_numpy(wavs[i]), 24000)

import os
import multiprocessing


def process_task(device_id, dict_list_temp):
    # 设置CUDA_VISIBLE_DEVICES，使得该进程只看到指定的GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device_id)

    texts = [x["Q"] for x in dict_list_temp]
    keys = [x["key"] for x in dict_list_temp]

    # 执行主要的TTS任务
    main(texts, keys)
    print(f"TTS application finished on GPU {device_id}.")


if __name__ == "__main__":
    input_jsonl_path = "/home/work_nfs15/asr_data/data/chat_data/test.jsonl"
    dict_list = utils_file.load_dict_list_from_jsonl(input_jsonl_path)

    little_thread_num = 8  # 总线程数
    num_device = 8  # GPU数量
    dict_list_list = utils_file.do_split_list(dict_list, little_thread_num)  # 拆分数据

    processes = []  # 存储进程的列表

    for thread_index in range(little_thread_num):
        # 计算当前线程分配的GPU ID（环绕分配）
        device_id = thread_index % num_device

        # 获取当前线程需要处理的数据
        dict_list_temp = dict_list_list[thread_index]

        # 创建一个新的进程来执行TTS任务
        p = multiprocessing.Process(target=process_task, args=(device_id, dict_list_temp))
        processes.append(p)
        p.start()

    # 等待所有进程结束
    for p in processes:
        p.join()

    print("All TTS applications finished.")

