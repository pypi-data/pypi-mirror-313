import argparse
import distutils
import functools
import os
import tempfile
from collections import Counter
from typing import Union, Optional, Text, List

from jsonlines import jsonlines

from gxl_ai_utils import AiConstant
import sentencepiece as spm

logger = AiConstant.AI_LOGGER(AiConstant.LOG_PATH + "gxl_ai_utils.log")

IGNORE_ID = -1
# `sos` and `eos` using same token
SOS = "<eos>"
EOS = SOS
UNK = "<unk>"
BLANK = "<blank>"
MASKCTC = "<mask>"
SPACE = "<space>"


def load_dict(dict_path: Optional[Text], maskctc=False) -> Optional[List[Text]]:
    if dict_path is None:
        return None

    with open(dict_path, "r") as f:
        dictionary = f.readlines()
    # first token is `<blank>`
    # multi line: `<blank> 0\n`
    # one line: `<blank>`
    # space is relpace with <space>
    char_list = [entry[:-1].split(" ")[0] for entry in dictionary]
    if BLANK not in char_list:
        char_list.insert(0, BLANK)
    if EOS not in char_list:
        char_list.append(EOS)
    # for non-autoregressive maskctc model
    if maskctc and MASKCTC not in char_list:
        char_list.append(MASKCTC)
    return char_list


class TextFeaturizer():
    def __init__(self, unit_type, vocab, spm_model_prefix=None, maskctc=False):
        """Text featurizer, for processing or extracting features from text.txt.

        Currently, it supports char/word/sentence-piece level tokenizing and conversion into
        a list of token indices. Note that the token indexing order follows the
        given vocabulary file.

        Args:
            unit_type (str): unit type, e.g. char, word, spm, spm 指的是sentencepiece的方式
            vocab Option[str, list]: Filepath to load vocabulary for token indices conversion, or vocab list.
            spm_model_prefix (str, optional): spm model prefix. Defaults to None.
        """
        assert unit_type in ('char', 'spm', 'word')
        self.unit_type = unit_type
        self.unk = UNK
        self.maskctc = maskctc
        self.vocab_path_or_list = vocab

        if self.vocab_path_or_list:
            self.vocab_dict, self._id2token, self.vocab_list, self.unk_id, self.eos_id, self.blank_id = self._load_vocabulary_from_file(
                vocab, maskctc)
            self.vocab_size = len(self.vocab_list)
        else:
            logger.warning(
                "TextFeaturizer: not have vocab file or vocab list. Only Tokenizer can use, can not convert to token idx"
            )

        if unit_type == 'spm':
            spm_model = spm_model_prefix + '.model'
            self.sp = spm.SentencePieceProcessor()
            self.sp.Load(spm_model)

    def tokenize(self, text, replace_space=True):
        """tokenizer split text.txt into text.txt tokens"""
        if self.unit_type == 'char':
            tokens = self.char_tokenize(text, replace_space)
        elif self.unit_type == 'word':
            tokens = self.word_tokenize(text)
        else:  # spm
            tokens = self.spm_tokenize(text)
        return tokens

    def detokenize(self, tokens):
        """tokenizer convert text.txt tokens back to text.txt"""
        if self.unit_type == 'char':
            text = self.char_detokenize(tokens)
        elif self.unit_type == 'word':
            text = self.word_detokenize(tokens)
        else:  # spm
            text = self.spm_detokenize(tokens)
        return text

    def featurize(self, text):
        """Convert text.txt string to a list of token indices.

        Args:
            text (str): Text to process.

        Returns:
            List[int]: List of token indices.
        """
        assert self.vocab_path_or_list, "toidx need vocab path or vocab list"
        tokens = self.tokenize(text)
        ids = []
        for token in tokens:
            if token not in self.vocab_dict:
                logger.debug(f"Text Token: {token} -> {self.unk}")
                token = self.unk
            ids.append(self.vocab_dict[token])
        return ids

    def defeaturize(self, idxs):
        """Convert a list of token indices to text.txt string,
        ignore index after eos_id.

        Args:
            idxs (List[int]): List of token indices.

        Returns:
            str: Text.
        """
        assert self.vocab_path_or_list, "toidx need vocab path or vocab list"
        tokens = []
        for idx in idxs:
            if idx == self.eos_id:
                break
            tokens.append(self._id2token[idx])
        text = self.detokenize(tokens)
        return text

    def char_tokenize(self, text, replace_space=True):
        """Character tokenizer.

        Args:
            text (str): text.txt string.
            replace_space (bool): False only used by build_vocab.py.

        Returns:
            List[str]: tokens.
        """
        text = text.strip()
        if replace_space:
            tokens = [SPACE if item == " " else item for item in list(text)]
        else:
            tokens = list(text)
        return tokens

    def char_detokenize(self, tokens):
        """Character detokenizer.

        Args:
            tokens (List[str]): tokens.

        Returns:
           str: text.txt string.
        """
        tokens = [t.replace(SPACE, " ") for t in tokens]
        return "".join(tokens)

    def word_tokenize(self, text):
        """Word tokenizer, separate by <space>."""
        return text.strip().split()

    def word_detokenize(self, tokens):
        """Word detokenizer, separate by <space>."""
        return " ".join(tokens)

    def spm_tokenize(self, text):
        """spm tokenize.

        Args:
            text (str): text.txt string.

        Returns:
            List[str]: sentence pieces str code
        """
        stats = {"num_empty": 0, "num_filtered": 0}

        def valid(line):
            return True

        def encode(l):
            return self.sp.EncodeAsPieces(l)

        def encode_line(line):
            line = line.strip()
            if len(line) > 0:
                line = encode(line)
                if valid(line):
                    return line
                else:
                    stats["num_filtered"] += 1
            else:
                stats["num_empty"] += 1
            return None

        enc_line = encode_line(text)
        return enc_line

    def spm_detokenize(self, tokens, input_format='piece'):
        """spm detokenize.

        Args:
            ids (List[str]): tokens.

        Returns:
            str: text.txt
        """
        if input_format == "piece":

            def decode(l):
                return "".join(self.sp.DecodePieces(l))
        elif input_format == "id":

            def decode(l):
                return "".join(self.sp.DecodeIds(l))

        return decode(tokens)

    def _load_vocabulary_from_file(self, vocab: Union[str, list],
                                   maskctc: bool):
        """Load vocabulary from file."""
        if isinstance(vocab, list):
            vocab_list = vocab
        else:
            vocab_list = load_dict(vocab, maskctc)
        assert vocab_list is not None
        logger.debug(f"Vocab: {vocab_list}")

        id2token = dict(
            [(idx, token) for (idx, token) in enumerate(vocab_list)])
        token2id = dict(
            [(token, idx) for (idx, token) in enumerate(vocab_list)])

        blank_id = vocab_list.index(BLANK) if BLANK in vocab_list else -1
        maskctc_id = vocab_list.index(MASKCTC) if MASKCTC in vocab_list else -1
        unk_id = vocab_list.index(UNK) if UNK in vocab_list else -1
        eos_id = vocab_list.index(EOS) if EOS in vocab_list else -1
        sos_id = vocab_list.index(SOS) if SOS in vocab_list else -1
        space_id = vocab_list.index(SPACE) if SPACE in vocab_list else -1

        logger.debug(f"BLANK id: {blank_id}")
        logger.debug(f"UNK id: {unk_id}")
        logger.debug(f"EOS id: {eos_id}")
        logger.debug(f"SOS id: {sos_id}")
        logger.debug(f"SPACE id: {space_id}")
        logger.debug(f"MASKCTC id: {maskctc_id}")
        return token2id, id2token, vocab_list, unk_id, eos_id, blank_id


