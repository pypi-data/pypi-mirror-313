import os.path

from gxl_ai_utils import gxl_trainer_wenet
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils.utils import  utils_file
from gxl_ai_utils.gxl_model_wenet.init_model import init_model
runner = gxl_trainer_wenet.GxlTrainer("./train_config_new.yaml")

from gxl_ai_utils.utils import utils_file

utils_file.do_uncompress_shard()
def handle_data():
    wav_dir = '/home/work_nfs7/xlgeng/gxl_data/aishell/data_aishell/wav/'
    utils_file.make_scp_file_for_wav_dir(os.path.join(wav_dir, 'train'), os.path.join('./data', 'train', 'wav.scp'))
    utils_file.make_scp_file_for_wav_dir(os.path.join(wav_dir, 'dev'), os.path.join('./data', 'dev', 'wav.scp'))
    utils_file.make_scp_file_for_wav_dir(os.path.join(wav_dir, 'test_gxl_ai_utils'), os.path.join('./data', 'test_gxl_ai_utils', 'wav.scp'))
    runner.prepare_data(data_dir='./data')

def gxl_test():
    args = GxlNode.get_config_from_yaml("./train_config_new.yaml")
    configs = GxlNode.get_dict_from_yaml(args.content_config)
    configs['input_dim'] = 256
    configs['output_dim'] = 4000
    model, _ = init_model(args, configs)
    print(model)
    params = model.state_dict()
    for key, value in params.items():
        print(key)

if __name__ == '__main__':
    """"""
    # handle_data()
    runner.train_run()

