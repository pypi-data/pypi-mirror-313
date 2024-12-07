import torch
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils.model_warehouse.paraformer import build_asr_model
if __name__ == '__main__':
    """"""
    model_checkpoint = './output/paraformer/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/model.pt'
    param = torch.load(model_checkpoint, map_location='cpu')
    for key, value in param.items():
        print(key, value.shape)
    config_yaml = 'E:\gengxuelong_study\server_local_adapter\gxl_work\gxl_ai_utils\eggs\knowledge_distillation\output\paraformer\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch\config.yaml'
    yaml_node = GxlNode.get_config_from_yaml(config_yaml)
    print(yaml_node)
    model = build_asr_model.build_asr_model(yaml_node)
    print(model)
    model.load_state_dict(param)
    input_data = torch.randn(10,1709042)
    input_len = torch.randint(100000, 1709042, (10,))
    output1 = model.frontend(input_data, input_len)
    print(output1[0].shape, output1[1].shape)
    output = model.encoder(output1[0], output1[1])
    print(output1[0].shape, output1[1].shape)


