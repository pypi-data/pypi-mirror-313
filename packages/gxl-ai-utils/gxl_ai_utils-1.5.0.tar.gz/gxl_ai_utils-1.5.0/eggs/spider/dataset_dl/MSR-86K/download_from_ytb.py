import os
import subprocess


def do_download_from_play_url(input_url, output_dir, wav_type='mp3', wav_name='loaded_audio', keep_title=False, is_list=False):
    """

    :param input_url:
    :param output_dir:
    :param wav_type: mp3 or wav
    :param wav_name:
    :param keep_title: 是不是要把标题保留到音频名称内
    :param is_list:  如果url为一个列表页面, 也就是那种一个音频在播放, 但是旁边有个系列列表(不是推荐视频列表).然后把此开启就可以自动下载整个列表
    :return:
    """
    template_dir = os.path.join(output_dir, wav_name)
    if keep_title:
        template_dir = f"{template_dir}_%(title)s.%(ext)s"
        template_dir = template_dir + "_%(title)s"
    if is_list:
        template_dir = template_dir + '_%(id)s'
    template_dir = template_dir + ".%(ext)s"
    if wav_type.startswith('.'):
        wav_type = wav_type[1:]
    command = [
        'yt-dlp',
        '-x',  # 仅提取音频
        '--audio-format', wav_type,  # 设置音频格式为wav,mp3等
        '--output', template_dir,  # 设置输出文件名模板
        input_url  # YouTube视频URL
    ]
    print(f'开始下载, link: {input_url}')
    res = subprocess.run(command, capture_output=True, text=True)
    res = str(res)[-100:]
    print(f"下载完成，link: {input_url}\n res:", res)

if __name__ == '__main__':
    do_download_from_play_url(input_url="https://www.youtube.com/watch?v=-oQNbCVmcrw", output_dir="./download")
    do_download_from_play_url(input_url="https://www.youtube.com/watch?v=kJeTPi7qJXw", output_dir="./download")