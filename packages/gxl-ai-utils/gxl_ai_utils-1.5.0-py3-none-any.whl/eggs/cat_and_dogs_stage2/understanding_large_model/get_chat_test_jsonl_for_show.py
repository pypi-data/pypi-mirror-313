from gxl_ai_utils.utils import utils_file
"""
从问题text.scp, 回答预测的text.scp和真实回答text.scp,分别得到 真实和预测的 问答jsonl文件，用来直观展示
"""


Q_path = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/text_Q"
A_path_hyp = "/home/node54_tmpdata/yzli/wenet_whisper_finetune/examples/wenetspeech/whisper/exp/qwen2_multi_task_6gpus_gxl_adapter_init_asr-sot_whisper/chat_epoch_9.pt_chunk-1_ctc0_reverse0.0_blankpenalty0.0_lengthpenalty0.0/llmasr_decode/text"
A_path_ref = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/text_A"

Q_dict = utils_file.load_dict_from_scp(Q_path)
A_hyp = utils_file.load_dict_from_scp(A_path_hyp)
A_ref = utils_file.load_dict_from_scp(A_path_ref)
dict_list_hyp = []
dict_list_ref = []
jsonl_hyp_path = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/test_hyp.jsonl"
jsonl_ref_path = "/home/node54_tmpdata/xlgeng/chat_data/shards_test/test_ref.jsonl"
for key, item in Q_dict.items():
    if key not in A_hyp or key not in A_ref:
        utils_file.logging_warning("warning: key not found: ", key)
        continue
    a_hyp_item = A_hyp[key]
    a_ref_item = A_ref[key]
    dict_item_hyp = {
        "key": key,
        "Q": item,
        "A": a_hyp_item,
    }
    dict_item_ref = {
        "key": key,
        "Q": item,
        "A": a_ref_item,
    }
    dict_list_hyp.append(dict_item_hyp)
    dict_list_ref.append(dict_item_ref)

utils_file.write_dict_list_to_jsonl(dict_list_hyp, jsonl_hyp_path)
utils_file.write_dict_list_to_jsonl(dict_list_ref, jsonl_ref_path)