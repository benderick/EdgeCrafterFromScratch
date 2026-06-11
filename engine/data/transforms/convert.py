from typing import Any
import torch
import torchvision
import torchvision.transforms.v2.functional as F
from torchvision.tv_tensors import BoundingBoxes

@register
class ConvertImage:
    def __init__(self, fmt="tensor", mode="raw", mean=[], std=[]):
        assert fmt in ("tensor", "pil"), "图片必须转换成Tensor或PIL格式"
        assert mode in ("normalize", "denormalize", "raw"), "标准化必须在normalize, denormalize, raw中选择"
        self.fmt = fmt
        self.mode = mode
        self.mean = mean
        self.std = std
    def __call__(self, image, target):
        if self.mode == "denormalize":
            mean = torch.tensor(self.mean).view(3,1,1)
            std = torch.tensor(self.std).view(3,1,1)
            image = (image * std + mean).clamp(0,1)
            
        if self.fmt=="tensor":
            image = F.pil_to_tensor(image)
            image = image.float() / 255.0
        else:
            image = F.to_pil_image(image)
            
        if self.mode == "normalize":
            image = F.normalize_image(image, self.mean, self.std)
        
        return image, target 

@register       
class ToBoundingBoxes:
    """
    将XYXY格式的像素的TensorBox转成BoundingBox
    """
    def __init__(self, fmt="XYXY") -> None:
        self.fmt = fmt
    def __call__(self, image, target) -> Any:
        h, w = target["size"]
        target["boxes"] = BoundingBoxes(target["boxes"], 
                                        format=self.fmt,
                                        canvas_size=(h,w)) # type: ignore
        return image, target
  
@register  
class ToTensorBoxes:
    def __call__(self, image, target) -> Any:
        target["size"] = target["boxes"].canvas_size
        target["boxes"] = target["boxes"].data
        return image, target

@register
class ConvertBoxes:
    """
    转变格式和标准化 用于Tensor
    Tensor[xyxy pixel] -> cxcywh normalized
    """
    def __init__(self, in_fmt="xyxy", out_fmt="cxcywh", mode="raw"):
        assert mode in ("normalize", "denormalize", "raw"), "标准化必须在normalize, denormalize, raw中选择"
        self.in_fmt = in_fmt.lower()
        self.out_fmt = out_fmt.lower()
        self.mode = mode

    def __call__(self, image, target):
        boxes = target["boxes"]
        
        if self.mode == "denormalize":
            image_size = target["size"]
            h, w = image_size
            scale = torch.tensor(
                [w, h, w, h],
                dtype=boxes.dtype,
                device=boxes.device,
            )
            boxes =  boxes * scale
                    
        if self.in_fmt != self.out_fmt:
            boxes = torchvision.ops.box_convert(
                boxes.float(),
                in_fmt=self.in_fmt,
                out_fmt=self.out_fmt,
            )
        
        if self.mode == "normalize":
            image_size = target["size"]
            h, w = image_size
            scale = torch.tensor(
                [w, h, w, h],
                dtype=boxes.dtype,
                device=boxes.device,
            )
            boxes = boxes / scale
        
        target["boxes"] = boxes
        return image, target