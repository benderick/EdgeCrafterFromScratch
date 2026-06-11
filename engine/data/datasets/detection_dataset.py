from torch.utils.data import Dataset
from torchvision.tv_tensors import BoundingBoxes

@register
class DetectionDataset(Dataset):

    def __init__(self, parser, transforms=None):
        self.parser = parser
        self.transforms = transforms
        self.epoch = -1

    def __getitem__(self, index):

        image = self.parser.load_image(index)

        target = self.parser.load_target(index)

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target
    
    def __len__(self):
        return len(self.parser)
    
    def set_epoch(self, epoch):
        self.epoch = epoch
        if hasattr(self.transforms, "set_epoch"):
            self.transforms.set_epoch(epoch) # type: ignore

