import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from gxl_ai_utils.utils import utils_file
path = "baichuan-inc/Baichuan2-7B-Chat"
path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/finetune_llm/output/models/models--baichuan-inc--Baichuan2-7B-Chat/snapshots/ea66ced17780ca3db39bc9f8aa601d8463db3da5"
tokenizer = AutoTokenizer.from_pretrained(path, use_fast=False, trust_remote_code=True, cache_dir="./output/models")
model = AutoModelForCausalLM.from_pretrained(path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True, cache_dir="./output/models")
model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan2-7B-Chat")
messages = []
messages.append({"role": "user", "content": "解释一下“温故而知新”"})
response = model.chat(tokenizer, messages)
print(response)

