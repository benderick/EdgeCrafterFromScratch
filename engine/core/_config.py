from engine.core.meta import Meta
from torch.utils.data import Dataset
class ExpConfig(object):
    def __init__(self):
        self.meta : Meta|None  = None
        self.dataset : Dataset|None = None