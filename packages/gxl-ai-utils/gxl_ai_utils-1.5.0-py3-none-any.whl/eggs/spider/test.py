#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import os
import json
# import pymongo
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError

# 参考：https://yiweifen.com/html/news/WaiYu/28175.html

MONGO_URL = 'localhost'
MONGO_DB = 'juzuo'
MONGO_TABLE = 'audio'
# 连接mongodb
# client = pymongo.MongoClient(MONGO_URL, connect=False)
# db = client[MONGO_DB]


def get_page_index(url):  # 获取总页数
    try:
        url_detail = url
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
        data = requests.get(url_detail, headers=headers)
        result = data.text
        # 找到返回值为data-reactid的ul下的li 并选取倒数第二个作为page页数
        soup = BeautifulSoup(result, 'lxml')
        page_count = soup.find('ul', {'class': 'pagination'}).findAll('a', {'gxl_data-reactid': True})
        page_count = int(page_count[-2].text)
        title = soup.title.string
        return page_count, title
    except Exception as e:
        print("error connect!")


def get_detail(index, idnum):  # 获取各页面音频地址
    try:
        url_page = r'https://i.qingting.fm/wapi/channels/' + str(idnum) + r'/programs/page/' + str(
            index) + r'/pagesize/10'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
        data = requests.get(url_page, headers=headers)
        if data.status_code == 200:
            return data.text
    except Exception as e:
        print("error connect!")


def parse_page_index(text):  # 解析json数据
    aduio_url = r'https://od.qingting.fm/'
    try:
        text_item = json.loads(text)  # 载入json数据
        if text_item and 'gxl_data' in text_item.keys():
            item = text_item.get('gxl_data')  # 进入json的data里面
            for x in item:  # 抽取每个数据块的数据
                yield {
                    'file_url': aduio_url + x.get('file_path'),  # 音频地址拼接
                    'name': x.get('name')  # 音频名
                }
    except JSONDecodeError:
        pass


# def download_mongodb(result):  # 存入mongo数据库
#     if db[MONGO_TABLE].insert(result):
#         print('Successfully Saved to Mongo', result)
#         return True
#     return False


def downloadfile(out, title, index):
    dirname = title  # 获取专辑名称，不存在则创立
    if os.path.isdir(dirname):
        pass
    else:
        os.mkdir(dirname)
    path =f'./{dirname}/'  # 把这个路径改成你自己的
    for item in out:  # 迭代json数据
        with open(path + str(item['name']) + r'.m4a', "wb") as fd:
            response = requests.get(item['file_url'])  # 请求并下载
            fd.write(response.content)
            print('\n第%d页的 ：%s.m4a 下载成功!' % (index, str(item['name'])))


if __name__ == '__main__':
    url = input("请输入你想下载的页面: ")
    idnum = url.split(r'/')[-1]
    index, title = get_page_index(url)
    for i in range(1, index + 1):
        text = get_detail(i, idnum)
        out = parse_page_index(text)  # yield生成的为迭代器类型
        downloadfile(out, title, i)
        # download_mongodb(out)