import os

from gxl_ai_utils.utils import utils_file, utils_data

if __name__ == '__main__':
    new_text_dict = utils_file.load_dict_from_scp('./text.fix')
    new_text_dict = {k+'_wenet': v for k, v in new_text_dict.items() if len(v) > 0}
    wav_scp_1 = utils_file.load_dict_from_scp('/home/work_nfs5_ssd/hfxue/data/data4w/source_1/WenetSpeech/wav.scp')
    wav_scp_2 = utils_file.load_dict_from_scp('/home/work_nfs5_ssd/hfxue/data/data4w/source_1/train_l/wav.scp')
    wav_dict = {}
    wav_dict.update(wav_scp_1)
    wav_dict.update(wav_scp_2)
    output_dir = "/home/work_nfs14/xlgeng/asr_data_shard/wenetspeech_new_all"
    utils_file.makedir_sil(output_dir)
    utils_file.write_dict_to_scp(wav_dict, os.path.join(output_dir, 'wav.scp'))
    utils_file.write_dict_to_scp(new_text_dict, os.path.join(output_dir, 'text'))
    utils_file.do_make_shard_file(os.path.join(output_dir, 'wav.scp'), os.path.join(output_dir, 'text'), output_dir)
