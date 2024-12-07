from torch import nn
from torchvision import models
from torchvision.models import ResNet18_Weights

from gxl_ai_utils import utils
from gxl_ai_utils import AiConstant

class RNNGxlModel(nn.Module):
    def __init__(self, output_num=102, feature_extract=True):
        super(RNNGxlModel, self).__init__()
        self.resnet_block = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        utils.utils_model.set_parameter_requires_grad(self.resnet_block, feature_extract)
        fc_in = self.resnet_block.fc.in_features
        self.resnet_block.fc = nn.Linear(fc_in, output_num)

    def forward(self, X):
        return self.resnet_block(X)


# class RnnModelConfig:
#     def __init__(self):
#         self.data_path = AiConstant.DATA_PATH +'text_data'
#         self.emb_n = 300
#         self.vocab_size = 30000
#         self.dropout = 0.001
#         self.class_list = [x.strip() for x in open(
#             self.data_path + '/class.txt').readlines()]
#         self.num_classes = len(self.class_list)
#         self.hidden_n = 333
#         self.layers = 3


# class RNNTextClassifyModel(nn.Module):
#     def __init__(self, config=RnnModelConfig()):
#         super(RNNTextClassifyModel, self).__init__()
#         self.config = config
#         self.embedding = nn.Embedding(self.config.vocab_size, self.config.emb_n, padding_idx=self.config.vocab_size - 1)
#         self.lstm = nn.LSTM(self.config.emb_n, self.config.hidden_n, self.config.layers, bidirectional=True,
#                             batch_first=True, dropout=self.config.dropout)
#         self.fc = nn.Linear(self.config.hidden_n * 2, self.config.num_classes)

#     def forward(self, X):
#         """"""
#         out = self.embedding(X)
#         out = self.lstm(out)[0]
#         out = self.fc(out[:, -1, :])
#         return out


def test_rnn_model():
    train_loader, valid_loader, test_loader = utils_text.provide_loader()
    model = RNNTextClassifyModel()
    one_batch_X, one_batch_lens, one_batch_y = next(iter(train_loader))
    model.eval()
    model((one_batch_X, one_batch_lens))