import tqdm

from gxl_ai_utils.utils import utils_spider, utils_file
from gxl_ai_utils.thread.my_thread import GxlFixedThreadPool


class GxlSpider(object):
    def __init__(self, output_root='./output/lizhi_fm/'):
        self.root_url = 'https://www.lizhi.fm'
        self.root_start_url = 'https://www.lizhi.fm/hot/'
        self.output_root = output_root
        utils_file.makedir_sil(self.output_root)

    def __del__(self):
        print('程序完全结束')

    def get_label_list_from_root(self):
        """得到每个类别的入口"""
        print('get_label_list________________________')
        xpath = '/html/body/div[1]/div[2]/div[2]/div/div/ul/li/a/@href'
        xpath_text = '/html/body/div[1]/div[2]/div[2]/div/div/ul/li/a/text.txt()'
        res_data = utils_spider.hande_href(self.root_start_url, xpath)
        res_text = utils_spider.hande_href(self.root_start_url, xpath_text)
        res = []
        for data, text in zip(res_data, res_text):
            data = utils_file.join_path(self.root_url, data)
            res.append({'url': data, 'label_text': utils_file.get_clean_filename(text)})
        utils_file.print_list(res)
        utils_file.write_dict_list_to_jsonl(res, self.output_root + 'label_list.jsonl')
        return res

    def get_album_list_from_label(self, label_root_url='https://www.lizhi.fm/label/24229910635091632/',
                                  label_text='古风剧'):
        xpath = '/html/body/div[1]/div[2]/div[1]/div/ul/li/p[1]/a/@href'
        xpath_text = '/html/body/div[1]/div[2]/div[1]/div/ul/li/p[1]/a/text.txt()'
        xpath_next_button_class = '/html/body/div[1]/div[2]/div[1]/div/div[3]/div/a/@class'
        xpath_next_button_href = '/html/body/div[1]/div[2]/div[1]/div/div[3]/div/a/@href'
        res = []
        temp_url = label_root_url
        print('开始爬取专辑列表for label: ', label_text)
        while True:
            res_data = utils_spider.hande_href(temp_url, xpath)
            res_text = utils_spider.hande_href(temp_url, xpath_text)
            for data, text in zip(res_data, res_text):
                data = 'https:' + data
                text = text.strip()
                res.append({'url': data, 'album_text': utils_file.get_clean_filename(text),
                            'label_text': utils_file.get_clean_filename(label_text)})
            res_tuple_list = utils_spider.handle_href_for_two(temp_url, xpath_next_button_class, xpath_next_button_href)
            next_class = res_tuple_list[-1][0]
            next_href = res_tuple_list[-1][1]
            if next_class is not None and next_class == 'next':
                print('存在下一页')
                next_href = utils_file.join_path(label_root_url, next_href)
                temp_url = next_href
            else:
                print('不存在下一页')
                break
        utils_file.print_list(res)
        utils_file.write_dict_list_to_jsonl(res, self.output_root + 'album_list.jsonl', True)
        return res

    def get_album_all(self, label_list_jsonl: str = None):
        if label_list_jsonl is None:
            label_list_jsonl = self.output_root + 'label_list.jsonl'
        res = utils_file.load_dict_list_from_jsonl(label_list_jsonl)
        album_list_jsonl = self.output_root + 'album_list.jsonl'
        utils_file.remove_file(album_list_jsonl)
        for album in res:
            try:
                self.get_album_list_from_label(album['url'], album['label_text'])
            except Exception as e:
                print(e)

    def get_wav_list_from_album(self, album_root_url='https://www.lizhi.fm/user/2508915499400425516',
                                album_text='风流逐声工作室', label_text='古风剧'):
        """
        egs:
        http://cdn5.lizhi.fm/audio/2018/12/18/5015683937864290822_hd.mp3
        https://www.lizhi.fm/3684359/5015683937864290822

        :param album_text:
        :param label_text:
        :param album_root_url:
        :return:
        """
        page_xpath = '/html/body/div[1]/div[2]/div[5]/div[2]/div/a/@href'
        temp_res = utils_spider.hande_href(album_root_url, page_xpath)
        res = [album_root_url]
        for data in temp_res:
            data = self.root_url + data
            res.append(data)
        res = res[:-1]
        utils_file.print_list(res)
        res_wav_page_url = []
        for index, page_url in enumerate(res):
            i_div = 5
            if index != 0:
                i_div = 4
            print(f'开始获得 {page_url} 这个album页面的wav列表')
            xpath_href = f'/html/body/div[1]/div[2]/div[{i_div}]/ul/li/a/@href'
            xpath_text = f'/html/body/div[1]/div[2]/div[{i_div}]/ul/li/a/@title'
            css = 'body > div.wrap > div.frame > div:nth-child(5) > ul'
            res_wav_temp = utils_spider.handle_href_for_two(page_url, xpath_href, xpath_text)
            for href, the_class in res_wav_temp:
                href = self.root_url + href
                res_wav_page_url.append((href, the_class))
            utils_file.print_list(res_wav_temp)
        utils_file.print_list(res_wav_page_url)
        print('开始得到wav文件的url地址')
        wav_mp3_list = []
        time_xpath = '/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/p[1]/span[1]/text.txt()'
        for href, text in tqdm.tqdm(res_wav_page_url, desc='获得wav文件的url地址', total=len(res_wav_page_url)):
            res = utils_spider.hande_href(href, time_xpath)
            year, month, day = res[0].split('-')
            wav_id = href.split('/')[-1]
            wav_mp3_data_url = f'http://cdn5.lizhi.fm/audio/{year}/{month}/{day}/{wav_id}_hd.mp3'
            wav_mp3_list.append({'url': wav_mp3_data_url,
                                 'wav_text': utils_file.get_clean_filename(text),
                                 'album_text': utils_file.get_clean_filename(album_text),
                                 'label_text': utils_file.get_clean_filename(label_text)})
        utils_file.print_list(wav_mp3_list)
        utils_file.write_dict_list_to_jsonl(wav_mp3_list, self.output_root + 'wav_list.jsonl')
        # return wav_mp3_list
        self.download_wav(wav_mp3_list)

    def download_wav(self, wav_list_jsonl: str | list = None):
        if wav_list_jsonl is None:
            wav_list_jsonl = self.output_root + 'wav_list.jsonl'
        if type(wav_list_jsonl) == str:
            wav_list: list[dict] = utils_file.load_dict_list_from_jsonl(wav_list_jsonl)
        else:
            wav_list: list[dict] = wav_list_jsonl
        multi_thread_runner = GxlFixedThreadPool(10)
        for wav in wav_list:
            wav_url = wav['url']
            wav_text = wav['wav_text']
            album_text = wav['album_text']
            label_text = wav['label_text']
            print(f'开始下载{wav_url}, {wav_text},{album_text},{label_text}')
            wav_id = wav_url.split('/')[-1].split('_')[0]
            filename = f'{wav_id}_{wav_text}'
            suffix = 'mp3'
            target_dir = self.output_root + label_text + '/' + album_text + '/'
            multi_thread_runner.add_thread(utils_file.download_file, [wav_url, target_dir, filename, suffix])
        multi_thread_runner.start()

    def get_wav_list_all(self, album_list_jsonl: str | list = None):
        """
        开始逐个专辑得下载音频
        :param album_list_jsonl:
        :return:
        """
        if album_list_jsonl is None:
            album_list_jsonl = self.output_root + 'album_list.jsonl'
        if isinstance(album_list_jsonl, str):
            album_list: list[dict] = utils_file.load_dict_list_from_jsonl(album_list_jsonl)
        else:
            album_list: list[dict] = album_list_jsonl
        for album in album_list:
            try:
                self.get_wav_list_from_album(album['url'], album['album_text'], album['label_text'])
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 得到下载器对象， output_root是得到文件的保存根地址。秩序指定根目录。所得音频会自动按照 root/类别目录/专辑目录/*.mp3 形式存放
    spider = GxlSpider(output_root='./output/lizhi_fm/')
    # 得到类列表，label_list.jsonl，耗时一会儿，一共63个类，供给下面函数使用
    spider.get_label_list_from_root()
    # 根据label_list.jsonl文件得到专辑列表,album_list.jsonl， 一共8000+专辑，耗时好一会儿， 供给下面函数使用
    spider.get_album_all()
    # 根据album_list.jsonl文件，开始正式下载,这个等师兄通知让做的时候在运行,逐个专辑得下载，下载时采用10个进程， 正式开始下载音频文件，原文件格式为mp3,暂未改动，会持续多天时间
    # 你在测试代码时，可以先运行过前2个函数，得到该下载函数所需的jsonl文件；之后如果想测试下载函数，可以在album_list.jsonl文件中只放入几个专辑，其他全部删除，然后运行该函数就可下载保留的专辑音频
    # spider.get_wav_list_all()
