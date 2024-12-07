import logging
import platform
import os

BASE_PATH = os.path.dirname((os.path.abspath(__file__))) + "/"
# if platform.system().lower() == 'windows':
#     print("windows 环境")
#     BASE_PATH = "F:\code\python\deeplearning\pythonProject/gxl_ai_utils/"
# elif platform.system().lower() == 'linux':
#     print("linux 环境")
#     BASE_PATH = "/home/work_nfs7/xlgeng/gxl_dir1/gxl_ai_utils/gxl_ai_utils/"

DATA_PATH = BASE_PATH + "../gxl_data/"
OUTPUT_PATH = BASE_PATH + "../output/"
LOG_PATH = OUTPUT_PATH + "log/"


def AI_LOGGER(log_file_path=None):
    """
    将日志输出到日志文件和控制台
    """
    if log_file_path is None:
        no_file = True
        log_file_path = 'None'
    else:
        no_file = False
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    if log_file_path in logging.Logger.manager.loggerDict:
        return logging.getLogger(log_file_path)
    logger = logging.getLogger(log_file_path)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # # 创建一个handler，用于将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 创建一个handler，用于写入日志文件
    if not no_file:
        file_handler = logging.FileHandler(
            filename=log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
    return logger
