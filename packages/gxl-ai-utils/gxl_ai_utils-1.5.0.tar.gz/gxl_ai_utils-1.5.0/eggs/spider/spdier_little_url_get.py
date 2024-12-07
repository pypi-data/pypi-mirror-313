xpath = '/html/body/table/tbody/tr/td[2]/a/@href'
url = 'https://dcapswoz.ict.usc.edu/wwwedaic/data/'
from gxl_ai_utils.utils import utils_spider,utils_file
res = utils_spider.hande_href_by_brower(url, xpath)
prefix = 'https://dcapswoz.ict.usc.edu/wwwedaic/data/'
res = [prefix + i for i in res]
utils_file.print_list(res)
utils_file.write_list_to_file(res, 'label_list.txt')