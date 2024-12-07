import os
import re

import tqdm

input_path= "https://maskgct.github.io/"
from gxl_ai_utils.utils import utils_file, utils_spider
# html_text_str = utils_spider.get_source_page_from_url(input_path)
# utils_spider.write_to_html(html_text_str[0], './text.html')
html_text_str = utils_spider.load_from_html('./text.html')
print(html_text_str)
pattern = r'<source src="(audios/[^"]+/[^"]+\.wav)"'

# 使用 re.findall() 提取所有匹配的内容
matches = re.findall(pattern, html_text_str)
path_list = []
# 输出结果
for match in matches:
    path_list.append(match)

utils_file.print_list(path_list)
output_dir = './data/MaskGCT_demo'
utils_file.makedir(output_dir)

for i, path in tqdm.tqdm(enumerate(path_list), total=len(path_list)):
    """"""
    file_name = str(i).zfill(3)
    utils_spider.download_file("https://maskgct.github.io/"+path, os.path.join(output_dir, f'{file_name}.wav'))

