import os
import threading
import time
import traceback

from sortedcontainers import SortedSet

from gxl_ai_utils.utils import utils_spider, utils_file
from gxl_ai_utils.AiConstant import AI_LOGGER

logger = AI_LOGGER()

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie": "_xmLog=h5&bbc1105d-db8f-4664-96af-86d46a1abadc&process.env.sdkVersion; 1&remember_me=y; 1&_token=293413321&4BAEDC40240N498E25AC5DD3EFA50F93A7308CB5D7574461E394BF9F4EB33C364865E35BA60C201MB4CD649CD4B91E3_; x-ats=ACNlNGE4Njc2MjAzZDdlM2Q1BTaNX3LXtAl4bXdlYl93d3c; xm-page-viewid=ximalaya-web; impl=www.ximalaya.com.login; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1696256199; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1696256199; web_login=1696256314748",
    "Host": "www.ximalaya.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}
#  下载wav时用的头
header2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "If-None-Match": "75a67e32a04595ac0c393b4c5ba53064",
    "Range": "bytes=0-104857500",  # 默认每个音频小于100兆, 多出的部分直接截断
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",

}

SAVE_PATH_OLD = utils_file.join_path("/home/work_nfs6/xlgeng/gxl_data", "pachong_ximalaya_2", "wav_files")
SAVE_PATH_OLD2 = '/home/backup_nfs5/xlgeng/asr_data/ximalaya'
SAVE_PATH = utils_file.join_path("/home/node36_data", "ximalaya")
# SAVE_PATH = join_path_plus(".", "output")
utils_file.makedir_for_file_or_dir(SAVE_PATH)
utils_file.makedir_for_file_or_dir(SAVE_PATH_OLD)
PAGE_SIZE = 30
SORT_TYPE = 0  # 0: 正序,1:倒序
SAVE_WITH_TITLE = True
SAVE_WITH_ALBUM_ID = True


def get_name_by_rules(id, album_id, title, with_album_id, with_title):
    adds = []
    if with_album_id:
        adds.append(album_id)
    if with_title:
        title = utils_file.get_clean_filename(title)
        adds.append(title)
    name = str(id)
    for item in adds:
        name = name + '_' + item
    name = name + '.wav'
    return name


def if_response_content_is_none(response):
    if response is None or response.content is None:
        logger.info('response or response.content为None,加载数据失败')
        return True
    return False


def if_json_data_is_none(json_data):
    if json_data is None:
        logger.info('json_data is None, 未获取到json数据')
        return True
    return False


def get_ids(datas):
    """
    datas: [strs]:str_list or str:str
    return : [ids]:list
    """
    if isinstance(datas, list):
        return [x.split('/')[-1] for x in datas]
    elif isinstance(datas, str):
        return [datas.split('/')[-1]]


def save_audio_from_url(category, src, id, album_id, title=""):
    audio_dir = utils_file.join_path(SAVE_PATH, category)
    utils_file.makedir_sil(audio_dir)
    # src = "https://aod.cos.tx.xmcdn.com/group30/M0B/8E/06/wKgJXlmENsjB7SPHAP-6990Rfew647-aacv2-48K.m4a"
    file_name = get_name_by_rules(id, album_id, title, SAVE_WITH_ALBUM_ID, SAVE_WITH_TITLE)
    logger.info(f'开始保存:file_name:{file_name},save_dir:{audio_dir}, album_id:{album_id},src:{src}')
    start = time.time()
    file_path = utils_file.join_path(audio_dir, file_name)
    file_path_old = utils_file.join_path(SAVE_PATH_OLD, category, file_name)
    file_path_old2 = utils_file.join_path(SAVE_PATH_OLD2, category, file_name)
    if os.path.exists(file_path) or os.path.exists(file_path_old) or os.path.exists(file_path_old2):
        logger.info(f'音频文{file_name}已存在, 不在需要请求该音频.')
        return
    response_audio = utils_spider.send_request(src, headers=header2)
    if response_audio is None:
        return
    if if_response_content_is_none(response_audio):
        return
    with open(file_path, 'wb') as f:
        f.write(response_audio.content)
    end = time.time()
    logger.info(f'结束保存, 用时:{end - start}秒,url:{src}, file_name:{file_name}')
    # logger.info("休眠1秒钟, 防止被封")
    logger.info("不再休眠,继续干..")
    # time.sleep(1)


