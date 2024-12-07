import glob
import os
import random
import re
from urllib.parse import unquote

from gxl_ai_utils.utils import utils_spider, utils_file



class CommonSpider:
    def __init__(self):
        """"""
        self.url = 'https://voicewiki.cn'
        self.output_dir = "./output"
        self.person_infor_dict = None


    def re_draw_func(self,string):
        """"""
        bad_words = ['关于', '特殊', '分类', '免责', '隐私政策']
        # string = '<a href="aaaa" title="bbbb">'
        pattern = r'<a href="(.*?)" title="(.*?)">'
        matches = re.findall(pattern, string)
        res_dict = {}
        # 打印所有匹配的结果
        for match in matches:
            href = match[0]
            href = unquote(href, 'utf-8')
            title = match[1]
            if title in res_dict:
                continue
            href_key = href.split('/')[-1]
            jump_flag = False
            for bad_word in bad_words:
                if bad_word in href_key:
                    jump_flag = True
                    break
            if jump_flag:
                continue
            if href_key == title:
                res_dict[title] = self.url + href
        return res_dict

    def re_func_2(self, string):
        pattern = r'<div class="download-link"><a href="(.*?)" class="internal" title="(.*?)">(.*?)</a></div>'
        matches = re.findall(pattern, string)
        res_list = []
        # 打印所有匹配的结果
        for match in matches:
            href = match[0]
            href = unquote(href, 'utf-8')
            href = self.url + href
            res_list.append(href)
        return res_list
    def get_all_game_url(self,):
        output_path = os.path.join(self.output_dir, 'game_url.json')
        # 首页
        input_url = "https://voicewiki.cn/wiki/%E9%A6%96%E9%A1%B5"
        xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td[1]/div/div/div[1]/a/@href'
        html_page = utils_spider.send_request(input_url).text
        tr_num_xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr'
        tr_num = len(utils_spider.handle_xpath(html_page, tr_num_xpath))
        td_num_xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td'
        td_num = len(utils_spider.handle_xpath(html_page, td_num_xpath))
        res_dict = {}
        for i in range(1, tr_num + 1):
            for j in range(1, td_num + 1):
                game_url_xpath = f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[{j}]/div/div/div[1]/a/@href'
                game_url = utils_spider.handle_xpath(html_page, game_url_xpath)
                if len(game_url) != 0:
                    url = self.url + game_url[0]
                    decoded_url = unquote(url, 'utf-8')
                    utils_file.logging_print(decoded_url)
                    key = decoded_url.split('/')[-1]
                    res_dict[key] = decoded_url
        utils_file.write_dict_to_json(res_dict, output_path)
        self.game_info_dict = res_dict

    def get_person_info_dict(self):
        """"""
        output_path = os.path.join(self.output_dir, 'person_infor_dict.json')
        person_infor_dict = {}
        for game_name, game_name_path in self.game_info_dict.items():
            """"""
            utils_file.logging_print(f"正在获取{game_name}的人物信息")
            str_html = utils_spider.send_request(game_name_path).text
            res_dict = self.re_draw_func(str_html)
            person_infor_dict[game_name] = res_dict
        utils_file.write_dict_to_json(person_infor_dict, output_path)
        self.person_infor_dict = person_infor_dict

    def get_wav_info_dict(self):
        """"""
        if self.person_infor_dict is None:
            self.person_infor_dict = utils_file.load_dict_from_json('./output/person_infor_dict_copy.json')
        output_path = os.path.join(self.output_dir, 'wav_info_dict.json')
        wav_info_output_dir = os.path.join(self.output_dir, 'wav_info')
        utils_file.makedir_sil(wav_info_output_dir)
        person_info_dir = os.path.join(self.output_dir, 'person_info')
        utils_file.makedir_sil(person_info_dir)
        wav_info_dict = {}
        for game_name, person_info_dict_i in self.person_infor_dict.items():
            try:
                game_info_i_dict = {}
                for person_name, person_page_url in person_info_dict_i.items():
                    try:
                        person_info_i_list = []
                        utils_file.logging_print(
                            f"正在获取{game_name}的{person_name}的音频信息, 地址：{person_page_url}")
                        html_str = utils_spider.send_request(person_page_url).text
                        if "守望先锋" in person_name:
                            """"""
                            res_list = []
                            # 守望先锋的游戏里 每个任务相当于个小游戏, 下面还有小人物
                            little_person_info_dict = self.re_draw_func(html_str)
                            for little_person_name, little_person_page_url in little_person_info_dict.items():
                                little_html_str = utils_spider.send_request(little_person_page_url).text
                                little_res_list = self.re_func_2(little_html_str)
                                res_list.extend(little_res_list)
                            person_info_i_list = res_list
                        else:
                            person_info_i_list = self.re_func_2(html_str)
                        game_info_i_dict[person_name] = person_info_i_list
                        output_path = os.path.join(wav_info_output_dir, f'{game_name}__{person_name}.list')
                        utils_file.write_list_to_file(person_info_i_list, output_path)
                    except Exception as e:
                        utils_file.logging_print(e)
                        continue
                wav_info_dict[game_name] = game_info_i_dict
                output_path = os.path.join(person_info_dir, f'{game_name}.json')
                utils_file.write_dict_to_json(game_info_i_dict, output_path)
            except Exception as e:
                utils_file.logging_print(e)
                continue


        all_person_info_dict_path_list = glob.glob(os.path.join(person_info_dir, '*.json'))
        for person_info_dict_path in all_person_info_dict_path_list:
            person_info_dict = utils_file.load_dict_from_json(person_info_dict_path)
            game_name = utils_file.get_file_pure_name_from_path(person_info_dict_path)
            wav_info_dict[game_name] = person_info_dict
        output_path = os.path.join(self.output_dir, 'wav_info_dict.json')
        utils_file.write_dict_to_json(wav_info_dict, output_path)








if __name__ == '__main__':
    spider = CommonSpider()
    # spider.get_all_game_url()
    # spider.get_person_info_dict()
    spider.get_wav_info_dict()