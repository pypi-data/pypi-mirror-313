# 10条以上的测试数据
test_data = [
    "Hello World < 你好 > Python",
    " 这个 是 测试 文本 < python > 代码 ",
    " 你 好吗 ？ <example> 让我们 试试 ",
    "空格    在 这里 < 123 > 不一样",
    "    汉字之间 也 不要 有 空格",
    "<  英文  > 在 <测试> 后面",
    "<   数据>和<样例>之间有  空格  ",
    "这个 是 测试 文本  < world > 看看",
    " 这是 一个  < TEST  > 字符串",
    "仅仅测试  <     a b > 之后的 <内容>",
    "另外测试   <hello world>    的字符串",
    "这是一个 示例  <测试> 文本。 还有 额外的空格",
    '我的名字是tom,你的呢？how are you'
]

# 处理函数
import re

import re


def process_text(text):
    # 1. 删除汉字左右两侧的空格
    text = re.sub(r'\s*([\u4e00-\u9fff])\s*', r'\1', text)

    # 2. 将英文转成小写
    text = text.lower()

    # 3. 删除 < 和 > 符号两侧的空格
    text = re.sub(r'\s*<\s*', '<', text)
    text = re.sub(r'\s*>\s*', '>', text)

    return text
from gxl_ai_utils.utils import utils_file
# 测试每个数据
now = utils_file.do_get_now_time()
for i, text in enumerate(test_data*1000, 1):
    print(f"Test {i}: {process_text(text)}")
the_time = utils_file.do_get_elapsed_time(now)
print(f"Total time: {the_time}")

