import argparse
import json

from numpy.core.numeric import ufunc


def test_acc_age(list_file, text_file):
    total_cnt = 0
    acc_cnt = 0

    with open(list_file, "r", encoding="utf-8") as l_file:
        ground_truth_data = {json.loads(line.strip())["key"]: json.loads(line.strip())["txt"] for line in l_file}
        # print(ground_truth_data)
    with open(text_file, "r", encoding="utf-8") as t_file:
        for line in t_file:
            if len(line.strip().split("\t"))<2:
                continue
            key, predict_txt = line.strip().split("\t")

            if key in ground_truth_data:
                # print("!!!")
                ground_truth_txt = ground_truth_data[key]
                # print(ground_truth_txt)
                ground_truth_label = ground_truth_txt.split('<')[-1].lower()
                # print(ground_truth_label)
                ground_truth_label = '<' + ground_truth_label
                # print(ground_truth_label)
                predict_label_list = predict_txt.split('<')
                if len(predict_label_list) == 1:
                    predict_label = ' '
                else:
                    predict_label = predict_label_list[-1].lower()
                predict_label = '<' + predict_label
                total_cnt += 1
                # print(total_cnt)
                if ground_truth_label == predict_label:
                    acc_cnt += 1

    accuracy = (acc_cnt / total_cnt) if total_cnt > 0 else 0.0
    print(f"age_acc: {accuracy * 100:.2f}%")
    return accuracy

from gxl_ai_utils.utils import utils_file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--ref_file', type=str, required=True, help='reference file, 真实的标签')
    parser.add_argument('--hyp_file', type=str, required=True, help='hypothesis file， 推理的标签')
    parser.add_argument('--output_file', type=str, required=True, help='output file')
    args = parser.parse_args()

    list_file = '/home/node54_tmpdata/yzli/wenet_whisper_finetune/examples/wenetspeech/whisper/data/test_sets/caption/data.list'
    # text_file = '/home/node54_tmpdata/yzli/wenet_whisper_finetune/examples/wenetspeech/whisper/exp/qwen2_multi_task_6gpus_gxl_adapter_init_asr-sot_whisper/emotion_epoch_9.pt_chunk-1_ctc0_reverse0.0_blankpenalty0.0_lengthpenalty0.0/llmasr_decode/text'
    # text_file = '/home/node54_tmpdata/yzli/wenet_whisper_finetune/examples/wenetspeech/whisper/exp/qwen2_multi_task_6gpus_gxl_adapter_init_asr-sot_whisper/gender_epoch_9.pt_chunk-1_ctc0_reverse0.0_blankpenalty0.0_lengthpenalty0.0/llmasr_decode/text'

    # text_file = '/home/node54_tmpdata/syliu/test/age_predict'
    # text_file = '/home/node54_tmpdata/yzli/wenet_whisper_finetune/examples/wenetspeech/whisper/exp/qwen2_multi_task_6gpus_gxl_adapter_init_asr-sot_whisper/caption_epoch_9.pt_chunk-1_ctc0_reverse0.0_blankpenalty0.0_lengthpenalty0.0/llmasr_decode/text'
    acc = test_acc_age(list_file, args.hyp_file)
    res_list = [f'age_acc: {acc * 100:.2f}%']
    utils_file.write_list_to_file(res_list, args.output_file)
