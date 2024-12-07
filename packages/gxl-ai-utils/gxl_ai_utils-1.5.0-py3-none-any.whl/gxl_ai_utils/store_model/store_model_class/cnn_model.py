import torch
from torch import nn
from gxl_ai_utils import AiConstant
import torch.nn.functional as F


class CNNGxlModel(nn.Module):
    def __init__(self):
        super(CNNGxlModel, self).__init__()
        self.net = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3), nn.ReLU(),
                                 nn.MaxPool2d(kernel_size=2), nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
                                 nn.ReLU(), nn.MaxPool2d(kernel_size=2))

    def forward(self, X):
        return self.net(X)


class CnnModelConfig:
    def __init__(self):
        self.data_path = AiConstant.DATA_PATH + 'text_data'
        self.emb_n = 300
        self.vocab_size = 30000
        self.filter_sizes = (2, 3, 4)  # 2d卷积核尺寸,个数为len()
        self.num_filters = 256
        self.dropout = 0.001
        self.class_list = [x.strip() for x in open(
            self.data_path + '/class.txt').readlines()]
        self.num_classes = len(self.class_list)


class CNNTextClassifyModel(nn.Module):
    def __init__(self, config: CnnModelConfig):
        super(CNNTextClassifyModel, self).__init__()
        self.config = config
        self.embedding = nn.Embedding(self.config.vocab_size, self.config.emb_n)
        self.convs = nn.ModuleList(
            [nn.Conv2d(1, self.config.num_filters, (k, self.config.emb_n)) for k in self.config.filter_sizes])
        self.dropout = nn.Dropout(self.config.dropout)
        self.fc = nn.Linear(self.config.num_filters * len(self.config.filter_sizes), self.config.num_classes)

    @staticmethod
    def conv_and_pool(x, conv):  # x: 32,1,40,300 -> 32,265,39,1 ->32,256,39,->32,256,1->39,256
        x = F.relu(conv(x)).squeeze(3)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        # print(x.shape)
        out = self.embedding(x)
        out = out.unsqueeze(1)
        out = torch.cat([self.conv_and_pool(out, conv) for conv in self.convs], 1)  # (32,256)*3 在dim=1拼接,得到 (32,768)
        out = self.dropout(out)
        out = self.fc(out)
        return out


def test_cnn_model():
    train_loader, valid_loader, test_loader = utils_text.provide_loader()
    model = CNNTextClassifyModel()
    one_batch_X, one_batch_lens, one_batch_y = next(iter(train_loader))
    model.eval()
    model((one_batch_X, one_batch_lens))
