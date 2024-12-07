import os.path
import re

from torch.utils.tensorboard import SummaryWriter

from ..config.gxl_config import GxlNode
from ..utils import utils_file
from ..gxl_model_wenet.utils.train_utils import *
from ..gxl_dataset_wenet.gxl_dataset import GxlAsrDataset
from ..gxl_model_wenet.init_model import init_model, ASRModel
from ..gxl_model_wenet.utils.executor import Executor
from ..gxl_model_wenet.utils.checkpoint import load_checkpoint, save_checkpoint, load_trained_modules
from ..gxl_lr_scheduler_wenet.scheduler import WarmupLR, NoamHoldAnnealing
from ..utils import utils_data

import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP


def read_non_lang_symbols(non_lang_sym_path):
    """read non-linguistic symbol from file.
    The file format is like below:
    {NOISE}\n
    {BRK}\n
    ...
    Args:
        non_lang_sym_path: non-linguistic symbol file path, None means no any
        syms.
    """
    if non_lang_sym_path is None:
        return None
    else:
        syms = utils_file.load_list_file_clean(non_lang_sym_path)
        non_lang_syms_pattern = re.compile(r"(\[[^\[\]]+\]|<[^<>]+>|{[^{}]+})")
        for sym in syms:
            if non_lang_syms_pattern.fullmatch(sym) is None:
                class BadSymbolFormat(Exception):
                    pass

                raise BadSymbolFormat(
                    "Non-linguistic symbols should be "
                    "formatted in {xxx}/<xxx>/[xxx], consider"
                    " modify '%s' to meet the requirment. "
                    "More details can be found in discussions here : "
                    "https://github.com/wenet-e2e/wenet/pull/819" % (sym))
        return syms


def read_symbol_table(symbol_table_file):
    symbol_table = {}
    with open(symbol_table_file, 'r', encoding='utf8') as fin:
        for line in fin:
            arr = line.strip().split()
            assert len(arr) == 2
            symbol_table[arr[0]] = int(arr[1])
    return symbol_table


class ToyModel(nn.Module):
    def __init__(self):
        super(ToyModel, self).__init__()
        self.conv = nn.Conv2d(3, 16, 3)
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(30 * 30 * 16, 10)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.conv(x)
        x = self.flatten(x)
        x = self.linear(x)
        x = self.softmax(x)
        return x


# 定义一个函数，用于在每个进程中进行DDP的初始化、模型的构造、训练的循环等操作
def run(rank, world_size):
    # DDP backend初始化
    dist.init_process_group(backend='nccl')
    # 设置当前进程使用的GPU设备
    torch.cuda.set_device(rank)
    # 构造模型，并将其封装为DDP模型
    model = ToyModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])
    # 定义损失函数和优化器
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)
    # 模拟一个batch的数据和标签
    inputs = torch.randn(20, 3, 32, 32).to(rank)
    labels = torch.randint(0, 10, (20,)).to(rank)
    # 前向传播
    outputs = ddp_model(inputs)
    # 计算损失
    loss = loss_fn(outputs, labels)
    # 后向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    # 打印损失值
    print(f'Rank {rank}, loss: {loss.item()}')


