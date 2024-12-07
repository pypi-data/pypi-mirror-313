import time
import traceback
from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool

from gxl_ai_utils.utils import utils_spider, utils_file
from gxl_ai_utils import AiConstant

root_path = 'https://www.qtfm.cn'
root_category = 'https://www.qtfm.cn/categories/3873/0/1'  # 以播客为起始页，放弃这个类别，里面的音频都不能听
save_path = '/home/backup_nfs5/xlgeng/asr_data/qt_fm/'
utils_file.makedir_sil(save_path)
logger = AiConstant.AI_LOGGER('./output/log/qt_fm.log')


def downloader_wav(save_dir, name, url):
    """
    url: https://www.qtfm.cn/channels/329130/programs/18324771
    :param save_dir:
    :param name:
    :param url:
    :return:
    """
    utils_file.makedir_sil(save_dir)
    name = utils_file.get_clean_filename(name)
    name = name + '.wav'
    save_path = utils_file.join_path(save_dir, name)
    start = time.time()
    utils_spider.download_file(url, save_path)
    logger.info(f'下载完成:{name},耗时:{time.time() - start}, 文件大小:{utils_file.get_file_size(save_path):.4f}MB')


def handle_ibum_index(save_path, href):
    """
    href : https://www.qtfm.cn/channels/136224/1/
    :param save_path:
    :param href:
    :return:
    """
    xpath_wav_list = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/ul/li/span[1]/a/@href'
    title_wav_list = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/ul/li/span[1]/a/p/text.txt()'
    res_wav_list = utils_spider.hande_href(href, xpath_wav_list)
    title_wav_list = utils_spider.hande_href(href, title_wav_list)
    for wav, title in zip(res_wav_list, title_wav_list):
        wav_href = utils_file.join_path(root_path, wav)
        print(wav_href)


def handle_ibum_index_fenye(save_path, href):
    """把一个专辑的音频拿下"""
    xpath_total_page = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div/ul/li/a/text.txt()'
    res = utils_spider.handle_xpath(utils_spider.send_request(href).text, xpath_total_page)
    total_page = int(res[-2])
    logger.info(f'总页数为{total_page}')
    for i in range(1, total_page + 1):
        logger.info(f'开始处理第{i}页')
        try:
            temp_href = utils_file.join_path(href, f'{i}')
            handle_ibum_index(save_path, temp_href)
        except Exception as e:
            logger.info(f'handle_ibum_index_fenye函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_category_index(title, href):
    """
    href: https://www.qtfm.cn/categories/3251/0/75
    :param title:
    :param href:
    :return:
    """
    xpath_href = "/html/body/div[1]/div/div[3]/div/div/div[2]/div[2]/div/a[1]/@href"
    response = utils_spider.send_request(href)
    res_href = utils_spider.handle_xpath(response.text, xpath_href)
    for i, href in enumerate(res_href):
        """可以处理所有种类页"""
        href = utils_file.join_path(root_path, href)
        logger.info(f'开始处理专辑：{href}, 每页固定12个专辑，现在是第{i + 1}个')
        temp_save_path = utils_file.join_path(save_path, title)
        utils_file.makedir_sil(temp_save_path)
        try:
            handle_ibum_index_fenye(temp_save_path, href)
        except Exception as e:
            logger.info(f'handle_category_index函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_category_index_fenye(title, href):
    for i in range(1, 76):
        logger.info(f'开始处理{title}类别的第{i}页')
        try:
            temp_href = utils_file.join_path(href, str(i))
            handle_category_index(title, temp_href)
        except Exception as e:
            logger.info(f'分页{i}的handle_category_index函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_root_category():
    """得到每个类别的入口"""
    xpath_href = '/html/body/div[1]/div/div[3]/div/div/div[1]/ul/li/a/@href'
    xpath_catefory_title = '/html/body/div[1]/div/div[3]/div/div/div[1]/ul/li/a/text.txt()'
    response = utils_spider.send_request(root_category)
    res_href = utils_spider.handle_xpath(response.text, xpath_href)
    res_title = utils_spider.handle_xpath(response.text, xpath_catefory_title)
    thread_runner = GxlDynamicThreadPool()
    for href, title in zip(res_href, res_title):
        logger.info(f'开始处理专辑{title}， href:{href}')
        href = utils_file.join_path(root_path, href)
        href = href[:href.rfind('/') + 1]
        thread_runner.add_task(handle_category_index_fenye, [title, href])
    thread_runner.start()


if __name__ == '__main__':
    """"""
    # handle_root_category()
    # handle_category_index('脱口秀', 'https://www.qtfm.cn/categories/3613/0/5')
    # handle_ibum_index_fenye('脱口秀', 'https://www.qtfm.cn/channels/136224/1')
    # handle_ibum_index_fenye('脱口秀', 'https://www.qtfm.cn/channels/329130')
    # handle_ibum_index('ss','https://www.qtfm.cn/channels/243418/1')
    downloader_wav('./output/wav', 'haha',
                   'https://hwod-sign.qtfm.cn/m4a/5dbfd43dd52003047b950377_14596141_24.m4a?auth_key=6559269b-922941-0-f133ddc3cb37db3459d694de5671ea59')

"""
e6f1c688221cca34b31740081edb7434
https://hwod-sign.qtfm.cn/m4a/595b84a37cb8913c4ea3073e_7581688_64.m4a?auth_key=65592b6f-342312-0-3b68fc39af6c925ab000ad5ecc282f3f
https://hwod-sign.qtfm.cn/m4a/5dbfd43dd52003047b950377_14596141_24.m4a?auth_key=6559269b-922941-0-f133ddc3cb37db3459d694de5671ea59')
https://audio.qtfm.cn/audiostream/redirect/136224/7405164?access_token=&device_id=MOBILESITE&qingting_id=&t=1700299379428&sign=5ecada7b1924520b93eca838fcb5ef11

https://i.qingting.fm/wapi/channels/136224/programs/page/1/pagesize/10
"""