def count_manifest(counter, text_feature, manifest_path):
    manifest_jsons = []
    with jsonlines.open(manifest_path, 'r') as reader:
        for json_data in reader:
            manifest_jsons.append(json_data)

    for line_json in manifest_jsons:
        if isinstance(line_json['text.txt'], str):
            tokens = text_feature.tokenize(
                line_json['text.txt'], replace_space=False)

            counter.update(tokens)
        else:
            assert isinstance(line_json['text.txt'], list)
            for text in line_json['text.txt']:
                tokens = text_feature.tokenize(text, replace_space=False)
                counter.update(tokens)


def dump_text_manifest(fileobj, manifest_path, key='text.txt'):
    """
    得到jsonl文件(manifest)中的key元素,并按行写入文件
    """
    manifest_jsons = []
    with jsonlines.open(manifest_path, 'r') as reader:
        for json_data in reader:
            manifest_jsons.append(json_data)

    for line_json in manifest_jsons:
        if isinstance(line_json[key], str):
            fileobj.write(line_json[key] + "\n")
        else:
            assert isinstance(line_json[key], list)
            for line in line_json[key]:
                fileobj.write(line + "\n")


def build_vocab(manifest_paths="",
                vocab_path="examples/librispeech/gxl_data/vocab.txt",
                unit_type="char",
                count_threshold=0,
                text_keys='text.txt',
                spm_mode="unigram",
                spm_vocab_size=0,
                spm_model_prefix="",
                spm_character_coverage=0.9995):
    manifest_paths = [manifest_paths] if isinstance(manifest_paths,
                                                    str) else manifest_paths

    fout = open(vocab_path, 'w', encoding='utf-8')
    fout.write(BLANK + "\n")  # 0 will be used for "blank" in CTC
    fout.write(UNK + '\n')  # <unk> must be 1

    if unit_type == 'spm':
        # tools/spm_train --input=$wave_data/lang_char/input.txt
        # --vocab_size=${nbpe} --model_type=${bpemode}
        # --model_prefix=${bpemodel} --input_sentence_size=100000000
        import sentencepiece as spm

        fp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        for manifest_path in manifest_paths:
            _text_keys = [text_keys] if type(
                text_keys) is not list else text_keys

            for text_key in _text_keys:
                dump_text_manifest(fp, manifest_path, key=text_key)
        fp.close()
        # train
        spm.SentencePieceTrainer.Train(
            input=fp.name,
            vocab_size=spm_vocab_size,
            model_type=spm_mode,
            model_prefix=spm_model_prefix,
            input_sentence_size=100000000,
            character_coverage=spm_character_coverage)
        os.unlink(fp.name)

    # encode
    text_feature = TextFeaturizer(unit_type, "", spm_model_prefix)
    counter = Counter()

    for manifest_path in manifest_paths:
        count_manifest(counter, text_feature, manifest_path)

    count_sorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    tokens = []
    for token, count in count_sorted:
        if count < count_threshold:
            break
        # replace space by `<space>`
        token = SPACE if token == ' ' else token
        tokens.append(token)

    tokens = sorted(tokens)
    for token in tokens:
        fout.write(token + '\n')

    fout.write(SOS + "\n")  # <sos/eos>
    fout.close()

