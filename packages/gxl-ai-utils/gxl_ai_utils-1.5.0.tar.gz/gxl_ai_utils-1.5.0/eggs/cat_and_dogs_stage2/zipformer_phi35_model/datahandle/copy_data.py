import os.path
import subprocess

import sys


sys.path.insert(0, '../../../../')
from gxl_ai_utils.utils import utils_file

def do_sync_files(file_list_path, password, username, remote_host, local_directory,remote_dir='/'):
    """
    使用 rsync 命令从远程主机下载文件，并支持断点续传(-P决定)。
    remote_dir使用的场景： 如果一个shards_list.txt文件中的pure文件名字不是唯一的， 则需要相对于某一个根目录，保留这个
    目录下面的子目录的结构，这样就不会出现覆盖文件的情况了。
    sync比scp更好用，功能相似的前体下sync支持断点续传
    :param file_list_path: 包含文件列表的文件路径
    :param password: 远程主机的 SSH 密码
    :param username: 远程主机的用户名
    :param remote_host: 远程主机的 IP 地址或主机名
    :param local_directory: 本地存储文件的目标目录
    :param remote_dir: 远程目录起始位置
    :return:
    """
    remote_dir = remote_dir if remote_dir.endswith('/') else remote_dir+'/'
    if len(remote_dir) !=1:
        utils_file.do_replace_str_to_file(remote_dir, '/', file_list_path, './tmp.list')
        file_list_path = './tmp.list'
        # 构造 rsync 命令
        rsync_command = [
            'sshpass', '-p', password,  # 使用 sshpass 提供密码
            'rsync', '-avrP',  # rsync 参数：-a（归档），-v（详细），-r（递归），-P（部分传输和进度）
            # '--no-relative',  # 去掉远程目录的层级结构
            f'--files-from={file_list_path}',  # 从文件列表中读取文件路径
            f'{username}@{remote_host}:{remote_dir}',  # 远程源路径
            local_directory  # 本地目标目录
        ]
    elif remote_dir=='/':
        # 构造 rsync 命令
        rsync_command = [
            'sshpass', '-p', password,  # 使用 sshpass 提供密码
            'rsync', '-avrP',  # rsync 参数：-a（归档），-v（详细），-r（递归），-P（部分传输和进度）
            '--no-relative',  # 去掉远程目录的层级结构
            f'--files-from={file_list_path}',  # 从文件列表中读取文件路径
            f'{username}@{remote_host}:{remote_dir}',  # 远程源路径
            local_directory  # 本地目标目录
        ]
    else:
        utils_file.logging_warning('remote dir格式不正确')
        return

    # 执行 rsync 命令
    try:
        subprocess.run(rsync_command, check=True)
        print("文件同步完成！")
        utils_file.do_remove_file('./tmp.list')
    except subprocess.CalledProcessError as e:
        print(f"rsync 命令执行失败: {e}")
    except FileNotFoundError as e:
        print(f"命令未找到: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 示例调用
# file_list_path = "/home/work_nfs15/asr_data/data/LibriSpeech/LibriSpeech_shard/shards_list.txt"
password = 'ASLPaslp'
username = 'aslp'
remote_host = '192.168.0.4'
local_directory = '/home/node48_tmpdata/xlgeng/data/asr_data'

data_info_dict = utils_file.load_dict_from_yaml('data.yaml')
for key, data_info in data_info_dict.items():
    file_list_path = data_info['path']
    local_dir_i = os.path.join(local_directory, key)
    utils_file.makedir_sil(local_dir_i)
    if key == 'librispeech':
        remote_dir = "/home/work_nfs15/asr_data/data/LibriSpeech/LibriSpeech_shard/"
    else:
        remote_dir = '/'
    do_sync_files(file_list_path, password, username, remote_host, local_dir_i, remote_dir)
