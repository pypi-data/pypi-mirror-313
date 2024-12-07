from funasr.models.frontend.wav_frontend import apply_lfr

from gxl_ai_utils.model_warehouse.paraformer import build_asr_model
import torch
from gxl_ai_utils.config.gxl_config import GxlNode


def wav_frontend_for_paraformer(input_data, input_len, lfr_m=7, lfr_n=6):
    """
    paraformer的模型要求的输入的waveform, 并降低帧率为1/7, 得到特征维度为560（80*7）
    改造成输入是fbank,只进行降低帧率
    :param input_data: (b, t, fbank)
    :param input_len: (b,)
    :return:
    """
    feats = []
    feats_lens = []
    for i in range(len(input_data)):
        mat = input_len[i]
        if lfr_m != 1 or lfr_n != 1:
            mat = apply_lfr(mat, lfr_m, lfr_n)
        feat_length = mat.size(0)
        feats.append(mat)
        feats_lens.append(feat_length)
    feats_lens = torch.as_tensor(feats_lens)



class GxlParaformerEncoder:
    """"""

    def __init__(self):
        """"""
        model_checkpoint = './output/paraformer/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/model.pt'
        param = torch.load(model_checkpoint, map_location='cpu')
        for key, value in param.items():
            print(key, value.shape)
        config_yaml = 'E:\gengxuelong_study\server_local_adapter\gxl_work\gxl_ai_utils\eggs\knowledge_distillation\output\paraformer\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch\config.yaml'
        yaml_node = GxlNode.get_config_from_yaml(config_yaml)
        print(yaml_node)
        _model = build_asr_model.build_asr_model(yaml_node)
        self.encoder = _model.encoder
