from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "5"
os.environ["HF_HOME"] = "./output/models-2B"
torch.manual_seed(0)

path = 'openbmb/MiniCPM-2B-sft-fp32'
path = "/home/work_nfs8/xlgeng/.cache/models--openbmb--MiniCPM-2B-sft-fp32/snapshots/35b90dd57d977b6e5bc4907986fa5b77aa15a82e"
print('hahaha')
tokenizer = AutoTokenizer.from_pretrained(path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float32, device_map='auto', trust_remote_code=True)

print('input: 山东省最高的山是哪座山, 它比黄山高还是矮？差距多少？')
responds, history = model.chat(tokenizer, "山东省最高的山是哪座山, 它比黄山高还是矮？差距多少？", temperature=0.8, top_p=0.8)
print(responds)
print('input:翻译如下英文至中文:China is an ancient country with a long history of civilization')
responds, history = model.chat(tokenizer, "翻译如下英文至中文:China is an ancient country with a long history of civilization", temperature=0.8, top_p=0.8)
print(responds)
print('input:翻译如下英文到中文:莎士比亚的文本具有一种高雅的美感')
responds, history = model.chat(tokenizer, "翻译如下英文到中文:莎士比亚的文本具有一种高雅的美感", temperature=0.8, top_p=0.8)
print(responds)
print('input:翻译如下句子到中文:我有一个pencil和ruler,你呢?')
responds, history = model.chat(tokenizer, "翻译如下句子到中文:我有一个pencil和ruler,你呢?", temperature=0.8, top_p=0.8)
print(responds)
print('input:翻译如下句子到英文:我有一个pencil和ruler,你呢?')
responds, history = model.chat(tokenizer, "翻译如下句子到英文:我有一个pencil和ruler,你呢?", temperature=0.8, top_p=0.8)
print(responds)