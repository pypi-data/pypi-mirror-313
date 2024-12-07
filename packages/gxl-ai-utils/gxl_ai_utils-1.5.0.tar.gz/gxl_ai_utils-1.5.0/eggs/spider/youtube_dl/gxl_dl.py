import os

from gxl_ai_utils.utils import utils_file
import subprocess

def do_get_mp3_from_web_url(url: str, output_dir: str, filename: str):
    """"""
    template_dir = os.path.join(output_dir, filename)
    template_dir = f"{template_dir}_%(title)s-%(id)s.%(ext)s"
    command = [
        'yt-dlp',
        '-x',  # 仅提取音频
        '--audio-format', 'mp3',  # 设置音频格式为wav
        '--output', template_dir,  # 设置输出文件名模板
        url  # YouTube视频URL
    ]
    res = subprocess.run(command, capture_output=True, text=True)
    utils_file.logging_print("Download mp3, res:", res)


urls = []
urls = utils_file.load_list_file_clean(
    '/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/spider/youtube_dl/B_true.txt')
utils_file.logging_print('共有' + str(len(urls)) + '个视频')
my_utils = urls[:164]
utils_file.logging_print('我处理' + str(len(my_utils)) + '个视频')


output_dir = '/home/work_nfs14/xlgeng/data/youtube_data'
output_dir = '/home/node36_data/youtube_down/xlgeng/audio'
utils_file.makedir(output_dir)
urls = []
runner = utils_file.GxlDynamicThreadPool()

num_thread = 20

path_list_list = utils_file.do_split_list(my_utils, num_thread)


def little_fuc(path_list, output_dir):
    for path in path_list:
        utils_file.logging_print("开始处理：url:", path)
        url = path
        filename = utils_file.do_generate_random_num(8)
        do_get_mp3_from_web_url(url, output_dir, filename)


for path_list in path_list_list:
    runner.add_task(little_fuc, [path_list, output_dir])

runner.start()
