import glob
import os.path
import traceback
import hmac
import time
import requests
import sys
import time

from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool, GxlFixedThreadPool

import gxl_ai_utils.AiConstant
from gxl_ai_utils.utils import utils_spider, utils_file

# logging = gxl_ai_utils.AiConstant.AI_logging()
import logging

utils_file.set_logging()


class GxlSpider:
    def __init__(self, output_dir='./output/qingting_fm/'):
        self.access_token = None
        self.qingting_id = None
        self.login_url = "https://user.qtfm.cn/u2/api/v4/user/login"
        self.root_url = 'https://www.qtfm.cn'
        self.start_url = 'https://www.qtfm.cn/categories'
        self.output_dir = output_dir
        utils_file.makedir_sil(self.output_dir)

    def handle_root_category(self):
        """得到每个类别的入口"""
        xpath_href = '/html/body/div[1]/div/div[3]/div/div/div[1]/ul/li/a/@href'
        xpath_catefory_title = '/html/body/div[1]/div/div[3]/div/div/div[1]/ul/li/a/text()'
        response = utils_spider.send_request(self.start_url)
        res_href = utils_spider.handle_xpath(response.text, xpath_href)
        res_title = utils_spider.handle_xpath(response.text, xpath_catefory_title)
        res_dict = {}
        for href, title in zip(res_href, res_title):
            res_dict[title] = utils_file.join_path(self.root_url, href)
        utils_file.write_dict_to_json(res_dict, self.output_dir + 'root_category.json')

    def handle_category_index_fenye(self):
        category_dict = utils_file.load_dict_from_json(self.output_dir + 'root_category.json')
        for title, href in category_dict.items():
            utils_file.logging_print(f'开始处理{title}类别')
            if title == '播客' or title == '小说':
                """播客的音频都是'该音频不存在'的提示音。 小说页面的结构不一样"""
                continue
            href = href[:-1]
            album_path_list = []
            save_path = utils_file.join_path(self.output_dir, 'album_info', f'{title}.list')
            utils_file.makedir_for_file_or_dir(save_path)
            for i in range(1, 76):
                utils_file.logging_print(f'开始处理{title}类别的第{i}页')
                try:
                    temp_href = utils_file.join_path(href, str(i))
                    utils_file.logging_print(f'开始处理的页的地址:{temp_href}')
                    xpath_href = "/html/body/div[1]/div/div[3]/div/div/div[2]/div[2]/div/a[1]/@href"
                    response = utils_spider.send_request(temp_href)
                    res_href = utils_spider.handle_xpath(response.text, xpath_href)
                    for i, href_i in enumerate(res_href):
                        href_i = utils_file.join_path(self.root_url, href_i)
                        utils_file.logging_print(href_i)
                        album_path_list.append(href_i)
                except Exception as e:
                    utils_file.logging_print(f'分页{i}的handle_category_index函数执行报错, 爆错内容为{e}')
                    traceback.print_exc()
            utils_file.write_list_to_file(album_path_list, save_path)
            # break

    def handle_ibum_index_fenye(self, ):
        """把一个专辑的音频拿下"""
        album_info_dir = utils_file.join_path(self.output_dir, 'album_info')
        category_s_album_list = glob.glob(utils_file.join_path(album_info_dir, '*.list'))
        utils_file.print_list(category_s_album_list)
        for album_list_path in category_s_album_list:
            category_name = utils_file.get_file_pure_name_from_path(album_list_path)
            album_list = utils_file.load_list_file_clean(album_list_path)
            album_info_category_dir = utils_file.join_path(self.output_dir, 'wav_info', category_name)
            for album_href in album_list:
                album_id = album_href.split('/')[-1]
                album_save_path = utils_file.join_path(album_info_category_dir, f'{album_id}.list')
                res_list = []
                utils_file.logging_print(f'开始处理专辑, url:{album_href}')
                try:
                    xpath_total_page = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div/ul/li/a/text()'
                    res = utils_spider.handle_xpath(utils_spider.send_request(album_href).text, xpath_total_page)
                    total_page = int(res[-2])
                    utils_file.logging_print(f'总页数为{total_page}')
                    for i in range(1, total_page + 1):
                        utils_file.logging_print(f'开始处理第{i}页')
                        try:
                            temp_href = utils_file.join_path(album_href, f'{i}')

                            xpath_wav_list = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/ul/li/span[1]/a/@href'
                            title_wav_list = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/ul/li/span[1]/a/p/text()'
                            res_wav_list = utils_spider.hande_href(temp_href, xpath_wav_list)
                            title_wav_list = utils_spider.hande_href(temp_href, title_wav_list)
                            for wav, title in zip(res_wav_list, title_wav_list):
                                wav_href = utils_file.join_path(self.root_url, wav)
                                res_list.append(wav_href)
                                utils_file.logging_print(wav_href)
                        except Exception as e:
                            utils_file.logging_print(f'handle_ibum_index_fenye函数执行报错, 爆错内容为{e}')
                            traceback.print_exc()
                    utils_file.write_list_to_file(res_list, album_save_path)
                except Exception as e:
                    utils_file.logging_print(f'handle_ibum_index_fenye函数执行报错, 爆错内容为{e}')
                    traceback.print_exc()
                # break

    def get_wav_info(self):
        album_info_dir = utils_file.join_path(self.output_dir, 'wav_info')
        album_path_list = glob.glob(utils_file.join_path(album_info_dir, '**/*.list'))
        utils_file.print_list(album_path_list)
        for album_path in album_path_list:
            self.login()
            album_path = utils_file.normal_path(album_path)
            utils_file.logging_print(f'\n')
            utils_file.logging_print(f'\n')
            utils_file.logging_print(f'\n')
            utils_file.logging_print(f'new album_path, album_path: {album_path}')
            category_name = album_path.split('/')[-2]
            utils_file.logging_print(category_name)
            wav_path_list = utils_file.load_list_file_clean(album_path)
            runner = GxlFixedThreadPool(50 if len(wav_path_list) > 50 else len(wav_path_list))
            runner.map(self.little_fun, wav_path_list, {'category_name': category_name})
            runner.start()
            # for wav_path in wav_path_list:
            #     runner
            #     utils_file.logging_print(f'耿雪龙： 开始下载如下音频:{wav_path}')
            #     wav_id = wav_path.split('/')[-1]
            #     album_id = wav_path.split('/')[-3]
            #     self.get_wav_whole_url(album_id, wav_id, category_name)

    def login(self, user_id='phone_number', password='password'):
        data = {
            'account_type': '5',
            'device_id': 'web',
            'user_id': user_id,
            'password': password
        }
        response = requests.post(self.login_url, data=data, headers=utils_spider.COMMON_HEADER)
        if response.status_code == 200:
            temp = response.json()
            errorno = temp['errorno']
            errormsg = temp['errormsg']
            if errorno == 0:
                utils_file.logging_print('login successful!')
                data = temp['data']
                self.qingting_id = data['qingting_id']
                self.access_token = data['access_token']

            else:
                utils_file.logging_print('Login failed')
                print(errormsg)
        self.print_token()

    def print_token(self):
        utils_file.logging_print(self.access_token)
        utils_file.logging_print(self.qingting_id)

    def get_wav_whole_url(self, album_id='474184', wav_id='25643023', category_name='音乐'):
        base_url = "https://audio.qingting.fm"
        bookid = album_id
        id = wav_id
        wav_path = utils_file.join_path(self.output_dir, 'wav', category_name, bookid,
                                        f'{wav_id}_{bookid}.mp3')
        utils_file.logging_print(f'开始得到如下音频的url,wav_path: {wav_path}')
        if os.path.exists(wav_path):
            utils_file.logging_print(f'{wav_id}_{bookid}已存在,不再下载')
            return
        access_token = ""
        qingting_id = ""
        timestamp = str(round(time.time() * 1000))
        data = f"/audiostream/redirect/{bookid}/{id}?access_token={access_token}&device_id=MOBILESITE&qingting_id={qingting_id}&t={timestamp}"
        message = data.encode('utf-8')
        key = "fpMn12&38f_2e".encode('utf-8')
        sign = hmac.new(key, message, digestmod='MD5').hexdigest()
        whole_url = base_url + data + "&sign=" + sign
        utils_file.logging_print(f'得到url, 如下：{whole_url}')
        try:
            utils_file.download_file(whole_url, utils_file.join_path(self.output_dir, 'wav', category_name, bookid),
                                     f'{wav_id}_{bookid}', 'mp3')
        except Exception as e:
            utils_file.logging_print(f'get_wav_whole_url函数执行报错, 爆错内容为{e}')
            # traceback.print_exc()

    def little_fun(self, wav_path, category_name):
        utils_file.logging_print(f'耿雪龙： 开始下载如下音频:{wav_path}')
        wav_id = wav_path.split('/')[-1]
        album_id = wav_path.split('/')[-3]
        self.get_wav_whole_url(album_id, wav_id, category_name)


