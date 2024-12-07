import glob
import os

import tqdm
import sys
sys.path.insert(0, "../../../")
from urllib.parse import unquote
from gxl_ai_utils.utils import utils_spider, utils_file

SAVE_DIR = '/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki_gxl/'
# SAVE_DIR = './output/voicewiki_gxl/'
utils_file.makedir(SAVE_DIR)

class Gxl_Spider_VoiceWiki:
    def __init__(self):
        super().__init__()
        self.url = 'https://voicewiki.cn'

    def get_url_from_one_page(self, input_url, url_list_file='./output/voicewike/police_audio_url.jsonl'):
        xpath4num = '//*[@id="mw-content-text"]/div/table'
        page_txt = utils_spider.send_request(input_url).text
        audio_num = len(utils_spider.handle_xpath(page_txt, xpath4num))
        utils_file.logging_print("该页面存在的音频数量为:" + str(audio_num))
        res_list = []
        for i in range(2, audio_num + 1):
            en_link_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/th/div/div[2]/div/div[2]/a/@href'
            cn_link_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[2]/th/div/div[2]/div/div[2]/a/@href'
            en_text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/td//text()'
            cn_text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[2]/td//text()'
            en_link = utils_spider.handle_xpath(page_txt, en_link_xpath)
            cn_link = utils_spider.handle_xpath(page_txt, cn_link_xpath)
            en_text = utils_spider.handle_xpath(page_txt, en_text_xpath)
            cn_text = utils_spider.handle_xpath(page_txt, cn_text_xpath)
            temp_dict = {}
            if len(en_link) != 0:
                temp_dict["en_link"] = self.url + en_link[0]
            else:
                temp_dict["en_link"] = ""
            if len(cn_link) != 0:
                temp_dict["cn_link"] = self.url + cn_link[0]
            else:
                temp_dict["cn_link"] = ""
            if len(en_text) != 0:
                temp_dict["en_text"] = en_text[0].strip()
            else:
                temp_dict["en_text"] = ""
            if len(cn_text) != 0:
                temp_dict["cn_text"] = cn_text[0].strip()
            else:
                temp_dict["cn_text"] = ""
            if len(en_link) != 0 or len(cn_link) != 0 or len(en_text) != 0 or len(cn_text) != 0:
                res_list.append(temp_dict)
                utils_file.logging_print("耿雪龙:temp_dict不为空,",temp_dict)
            else:
                utils_file.logging_print("warning:temp_dict为空, i:", i)
        utils_file.write_dict_list_to_jsonl(res_list, url_list_file)

    def start_download_from_one_page_url_file(self, url_list_file='./output/voicewike/police_audio_url.jsonl',
                                              download_dir='./output/voicewike/police_audio',
                                              output_list_file='./output/voicewike/police_audio_path.jsonl'):
        res_list = []
        url_list = utils_file.load_dict_list_from_jsonl(url_list_file)
        for url_dict in tqdm.tqdm(url_list, desc="下载中", total=len(url_list)):
            try:
                en_link = url_dict['en_link']
                cn_link = url_dict['cn_link']
                en_file_path = ""
                cn_file_path = ""
                if len(en_link) != 0:
                    suffix = en_link.split('.')[-1]
                    en_file_path = utils_file.download_file(en_link, download_dir, suffix=suffix)
                if len(cn_link) != 0:
                    suffix = cn_link.split('.')[-1]
                    cn_file_path = utils_file.download_file(cn_link, download_dir, suffix=suffix)
                url_dict['en_file_path'] = en_file_path
                url_dict['cn_file_path'] = cn_file_path
                res_list.append(url_dict)
            except Exception as e:
                utils_file.logging_print(e)
                utils_file.logging_print("下载音频失败,error:url_dict:", url_dict)
                continue
        utils_file.write_dict_list_to_jsonl(res_list, output_list_file)

    # def get_all_parson_page_url_from_a_game_page(self, game_page_url="https://voicewiki.cn/wiki/%E4%BE%A0%E7%9B%97%E7%8C%8E%E8%BD%A6%E6%89%8B%EF%BC%9A%E7%BD%AA%E6%81%B6%E9%83%BD%E5%B8%82", output_list_file='./output/voicewike/侠盗猎车手_page_url_list.list'):
    #     """"""
    #     a_xpath = "//a/@href"
    #     a_list = utils_spider.handle_xpath(utils_spider.send_request(game_page_url).text, a_xpath)
    #     res_list = []
    #     for a in a_list:
    #         if a.startswith("/wiki/"):
    #             url_i = self.url + a
    #             decode_url = unquote(url_i)
    #             res_list.append(decode_url)
    #     utils_file.write_list_to_file(res_list, output_list_file)
    #     utils_file.print_list(res_list)
    #

    def get_all_page_url_from_a_game_page(self,game_page_url="https://voicewiki.cn/wiki/%E4%BE%A0%E7%9B%97%E7%8C%8E%E8%BD%A6%E6%89%8B%EF%BC%9A%E7%BD%AA%E6%81%B6%E9%83%BD%E5%B8%82", output_list_file='./output/voicewike/侠盗猎车手_page_url_list.list'):
        """"""
        xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr/td[1]/div/div[1]/a/@href'
        xpath_2 = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr/td[2]/div/div[1]/a/@href'
        xpath_3 = '//*[@id="mw-content-text"]/div/table[3]/tbody/tr/td[1]/div/div[1]/a/@href'
        xpath_4 = '//*[@id="mw-content-text"]/div/table[4]/tbody/tr[1]/td[2]/div/div[1]/a/@href'
        xpath_5 = '//*[@id="mw-content-text"]/div/table[5]/tbody/tr[1]/td[2]/div/div[1]/a/@href'
        xpath_6 = '//*[@id="mw-content-text"]/div/table[5]/tbody/tr[2]/td[3]/div/div[1]/a/@href'
        xpath_7 = '//*[@id="mw-content-text"]/div/div/table[3]/tbody/tr[1]/td[2]/div/a/@href'
        xpath_8 = '//*[@id="mw-content-text"]/div/table[10]/tbody/tr[1]/td[2]/span/a/@href'
        page_txt = utils_spider.send_request(game_page_url).text
        num4table_xpath = '//*[@id="mw-content-text"]/div/table'
        num4table = len(utils_spider.handle_xpath(page_txt, num4table_xpath))
        res_list = []
        utils_file.logging_print('一共有: num4table:', num4table)
        for i in range(1, num4table + 1):
            num4person_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr/td'
            num4person = len(utils_spider.handle_xpath(page_txt, num4person_xpath))
            utils_file.logging_print(f'第{i}个表格有: num4person个人:', num4person)
            num4tr_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr'
            num4tr = len(utils_spider.handle_xpath(page_txt, num4tr_xpath))
            utils_file.logging_print(f'第{i}个表格有: num4tr行:', num4tr)
            num4td_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/td'
            num4td = len(utils_spider.handle_xpath(page_txt, num4td_xpath))
            utils_file.logging_print(f'第{i}个表格有: num4td列:', num4td)
            for j in range(1, num4tr + 1):
                for k in range(1, num4td + 1):
                    person_url_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[{j}]/td[{k}]/div/div[1]/a/@href'
                    person_url = utils_spider.handle_xpath(page_txt, person_url_xpath)
                    if len(person_url) != 0:
                        url = self.url + person_url[0]
                        decoded_url = unquote(url, 'utf-8')
                        res_list.append(decoded_url)
                        utils_file.logging_print(decoded_url)
        res_list = list(set(res_list))
        utils_file.write_list_to_file(res_list, output_list_file)
    def get_all_game_url(self, output_path='./output/voicewike/all_game_url.txt'):
        # 首页
        input_url = "https://voicewiki.cn/wiki/%E9%A6%96%E9%A1%B5"
        xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td[1]/div/div/div[1]/a/@href'
        html_page = utils_spider.send_request(input_url).text
        tr_num_xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr'
        tr_num = len(utils_spider.handle_xpath(html_page, tr_num_xpath))
        td_num_xpath = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td'
        td_num = len(utils_spider.handle_xpath(html_page, td_num_xpath))
        res_list = []
        for i in range(1, tr_num + 1):
            for j in range(1, td_num + 1):
                game_url_xpath = f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[{j}]/div/div/div[1]/a/@href'
                game_url = utils_spider.handle_xpath(html_page, game_url_xpath)
                if len(game_url) != 0:
                    url = self.url + game_url[0]
                    decoded_url = unquote(url, 'utf-8')
                    res_list.append(decoded_url)
                    utils_file.logging_print(decoded_url)
        utils_file.write_list_to_file(res_list, output_path)

