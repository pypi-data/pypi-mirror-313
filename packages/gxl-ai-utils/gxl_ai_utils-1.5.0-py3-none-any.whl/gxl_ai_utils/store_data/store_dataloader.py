from torch.utils.data import DataLoader


class TextClassifyDataLoader(DataLoader):
    def __init__(self, dataset, batch_size=32, sampler=None, **kwargs):
        super().__init__(dataset=dataset, batch_size=batch_size, sampler=sampler, **kwargs)

    def __iter__(self):  # 换成常规Dataloader仍然没解决多卡反而慢的问题,说明这种自定义loader可行
        for X, l, y in super().__iter__():
            yield (X, l), y