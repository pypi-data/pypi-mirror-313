import os.path
import re
import time

from tqdm import tqdm

from gxl_ai_utils.utils import utils_spider, utils_file
from bs4 import BeautifulSoup


# ai_yuyin_zhuanlan_url = "https://www.zhihu.com/column/c_1306669801105391616"
# article_url_xpath = "/html/body/div[1]/div/main/div/div[4]/div/div/div/div/h2/span/a/@href"

def get_zhuanji_list_by_search_word(search_word="语音"):
    """"""
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(50)
    # time.sleep(50)
    url = f'https://www.zhihu.com/search?q={search_word}&type=column'
    url = "https://www.zhihu.com/search?type=column&q=%E5%93%88%E5%93%88"
    # page_str = utils_spider.send_request(url).text
    # print(page_str)
    with open("./zhihu_search_by_语音.html", 'r', encoding='utf-8') as file:
        page_str = file.read()
    print(page_str)
    # page_str, driver = utils_spider.get_source_page_from_url(url, is_debug_chrome=False, wait_time=5)
    # href_xpath =  "/html/body/div[1]/div/main/div/div[2]/div[3]/div/div/div/div/div/div/div/div/div[2]/h2/span/div/a/@href"
    href_xpath = '//*[@id="SearchMain"]/div/div/div/div/div/div/div/div/div[2]/h2/span/div/a/@href'
    href_list = utils_spider.handle_xpath(page_str, href_xpath)
    res_dict = []
    for href in href_list:
        print(href)
        res_dict.append(href)
    utils_file.write_list_to_file(res_dict, "./output/zhihu/zhuanji_list.txt")

def do_get_url_for_a_zhaunji(zhuanji_url:str):
    ai_yuyin_zhuanlan_url = zhuanji_url
    zhuanji_name_xpath = "/html/body/div[1]/div/main/div/div[2]/div/div[1]/text()"
    article_url_xpath = "/html/body/div[1]/div/main/div/div[4]/div/div/div/div/h2/span/a/@href"
    output_dir = './output/zhihu'
    utils_file.makedir_sil(output_dir)
    page_str, driver = utils_spider.get_source_page_from_url(ai_yuyin_zhuanlan_url)
    article_path_list = utils_spider.handle_xpath(page_str, article_url_xpath)
    zhuanji_name = utils_spider.handle_xpath(page_str, zhuanji_name_xpath)[0]
    now_lens = len(article_path_list)
    for i in range(500):
        # 执行JavaScript来滚动滑轮
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待页面加载
        time.sleep(2)
        page_str = driver.page_source
        article_path_list = utils_spider.handle_xpath(page_str, article_url_xpath)
        next_lens = len(article_path_list)
        if now_lens == next_lens:
            break
        else:
            now_lens = next_lens
        utils_file.logging_print(f"i:{i} now_lens:{now_lens} next_lens:{next_lens}")
    utils_file.write_list_to_file(article_path_list,
                                  os.path.join(output_dir, "article_path_list", f"article_path_list_{zhuanji_name}.txt"))

    output_file_path = os.path.join(output_dir, "article_content", f"zhihu_{zhuanji_name}.jsonl")
    utils_file.makedir_for_file_or_dir(output_file_path)
    for url in tqdm(article_path_list, total=len(article_path_list)):
        url = 'https:' + url
        dict_res = handle_a_page_url(url, driver)
        utils_file.write_single_dict_to_jsonl(dict_res, output_file_path)


def handle_a_page_url(page_url, driver):
    """
    知乎的request得到的文本被加密了,无法解码成正常字符串,都是乱码
    :param page_url:
    :return:
    """
    # response = utils_spider.send_request(page_url, encoding='utf-8')
    # content = response.content
    # print(response.apparent_encoding)
    # print(response.encoding)
    # html_str = content[100:].decode()
    # soup = BeautifulSoup(response.content, "html.parser")
    # 打印解析后的文本内容
    # html_str = (soup.get_text())
    id = page_url.split("/")[-1]
    html_str, driver = utils_spider.get_source_page_from_url_have_driver(page_url, driver)
    title_xpath = "/html/body/div[1]/div/main/div/article/header/h1/text()"
    title = utils_spider.handle_xpath(html_str, title_xpath)[0]
    title = title.replace("\u200b", "")
    title = title.replace("​", "")
    content_xpath = "/html/body/div[1]/div/main/div/article/div[1]/div/div/div//text()"
    res = utils_spider.handle_xpath(html_str, content_xpath)
    # print(res)
    final_txt = ""
    for txt in res:
        if txt is None or txt == "" or txt == "\n" or txt == "\t" or txt == "\u200b":
            continue
        final_txt += txt
    final_txt = final_txt.replace("\u200b", "")
    final_txt = re.sub(r'\s{2,}', ' ', final_txt)
    final_txt = final_txt.replace("\n", "")
    return dict(id=id, title=title, content=final_txt)


if __name__ == '__main__':
    """"""
    all_zhuanji_list = utils_file.load_list_file_clean("./output/zhihu/zhuanji_list.txt")
    runner = utils_file.GxlFixedThreadPool(10)
    for zhuanji_url in all_zhuanji_list:
        zhuanji_url = 'https:' + zhuanji_url
        runner.add_task(do_get_url_for_a_zhaunji, [zhuanji_url])
    runner.start()
