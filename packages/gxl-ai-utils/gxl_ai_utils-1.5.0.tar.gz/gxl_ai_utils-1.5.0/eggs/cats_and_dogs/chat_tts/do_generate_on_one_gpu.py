import argparse
import ChatTTS
import torch
import torchaudio
import tqdm

from gxl_ai_utils.utils import utils_file
def get_args():
    parser = argparse.ArgumentParser(description='借助chatTTS进行语音的生成')
    parser.add_argument('--chat_jsonl_path', type=str)
    parser.add_argument('--output_wav_dir_path', type=str)
    parser.add_argument('--gen_Q', type=bool, default=True)
    parser.add_argument('--vision', type=bool, default=True)
    parser.add_argument('--batch_size', type=int, default=1)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    utils_file.logging_info(args)
    chat = ChatTTS.Chat()
    chat.load(compile=False)  # Set to True for better performance
    dict_list = utils_file.load_dict_list_from_jsonl(args.chat_jsonl_path)
    key_list = []
    text_list = []
    vision = args.vision
    if vision:
        for dict_item in tqdm.tqdm(dict_list, total=len(dict_list), desc='prepare data'):
            key_list.append(dict_item['key'])
            if args.gen_Q:
                text_list.append(dict_item['Q'])
            else:
                text_list.append(dict_item['A'])
    else:
        for dict_item in dict_list:
            key_list.append(dict_item['key'])
            if args.gen_Q:
                text_list.append(dict_item['Q'])
            else:
                text_list.append(dict_item['A'])

    batch_size = args.batch_size
    output_dir = args.output_wav_dir_path
    utils_file.makedir_sil(output_dir)
    batch_cache_list_text = []
    batch_cache_list_key = []
    if vision:
        for key, text in tqdm.tqdm(zip(key_list, text_list), total=len(key_list), desc='generate wav'):
            batch_cache_list_key.append(key)
            batch_cache_list_text.append(text)
            if len(batch_cache_list_text) == batch_size:
                wavs = chat.infer(batch_cache_list_text)
                for i in range(len(wavs)):
                    """
                    In some versions of torchaudio, the first line works but in other versions, so does the second line.
                    """
                    try:
                        resampler = torchaudio.transforms.Resample(orig_freq=24000, new_freq=16000)
                        resampled_wav = resampler(torch.from_numpy(wavs[i]).unsqueeze(0))
                        torchaudio.save(f"{output_dir}/{batch_cache_list_key[i]}.wav", resampled_wav, 16000)
                    except:
                        resampler = torchaudio.transforms.Resample(orig_freq=24000, new_freq=16000)
                        resampled_wav = resampler(torch.from_numpy(wavs[i]))
                        torchaudio.save(f"{output_dir}/{batch_cache_list_key[i]}.wav", resampled_wav, 16000)
                batch_cache_list_key = []
                batch_cache_list_text = []
            else:
                continue
    else:
        for key, text in zip(key_list, text_list):
            batch_cache_list_key.append(key)
            batch_cache_list_text.append(text)
            if len(batch_cache_list_text) == batch_size:
                wavs = chat.infer(batch_cache_list_text)
                for i in range(len(wavs)):
                    """
                    In some versions of torchaudio, the first line works but in other versions, so does the second line.
                    """
                    try:
                        resampler = torchaudio.transforms.Resample(orig_freq=24000, new_freq=16000)
                        resampled_wav = resampler(torch.from_numpy(wavs[i]).unsqueeze(0))
                        torchaudio.save(f"{output_dir}/{batch_cache_list_key[i]}.wav", resampled_wav, 16000)
                    except:
                        resampler = torchaudio.transforms.Resample(orig_freq=24000, new_freq=16000)
                        resampled_wav = resampler(torch.from_numpy(wavs[i]))
                        torchaudio.save(f"{output_dir}/{batch_cache_list_key[i]}.wav", resampled_wav, 16000)
                batch_cache_list_key = []
                batch_cache_list_text = []
            else:
                continue