def main():
    output_dir_root = "/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki"
    utils_file.makedir_sil(output_dir_root)
    spider = Gxl_Spider_VoiceWiki()
    utils_file.logging_print('首先得到所有游戏的url')
    all_game_revord_file = os.path.join(output_dir_root, 'all_game_url.list')
    spider.get_all_game_url(output_path=all_game_revord_file)
    utils_file.logging_print('得到所有游戏的url完成')
    utils_file.logging_print('开始得到所有游戏的所有人物页面的url')
    persons4game_record_dir = os.path.join(output_dir_root, 'persons4game')
    audio4persons_record_dir = os.path.join(output_dir_root, 'audio4persons')
    utils_file.makedir_sil(persons4game_record_dir)
    game_url_list = utils_file.load_list_file_clean(all_game_revord_file)
    for game_url in tqdm.tqdm(game_url_list,desc='游戏数目进度',total=len(game_url_list)):
        try:
            game_name = game_url.split('/')[-1]
            utils_file.logging_print('开始处理:', game_name)
            utils_file.logging_print(f'开始得到{game_name}的所有人物页面的url')
            persons4game_file = os.path.join(persons4game_record_dir, game_name + '.list')
            spider.get_all_page_url_from_a_game_page(game_page_url=game_url, output_list_file=persons4game_file)
            utils_file.logging_print(f'得到{game_name}的所有人物页面的url完成,存入:{persons4game_file}')
            person_url_list = utils_file.load_list_file_clean(persons4game_file)
            temp_audio4persons_record_dir = os.path.join(audio4persons_record_dir, game_name)
            utils_file.makedir_sil(temp_audio4persons_record_dir)
            for person_url in tqdm.tqdm(person_url_list,desc=f'{game_name}的人物数目进度',total=len(person_url_list)):
                try:
                    person_name = person_url.split('/')[-1]
                    utils_file.logging_print('开始处理:', person_name)
                    utils_file.logging_print(f'开始得到{person_name}的音频url')
                    output_person_file = os.path.join(temp_audio4persons_record_dir, person_name+'_url.jsonl')
                    spider.get_url_from_one_page(person_url, output_person_file)
                    utils_file.logging_print(f'得到{person_name}的音频url完成,存入:{output_person_file}')
                    utils_file.logging_print('开始下载所有音频:', person_name)
                    output_person_audio_file = os.path.join(temp_audio4persons_record_dir, person_name + '_file_path.jsonl')
                    download_dir_temp = os.path.join(output_dir_root, 'audio', game_name, person_name)
                    spider.start_download_from_one_page_url_file(output_person_file,download_dir_temp, output_list_file=output_person_audio_file)
                    utils_file.logging_print(f'音频下载完成处理完成:{person_name}')
                except Exception as e:
                    utils_file.logging_print('error:', e)
                    utils_file.logging_print(f'error: {person_url},处理失败,开始下一个')
                    continue

        except Exception as e:
            utils_file.logging_print('error:', e)
            utils_file.logging_print(f'error: {game_url},处理失败,开始下一个')
            continue

