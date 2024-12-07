import os.path

import tqdm

from gxl_ai_utils.utils import utils_spider, utils_file
from gxl_ai_utils.thread.my_thread import GxlFixedThreadPool


class GxlSpider(object):
    def __init__(self, output_root='./output/yunting/'):
        self.root_url = 'https://www.radio.cn/pc-portal/erji/radioStation.html'
        self.root_start_url = 'https://www.radio.cn/pc-portal/erji/radioStation.html'
        self.output_root = output_root
        utils_file.makedir_sil(self.output_root)

    def __del__(self):
        print('程序完全结束')

    def get_audio_station(self):
        """
        得到所有的广播台的地址，每个广播台有多个节目，每个节目有多个音频
        得到每个节目的往期页面的地址， 每个地址可由节目id唯一确定，所以可以只存id
        格式： https://www.radio.cn/pc-portal/sanji/zhibo_2.html?channelname=0&name={id}&title=radio
        :return:
        """
        url_list_dict = {}
        xpath_daintai = '/html/body/div[3]/div/div[2]/div[2]/div/ul/li[22]'
        xpath_wangqi = '/html/body/div[3]/div/div[2]/div[3]/div[1]/table/tr/td[4]/a/@onclick'
        # xpath_wangqi_title = '/html/body/div[3]/div/div[2]/div[3]/div[1]/table/tr/td[2]/a/text()'
        html_txt, driver = utils_spider.get_source_page_from_url(self.root_url,True)
        res = utils_spider.handle_xpath(html_txt,xpath_wangqi)
        res = [i[6:13] for i in res]
        res = [f'https://www.radio.cn/pc-portal/sanji/zhibo_2.html?channelname=0&name={i}&title=radio' for i in res]
        url_list_dict['中国之声'] = list(set(res))
        for i in range(1,23):
            xpath_daintai = f'/html/body/div[3]/div/div[2]/div[2]/div/ul/li[{i}]'
            xpath_daintai_name = f'/html/body/div[3]/div/div[2]/div[2]/div/ul/li[{i}]/div/span/a/text()'
            html_txt, driver = utils_spider.do_a_click_to_a_driver(driver, xpath_daintai)
            res = utils_spider.handle_xpath(html_txt, xpath_wangqi)
            tiantai_name = utils_spider.handle_xpath(html_txt, xpath_daintai_name)
            print('tiantai_name:', tiantai_name)
            # res2 = utils_spider.handle_xpath(html_txt, xpath_wangqi_title)
            res = [i[6:13] for i in res]
            # res = [f'https://www.radio.cn/pc-portal/sanji/zhibo_2.html?channelname=0&name={i}&title=radio' for i in res]
            # assert len(res) == len(res2)
            # res_big = [(i,j) for i,j in zip(res,res2)]
            url_list_dict[tiantai_name[0]] = list(set(res))
        utils_file.write_dict_to_json(url_list_dict, self.output_root + 'url_wangqi_list.json')




    def get_wav_url_from_program(self,station_name:str='中国之声',program_id:str='1396889',):
        """
        url: https://www.radio.cn/pc-portal/sanji/zhibo_2.html?channelname=0&name=1396889&title=radio
        每个节目的往期页面
        :param program_url:
        :return:
        """
        program_url = f'https://www.radio.cn/pc-portal/sanji/zhibo_2.html?channelname=0&name={program_id}&title=radio'

        print('开始得到该节目下所有的音频地址')

        print('先点击到最后一页，看清楚有多少页')
        xpath_last_page = '/html/body/div[3]/div/div/div[3]/a[last()]'
        html_txt, driver = utils_spider.get_source_page_from_url(program_url,True)
        html_txt, driver = utils_spider.do_a_click_to_a_driver(driver, xpath_last_page)
        xpath_last_page_num = '/html/body/div[3]/div/div/div[3]/a[last()-2]/text()'
        page_num = utils_spider.handle_xpath(html_txt, xpath_last_page_num)[0]
        print('这个节目共有页数:', page_num)
        print('开始逐个点击上一页，直到点击够page_num次')
        xpath_previous_button = '/html/body/div[3]/div/div/div[3]/a[2]'
        page_num = int(page_num)
        audio_url_list = []
        for i in tqdm.tqdm(range(page_num), desc='正在处理的页数', total=page_num):
            xpath_download = '//*[@id="programList"]/tbody/tr/td[3]/a/@onclick'
            res = utils_spider.handle_xpath(html_txt, xpath_download)
            res = [i[16:-15] for i in res]
            audio_url_list.extend(res)
            html_txt, driver = utils_spider.do_a_click_to_a_driver(driver, xpath_previous_button)
        print('将该专辑的所有音频url存入文件')
        utils_file.write_list_to_file(audio_url_list, os.path.join(self.output_root,station_name,f"{program_id}_album_id.txt"))

    def download_wav_for_program(self,station_name:str='中国之声',program_id:str='1396889'):
        id_list_file = os.path.join(self.output_root,station_name,f"{program_id}_album_id.txt")
        if not os.path.exists(id_list_file):
            print('请先获取该节目/专辑的音频url列表文件，方式为调用get_wav_url_from_program()函数,参数同本函数')
            return
        url_list = utils_file.load_list_file_clean(id_list_file)
        target_dir = os.path.join(self.output_root,station_name,program_id)
        # for url_i in url_list:
        #     utils_file.download_file(url_i, target_dir)
        runner = GxlFixedThreadPool(num_threads=3)
        other_args = {'target_dir':target_dir}
        runner.map(utils_file.download_file,url_list, other_args)

    def download_wav_for_station(self):
        list_dict_file = os.path.join(self.output_root , 'url_wangqi_list.json')
        if not os.path.exists(list_dict_file):
            print('请先获取音频url列表文件，方式为调用get_audio_station()函数')
            return
        res_dict = utils_file.load_dict_from_json(self.output_root + 'url_wangqi_list.json')
        for station_name, url_list in res_dict.items():
            for program_id in url_list:
                # 先得到该专辑的所有音频地址
                self.get_wav_url_from_program(station_name, program_id)
                # 再下载该专辑的所有音频
                self.download_wav_for_program(station_name, program_id)


if __name__ == '__main__':
    # 首先设置output_root的位置
    # 最后设置为debug模式，也就是先开起chrome的debug模式的浏览器，启动命令，windows的cmd中运行：
    # chrome.exe --remote-debugging-port=9222 --user-gxl_data-dir="D:\temp"
    # 这样就不用每次执行一次命令就重启一下浏览器，而是可以在一个浏览器内部连贯执行，
    # 程序默认启动debug模式，如果不启动可以吧所有utils_spider.get_source_page_from_url(program_url,True)中的True改为False
    gxl_spider = GxlSpider(output_root='./output/yunting/')
    # 首先得到url_wangqi_list.json,这是所有电台旗下的所有节目的往期页的集合，爬取音频就依赖于这些往期页
    gxl_spider.get_audio_station()
    # 然后开始逐个电台得下载其中的音频， 在download_wav_for_program（）函数中设置下载时具体的线程数
    gxl_spider.download_wav_for_station()


