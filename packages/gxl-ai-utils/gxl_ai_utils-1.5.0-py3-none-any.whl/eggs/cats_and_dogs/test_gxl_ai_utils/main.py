from gxl_ai_utils.gxl_trainer_wenet import gxl_trainer
from gxl_ai_utils.utils import utils_data, utils_file

if __name__ == '__main__':
    """"""
    runner = gxl_trainer.GxlTrainer("train_config.yaml")
    runner.prepare_data("./gxl_data/train/wav.scp", "./gxl_data/train/text.txt.scp", "./gxl_data/dev/wav.scp", "./gxl_data/dev/text.txt.scp")
    # data_path = 'E:\gengxuelong_study\server_local_adapter\\ai\gxl_data\small_aishell'
    # utils_data.get_scp_for_wav_dir(data_path+'/train', './gxl_data/train/wav.scp')
    # utils_data.get_scp_for_wav_dir(data_path+'/dev', './gxl_data/dev/wav.scp')
    # utils_data.get_scp_for_wav_dir(data_path+'/test_gxl_ai_utils', './gxl_data/test_gxl_ai_utils/wav.scp')
    runner.train_run()
