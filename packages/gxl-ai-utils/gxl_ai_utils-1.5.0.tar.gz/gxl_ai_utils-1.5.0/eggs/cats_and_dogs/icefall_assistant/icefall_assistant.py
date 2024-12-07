import os
import sys
sys.path.insert(0, '../../../')
from gxl_ai_utils.utils import utils_file, utils_data
import tqdm
import gzip
import random

sys.path.insert(0, './')
from compute_fbank_common import compute_fbank_gxldata


def get_jsonl_filename4icefall(prefix: str = 'gxldata', partition: str = 'train'):
    return f'{prefix}_recordings_{partition}.jsonl', f'{prefix}_supervisions_{partition}.jsonl'


def do_compress_file_by_gzip(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)


def build_wav_dict_for_icefall(key, input_wav_path):
    sample_num, sample_rate = utils_data.get_sample_count(input_wav_path)
    # file_name = utils_file.get_file_pure_name_from_path(input_wav_path)
    duration = sample_num / sample_rate
    res_dict = {}
    res_dict['id'] = key
    res_dict['sources'] = [dict(
        type='file',
        channels=[0],
        source=input_wav_path,
    )]
    res_dict['sampling_rate'] = sample_rate
    res_dict['num_samples'] = sample_num
    res_dict['duration'] = duration
    res_dict['channel_ids'] = [0]
    return res_dict


def build_text_dict_for_icefall(key, input_text_str,duration_dict):
    if key not in duration_dict:
        # utils_file.logging_print('key not in duration dict,也就是text中有的key wav.scp没有: ' + key)
        return {}
    res_dict = {}
    res_dict['id'] = key
    res_dict['recording_id'] = key
    res_dict['start'] = 0.0
    res_dict['duration'] = duration_dict[key]
    res_dict['channel'] = 0
    res_dict['text'] = input_text_str
    res_dict['language'] = 'Chinese'
    res_dict['speaker'] = 'S0901'
    return res_dict


def little_func4wav_convert(res_list, wav_dict):
    temp_list = []
    for key, wav_path in tqdm.tqdm(wav_dict.items(), total=len(wav_dict)):
        temp_list.append(build_wav_dict_for_icefall(key, wav_path))
    res_list.extend(temp_list)


def little_func4text_convert(res_list, wav_dict,duration_dict):
    temp_list = []
    for key, wav_path in tqdm.tqdm(wav_dict.items(), total=len(wav_dict)):
        temp_dict = build_text_dict_for_icefall(key, wav_path, duration_dict)
        if len(temp_dict) > 0:
            temp_list.append(temp_dict)
    res_list.extend(temp_list)


def do_convert_scp_to_manifest(wav_scp_path, text_scp_path, wav_manifest_path, text_manifest_path):
    utils_file.logging_print('哈哈哈啊哈啊哈哈哈啊哈哈')
    utils_file.makedir_for_file(wav_manifest_path)
    utils_file.makedir_for_file(text_manifest_path)
    wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
    res_wav_dict_list = []
    runner = utils_file.GxlDynamicThreadPool()
    wav_dict_list = utils_file.do_split_dict(wav_dict, 32)
    for wav_dict_i in wav_dict_list:
        runner.add_task(little_func4wav_convert, [res_wav_dict_list, wav_dict_i])
    utils_file.logging_print('do_convert_scp_to_manifest():开始执行为wav生成manifest')
    runner.start()
    utils_file.write_dict_list_to_jsonl(res_wav_dict_list, wav_manifest_path)
    wav_manifest_path_gz = wav_manifest_path + '.gz'
    do_compress_file_by_gzip(wav_manifest_path, wav_manifest_path_gz)
    # res_wav_dict_list = utils_file.load_dict_list_from_jsonl(wav_manifest_path)

    # 得到duration信息的字典
    utils_file.logging_print('do_convert_scp_to_manifest():开始生成duration字典')
    duration_dict = {}
    for dict_i in tqdm.tqdm(res_wav_dict_list,total=len(res_wav_dict_list)):
        id = dict_i['id']
        duration = dict_i['duration']
        duration_dict[id] = duration
    utils_file.logging_print('do_convert_scp_to_manifest():生成duration字典完成')

    res_text_dict_list = []
    text_dict = utils_file.load_dict_from_scp(text_scp_path)
    runner = utils_file.GxlDynamicThreadPool()
    text_dict_list = utils_file.do_split_dict(text_dict, 32)
    for text_dict_i in text_dict_list:
        runner.add_task(little_func4text_convert, [res_text_dict_list, text_dict_i, duration_dict])
    utils_file.logging_print('do_convert_scp_to_manifest():开始执行为text生成manifest')
    runner.start()
    utils_file.write_dict_list_to_jsonl(res_text_dict_list, text_manifest_path)
    text_manifest_path_gz = text_manifest_path + '.gz'
    do_compress_file_by_gzip(text_manifest_path, text_manifest_path_gz)


