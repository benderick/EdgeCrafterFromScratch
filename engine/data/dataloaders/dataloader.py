import torch
import torch.utils.data as data

@register
class DataLoader(data.DataLoader):
    def set_epoch(self, epoch):
        self.dataset.set_epoch(epoch)
        self.collate_fn.set_epoch(epoch)



class BaseCollateFn(object):
    def __init__(self) -> None:
        self.epoch = -1
    
    def set_epoch(self, epoch):
        self.epoch = epoch

    def __call__(self, batch):
        raise NotImplementedError('')


@register
class DetectionCollateFn(BaseCollateFn):
    def __call__(self, batch):
        images = torch.stack([x[0] for x in batch])
        targets = [x[1] for x in batch]
        return images, targets
