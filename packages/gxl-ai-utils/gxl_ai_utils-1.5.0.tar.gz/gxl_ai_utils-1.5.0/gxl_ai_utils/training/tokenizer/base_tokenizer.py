from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from typing import Union, List, Tuple, AbstractSet, Dict

T = Union[str,bytes]
class BaseTokenizer(ABC):
    """"""
    def tokenize(self, line:str) -> Tuple[List[T], List[int]]:
        """"""
        tokens = self.text2tokens(line)
        ids = self.tokens2ids(tokens)
        return tokens, ids

    def detokenize(self, ids:List[int])-> Tuple[str, List[T]]:
        tokens = self.ids2tokens(ids)
        line = self.tokens2text(tokens)
        return line, tokens

    @abstractmethod
    def text2tokens(self, line: str) -> List[T]:
        raise NotImplemented()

    @abstractmethod
    def tokens2text(self, tokens:List[T])->str:
        raise NotImplemented()

    @abstractmethod
    def ids2tokens(self, ids:List[int])->List[T]:
        raise NotImplemented()

    @abstractmethod
    def tokens2ids(self, tokens:List[T])->List[int]:
        raise NotImplemented()

    @abstractmethod
    def vocab_size(self)->int:
        raise  NotImplemented()

    @property
    def symbol_table(self)->Dict[T, int]:
        raise NotImplemented()