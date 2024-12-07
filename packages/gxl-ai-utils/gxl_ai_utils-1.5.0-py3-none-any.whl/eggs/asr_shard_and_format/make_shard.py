import os

from gxl_ai_utils.audio_dataset import common_data_handler

from gxl_ai_utils.utils import utils_file, utils_data
from gxl_ai_utils.AiConstant import AI_LOGGER

def make_shard():
    source_dir = '/home/work_nfs7/xlgeng/gxl_data/asr_data_inventory/'
    output_dir_source = '/home/backup_nfs5/xlgeng/gxl_data/shard_asr/'
    utils_file.makedir_sil(output_dir_source)
    logger = AI_LOGGER('./output/make_shard_to_data_big.log')
    for root, dirs, files in os.walk(source_dir):
        for dir in dirs:
            logger.info(f'开始处理{dir}目录')
            wav_scp = utils_file.join_path(root, dir, "wav.scp")
            text_scp = utils_file.join_path(root, dir, "text")
            if not os.path.exists(wav_scp) or not os.path.exists(text_scp):
                logger.info(f'skip {dir}, the dir do not have wav.scp or text file')
                continue
            if dir == "gigaspeech":
                logger.info(f'skip {dir}, the dir is gigaspeech, and the dir has handled before')
                continue
            output_dir = utils_file.join_path(output_dir_source, dir)
            # size = utils_file.get_dir_size(output_dir)
            # if size > 10:
            #     logger.info(f'skip {dir}, size:{size} the dir is big, and the dir has handled before')
            #     continue
            # if os.path.exists(output_dir):
            #     shutil.rmtree(output_dir)
            common_data_handler.make_shard_file(wav_scp, text_scp, output_dir, num_utt_per_shard=1000,
                                                prefix_for_tar_file=dir, logger=logger)
        break

if __name__ == '__main__':
    make_shard()
