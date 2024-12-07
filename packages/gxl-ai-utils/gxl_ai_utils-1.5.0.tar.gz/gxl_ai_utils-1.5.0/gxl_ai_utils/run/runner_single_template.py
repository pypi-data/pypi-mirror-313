import torch
from torch import nn
from gxl_ai_utils import store_model
from gxl_ai_utils.run.runner import RunnerGxl
from gxl_ai_utils.store_data.store_data import DataStore
from gxl_ai_utils.store_model import store_model_name

if __name__ == "__main__":
    model = store_model.store_model.load_model(store_model_name.MNIST)
    optim = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_f = nn.CrossEntropyLoss()
    train_loader, valid_loader = DataStore('mnist').get_dataloader()
    runner = RunnerGxl(model, optim, loss_f, train_loader, valid_loader)
    runner.run(15)
