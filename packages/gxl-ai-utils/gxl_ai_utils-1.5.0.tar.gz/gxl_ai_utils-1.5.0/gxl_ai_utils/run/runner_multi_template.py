# ddp_demo.py
import torch
import torch.nn as nn
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
import os
import argparse

import gxl_ai_utils
import runner
from torch import distributed, optim
from config import get_logger
import config
import tokenize_vocab_word
from chat_model_module_rnn import GxlChatRnnModel
from data_handle import get_loss, get_dataset

os.environ['OMP_NUM_THREADS'] = "1"

parser = argparse.ArgumentParser()
parser.add_argument('--gpu_id', type=str, default='0,1,2')  # 不设置默认值也不赋值的话会爆出找不到gpus的错误
parser.add_argument('--batchSize', type=int, default=612)
parser.add_argument('--epochs', type=int, default=15)
config_parser = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = config_parser.gpu_id
torch.distributed.init_process_group(backend="nccl")

local_rank = torch.distributed.get_rank()
torch.cuda.set_device(
    local_rank)  # 只能设置local_rank，设为int(config_parser.gpu_id.split(',')[localrank]),
# 由于环境变量的设置，程序会使用gpu_id里面的设别，但是计数仍然是0,1,2...

# --------------------------------------------------------- start your code
tokenizer = tokenize_vocab_word.get_tokenizer()
net = GxlChatRnnModel(len(tokenizer))
#/model_params_150_2023-08-26_15:16:12.pth
params_with_prefix = torch.load(config.MODELSAVEPATH + "model_params_150_2023-08-26_15:16:12.pth",
                                map_location=torch.device('cuda:' + str(local_rank)))
params_without_prefix = {k.replace("module.", ""): v for k, v in params_with_prefix.items()}
net.load_state_dict(params_without_prefix)
optimizer = torch.optim.Adam(net.parameters(), lr=1e-4)
lr_schedule = lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=5, T_mult=2)
loss_func = get_loss()
train_dataset = get_dataset()
# -------------------------------------------------------- end your code


sampler1 = DistributedSampler(train_dataset)  # 这个sampler会自动分配数据到各个gpu上
loader1 = DataLoader(train_dataset, batch_size=config_parser.batchSize, sampler=sampler1)
# loader = DataLoader(dataset, batch_size=config.batchSize, shuffle=True)

if torch.cuda.is_available():
    net.cuda()
model = torch.nn.parallel.DistributedDataParallel(net)

runner_o = runner.RunnerGxl(model, optimizer, loss_func, loader1, logger=get_logger(), valid_loader=None, multi=True,
                            local_rank=local_rank)
runner_o.run(config_parser.epochs)
