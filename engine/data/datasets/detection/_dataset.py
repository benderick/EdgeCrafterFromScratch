from torch.utils.data import Dataset

@register
class DetectionDataset(Dataset):

    def __init__(self, parser, transforms=None):
        self.parser = parser
        self.transforms = transforms

    def __len__(self):
        return len(self.parser)

    def __getitem__(self, index):

        image = self.parser.load_image(index)

        target = self.parser.load_target(index)

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target