def main_2():
    """侠盗猎车游戏"""
    output_dir_root = "/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki_2"
    utils_file.makedir_sil(output_dir_root)
    spider = Gxl_Spider_VoiceWiki()
    game_url = "https://voicewiki.cn/wiki/%E4%BE%A0%E7%9B%97%E7%8C%8E%E8%BD%A6%E6%89%8B%EF%BC%9A%E7%BD%AA%E6%81%B6%E9%83%BD%E5%B8%82"
    game_name = game_url.split('/')[-1]
    utils_file.logging_print('开始处理:', game_name)
    utils_file.logging_print(f'开始得到{game_name}的所有人物页面的url')
    persons4game_record_dir = os.path.join(output_dir_root, 'persons4game')
    persons4game_file = os.path.join(persons4game_record_dir, game_name + '.list')
    spider.get_all_page_url_from_a_game_page(game_page_url=game_url, output_list_file=persons4game_file)
    utils_file.logging_print(f'得到{game_name}的所有人物页面的url完成,存入:{persons4game_file}')
    person_url_list = utils_file.load_list_file_clean(persons4game_file)
    audio4persons_record_dir = os.path.join(output_dir_root, 'audio4persons')
    temp_audio4persons_record_dir = os.path.join(audio4persons_record_dir, game_name)
    utils_file.makedir_sil(temp_audio4persons_record_dir)
    for person_url in tqdm.tqdm(person_url_list,desc=f'{game_name}的人物数目进度',total=len(person_url_list)):
        try:
            person_name = person_url.split('/')[-1]
            utils_file.logging_print('开始处理:', person_name)
            utils_file.logging_print(f'开始得到{person_name}的音频url')
            output_person_file = os.path.join(temp_audio4persons_record_dir, person_name+'_url.jsonl')
            spider.get_url_from_one_page(person_url, output_person_file)
            utils_file.logging_print(f'得到{person_name}的音频url完成,存入:{output_person_file}')
            utils_file.logging_print('开始下载所有音频:', person_name)
            output_person_audio_file = os.path.join(temp_audio4persons_record_dir, person_name + '_file_path.jsonl')
            download_dir_temp = os.path.join(output_dir_root, 'audio', game_name, person_name)
            spider.start_download_from_one_page_url_file(output_person_file,download_dir_temp, output_list_file=output_person_audio_file)
            utils_file.logging_print(f'音频下载完成处理完成:{person_name}')
        except Exception as e:
            utils_file.logging_print('error:', e)
            utils_file.logging_print(f'error: {person_url},处理失败,开始下一个')
            continue


