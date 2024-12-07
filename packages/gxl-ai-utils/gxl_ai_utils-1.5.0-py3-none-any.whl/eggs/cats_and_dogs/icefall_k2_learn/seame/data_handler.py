from gxl_ai_utils.utils import utils_file

shard_dir = "/home/41_data/hwang/huawei_cn_en/seame_train"
_,shard_path_list = utils_file.do_listdir(shard_dir, return_path=True)
output_raw_dir = "/home/work_nfs13/xlgeng/data/seame/train/row_wav"
utils_file.makedir(output_raw_dir)
wav_scp_path = "/home/work_nfs13/xlgeng/data/seame/train/wav.scp"
text_scp_path = "/home/work_nfs13/xlgeng/data/seame/train/text"
utils_file.do_uncompress_shard(shard_path_list, output_raw_dir, wav_scp_path, text_scp_path)

shard_dir_dev_1 = "/home/41_data/hwang/huawei_cn_en/seame_dev_man"
_,shard_path_list = utils_file.do_listdir(shard_dir_dev_1, return_path=True)
output_raw_dir = "/home/work_nfs13/xlgeng/data/seame/dev1/row_wav"
utils_file.makedir(output_raw_dir)
wav_scp_path = "/home/work_nfs13/xlgeng/data/seame/dev1/wav.scp"
text_scp_path = "/home/work_nfs13/xlgeng/data/seame/dev1/text"
utils_file.do_uncompress_shard(shard_path_list, output_raw_dir, wav_scp_path, text_scp_path)

shard_dir_dev_2 = "/home/41_data/hwang/huawei_cn_en/seame_dev_seg"
_,shard_path_list = utils_file.do_listdir(shard_dir_dev_2, return_path=True)
output_raw_dir = "/home/work_nfs13/xlgeng/data/seame/dev2/row_wav"
utils_file.makedir(output_raw_dir)
wav_scp_path = "/home/work_nfs13/xlgeng/data/seame/dev2/wav.scp"
text_scp_path = "/home/work_nfs13/xlgeng/data/seame/dev2/text"
utils_file.do_uncompress_shard(shard_path_list, output_raw_dir, wav_scp_path, text_scp_path)