class GxlTrainer(object):
    def __init__(self, train_config_yaml_path: str = os.path.dirname(os.path.abspath(__file__)) + '/train_config.yaml'):
        self.args = GxlNode.get_config_from_yaml(train_config_yaml_path)
        torch.manual_seed(777)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')
        self.configs = GxlNode.get_dict_from_yaml(self.args.content_config)

    def prepare_data(self, data_dir: str):
        """
        数据处理：
        1. 移除text_scp中的空白间隔，如果没有空白间隔，则不作为
        2. 根据配置文件中的设置选择是否计算cmvn
        3. 提取训练集和验证集文本中的token并得到token_symbol_table文件
        4. 最后得到dataset需要的data.list数据。
        :param train_wav_scp_path:
        :param train_text_scp_path:
        :param cv_wav_scp_path:
        :param cv_text_scp_path:
        :return:
        """
        train_text_scp_path = os.path.join(data_dir, 'train', 'text.txt')
        train_wav_scp_path = os.path.join(data_dir, 'train', 'wav.scp')
        cv_text_scp_path = os.path.join(data_dir, 'dev', 'text.txt')
        cv_wav_scp_path = os.path.join(data_dir, 'dev', 'wav.scp')
        utils_data.do_remove_blank_for_text_scp(train_text_scp_path)
        utils_data.do_remove_blank_for_text_scp(cv_text_scp_path)
        # if self.args.cmvn is not None:
        #     utils_data.do_compute_cmvn_stats(self.args.num_workers, self.args.content_config,
        #                                      train_wav_scp_path, self.args.cmvn)
        utils_data.do_text2token(train_text_scp_path, self.args.symbol_table)

        utils_data.do_make_raw_list(train_wav_scp_path, train_text_scp_path, self.args.train_data)
        utils_data.do_make_raw_list(cv_wav_scp_path, cv_text_scp_path, self.args.cv_data)

    def train_run(self):
        """"""
        args = self.args
        configs = self.configs
        is_distributed = torch.cuda.is_available() and torch.cuda.device_count() >= 1
        # Init env for ddp OR deepspeed
        if is_distributed:
            world_size, local_rank, rank = init_distributed(args)
        else:
            world_size, local_rank, rank = 1, 0, 0

        # Get dataset & dataloader
        train_dataset, cv_dataset, train_data_loader, cv_data_loader = \
            init_dataset_and_dataloader(args, configs)

        # Do some sanity checks and save config to arsg.model_dir
        configs = check_modify_and_save_config(args, configs)

        # Init asr model from configs
        model, configs = init_model(args, configs)

        # Check model is jitable & print model archtectures
        trace_and_print_model(args, model)

        # Tensorboard summary
        writer = init_summarywriter(args)

        # Dispatch model from cpu to gpu
        if is_distributed:
            model, device = wrap_cuda_model(args, model)

        # Get optimizer & scheduler
        model, optimizer, scheduler = init_optimizer_and_scheduler(
            args, configs, model)

        # Save checkpoints
        save_model(model, info_dict={
            "save_time": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            "tag": "init", **configs
        })

        # Get executor
        executor = Executor()
        executor.step = configs["init_infos"].get('step', 0)

        # Init scaler, used for pytorch amp mixed precision training
        scaler = None
        if args.use_amp:
            scaler = torch.cuda.amp.GradScaler()

        # Start training loop
        start_epoch = configs["init_infos"].get('epoch', -1) + 1
        final_epoch = None
        for epoch in range(start_epoch, configs.get('max_epoch', 100)):
            train_dataset.set_epoch(epoch)
            configs['epoch'] = epoch

            lr = optimizer.param_groups[0]['lr']
            logging.info('Epoch {} TRAIN info lr {} rank {}'.format(epoch, lr, rank))

            # NOTE(xcsong): Why we need a new group? see `train_utils.py::wenet_join`
            if is_distributed:
                group_join = dist.new_group(backend="gloo",
                                        timeout=datetime.timedelta(seconds=args.timeout))
            else:
                group_join = None
            if is_distributed:
                dist.barrier()  # NOTE(xcsong): Ensure all ranks start Train at the same time.
            executor.train(model, optimizer, scheduler, train_data_loader,
                           writer, configs, scaler, group_join)
            if is_distributed:
                dist.barrier()  # NOTE(xcsong): Ensure all ranks start CV at the same time.
            total_loss, num_seen_utts = executor.cv(model, cv_data_loader, configs)
            cv_loss = total_loss / num_seen_utts

            logging.info('Epoch {} CV info cv_loss {} rank {}'.format(epoch, cv_loss, rank))
            info_dict = {
                'epoch': epoch, 'lr': lr, 'cv_loss': cv_loss, 'step': executor.step,
                'save_time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'tag': str(epoch), **configs
            }
            log_per_epoch(writer, info_dict=info_dict)
            save_model(model, info_dict=info_dict)

            final_epoch = epoch

        if final_epoch is not None and rank == 0:
            final_model_path = os.path.join(args.model_dir, 'final.pt')
            os.remove(final_model_path) if os.path.exists(final_model_path) else None
            os.symlink('{}.pt'.format(final_epoch), final_model_path)
            writer.close()

    def run_multi_thread(self):
        pass

    @staticmethod
    def run_multi_thread_test():
        # 获取GPU数量
        os.environ['CUDA_VISIBLE_DEVICES'] = '1,2,3'
        os.environ['TRITON_LOG_LEVEL'] = "0"
        os.environ['RANK'] = "0"
        os.environ['WORLD_SIZE'] = "3"
        os.environ['MASTER_ADDR'] = "127.0.0.1"
        os.environ['MASTER_PORT'] = "100862"
        n_gpus = torch.cuda.device_count()
        # 启动多个进程，每个进程调用run函数
        mp.spawn(run, args=(n_gpus,), nprocs=n_gpus, join=True)