def do_make_data4icefall(wav_scp_path,
                         text_scp_path,
                         manifest_dir,
                         fbank_dir,
                         partition: str = 'train',
                         prefix: str = 'gxldata',
                         only_manifest: bool = False,
                         only_fbank: bool = False):
    """

    :param wav_scp_path:
    :param text_scp_path:
    :param manifest_dir:
    :param fbank_dir:
    :param partition:
    :param prefix:
    :return:
    """
    utils_file.logging_print('开始处理{}的数据'.format(partition))
    utils_file.makedir_sil(manifest_dir)
    utils_file.makedir_sil(fbank_dir)
    if not only_fbank:
        utils_file.logging_print('首先得到manifest,文件为.jsonl.gz')
        manifest_wav_filename, manifest_text_filename = get_jsonl_filename4icefall(prefix, partition)
        manifest_wav_path = os.path.join(manifest_dir, manifest_wav_filename)
        manifest_text_path = os.path.join(manifest_dir, manifest_text_filename)
        do_convert_scp_to_manifest(wav_scp_path, text_scp_path, manifest_wav_path, manifest_text_path)
        utils_file.logging_print('得到manifest完成')
    if only_manifest:
        utils_file.logging_print(f'only_manifest={only_manifest}')
        return
    utils_file.logging_print('开始生成fbank')
    compute_fbank_gxldata(
        manifests_dir=manifest_dir,
        fbank_dir=fbank_dir,
        partition=partition,
        prefix=prefix,
        perturb_speed=(partition == 'train')
    )
    utils_file.logging_print('生成fbank完成')

def do_make_tokens_table(text_scp_path, lang_dir):
    output_path = os.path.join(lang_dir, 'tokens.txt')
    utils_file.do_convert_text2chars_dict(text_scp_path, output_path, blank_sym='<blk>')


def main():
    prefix = '3000h'
    data_output_dir =  '/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data/3000h/'
    fbank_dir = os.path.join(data_output_dir, 'fbank_common')
    lang_dir = os.path.join(data_output_dir, 'lang_char')
    manifest_dir = os.path.join(data_output_dir, 'manifest')
    partitions = ['train' ]
    for partition in partitions:
        scp_dir = f'/home/work_nfs14/xlgeng/asr_scp_raw/aishell1/{partition}'
        wav_scp_path = os.path.join(scp_dir, 'wav.scp')
        text_scp_path = os.path.join(scp_dir, 'text')
        utils_file.logging_print('耿雪龙:开始处理{}的数据'.format(partition))
        do_make_data4icefall(
            wav_scp_path=wav_scp_path,
            text_scp_path=text_scp_path,
            manifest_dir=manifest_dir,
            fbank_dir=fbank_dir,
            partition=partition,
            prefix=prefix,
            # only_manifest=True,
            only_fbank=True
        )
        if partition == 'train':
            do_make_tokens_table(text_scp_path, lang_dir)

