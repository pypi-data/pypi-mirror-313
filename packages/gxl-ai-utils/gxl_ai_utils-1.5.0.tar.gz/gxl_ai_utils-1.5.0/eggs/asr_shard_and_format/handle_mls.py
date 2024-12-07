import os

output_dir = '/home/work_nfs7/xlgeng/gxl_data/asr_data_inventory/mls_english'
input_dir = '/home/work_nfs6/gxl_data/mls_english/'
from gxl_ai_utils.utils import utils_file, utils_data
def make_total_text_wavscp():
    utils_file.makedir(output_dir)
    dirname = [
        'train',
        'dev',
        'test_gxl_ai_utils',
    ]
    total_wav_scp_dict = {}
    total_text_dict = {}
    for d in dirname:
        print('Processing {}'.format(d))
        temp_wav_scp_dict = utils_file.get_scp_for_wav_dir(os.path.join(input_dir, d, 'audio'), suffix='.flac')
        temp_text_scp_dict = utils_file.load_dict_from_scp(os.path.join(input_dir, d, 'transcripts.txt'))
        total_wav_scp_dict.update(temp_wav_scp_dict)
        total_text_dict.update(temp_text_scp_dict)
    utils_file.write_dict_to_scp(total_wav_scp_dict, os.path.join(output_dir, 'wav.scp'))
    utils_file.write_dict_to_scp(total_text_dict, os.path.join(output_dir, 'text'))


if __name__ == '__main__':
    make_total_text_wavscp()