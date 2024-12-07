import gxl_ai_utils.gxl_whisper as whisper
from gxl_ai_utils.gxl_whisper import tokenizer
import glob
from gxl_ai_utils.utils import utils_data, utils_model

data_dir = 'E:\gengxuelong_study\server_local_adapter\\ai\data\small_aishell\\train'


def whisper_load_audio(audio_file_path: str):
    """
    whisper.load_audio(audio_file_path) 和 utils_data.torchaudio_load(audio_file_path)比较：
    前者得到的数据更加精确， 后者精确到小数点4位，前者精确到8位
    :param audio_file_path:
    :return:
    """
    # audio_waveform = whisper.load_audio(audio_file_path)
    # audio_waveform = whisper.pad_or_trim(audio_waveform)
    # audio_mel = whisper.log_mel_spectrogram(audio_waveform)
    # return audio_mel
    audio_mel = whisper.log_mel_spectrogram(audio_file_path, 80, 480000)
    mel_segment = whisper.pad_or_trim(audio_mel, 3000)
    print(mel_segment[:,1511])
    return mel_segment


def detect_language(audio_file_path: str, model: whisper.Whisper):
    """
    :param audio_file_path:
    :param model:
    :return:
    """
    audio_mel = whisper_load_audio(audio_file_path)
    res, probs = model.detect_language(audio_mel)
    # print(res)
    # print(probs)
    sorted_item = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_item)
    tokenizer_obj = tokenizer.get_tokenizer(model.is_multilingual)
    token = tokenizer_obj.decode([res])
    print(f'detect_language():language token: {token}')
    return token


def transcribe_audio(audio_file_path: str, model: whisper.Whisper):
    res = model.transcribe(audio_file_path, initial_prompt='简体字：')
    print(res['text'])
    print(res)


def gxl_test_encoder(model: whisper.Whisper, audio_file_path):
    encoder = model.encoder
    print(encoder)
    utils_model.get_model_param_num(encoder)
    input_data = whisper_load_audio(audio_file_path)
    print(input_data.shape)
    dim = model.dims
    print(dim)
    input_data = input_data.unsqueeze(0)
    output = encoder(input_data)
    print(output.shape)


def main():
    """"""
    file_list = glob.glob(data_dir + '/*.wav')
    model = whisper.load_model('tiny', download_root='./output/whisper', device='cpu')
    transcribe_audio(file_list[0], model)



if __name__ == '__main__':
    # main()
    file_list = glob.glob(data_dir + '/*.wav')
    a ,_ = utils_data.torchaudio_load(file_list[0])
    print(a)
