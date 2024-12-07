from gxl_ai_utils.utils import utils_file
shard_path = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all/shards_list.txt"
output_dir = "/home/work_nfs14/xlgeng/asr_data_raw/wenetspeech_fix"
wav_dir = "/home/work_nfs14/xlgeng/asr_data_raw/wenetspeech_fix/wav"
utils_file.makedir(wav_dir)
wav_path = output_dir + "/wav.scp"
text_path = output_dir + "/text"
shard_path_list = utils_file.load_list_file_clean(shard_path)
shard_path_list = shard_path_list[:100]
utils_file.logging_print('浅浅提取一百条')
utils_file.do_uncompress_shard(shard_path_list, wav_dir, wav_path, text_path)
