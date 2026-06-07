import os
from pathlib import Path
import torch
from PIL import Image
from engine.data.datasets.detection._parser import BaseParser

@register
class YOLOParser(BaseParser):
    """
    YOLO Detection Parser

    Assumptions
    ----------
    1. labels use YOLO format

       class cx cy w h

    2. coordinates are normalized

    3. classes start from 0

    """

    IMG_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff",
        ".webp",
    }

    def __init__(
        self,
        img_dir: str,
        label_dir: str,
        categories: list[str],
    ):
        self.img_dir = img_dir
        self.label_dir = label_dir

        assert len(categories) > 0, "数据集类别列表不能为空"
        self.cat_names = categories
            
        self.img_paths = []
        for file in os.listdir(img_dir):
            ext = Path(file).suffix.lower()
            if ext in self.IMG_EXTENSIONS:
                self.img_paths.append(os.path.join(img_dir, file))

    @property
    def num_classes(self):
        return len(self.cat_names)
    
    def __len__(self):
        return len(self.img_paths)
    
    def get_image_id(self, index):
        return Path(self.img_paths[index]).stem
    
    def get_image_info(self, index):
        img_path = self.img_paths[index]
        with Image.open(img_path) as image:
            width, height = image.size
        return {
            "width": width,
            "height": height,
            "file_name": img_path,
        }
        
    def load_image(self, index):
        img_path = self.img_paths[index]
        image = Image.open(img_path).convert("RGB")
        return image
    
    def load_target(self, index):
        img_id = self.get_image_id(index)
        img_info = self.get_image_info(index)
        width, height = img_info["width"], img_info["height"]
            
        label_path = os.path.join(self.label_dir, img_id + ".txt")
        
        boxes = []
        labels = []
        
        if os.path.exists(label_path):
            with open(label_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                cls, cx, cy, bw, bh = map(float, line.split())
                x1 = (cx - bw / 2) * width
                y1 = (cy - bh / 2) * height
                x2 = (cx + bw / 2) * width
                y2 = (cy + bh / 2) * height
                
                boxes.append([x1, y1, x2, y2])
                labels.append(int(cls))
        if len(boxes) == 0:
            boxes = torch.zeros((0, 4), dtype=torch.float32)
            labels = torch.zeros((0,), dtype=torch.long)
        else:
            boxes = torch.tensor(boxes, dtype=torch.float32)
            labels = torch.tensor(labels, dtype=torch.long)
        
        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": img_id,
            "ori_size": (height, width),
            "size": (height, width),
        }
        return target
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}(\n"
            f"  images={len(self)},\n"
            f"  classes={self.num_classes},\n"
            f"  img_dir='{self.img_dir}',\n"
            f"  label_dir='{self.label_dir}'\n"
            f")"
        )