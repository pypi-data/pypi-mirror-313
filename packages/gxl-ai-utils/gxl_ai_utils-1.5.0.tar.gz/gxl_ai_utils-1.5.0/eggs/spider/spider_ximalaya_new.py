import glob
import math
import os
import traceback

import tqdm

import gxl_ai_utils.AiConstant
from gxl_ai_utils.utils import utils_file, utils_spider

logger = gxl_ai_utils.AiConstant.AI_LOGGER()

PAGE_SIZE = 30
SORT_TYPE = 0  # 0: 正序,1:倒序
SAVE_WITH_TITLE = True
SAVE_WITH_ALBUM_ID = True


class GxlSpider(object):
    def __init__(self, output_root='./output/ximalaya/'):
        self.root_url = "https://www.ximalaya.com/category"
        self.root_start_url = "https://www.ximalaya.com/category"
        self.output_root = output_root
        utils_file.makedir_sil(self.output_root)

    def get_category_info(self):
        """
        得到每个类别的地址，存储为output_root/category.json
        :return:
        """
        xpath_href = '//*[@id="award"]/main/div[1]/div[2]/div/a/@href'
        xpath_title = '//*[@id="award"]/main/div[1]/div[2]/div/a/text()'
        hrefs = utils_spider.hande_href(self.root_start_url, xpath_href)
        titles = utils_spider.hande_href(self.root_start_url, xpath_title)
        datas = {}
        for title, href in zip(titles, hrefs):
            datas[title] = utils_file.join_path(self.root_start_url, href.split('/')[2])
        utils_file.print_dict(datas)
        utils_file.write_dict_to_json(datas, utils_file.join_path(self.output_root, 'category.json'))
        # threads = []
        # for item in datas.items():
        #     if item[0] == "音乐":
        #         logger.info('不再处理音乐专辑音乐')
        #         continue
        #     thread = threading.Thread(target=handle_category_index_fenye, args=(item[0], item[1]))
        #     thread.start()
        #     threads.append(thread)
        # for thread in threads:
        #     thread.join()

    def handle_category_fenye(self):
        """
        分页处理函数
        通过category.json文件数据， 分别获取每个类别的所有专辑的ID list, 并存入文件保存。
        文件保存地址为 output_root/album_info/{category}.list
        """
        category_info = utils_file.load_dict_from_json(os.path.join(self.output_root, 'category.json'))
        for category, url in category_info.items():
            logger.info(f'开始处理{category}')
            utils_file.makedir_for_file_or_dir(os.path.join(self.output_root, 'album_info', f'{category}.list'))
            utils_file.remove_file(os.path.join(self.output_root, 'album_info', f'{category}.list', 'index'))
            # 先得到该类别的分页数
            xpath = '//*[@id="award"]/main/div[1]/div[3]/div[3]/nav/div/form/input[2]/@max'
            res = utils_spider.hande_href(url, xpath)
            num_fenye = int(res[0])
            logger.info(f'该类别的分页数为{num_fenye}')
            try:
                self.handle_category_index(category, url)
            except Exception as e:
                logger.info(f'分页1的handle_category_index函数执行报错, 爆错内容为{e}')
                traceback.print_exc()
            for i in range(2, num_fenye + 1):
                try:
                    self.handle_category_index(category, utils_file.join_path(url, f'p{i}'))
                except Exception as e:
                    logger.info(f'分页{i}的handle_category_index函数执行报错, 爆错内容为{e}')
                    traceback.print_exc()
            break

    def handle_category_index(self, category, url):
        """
        得到当前类别的当前分页的所有的album ID, 并写入文件保存。
        :param category:
        :param url:
        :return:
        """
        logger.info(f'开始加载 {category} 类别的如下分页页面:' + url + ' ------------------------------')
        logger.info(f'加载成功, 开始处理 {category} 主页')
        xpath = '//ul[@class="_ZV"]/li[@class="_ZV"]/div[@class="album-wrapper   undefined T_G"]//div[@class="album-wrapper-card T_G"]/a[@class="album-cover   lg needhover _hW"]'
        datas = utils_spider.hande_href(url, xpath)
        xpath_for_title = '//*[@id="award"]/main/div[1]/div[3]/div[2]/ul/li/div/a[1]/span/text()'
        titles = utils_spider.hande_href(url, xpath_for_title)
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
        res3 = set(res3)
        logger.info(f"处理{category}主页成功, 得到当前分页的每个免费专辑的地址:")  # 删除付费专辑
        utils_file.print_list(list(res3))
        res3 = [x.split('/')[-1] for x in res3]
        utils_file.write_list_to_file(res3,
                                      utils_file.join_path(self.output_root, 'album_info', f'{category}.list'), True)

    def handle_album_fenye(self):
        """
        通过album_info 目录，得到每个分类下的每个专辑下的所有音频链接。并存储到文件中。

        :return:
        """
        albums_path_list = glob.glob(os.path.join(self.output_root, 'album_info', '*.list'))
        utils_file.print_list(albums_path_list)
        for albums_path in albums_path_list:
            category = os.path.basename(albums_path).split('.')[0]
            logger.info(f'开始得到{category}专辑的音频链接')
            utils_file.makedir_sil(os.path.join(self.output_root, 'audio_info', category))
            album_id_list = utils_file.load_list_file_clean(albums_path)
            for album_id in tqdm.tqdm(album_id_list):
                self.handle_album(category, album_id)

    def handle_album(self, category, album_id):
        """
        获得每个专辑的所有音频地址，并存储为文件， 文件位置为：
        output_root/audio_info/{category}/{album_id}.list
        album_id:型如 '9723091'
        分页获取数据
        audio:
        https://aod.cos.tx.xmcdn.com/storages/3842-audiofreehighqps/AC/76/GKwRIasJOqrJAU25xAKDendP.m4a
        https://aod.cos.tx.xmcdn.com/storages/eb2c-audiofreehighqps/48/79/GKwRIUEJDNFhARzq2gJyonzx.m4a


        """
        url_data = f"https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={str(album_id)}&pageNum={1}&sort={SORT_TYPE}&pageSize={PAGE_SIZE}"
        logger.info(f'开始处理专辑(伴随分页模式),album_id:{album_id} ========')
        logger.info('开始获取总页数')
        response = utils_spider.send_request(url_data)
        if response is None:
            return
        json_data = response.json()
        if json_data is None:
            return
        try:
            total_num = json_data['gxl_data']['trackTotalCount']
        except Exception as e:
            logger.info('json_data解析失败,未在指定路径获取该专辑音频总数')
            return
        # total_page = int(total_num / 30) + 1
        total_page = math.ceil(int(total_num) / 30)
        logger.info(f'总页数为:{total_page}')
        utils_file.remove_file(os.path.join(self.output_root, 'audio_info', category, f'{album_id}.list'))
        for i in range(1, total_page + 1):
            logger.info(f'开始处理专辑{album_id}的第{i}页')
            url = f"https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={album_id}&pageNum={i}&sort={SORT_TYPE}&pageSize={PAGE_SIZE}"
            response = utils_spider.send_request(url)
            if response is None:
                continue
            json_data = response.json()
            if json_data is None:
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
            if title_list is None:
                title_list = []
            logger.info(f'开始利用异步请求从ids得到每个id对应的音频路径')
            if len(ids) != len(title_list):
                logger.info("ids与titles长度不一致, title并不重要, 使其强行一致即可")
                if len(ids) > len(title_list):
                    for _ in range(len(ids) - len(title_list)):
                        title_list.append("")
                else:
                    title_list = title_list[:len(ids)]
            res = []
            for id, title in zip(ids, title_list):
                logger.info(f'开始加载音频{id}的json数据')
                url = f"https://www.ximalaya.com/revision/play/v1/audio?id={id}&ptype=1"
                response = utils_spider.send_request(url)
                if response is None:
                    continue

                json_res = response.json()
                if json_data is None:
                    continue
                else:
                    logger.info(f'音频{id}的json数据加载成功')

                try:
                    src = json_res['gxl_data']['src']
                except Exception as e:
                    logger.info(f'音频{id}的json数据解析失败,未在指定路径得到音频地址')
                    continue
                logger.info(f'音频{id}的json数据解析成功,开始保存音频')
                res.append({'title': title, 'src': src, "id": id})
            utils_file.print_list(res)
            utils_file.write_dict_list_to_jsonl(res, os.path.join(self.output_root, 'audio_info', category,
                                                                 f'{album_id}.list'), True)


if __name__ == '__main__':
    spider = GxlSpider()
    # spider.get_category_info()
    # spider.handle_category_fenye()
    spider.handle_album_fenye()