def get_wav_from_ids(category, ids, album_id, titles=None):
    if titles is None:
        titles = []
    logger.info(f'开始利用异步请求从ids得到每个id对应的音频路径')
    if len(ids) != len(titles):
        logger.info("ids与titles长度不一致, title并不重要, 使其强行一致即可")
        if len(ids) > len(titles):
            for _ in range(len(ids) - len(titles)):
                titles.append("")
        else:
            titles = titles[:len(ids)]
    for id, title in zip(ids, titles):
        logger.info(f'开始加载音频{id}的json数据')
        url = f"https://www.ximalaya.com/revision/play/v1/audio?id={id}&ptype=1"
        response = utils_spider.send_request(url, headers=header)
        if response is None:
            continue

        json_res = response.json()
        if if_json_data_is_none(json_res):
            continue
        else:
            logger.info(f'音频{id}的json数据加载成功')

        try:
            src = json_res['gxl_data']['src']
        except Exception as e:
            logger.info(f'音频{id}的json数据解析失败,未在指定路径得到音频地址')
            continue
        logger.info(f'音频{id}的json数据解析成功,开始保存音频')
        try:
            save_audio_from_url(category, src, id, album_id, title)
        except Exception as e:
            logger.info(f'音频{id}的保存函数save_audio_from_url执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_alum_dependent_static_page(category, url):
    """
    通过解析静态页面获得音频地址,有错误的风险，获取的html文件并不一定是在浏览器看到的样子，可能是没渲染的状态
    url: 'https://www.ximalaya.com/album/9741525'
    """
    response = utils_spider.send_request(url, headers=header)
    if if_response_content_is_none(response):
        return
    logger.info('加载成功, 开始处理专辑')
    text = response.text
    tree = utils_spider.text2special_file(text)
    if tree is None:
        return
    xpath = "//li[@class='b_t']/div[@class='text b_t']/a/@to"
    datas = tree.xpath(xpath)
    ids = get_ids(datas)
    logger.info(f'处理专辑成功,得到该专辑所有音频id为:{ids}')
    get_wav_from_ids(category, ids, get_ids(url)[-1])


def handle_alum(category, album_id: str | int):
    """
    根据json数据获取信息
    album_id:型如 '9723091'
    分页获取数据
    """
    url_data = f"https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={str(album_id)}&pageNum={1}&sort={SORT_TYPE}&pageSize={PAGE_SIZE}"
    logger.info(f'开始处理专辑(伴随分页模式),album_id:{album_id} ========')
    logger.info('开始获取总页数')
    response = utils_spider.send_request(url_data, headers=header)
    if if_response_content_is_none(response):
        return
    json_data = response.json()
    if if_json_data_is_none(json_data):
        return
    try:
        total_num = json_data['gxl_data']['trackTotalCount']
    except Exception as e:
        logger.info('json_data解析失败,未在指定路径获取该专辑音频总数')
        return
    total_page = int(total_num / 30) + 1
    logger.info(f'总页数为:{total_page}')
    for i in range(1, total_page + 1):
        logger.info(f'开始处理专辑{album_id}的第{i}页')
        url = f"https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={album_id}&pageNum={i}&sort={SORT_TYPE}&pageSize={PAGE_SIZE}"
        response = utils_spider.send_request(url, headers=header)
        if if_response_content_is_none(response):
            continue
        json_data = response.json()
        if if_json_data_is_none(json_data):
            continue
        try:
            data_list = json_data['gxl_data']['tracks']
            ids_list = [track['trackId'] for track in data_list]
            title_list = [track['title'] for track in data_list]
        except Exception as e:
            logger.info('json_data解析失败,未在指定路径获取该专辑音频id列表')
            continue
        ids = ids_list
        logger.info(f'处理专辑成功,得到该专辑所有音频id为:{ids}')
        logger.info(f'处理专辑成功,得到该专辑所有音频titles为:{title_list}')
        try:
            get_wav_from_ids(category, ids, album_id, title_list)
        except Exception as e:
            logger.info(f'专辑{album_id}的get_wav_from_ids函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_category_index(category, url):
    logger.info(f'开始加载 {category} 主页:' + url + ' ------------------------------')
    response = utils_spider.send_request(url, headers=header)
    if if_response_content_is_none(response):
        return
    logger.info(f'加载成功, 开始处理 {category} 主页')
    response.encoding = 'utf-8'
    text = response.text  # 相声主页
    tree = utils_spider.text2special_file(text)
    if tree is None:
        return
    xpath = '//ul[@class="_ZV"]/li[@class="_ZV"]/div[@class="album-wrapper   undefined T_G"]//div[@class="album-wrapper-card T_G"]/a[@class="album-cover   lg needhover _hW"]'
    datas = tree.xpath(xpath)
    xpath_for_title = '//*[@id="award"]/main/div[1]/div[3]/div[2]/ul/li/div/a[1]/span/text()'
    titles = tree.xpath(xpath_for_title)
    res = []
    res2 = []
    res3 = []
    titles_res = []
    for data in datas:
        res.append(data.xpath(".//@href"))
        res2.append(data.xpath(".//img[@class='corner-img _hW']/@src"))  # 付费专辑特有图标
        for re1, re2, title in zip(res, res2, titles):
            if len(re2) == 0:
                res3.append(re1)
                titles_res.append(title)
    res3 = [x[0] for x in res3]
    res3 = SortedSet(res3)
    logger.info(f"处理{category}主页成功, 得到当前分页的每个免费专辑的地址:" + str(res3))  # 删除付费专辑
    # logger.info("处理主页成功, 得到当前分页的每个免费专辑的地址:" + str(titles))  # 删除付费专辑
    for data in res3:
        album_id = -1
        try:
            album_id = get_ids(data)[-1]
            handle_alum(category, album_id)
        except Exception as e:
            logger.info(f'主页:{url}的专辑{album_id}的handle_alum函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_category_index_fenye(category, url):
    """
    对类别主页进行分页处理
    """
    xpath = '//*[@id="award"]/main/div[1]/div[3]/div[3]/nav/div/form/input[2]/@max'
    response = utils_spider.send_request(url, headers=header)
    res = utils_spider.handle_xpath(response.text, xpath)
    num_fenye = int(res[0])
    try:
        handle_category_index(category, url)
    except Exception as e:
        logger.info(f'分页1的handle_category_index函数执行报错, 爆错内容为{e}')
        traceback.print_exc()
    for i in range(2, num_fenye + 1):
        try:
            handle_category_index(category, utils_file.join_path(url, f'p{i}'))
        except Exception as e:
            logger.info(f'分页{i}的handle_category_index函数执行报错, 爆错内容为{e}')
            traceback.print_exc()


def handle_big_index(url=None):
    url = "https://www.ximalaya.com/category"
    xpath_href = '//*[@id="award"]/main/div[1]/div[2]/div/a/@href'
    xpath_title = '//*[@id="award"]/main/div[1]/div[2]/div/a/text()'
    response = utils_spider.send_request(url, headers=header)
    tree = utils_spider.text2special_file(response.text)
    hrefs = tree.xpath(xpath_href)
    titles = tree.xpath(xpath_title)
    datas = {}
    for title, href in zip(titles, hrefs):
        datas[title] = utils_file.join_path(url, href.split('/')[2])
    print(datas)
    for item in datas.items():
        if item[0] == "音乐":
            logger.info('不再处理音乐专辑音乐')
            continue
        handle_category_index_fenye(item[0], item[1])


def handle_big_index_with_multi_thread(url=None):
    url = "https://www.ximalaya.com/category"
    xpath_href = '//*[@id="award"]/main/div[1]/div[2]/div/a/@href'
    xpath_title = '//*[@id="award"]/main/div[1]/div[2]/div/a/text()'
    response = utils_spider.send_request(url, headers=header)
    tree = utils_spider.text2special_file(response.text)
    hrefs = tree.xpath(xpath_href)
    titles = tree.xpath(xpath_title)
    datas = {}
    for title, href in zip(titles, hrefs):
        datas[title] = utils_file.join_path(url, href.split('/')[2])
    print(datas)
    threads = []
    for item in datas.items():
        if item[0] == "音乐":
            logger.info('不再处理音乐专辑音乐')
            continue
        thread = threading.Thread(target=handle_category_index_fenye, args=(item[0], item[1]))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