class GxlSpider_2:
    """"""

    def __init__(self,thread_num = 4, output_dir='/home/node36_data/qingting_fm'):
        """"""
        self.access_token = None
        self.qingting_id = None
        self.login_url = "https://user.qtfm.cn/u2/api/v4/user/login"
        self.root_url = 'https://www.qtfm.cn'
        self.start_url = 'https://www.qtfm.cn/categories'
        self.output_dir = output_dir
        utils_file.makedir_sil(self.output_dir)
        self.thread_num = thread_num
        self.login()
        self.print_token()

    def login(self, user_id='phone_number', password='password'):
        data = {
            'account_type': '5',
            'device_id': 'web',
            'user_id': user_id,
            'password': password
        }
        response = requests.post(self.login_url, data=data, headers=utils_spider.COMMON_HEADER)
        if response.status_code == 200:
            temp = response.json()
            errorno = temp['errorno']
            errormsg = temp['errormsg']
            if errorno == 0:
                utils_file.logging_print('login successful!')
                data = temp['data']
                self.qingting_id = data['qingting_id']
                self.access_token = data['access_token']

            else:
                utils_file.logging_print('Login failed')
                print(errormsg)
        self.print_token()

    def print_token(self):
        utils_file.logging_print(self.access_token)
        utils_file.logging_print(self.qingting_id)

    def download_each_category(self):
        utils_file.logging_print("开始逐个下载每一个种类的音频")
        input_root_dir = "/home/node36_data/qingting_fm/wav_info/"
        category_name_list = os.listdir(input_root_dir)
        utils_file.logging_print(f'一共有{len(category_name_list)}个种类, 这些种类分别为:')
        utils_file.logging_print(f'{category_name_list}')
        for category_name in category_name_list:
            utils_file.logging_print(f'开始下载 {category_name} 种类的音频')
            album_info_dir = utils_file.join_path(input_root_dir, category_name)
            album_path_list = glob.glob(utils_file.join_path(album_info_dir, '*.list'))
            utils_file.logging_print(f'开始逐个下载每一个专辑的音频, 一共有 {len(album_path_list)} 个专辑')
            for i, album_path in enumerate(album_path_list):
                utils_file.logging_print(
                    f'开始下载  {category_name} 种类的第 {i + 1}/{len(album_path_list)} 个专辑的音频,使用线程数:{self.thread_num} 这个专辑信息的path是 {album_path}')
                finish_file_path = utils_file.join_path(album_path.replace('.list', '.finish'))
                if os.path.exists(finish_file_path):
                    utils_file.logging_print(
                        f'该专辑下载已被下载完毕,不再重复下载，下载的是 {category_name} 的第 {i + 1}/{len(album_path_list)} 个专辑')
                    continue
                wav_path_list = utils_file.load_list_file_clean(album_path)
                runner = GxlFixedThreadPool(
                    self.thread_num if len(wav_path_list) > self.thread_num else len(wav_path_list))
                runner.map(self.little_fun4download_wav, wav_path_list, {'category_name': category_name})
                runner.start()
                utils_file.logging_print(
                    f"该专辑下载完成， 下载的是 {category_name} 的第 {i + 1}/{len(album_path_list)} 个专辑")
                utils_file.logging_print(f'下载完成后休眠 1 秒')
                utils_file.logging_print()
                utils_file.logging_print()
                utils_file.logging_print()
                utils_file.logging_print()
                finish_file_path = utils_file.join_path(album_path.replace('.list', '.finish'))
                with open(finish_file_path, 'w') as f:
                    pass
                time.sleep(1)

    def little_fun4download_wav(self, wav_path, category_name):
        """"""
        utils_file.logging_print(f'耿雪龙： 开始下载如下音频:{wav_path}')
        wav_id = wav_path.split('/')[-1]
        album_id = wav_path.split('/')[-3]
        base_url = "https://audio.qingting.fm"
        bookid = album_id
        id = wav_id
        wav_path = utils_file.join_path(self.output_dir, 'wav', category_name, bookid,
                                        f'{wav_id}_{bookid}.mp3')
        utils_file.logging_print(f'开始得到如下音频的url,wav_path: {wav_path}')
        if os.path.exists(wav_path):
            utils_file.logging_print(f'{wav_id}_{bookid}已存在,不再下载')
            return
        timestamp = str(round(time.time() * 1000))
        data = f"/audiostream/redirect/{bookid}/{id}?access_token={self.access_token}&device_id=MOBILESITE&qingting_id={self.qingting_id}&t={timestamp}"
        message = data.encode('utf-8')
        key = "fpMn12&38f_2e".encode('utf-8')
        sign = hmac.new(key, message, digestmod='MD5').hexdigest()
        whole_url = base_url + data + "&sign=" + sign
        utils_file.logging_print(f'得到url, 如下：{whole_url}')
        try:
            utils_file.download_file(whole_url, utils_file.join_path(self.output_dir, 'wav', category_name, bookid),
                                     f'{wav_id}_{bookid}', 'mp3')
        except Exception as e:
            utils_file.logging_print(f'get_wav_whole_url函数执行报错, 爆错内容为{e}')
            # traceback.print_exc()


if __name__ == '__main__':
    # gxl_spider = GxlSpider('/home/node36_data/qingting_fm/')
    # gxl_spider = GxlSpider('./output/qingting_fm/')
    # gxl_spider.handle_root_category()
    # gxl_spider.handle_category_index_fenye()
    # gxl_spider.handle_ibum_index_fenye()
    # gxl_spider.get_wav_info()
    # gxl_spider.login()
    # gxl_spider.print_token()
    # gxl_spider.get_wav_whole_url()
    gxl_spider = GxlSpider_2()
    gxl_spider.download_each_category()
