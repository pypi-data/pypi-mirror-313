import subprocess

import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import os
from gxl_ai_utils.utils import utils_file

torch.manual_seed(1234)
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


# 打开bf16精度，A100、H100、RTX3060、RTX3070等显卡建议启用以节省显存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio", device_map="auto", trust_remote_code=True, bf16=True).eval()
# 打开fp16精度，V100、P100、T4等显卡建议启用以节省显存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio", device_map="auto", trust_remote_code=True, fp16=True).eval()
# 使用CPU进行推理，需要约32GB内存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio", device_map="cpu", trust_remote_code=True).eval()
# 默认gpu进行推理，需要约24GB显存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio", trust_remote_code=True).eval()
# 可指定不同的生成长度、top_p等相关超参（transformers 4.32.0及以上无需执行此操作）
# model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-Audio", trust_remote_code=True)

def compute_wer(true_text_path, hyp_text_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    command = "python compute-wer.py --char=1 --v=1 \
          {} {} > {}/wer".format(true_text_path, hyp_text_path, output_dir)
    # 执行命令
    subprocess.run(command, shell=True)


def model_forward(model, tokenizer, wav_path):
    # audio_url = "/home/work_nfs/common/data/data_aishell/wav/test/S0764/BAC009S0764W0124.wav"
    sp_prompt = "<|startoftranscription|><|zh|><|transcribe|><|zh|><|notimestamps|><|wo_itn|>"
    query = f"<audio>{wav_path}</audio>{sp_prompt}"
    audio_info = tokenizer.process_audio(query)
    inputs = tokenizer(query, return_tensors='pt', audio_info=audio_info)
    inputs = inputs.to(model.device)
    pred = model.generate(**inputs, audio_info=audio_info)
    response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True, audio_info=audio_info)
    response = response.split('<|startoftranscription|>')
    # key = utils_file.get_file_pure_name_from_path(response[0])
    res = response[1]
    return res


def recognize():
    """"""
    tokenizer = AutoTokenizer.from_pretrained(
        "/home/work_nfs8/xlgeng/.cache/transformers/models--Qwen--Qwen-Audio/snapshots/cbb9c956a096a5d5420d6c4927fef30d00eff144",
        trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        "/home/work_nfs8/xlgeng/.cache/transformers/models--Qwen--Qwen-Audio/snapshots/cbb9c956a096a5d5420d6c4927fef30d00eff144",
        device_map="cuda", trust_remote_code=True).eval()
    output_dir = './res_out_kespeech'
    os.makedirs(output_dir, exist_ok=True)
    data_dir = "/home/work_nfs8/xlgeng/data/scp_test"
    data_dir = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/data_list/kespeech"
    test_sets = ['test_net', 'test_meeting', 'speechio_0', 'speechio_1', 'speechio_2', 'speechio_3', 'speechio_4']
    test_sets = ["Beijing", "Jiang-Huai", "Jiao-Liao", "Ji-Lu", "Lan-Yin", "Northeastern", "Southwestern", "Zhongyuan"]
    for test_set in test_sets:
        utils_file.logging_print(f"耿雪龙: 开始测试test_set: {test_set}")
        res_dict = {}
        test_set_dir = os.path.join(data_dir, test_set, 'train')
        wav_scp_path = os.path.join(test_set_dir, 'wav.scp')
        text_scp_path = os.path.join(test_set_dir, 'text')
        wav_line_list = utils_file.load_list_file_clean(wav_scp_path)
        for wav_line in wav_line_list:
            items = wav_line.split()
            if len(items) != 2:
                continue
            key = items[0]
            wav_path = items[1]
            text_res = model_forward(model, tokenizer, wav_path)
            utils_file.logging_print(f'{key}: {text_res}')
            res_dict[key] = text_res
        output_dir_i = os.path.join(output_dir, test_set)
        utils_file.makedir_sil(output_dir_i)
        utils_file.copy_file2(text_scp_path, output_dir_i)
        output_path = os.path.join(output_dir_i, f"{test_set}_text")
        utils_file.write_dict_to_scp(res_dict, output_path)
        utils_file.compute_wer(text_scp_path, output_path, output_dir_i)


def handle_log():
    input_log_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_salmonn/output/run_res/gxl.nohup"
    lines = utils_file.load_list_file_clean(input_log_path)
    res_dict = {}
    key_word = 'INFO TEST_NET_Y0000'
    for lines in tqdm.tqdm(lines, total=len(lines)):
        if key_word not in lines:
            continue
        items = lines.split()
        key = items[3]
        key = key.split(":")[0]
        val = " ".join(items[4:])
        res_dict[key] = val
    output_path = "./res_out/text_net/text_hyp"
    utils_file.makedir_for_file(output_path)
    utils_file.write_dict_to_scp(res_dict, output_path)
    true_path = "/home/work_nfs8/xlgeng/data/scp_test/test_net/text"
    utils_file.compute_wer(true_path, output_path, "./res_out/text_net")


if __name__ == '__main__':
    # true_path = "/home/work_nfs8/xlgeng/data/scp_test/aishell/text"
    # hyp_path = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v15/2_epoch_new/test_step_16422/aishell/text"
    # output_dir = "./res_out"
    # utils_file.compute_wer(true_path, hyp_path, output_dir)
    # compute_wer(true_path,hyp_path,output_dir)
    # handle_log()
    recognize()
