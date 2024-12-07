import time

from gxl_ai_utils.utils import utils_file, utils_spider
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Spider_Wangyiyun:

    def __init__(self):
        pass

    def do_spider(self):
        url = "view-source:https://music.163.com/discover/artist/cat?id=1001"
        url2 = "https://music.163.com/#/discover/artist/cat?id=1002"
        xpath = '/html/body/div[3]/div[2]/div/div/div[2]/ul/li[12]/a[2]/@href'

        driver = utils_spider.get_a_driver()
        driver.get(url)
        driver.implicitly_wait(2)
        time.sleep(2)
        page_html = driver.page_source
        utils_spider.write_to_html(page_html, './text2.html')
        res = utils_spider.handle_xpath(page_html, xpath)
        print(res)


if __name__ == '__main__':
    spider = Spider_Wangyiyun()
    # spider.do_spider()
    import re

    # 读取文件中的字符串
    with open('./text2.html', 'r', encoding='utf-8') as file:
        data = file.read()

    # 使用正则表达式匹配所有 id 值
    ids = re.findall(r'/user/home\?id=(\d+)', data)

    # 输出所有匹配到的 id 值
    for id_value in ids:
        print(id_value)
