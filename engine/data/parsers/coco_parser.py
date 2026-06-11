import os
from PIL import Image
import torch
from pycocotools.coco import COCO
from engine.data.parsers._parser import BaseParser

@register
class COCOParser(BaseParser):
    """
    COCO-style Detection Parser

    Assumptions
    ----------
    1. category_id is continuous
    2. category_id may start from any integer
    3. category_id is automatically remapped to:
       0 ~ num_classes-1
    """

    def __init__(self, img_dir: str, ann_file: str):
        self.img_dir = img_dir
        self.ann_file = ann_file

        # 调用 pycocotools 解析 COCO 注释文件，能获取到图片和标注信息
        self.coco = COCO(ann_file) 

        # 获取每张图片的id键值（整数值）列表，
        # 列表索引和之后的取图片的索引一致 
        self.img_ids : list = self.coco.getImgIds()

        # Categories sorted by category id
        categories = sorted(
            self.coco.dataset["categories"],
            key=lambda x: x["id"])

        # Category names
        self.cat_names : list = [cat["name"] for cat in categories]

        # 类别开始值一般是0或1
        self.category_start_id = categories[0]["id"]

    @property
    def num_classes(self):
        return len(self.cat_names)
    
    def __len__(self):
        return len(self.img_ids)

    def get_image_id(self, index):
        return self.img_ids[index]

    def load_image(self, index):
        """
        返回 PIL.Image
        """
        image_id = self.img_ids[index]
        img_info = self.coco.imgs[image_id]
        img_path = os.path.join(self.img_dir, img_info["file_name"])
        image = Image.open(img_path).convert("RGB")
        return image

    def load_target(self, index):
        """
        返回协议字典
        """
        image_id = self.img_ids[index]
        img_info = self.coco.imgs[image_id]
        
        height = img_info["height"]
        width = img_info["width"]
        
        ann_ids = self.coco.getAnnIds(imgIds=image_id)
        anns = self.coco.loadAnns(ann_ids)

        boxes = []
        labels = []

        for ann in anns:
            x, y, bw, bh = ann["bbox"]
            boxes.append([x, y, x + bw, y + bh])
            # 类别重映射到从零开始
            labels.append(ann["category_id"] - self.category_start_id)

        if len(boxes) == 0:
            boxes = torch.zeros((0, 4), dtype=torch.float32)
            labels = torch.zeros((0,), dtype=torch.long)
        else:
            boxes = torch.tensor(boxes, dtype=torch.float32)
            labels = torch.tensor(labels, dtype=torch.long)

        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": image_id,
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
            f"  ann_file='{self.ann_file}'\n"
            f")"
        )
