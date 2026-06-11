from typing import Union

from engine.core.meta import Meta
from torch.utils.data import Dataset, DataLoader
class ExpConfig(object):
    def __init__(self):
        self.meta : Union[Meta,None]  = None
        # self.dataset : Union[Dataset,None] = None
        self.dataloader : Union[DataLoader,None] = None