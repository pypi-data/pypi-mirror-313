import os
import sys

os.environ['MODELSCOPE_CACHE'] = '/home/work_nfs7/xlgeng/.cache/modelscope/'
os.environ['MODELSCOPE_MODULES_CACHE'] = '/home/work_nfs7/xlgeng/.cache/modelscope2/'
os.environ['MODELSCOPE_CACHE_DIR'] = '/home/work_nfs7/xlgeng/.cache/modelscope2/'
sys.path.append('/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils')
import random
import time
import tqdm
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from gxl_ai_utils.utils import utils_file
from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool

num_thread = 9
models_warehouse = []
print('开始加载个线程的model')
for i in range(num_thread):
    models_warehouse.append(pipeline(
        task=Tasks.punctuation,
        model='damo/punc_ct-transformer_cn-en-common-vocab471067-large',
        model_revision="v1.0.0"))


def do_work(res_list, all_output_dict: dict, index):
    inference_pipline_zh_en = models_warehouse[index]
    output_dic = {}
    num_per_time = 500
    utils_file.makedir_sil('./output/tmp')
    for i in tqdm.tqdm(range(0, len(res_list), num_per_time), total=len(res_list) // num_per_time + 1,
                       desc='punctuation'):
        """"""
        num_rand = random.randint(0, 100000000)
        temp_file_path = f'./output/tmp/{num_rand}.txt'
        list_temp = res_list[i:i + num_per_time]
        utils_file.write_list_to_file(list_temp, temp_file_path)
        res_out: dict = inference_pipline_zh_en(text_in=temp_file_path)
        os.remove(temp_file_path)
        first_item: str = list_temp[0]
        first_key = first_item.strip().split('\t')[0]
        first_value = res_out['text']
        res_out[first_key] = first_value
        res_out.pop('text')
        output_dic.update(res_out)
    all_output_dict.update(output_dic)


def process_text(input_text_path: str, output_dir_text_path: str):
    text_path = input_text_path
    output_path = output_dir_text_path
    text_dic = utils_file.load_dict_from_scp(text_path)
    res_list = []
    for k, v in tqdm.tqdm(text_dic.items(), total=len(text_dic)):
        res_list.append(f'{k}\t{v}')
    # utils_file.write_list_to_file(res_list, text_pat h2)
    now = time.time()
    print('start。。。。')
    thread_runner = GxlDynamicThreadPool()
    # num_thread = 9
    all_output_dict = {}
    for i in range(num_thread):
        list_temp = res_list[i::num_thread]
        thread_runner.add_thread(do_work, [list_temp, all_output_dict, i])
    thread_runner.start()
    utils_file.write_dict_to_scp(all_output_dict, output_path)
    print(f'process text 耗时:{time.time() - now}s')


def handle_work(dir, input_text_path, output_dir, output_file_name='text_process2'):
    utils_file.makedir_sil(f'./output/{dir}/tmp2')
    text_dict = utils_file.load_dict_from_scp(input_text_path)
    dict_list = utils_file.do_split_dict(text_dict, 500)
    little_dict_path_list = []
    for i in tqdm.tqdm(range(len(dict_list)), total=len(dict_list), desc='分解为若干小字典'):
        dict_temp = dict_list[i]
        output_path_temp = os.path.join(f'./output/{dir}/tmp2', f'source_{i}.scp')
        little_dict_path_list.append(output_path_temp)
        if os.path.exists(output_path_temp):
            print(f'{output_path_temp}文件已存在,跳过')
            continue
        utils_file.write_dict_to_scp(dict_temp, output_path_temp)
    utils_file.makedir_sil(f'./output/{dir}/tmp3')
    for i, path in enumerate(little_dict_path_list):
        print(f'开始处理{path}')
        output_little_file_path = f'./output/{dir}/tmp3/target_{i}.scp'
        if os.path.exists(output_little_file_path):
            print(f'{output_little_file_path}文件已存在,跳过')
            continue
        process_text(path, output_little_file_path)
    print('完全处理完毕。。。。。')
    final_output_text_path = os.path.join(output_dir, output_file_name)
    utils_file.makedir_sil(output_dir)
    utils_file.do_merge_scp(f'./output/{dir}/tmp3', final_output_text_path)


def handle_big():
    """"""
    input_dir = '/home/work_nfs5_ssd/hfxue/gxl_data/data4w/source_1/'
    output_dir = '/home/backup_nfs5/data_tts/'
    for root, dirs, files in os.walk(input_dir):
        for dir in dirs:
            if dir == 'wenetspeech':
                continue
            input_text_path = os.path.join(root, dir, 'text')
            print('开始handle: input_text_path：', input_text_path)
            if not os.path.exists(input_text_path):
                print(f'{input_text_path}文件不存在,跳过')
                continue
            output_dir_path = os.path.join(output_dir, dir)
            handle_work(dir, input_text_path, output_dir_path, output_file_name='text_process')
        break


if __name__ == '__main__':
    """"""
    # input_text_path = '/home/backup_nfs5/data_tts/wenetspeech/text'
    # output_dir = '/home/backup_nfs5/data_tts/wenetspeech'
    # handle_work(input_text_path, output_dir, output_file_name='text_process2')
    handle_big()
