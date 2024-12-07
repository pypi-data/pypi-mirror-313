import sys
import time
import torch

from gxl_ai_utils import utils
from gxl_ai_utils.config.gxl_config import GxlNode
from gxl_ai_utils.run.base_train_runner import GxlBaseRunner
from gxl_ai_utils.AiConstant import AI_LOGGER
from gxl_ai_utils.utils import utils_model, utils_file


class RunnerGxl(GxlBaseRunner):
    def __init__(self, model, optim, loss_f, train_loader, config: GxlNode,
                 valid_loader=None, scheduler=None, multi=False,
                 local_rank=0, is_class=True,
                 device=torch.device('cpu')):
        super(RunnerGxl, self).__init__(model, optim, loss_f, train_loader,
                                        config, valid_loader, scheduler, multi,
                                        local_rank, is_class, device)

    def handle_batch(self, batch):
        X, y = batch
        X, y = utils_model.put_data_to_device(X, y, self.device)
        out = self.model(X)
        loss = self.loss_f(out, y)
        loss.backward()
        self.optim.step()
        if self.scheduler is not None:
            self.scheduler.step()
        return loss

    def calculate_valid_loss(self):
        accumulate_loss = 0.0
        with torch.no_grad:
            for i, X, y in enumerate(self.valid_loader):
                self.model.eval()
                X, y = utils_model.put_data_to_device(X, y, self.device)
                out = self.model(X)
                accumulate_loss += self.loss_f(out, y)
        return accumulate_loss / len(self.valid_loader)

    def calculate_valid_accuracy(self, dataloader: torch.utils.data.DataLoader = None):
        self.model.eval()
        all_accuracy = 0.0
        batch_num = 0
        with torch.no_grad():
            for X, y in self.valid_loader:
                X, y = utils_model.put_data_to_device(X, y, self.device)
                out = self.model(X)
                accuracy = self.accuracy(out, y)
                all_accuracy += accuracy
                batch_num += 1
        return all_accuracy / batch_num

    def inference(self, dataloader: torch.utils.data.DataLoader, file_save_path: str = './output/inference.jsonl'):
        self.model.eval()
        dic_list = []
        with torch.no_grad():
            for X, _, y in dataloader:
                X, y = utils_model.put_data_to_device(X, y, self.device)
                out = self.model(X)
                res = out.argmax(dim=1)
                assert len(res) == len(y)
                for re, y_i in zip(res, y):
                    res = {'true': y_i.item(), 'pred': re.item()}
                    dic_list.append(res)
        utils_file.write_dict_list_to_jsonl(dic_list, file_save_path)
        accuracy = self.calculate_valid_accuracy(dataloader)
        str = f"该次测试集的正确率为{accuracy * 100:.6f}%"
        with open(file_save_path, 'a') as f:
            f.write('\n')
            f.write(str)
        print(str)


if __name__ == '__main__':
    """"""
