import re
from os import PathLike
from typing import Dict, List, Union, Optional

from gxl_ai_utils.training.tokenizer.base_tokenizer import BaseTokenizer, T
from gxl_ai_utils.utils import utils_file

class CharTokenizer(BaseTokenizer):
    def __init__(self,
                 symbol_table: Union[str, PathLike, Dict],
                 non_lang_syms:Optional[Union[str, PathLike, List]]=None,
                 split_by_blank:bool=False,
                 connect_sym:str="",
                 unk_sym:str="<unk>"):
        """"""
        self.non_lang_pattern = None
        if non_lang_syms is not None:
            self.non_lang_pattern = re.compile(
                r"(\[[^\[\]]+\]|<[^<>]+>|{[^{}]+})"  # r，原始字符串， 不对\进行特殊转义
            )
            # 得到非语言序列
            if isinstance(non_lang_syms, List):
                self.non_lang_syms = non_lang_syms
            else:
                self.non_lang_syms = utils_file.load_list_file_clean(non_lang_syms)
        else:
            self.non_lang_syms = []
        # 得到symbol_table
        if isinstance(symbol_table, Dict):
            self._symbol_table = symbol_table
        else:
            self._symbol_table = utils_file.load_dict_from_scp_for_symbol_table(symbol_table)
        # 得到char_table
        self._chat_table = {v:k for k,v in self._symbol_table.items()}


        # 赋值类属性
        self.connect_sym = connect_sym
        self.unk_sym = unk_sym
        self.split_by_blank = split_by_blank



    def text2tokens(self, line: str) -> List[T]:
        # 为line洗个澡
        line = line.strip()
        # 对非语言符号进行切分
        if self.non_lang_pattern is not None:
            parts = self.non_lang_pattern.split(line.upper())
        else:
            parts = [line]
        # 对切分后的结果进行token提取
        tokens = []
        for part in parts:
            if len(part.strip())==0:
                continue
            if part in self.non_lang_syms:
                tokens.append(part)
            if self.split_by_blank:
                part = part.split(" ")
            for char in part:
                if char == " ":
                    char = "▁"
                tokens.append(char)
        return tokens

    def tokens2text(self, tokens: List[T]) -> str:
        return self.connect_sym.join(tokens)

    def ids2tokens(self, ids: List[int]) -> List[T]:
        return [self._chat_table[idx] for idx in ids]

    def tokens2ids(self, tokens: List[T]) -> List[int]:
        ids = []
        for ch in tokens:
            if ch in self._symbol_table:
                ids.append(self._symbol_table[ch])
            else:
                ids.append(self._symbol_table[self.unk_sym])
        return ids

    def vocab_size(self) -> int:
        return len(self._symbol_table)

    @property
    def symbol_table(self) -> Dict[T, int]:
        return self._symbol_table


def _test_re():
    non_lang_pattern = re.compile(
        r"(\[[^\[\]]+\]|<[^<>]+>|{[^{}]+})"  # r，原始字符串， 不对\进行特殊转义
    )
    test_str = "你好，我是耿雪龙， 我来自西北工业大学，喜喜，{{争吵}} ，不要呀啊啊啊[[[大哭]]] 呜呜，唉，别闹了<下雨了>快多于呀"
    res1 = non_lang_pattern.search(test_str)
    print(res1)
    print(res1.string)
    res2 = non_lang_pattern.findall(test_str)
    for item in res2:
        print(item)
    print(res2)
    res3 = non_lang_pattern.finditer(test_str)
    for item in res3:
        print(item)
    print(res3)
    res4 = non_lang_pattern.split(test_str)
    print(res4)
    for item in res4:
        print(item)

if __name__ =="__main__":
    """"""
    symbol_path = "./aishell.txt"
    tokenizer = CharTokenizer(
        symbol_table=symbol_path,
    )
    str_test = '我是耿雪龙，你好呀，无锡吸星大法，胜多负少发撒给大家十大发射点范德萨范文芳是滴，，发射点发生挂上为，说的都是，十大高手'
    tokens, ids = tokenizer.tokenize(str_test)
    print(tokens)
    print(ids)
    utils_file.print_dict(tokenizer.symbol_table)
    print(tokenizer.vocab_size())