def add_arguments(argname, type, default, help, argparser, **kwargs):
    """Add argparse's argument.

    Usage:

    .. code-block:: python

        parser = argparse.ArgumentParser()
        add_argument("name", str, "Jonh", "User name.", parser)
        args = parser.parse_args()
    """
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument(
        "--" + argname,
        default=default,
        type=type,
        help=help + ' Default: %(default)s.',
        **kwargs)
def define_argparse():
    parser = argparse.ArgumentParser(description=__doc__)
    add_arg = functools.partial(add_arguments, argparser=parser)

    # yapf: disable
    add_arg('unit_type', str, "char", "Unit type, e.g. char, word, spm")
    add_arg('count_threshold', int, 0,
            "Truncation threshold for char/word counts.Default 0, no truncate.")
    add_arg('vocab_path', str,
            'examples/librispeech/gxl_data/vocab.txt',
            "Filepath to write the vocabulary.")
    add_arg('manifest_paths', str,
            None,
            "Filepaths of manifests for building vocabulary. "
            "You can provide multiple manifest files.",
            nargs='+',
            required=True)
    add_arg('text_keys', str,
            'text.txt',
            "keys of the text.txt in manifest for building vocabulary. "
            "You can provide multiple k.",
            nargs='+')
    # bpe
    add_arg('spm_vocab_size', int, 0, "Vocab size for spm.")
    add_arg('spm_mode', str, 'unigram', "spm model type, e.g. unigram, spm, char, word. only need when `unit_type` is spm")
    add_arg('spm_model_prefix', str, "", "spm_model_%(spm_mode)_%(count_threshold), spm model prefix, only need when `unit_type` is spm")
    add_arg('spm_character_coverage', float, 0.9995, "character coverage to determine the minimum symbols")
    # yapf: disable

    args = parser.parse_args()
    return args

def print_arguments(args, info=None):
    """Print argparse's arguments.

    Usage:

    .. code-block:: python

        parser = argparse.ArgumentParser()
        parser.add_argument("name", default="Jonh", type=str, help="User name.")
        args = parser.parse_args()
        print_arguments(args)

    :param args: Input argparse.Namespace for printing.
    :type args: argparse.Namespace
    """
    filename = ""
    if info:
        filename = info["__file__"]
    filename = os.path.basename(filename)
    print(f"----------- {filename} Configuration Arguments -----------")
    for arg, value in sorted(vars(args).items()):
        print("%s: %s" % (arg, value))
    print("-----------------------------------------------------------")

def main():
    args = define_argparse()
    print_arguments(args, globals())
    build_vocab(**vars(args))

if __name__ == '__main__':
    main()