def main2():
    prefix = '3000h'
    data_output_dir =  '/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data/3000h/'
    fbank_dir = os.path.join(data_output_dir, 'fbank_common')
    lang_dir = os.path.join(data_output_dir, 'lang_char')
    manifest_dir = os.path.join(data_output_dir, 'manifest')
    partitions = [ 'dev' ]
    for partition in partitions:
        scp_dir = data_output_dir
        wav_scp_path = os.path.join(scp_dir, 'wav_dev.scp')
        text_scp_path = os.path.join(scp_dir, 'text_dev')
        utils_file.logging_print('耿雪龙:开始处理{}的数据'.format(partition))
        do_make_data4icefall(
            wav_scp_path=wav_scp_path,
            text_scp_path=text_scp_path,
            manifest_dir=manifest_dir,
            fbank_dir=fbank_dir,
            partition=partition,
            prefix=prefix,
            # only_manifest=True,
            # only_fbank=True
        )
        # if partition == 'train':
        #     do_make_tokens_table(text_scp_path, lang_dir)

def scp_prepare_for_3000h():
    """"""
    # train ,
    utils_file.logging_print('开始处理train')
    scp4aishell2_dir = "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/AISHELL-2/"
    scp4librispeech_dir = "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/LibriSpeech/"
    scp4asru_cn_en_dir =  "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/ASRU700"
    output_dir = '/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data/3000h/'
    utils_file.makedir_sil(output_dir)
    utils_file.logging_print('开始处理wav.scp')
    wav_path_1 = os.path.join(scp4librispeech_dir, 'wav.scp')
    wav_path_2 = os.path.join(scp4aishell2_dir, 'wav.scp')
    wav_path_3 = os.path.join(scp4asru_cn_en_dir, 'wav.scp')
    output_path = os.path.join(output_dir, 'wav.scp')
    utils_file.do_merge_file(wav_path_1, wav_path_2, wav_path_3, output_path)
    utils_file.logging_print('处理wav.scp完成')
    utils_file.logging_print('开始处理text')
    text_path_1 = os.path.join(scp4librispeech_dir, 'text')
    text_path_2 = os.path.join(scp4aishell2_dir, 'text')
    text_path_3 = os.path.join(scp4asru_cn_en_dir, 'text')
    output_path = os.path.join(output_dir, 'text')
    utils_file.do_merge_file(text_path_1, text_path_2, text_path_3, output_path)
    utils_file.logging_print('处理text完成')
    all_text_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'text'))
    key_list = list(all_text_dict.keys())
    random.shuffle(key_list)
    new_text_dict = {}
    for key_i in tqdm.tqdm(key_list, desc='shuffling', total=len(key_list)):
        new_text_dict[key_i] = all_text_dict[key_i]
    utils_file.write_dict_to_scp(new_text_dict, os.path.join(output_dir, 'text'))
    all_wav_dict = utils_file.load_dict_from_scp(os.path.join(output_dir, 'wav.scp'))
    new_wav_dict = {}
    key_list = list(all_wav_dict.keys())
    random.shuffle(key_list)
    for key_i in tqdm.tqdm(key_list, desc='shuffling', total=len(key_list)):
        new_wav_dict[key_i] = all_wav_dict[key_i]
    utils_file.write_dict_to_scp(new_wav_dict, os.path.join(output_dir, 'wav.scp'))

def scp_prepare_for_3000h_dev():
    scp4asru_cn_en_dir = "/home/work_nfs5_ssd/hfxue/data/data4w/source_1/ASRU700"
    output_dir = '/home/work_nfs8/xlgeng/new_workspace/icefall/egs/multi_zh_en/ASR/gxl_data/3000h/'
    utils_file.makedir_sil(output_dir)
    wav_dict = utils_file.load_dict_from_scp(os.path.join(scp4asru_cn_en_dir, 'wav.scp'))
    little_wav_dict = utils_file.get_random_subdict(wav_dict, 1000)
    utils_file.write_dict_to_scp(little_wav_dict, os.path.join(output_dir, 'wav_dev.scp'))
    text_dict = utils_file.load_dict_from_scp(os.path.join(scp4asru_cn_en_dir, 'text'))
    little_text_dict = {k: text_dict[k] for k in little_wav_dict.keys()}
    utils_file.write_dict_to_scp(little_text_dict, os.path.join(output_dir, 'text_dev'))





if __name__ == '__main__':
    """"""
    # scp_prepare_for_3000h()
    # main2()
    scp_prepare_for_3000h_dev()
    main2()

