from gxl_ai_utils.utils import utils_data, utils_file
import os

input_dir = '/home/work_nfs6/disk2/zhyyao/data_16k/src/ench_haoweilai_587h'
output_dir = '/home/work_nfs7/xlgeng/gxl_data/asr_data_inventory/haoweilai_587h'

def make_total_text_wavscp():
    utils_file.makedir(output_dir)
    txt_scp_dict = utils_file.load_dict_from_scp(os.path.join(input_dir, 'label'))
    wav_scp_dict = utils_file.get_scp_for_wav_dir(os.path.join(input_dir, 'cs_wav'))
    utils_file.write_dict_to_scp(txt_scp_dict, os.path.join(output_dir, 'text'))
    utils_file.write_dict_to_scp(wav_scp_dict, os.path.join(output_dir, 'wav.scp'))

if __name__ == '__main__':
    make_total_text_wavscp()
