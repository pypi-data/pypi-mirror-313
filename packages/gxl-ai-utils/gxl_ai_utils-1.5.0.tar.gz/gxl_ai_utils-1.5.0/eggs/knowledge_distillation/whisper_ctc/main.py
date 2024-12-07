from gxl_ai_utils.gxl_model_wenet.init_model import init_model
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils.gxl_trainer_wenet.gxl_trainer import GxlTrainer
from gxl_ai_utils.gxl_model_wenet.utils.train_utils import check_modify_and_save_config
import os
os.environ['WHISPER_CACHE'] = './whisper_cache/'
def main():
    """"""
    args = GxlNode.get_config_from_yaml('conf/train_config.yaml')
    configs = GxlNode.get_config_from_yaml('conf/whisper_ctc.yaml').dict_f()
    configs = check_modify_and_save_config(args, configs)
    model, _ = init_model(args, configs)
    print(model)
    runner = GxlTrainer('conf/train_config.yaml')
    runner.train_run()



if __name__ == '__main__':
    main()