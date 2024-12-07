import glob
import os
import random
import sys

sys.path.append("/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils/")

import torch
from gxl_ai_utils.gxl_model_wenet.transformer.encoder import TransformerEncoder
from transformers import AutoModelForCausalLM, AutoTokenizer

from gxl_ai_utils.utils import utils_file, utils_data
from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool


def do_prepare_data():
    aishell4_raw_scp_dir = '/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump3/raw/aishell4'
    aishell4_raw_now = '/home/work_nfs6/xlgeng/gxl_data/data_scp/aishell4'
    utils_file.makedir_sil(aishell4_raw_now)
    aishell4_prefix = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/"
    wav_scp = utils_file.load_dict_from_scp(utils_file.join_path(aishell4_raw_scp_dir, "wav.scp"))
    for k, v in wav_scp.items():
        wav_scp[k] = utils_file.join_path(aishell4_prefix, v)
    utils_file.write_dict_to_scp(wav_scp, utils_file.join_path(aishell4_raw_now, "wav.scp"))
    utils_file.copy_file(utils_file.join_path(aishell4_raw_scp_dir, "text"),
                         utils_file.join_path(aishell4_raw_now, "text"))

    ali_near_dir = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump4/raw/Train_Ali_near"
    ali_far_dir = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump2/raw/Train_Ali_far"
    # ali_far_dir_gxl = "/home/work_nfs6/xlgeng/gxl_data/data_scp/Train_Ali_far"
    # ali_near_dir_gxl = "/home/work_nfs6/xlgeng/gxl_data/data_scp/Train_Ali_near"
    # for file_name in ['wav.scp', 'text']:
    #     utils_file.copy_file(os.path.join(ali_far_dir, file_name), os.path.join(ali_far_dir_gxl, file))
    #     utils_file.copy_file(os.path.join(ali_near_dir, file_name), os.path.join(ali_near_dir_gxl, file))
    #
    # aishell4_dir_gxl = "/home/work_nfs6/xlgeng/gxl_data/data_scp/aishell4"

    runer = GxlDynamicThreadPool()
    output_root_dir = '/home/41_data/xlgeng/gxl_data/shards'
    utils_file.makedir_sil(output_root_dir)
    for dataset_dir in [aishell4_raw_now, ali_far_dir, ali_near_dir]:
        dataset_name = os.path.basename(dataset_dir)
        utils_file.logging_print(f"dataset_name: {dataset_name}")
        wav_scp_path = os.path.join(dataset_dir, 'wav.scp')
        text_path = os.path.join(dataset_dir, 'text')
        output_dir = os.path.join(output_root_dir, dataset_name)
        runer.add_task(utils_data.do_make_shard_file, [wav_scp_path, text_path, output_dir, 1000])
    runer.start()


def do_concat_shards_list():
    now_shard_list__path = "/home/work_nfs7/xlgeng/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/gxl_data/train/gxl_data.list.all.shuf"
    now_shard_list__path_2 = "/home/work_nfs7/xlgeng/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/gxl_data/train/data_2.list.all.shuf"
    data_dir = "/home/41_data/xlgeng/gxl_data/shards/"
    now_list = utils_file.load_list_file_clean(now_shard_list__path)
    dir_name_list = os.listdir(data_dir)
    for dir_name in dir_name_list:
        list_path = os.path.join(data_dir, dir_name, "shards_list.txt")
        temp_list = utils_file.load_list_file_clean(list_path)
        now_list.extend(temp_list)
    random.shuffle(now_list)
    utils_file.write_list_to_file(now_list, now_shard_list__path_2)


def do_test_model():
    import os

    tokenizer = AutoTokenizer.from_pretrained("/home/local_data/Atom-7B")
    model = AutoModelForCausalLM.from_pretrained("/home/local_data/Atom-7B")
    print(model)
    utils_file.print_model_size(model)
    embed_tokens = model.model.embed_tokens
    print(embed_tokens.weight.shape)


def do_test_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("/home/local_data/Atom-7B")
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenizer.padding_side = "right"
    text_list = [
        '大家好，我是耿雪龙。hello every one. i am gengxuelong. ',
        '胜多负少沙发沙发上事实上。水电费。'
    ]
    prompt_left_ids = tokenizer(
        text_list[0],
        return_tensors="pt",
        add_special_tokens=False
    ).to(
        torch.device('cpu')).input_ids
    print(prompt_left_ids)

    prompt_left_ids = tokenizer(
        text_list[0],
        return_tensors="pt",
        add_special_tokens=False
    ).to(
        torch.device('cpu')).input_ids
    print(prompt_left_ids)


def do_test_model_2():
    speech_transformer = TransformerEncoder(
        input_size=1280,
        output_size=1280,
        attention_heads=4,
        linear_units=2560,
        num_blocks=4,
        dropout_rate=0.1,
        positional_dropout_rate=0.1,
        attention_dropout_rate=0.0,
        input_layer="linear",
        pos_enc_layer_type="abs_pos",
        normalize_before=True
    )
    utils_file.print_model_size(speech_transformer)


def do_test_llm_forward():
    model = AutoModelForCausalLM.from_pretrained("/home/local_data/Atom-7B")
    print(model)
    utils_file.print_model_size(model)
    embeds = torch.randn((2, 5, 4096))
    labels = torch.randint(122, 10000, (2, 6))
    outputs = model(
        inputs_embeds=embeds,
        labels=labels,
    )
    print(type(outputs))
    for k, v in outputs.items():
        if k == "loss":
            print(k, v)
        if k == "logits":
            print(k, v.shape)
        if k == "past_key_values":
            print(k, len(v))
            for i in v:
                print(i.shape)


def do_test():
    do_test_llm_forward()
    try:
        do_test_tokenizer()
    except RuntimeError as e:
        print(e)
    # for batch_idx, batch in enumerate(test_data_loader):
    #     sorted_keys, padded_feats, padding_labels, feats_lengths, label_lengths = batch
    #     print(sorted_keys)
    #     print(padded_feats.shape, padded_feats.dtype)
    #     print(padding_labels.shape, padding_labels.dtype)
    #     print(feats_lengths)
    #     print(label_lengths)
    #     padded_feats.to(torch.float32)

def added_trainl_data_to_gxl_all():
    """"""
    gxl_all_path = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/data_list/gxl_all.list"
    gxl_all_path_o = "/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/data_list/gxl_all_2.list"
    gxl_all_list = utils_file.load_list_file_clean(gxl_all_path)
    trainl_dir = "/home/local_data/data4w/shard_1/train_l"
    trainl_list = glob.glob(os.path.join(trainl_dir, "*.tar"))
    gxl_all_list.extend(trainl_list)
    random.shuffle(gxl_all_list)
    utils_file.write_list_to_file(gxl_all_list, gxl_all_path_o)




if __name__ == '__main__':
    """"""
    added_trainl_data_to_gxl_all()
