from gxl_ai_utils.utils import utils_file

input_wav_path = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/yunting_zhongguozhisheng/wav.scp"
input_text_path = "/home/node36_data/xlgeng/asr_data_from_pachong/gxl_output/yunting_zhongguozhisheng/text"
output_dir = './temp/tar_1/'
utils_file.do_make_shard_file(input_wav_path, input_text_path, output_dir, num_threads=2,num_utt_per_shard=10)