class WangZhe_spider:
    def __init__(self):
        self.url = "https://voicewiki.cn"
        self.game_url = "https://voicewiki.cn/wiki/%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80"
        self.save_dir = os.path.join(SAVE_DIR,'王者荣耀')
    def get_person_pages_url(self):
        xpath_person_page_url = '//*[@id="mw-content-text"]/div/table/tbody/tr[3]/td[2]/p/span[3]/a/@href'
        xpath =                 '//*[@id="mw-content-text"]/div/table/tbody/tr[4]/td[2]/p/span[4]/a/@href'
        xpath_22 =              '//*[@id="mw-content-text"]/div/table/tbody/tr[7]/td[2]/p/span[13]/a/@href'
        tr_num_xpath = '//*[@id="mw-content-text"]/div/table/tbody/tr'
        html_page = utils_spider.send_request(self.game_url).text
        tr_num = len(utils_spider.handle_xpath(html_page, tr_num_xpath))
        utils_file.logging_print(f'一共有{tr_num}个数据块')
        res_dict = {}
        for i in range(1,tr_num+1):
            td_num_xpath = f'//*[@id="mw-content-text"]/div/table/tbody/tr[{i}]/td[2]/p/span'
            td_num = len(utils_spider.handle_xpath(html_page, td_num_xpath))
            utils_file.logging_print(f'开始处理第{i}个数据块，这个数据块共有{td_num}个人物')
            for j in range(1,td_num+1):
                person_url_xpath = f'//*[@id="mw-content-text"]/div/table/tbody/tr[{i}]/td[2]/p/span[{j}]/a/@href'
                person_url = utils_spider.handle_xpath(html_page, person_url_xpath)[-1]
                decode_person_url = unquote(person_url)
                person_name = decode_person_url.split('/')[-1]
                res_dict[person_name] =self.url + decode_person_url
        utils_file.logging_print(f'处理完成，一共有{len(res_dict)}个人物')
        utils_file.write_dict_to_scp(res_dict,os.path.join(self.save_dir,'person_page_url.scp'))
        return res_dict

    def get_audio_url_from_person_page(self,person_page_url='https://voicewiki.cn/wiki/朵莉亚（王者荣耀）', person_name=None):
        """"""
        if person_name is None:
            person_name = person_page_url.split('/')[-1]
        html_page_tree = utils_spider.send_request(person_page_url)
        if html_page_tree is None:
            return
        html_page = html_page_tree.text
        xpath_1 = '//*[@id="mw-content-text"]/div/table[3]/tbody/tr[1]/td[1]/span/div[1]/div[2]'
        xpath_2 = '//*[@id="mw-content-text"]/div/table[3]/tbody/tr[1]/td[1]/span/div[2]/div[2]'
        xpath_3 = '//*[@id="mw-content-text"]/div/table[5]/tbody/tr[1]/td[1]/span/div[1]/div[2]'
        xpath_4 = '//*[@id="mw-content-text"]/div/table[6]/tbody/tr[1]/td[1]/span/div[1]/div[2]'
        xpath_5 = '//*[@id="mw-content-text"]/div/table[55]/tbody/tr[1]/td[1]/span/div[1]/div[2]'
        xpath_6 = '//*[@id="mw-content-text"]/div/table[55]/tbody/tr[1]/td[1]/span/div[1]/div[2]/div/div[2]/a/@href'
        xpath_8 = '//*[@id="mw-content-text"]/div/table[5]/tbody/tr[1]/td[1]/span/div[1]/div[2]/div/div[2]/a/@href'
        utils_file.logging_print('开始得到所有的音频块数')
        num_table_xpath = '//*[@id="mw-content-text"]/div/table'
        num_table = len(utils_spider.handle_xpath(html_page, num_table_xpath))
        utils_file.logging_print(f'一共有{num_table}个音频块')
        res_list = []
        for i in range(1,num_table+1):
            num_audio_xpath = '//*[@id="mw-content-text"]/div/table[5]/tbody/tr[1]/td[1]/span/div'
            num_audio = len(utils_spider.handle_xpath(html_page, num_audio_xpath))
            if num_audio == 2:
                utils_file.logging_print('这个音频块有中英两种语音')
                # 中英双语的情况
                cn_audio_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/td[1]/span/div[1]/div[2]/div/div[2]/a/@href'
                en_audio_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/td[1]/span/div[2]/div[2]/div/div[2]/a/@href'
                en_text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[1]/td[2]//text()'
                cn_text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr[2]/td//text()'
                en_audio_url = utils_spider.handle_xpath(html_page, en_audio_xpath)
                cn_audio_url = utils_spider.handle_xpath(html_page, cn_audio_xpath)
                en_text = utils_spider.handle_xpath(html_page, en_text_xpath)
                cn_text = utils_spider.handle_xpath(html_page, cn_text_xpath)
                temp_dict = {}
                if len(cn_audio_url) != 0:
                    audio_url = self.url + cn_audio_url[0]
                    decode_audio_url = unquote(audio_url, 'utf-8')
                    temp_dict['cn_link'] = decode_audio_url
                if len(en_audio_url) != 0:
                    audio_url = self.url + en_audio_url[0]
                    decode_audio_url = unquote(audio_url, 'utf-8')
                    temp_dict['en_link'] = decode_audio_url
                if len(en_text) != 0:
                    temp_dict['en_text'] = en_text[0].strip()
                if len(cn_text) != 0:
                    temp_dict['cn_text'] = cn_text[0].strip()
                if len(temp_dict) != 0:
                    res_list.append(temp_dict)
                    utils_file.logging_print(f'temp_dict不为空:{temp_dict}')
            elif num_audio == 1:
                utils_file.logging_print('这个音频块只有中文')
                # 只用中文的情况
                temp_dict = {}
                audio_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr/th/div/div[2]/div/div[2]/a/@href'
                audio_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr/th/div/div[2]/div/div[2]/a/@href'
                audio_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr//div[2]/a/@href'
                text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody//tr/td//text()'
                text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr/td//text()'
                # text_xpath = f'//*[@id="mw-content-text"]/div/table[{i}]/tbody/tr/td[2]//text()'
                audio_url = utils_spider.handle_xpath(html_page, audio_xpath)
                text = utils_spider.handle_xpath(html_page, text_xpath)
                if len(audio_url) != 0:
                    audio_url = self.url + audio_url[-1]
                    decode_audio_url = unquote(audio_url, 'utf-8')
                    temp_dict['cn_link'] = decode_audio_url
                if len(text) != 0:
                    temp_dict['cn_text'] = text[-1].strip()
                if len(temp_dict) != 0:
                    res_list.append(temp_dict)
                    utils_file.logging_print(f'temp_dict不为空:{temp_dict}')
            else:
                utils_file.logging_print('多语的情况直接舍弃')
        utils_file.write_dict_list_to_jsonl(res_list,os.path.join(self.save_dir,person_name,f'{person_name}_audio_url.jsonl'))
        return res_list

    def download_audio_from_person_page(self,dict_list, person_name):
        utils_file.logging_print('开始下载音频 for person: {}'.format(person_name))
        res_list = []
        for dict_i in tqdm.tqdm(dict_list, desc=f'{person_name}的音频下载进度', total=len(dict_list)):
            if 'en_link' in dict_i:
                en_wav_path = utils_file.download_file(dict_i['en_link'], os.path.join(self.save_dir,person_name,"audio"))
                dict_i['en_file_path'] = en_wav_path
            if 'cn_link' in dict_i:
                cn_wav_path = utils_file.download_file(dict_i['cn_link'], os.path.join(self.save_dir,person_name,"audio"))
                dict_i['cn_file_path'] = cn_wav_path
            res_list.append(dict_i)
        utils_file.write_dict_list_to_jsonl(res_list,os.path.join(self.save_dir,person_name,f'{person_name}_audio.jsonl'))

    def get_all_result_and_cat(self):
        utils_file.logging_print(f'保存路径为:{self.save_dir}')
        res_path_list = glob.glob(os.path.join(self.save_dir, '*','*_audio.jsonl'))
        utils_file.print_list(res_path_list)
        res_list = []
        for res_path in tqdm.tqdm(res_path_list, total=len(res_path_list)):
            res_list.extend(utils_file.load_list_file_clean(res_path))
        utils_file.write_list_to_file(res_list, os.path.join(self.save_dir, 'all_audio.jsonl'))
    def run(self):
        res_dict = self.get_person_pages_url()
        for person_name, person_page_url in tqdm.tqdm(res_dict.items(), desc='人物进度', total=len(res_dict)):
            try:
                utils_file.makedir(os.path.join(self.save_dir, person_name))
                dict_list = self.get_audio_url_from_person_page(person_page_url=person_page_url,
                                                                person_name=person_name)
                self.download_audio_from_person_page(dict_list, person_name=person_name)
            except Exception as e:
                utils_file.logging_print(e)
                continue


class Huangshizhanzheng_spider:
    """
    皇室战争
    """



if __name__ == '__main__':
    """"""
    # wangzherongyao = WangZhe_spider()
    # wangzherongyao.get_all_result_and_cat()
    save_dir = ''
    res_path_list = glob.glob(os.path.join("/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki/audio4persons/侠盗猎车手：罪恶都市", '*file_path.jsonl'))
    utils_file.print_list(res_path_list)
    res_list = []
    for res_path in tqdm.tqdm(res_path_list, total=len(res_path_list)):
        res_list.extend(utils_file.load_list_file_clean(res_path))
    utils_file.write_list_to_file(res_list, os.path.join('/home/work_nfs14/xlgeng/tts_data_pachong_high_quality/voicewiki/audio4persons/侠盗猎车手：罪恶都市', 'all_audio.jsonl'))