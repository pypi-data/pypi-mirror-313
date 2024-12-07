import codecs
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
import json
import os

def load_list_file_clean(path: str):
    """
    得到不包含换行符的str_list
    :param path:
    :return:
    """
    if not os.path.exists(path):
        print(f'load_list_file_clean()_{path}文件不存在')
        return []

    with codecs.open(path, 'r', encoding='utf=8') as f:
        cat_to_name: list = f.read().splitlines()
        # cat_to_name: list = f.readlines() -> 包含换行符
        print(f"load_list_file_clean()_数据总条数为:{len(cat_to_name)}")
    return cat_to_name


# # 假设这是你的YouTube视频URL列表
# urls = [
#     "https://www.youtube.com/watch?v=Ds6rTnXZqUg",
#     # 添加更多的URLs
# ]

# 初始化日志列表，用于存储失败的下载索引
log = {'downed_num': 0, 'err': []}


def download_audio_as_wav(url, output_template, index):
    command = [
        'yt-dlp',
        '-x',  # 仅提取音频
        '--audio-format', 'mp3',  # 设置音频格式为wav
        '--output', output_template,  # 设置输出文件名模板
        url  # YouTube视频URL
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    # 如果返回代码不是0（即发生错误），则记录索引
    if result.returncode != 0:
        log['err'].append({
            "index": index,
            "url": url,
            "error": result.stderr
        })


# 使用ThreadPoolExecutor来管理多线程
def download_videos(urls, pre_num):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for index, url in enumerate(urls):
            output_template = f"{index + pre_num:010d}.%(ext)s"
            executor.submit(download_audio_as_wav, url, output_template, index + pre_num)





if os.path.exists('./log.json'):
    with open('./log.json', 'r') as js:
        log = json.load(js)

urls = []
urls = load_list_file_clean(
    '/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/spider/youtube_dl/B_true.txt')
print('共有' + str(len(urls)) + '个视频')
my_utils = urls[:164]
print('我处理' + str(len(my_utils)) + '个视频')
output_dir = '/home/work_nfs14/xlgeng/youtube_data'
# os.makedirs(output_dir)
urls = []
for video_path in my_utils:
    urls.append(video_path.strip())
    print('把' + video_path + '加入队列')
    if len(urls) == 10:
        print('开始下载')
        download_videos(urls, log['downed_num'])
        urls = []
        log['downed_num'] = log['downed_num'] + 10
        print('has downed' + str(log['downed_num']) + 'lines')
        with open('log.json', 'w') as log_file:
            json.dump(log, log_file, indent=4)
        break


# with open('/home/node36_data/kxxia/song/DISCO-10M_train_noembed.csv', 'r') as file:
#     # head  = file.readline()
#     pre_num = log['downed_num']
#     for i in range(pre_num):
#         _ = file.readline()
#     for line in file:
#         urls.append(line.strip().split(',')[0])
#         if len(urls) == 10:
#             download_videos(urls, log['downed_num'])
#             urls = []
#             log['downed_num'] = log['downed_num'] + 10
#             print('has downed' + str(log['downed_num']) + 'lines')
#             with open('log.json', 'w') as log_file:
#                 json.dump(log, log_file, indent=4)
