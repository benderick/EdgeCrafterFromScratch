from typing import List, Union

@register
class Compose:
    """
    Detection Transform Pipeline

    支持：
        1. 顺序执行 Transform
        2. Epoch感知
        3. 后期关闭增强
    """
    def __init__(self, ops=[], stop_epoch=None, remove_ops=None):
        self.transforms = ops
        self.stop_epoch = stop_epoch
        self.remove_ops = set(remove_ops or [])
        self.epoch = -1

    def set_epoch(self, epoch: int):
        self.epoch = epoch
        for t in self.transforms:
            if hasattr(t, "set_epoch"):
                t.set_epoch(epoch)

    def __call__(self, image, target):
        for t in self.transforms:
            name = type(t).__name__
            if (self.stop_epoch is not None
                and self.epoch >= self.stop_epoch
                and name in self.remove_ops
            ):
                continue
            image, target = t(image, target)
        return image, target