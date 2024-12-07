import torch
import torch.nn as nn
import time

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.linears = nn.Sequential(
            nn.Linear(100, 20000),
            nn.Linear(20000, 2000),
            nn.Linear(2000, 10000),
        )

    def forward(self, data):
        return self.linears(data)

data_input = [
    torch.randn(43, 100) for _ in range(10000)
]
model = MyModel()
optimer = torch.optim.Adam(model.parameters(), lr=0.001)
model = model.to('cuda:0')
while True:
    time.sleep(10)
