import torch
import copy
import logging
import os
import sys

import torch
import yaml
from torch.utils.data import DataLoader

from ..gxl_dataset_wenet.gxl_dataset import GxlAsrDataset as Dataset
from ..gxl_model_wenet.utils.context_graph import ContextGraph
from ..gxl_model_wenet.utils.file_utils import read_symbol_table, read_non_lang_symbols
from ..gxl_model_wenet.utils.config import override_config
from ..gxl_model_wenet.init_model import init_model
import re
import zhconv

from ..config.gxl_config import GxlNode
from ..gxl_model_wenet.utils.train_utils import check_modify_and_save_config


class GxlInterfacer:
    def __init__(self, params_config_yaml_path: str):
        self.args = GxlNode.get_config_from_yaml(params_config_yaml_path)
        self.configs = GxlNode.get_dict_from_yaml(self.args.content_config)

    def clean_text(self, text):
        # 将繁体字转换为简体字
        text = zhconv.convert(text, 'zh-cn')
        # 去掉标点符号
        text = re.sub('[^a-zA-Z0-9一-龥]+', '', text)
        return text

    def run_infer(self):
        args = self.args
        configs = self.configs
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')
        os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
        if len(args.override_config) > 0:
            configs = override_config(configs, args.override_config)

        symbol_table = read_symbol_table(args.dict)
        test_conf = copy.deepcopy(configs['dataset_conf'])

        test_conf['filter_conf']['max_length'] = 102400
        test_conf['filter_conf']['min_length'] = 0
        test_conf['filter_conf']['token_max_length'] = 102400
        test_conf['filter_conf']['token_min_length'] = 0
        test_conf['filter_conf']['max_output_input_ratio'] = 102400
        test_conf['filter_conf']['min_output_input_ratio'] = 0
        test_conf['speed_perturb'] = False
        test_conf['spec_aug'] = False
        test_conf['spec_sub'] = False
        test_conf['spec_trim'] = False
        test_conf['shuffle'] = False
        test_conf['sort'] = False
        if 'fbank_conf' in test_conf:
            test_conf['fbank_conf']['dither'] = 0.0
        elif 'mfcc_conf' in test_conf:
            test_conf['mfcc_conf']['dither'] = 0.0
        test_conf['batch_conf']['batch_type'] = "static"
        test_conf['batch_conf']['batch_size'] = args.batch_size
        non_lang_syms = read_non_lang_symbols(args.non_lang_syms)

        test_dataset = Dataset(args.data_type,
                               args.test_data,
                               symbol_table,
                               test_conf,
                               args.bpe_model,
                               non_lang_syms,
                               partition=False)

        test_data_loader = DataLoader(test_dataset, batch_size=None, num_workers=0)

        # Init asr model from configs
        model, configs = init_model(args, configs)

        # Load dict
        char_dict = {v: k for k, v in symbol_table.items()}

        use_cuda = args.gpu >= 0 and torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        model = model.to(device)
        model.eval()

        context_graph = None
        if 'decoding-graph' in args.context_bias_mode:
            context_graph = ContextGraph(args.context_list_path, symbol_table,
                                         args.bpe_model, args.context_graph_score)

        # TODO(Dinghao Zhou): Support RNN-T related decoding
        # TODO(Lv Xiang): Support k2 related decoding
        # TODO(Kaixun Huang): Support context graph
        files = {}
        for mode in args.modes:
            dir_name = os.path.join(args.result_dir, mode)
            os.makedirs(dir_name, exist_ok=True)
            file_name = os.path.join(dir_name, 'text.txt')
            files[mode] = open(file_name, 'w', encoding='utf-8')
        max_format_len = max([len(mode) for mode in args.modes])
        with torch.no_grad():
            for batch_idx, batch in enumerate(test_data_loader):
                keys = batch["keys"]
                feats = batch["feats"].to(device)
                target = batch["target"].to(device)
                feats_lengths = batch["feats_lengths"].to(device)
                target_lengths = batch["target_lengths"].to(device)
                results = model.decode(
                    args.modes,
                    feats,
                    feats_lengths,
                    args.beam_size,
                    decoding_chunk_size=args.decoding_chunk_size,
                    num_decoding_left_chunks=args.num_decoding_left_chunks,
                    ctc_weight=args.ctc_weight,
                    simulate_streaming=args.simulate_streaming,
                    reverse_weight=args.reverse_weight,
                    context_graph=context_graph)
                for i, key in enumerate(keys):
                    for mode, hyps in results.items():
                        content = [char_dict[w] for w in hyps[i].tokens]
                        line = '{} {}'.format(key,
                                              args.connect_symbol.join(content))
                        logging.info('{} {}'.format(mode.ljust(max_format_len),
                                                    line))
                        files[mode].write(line + '\n')
        for mode, f in files.items():
            f.close()
