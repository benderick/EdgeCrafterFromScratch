import torchvision.transforms.v2 as T
from engine.core.workspace import register

# 调整尺寸
Resize = register(T.Resize)
# 随机左右翻转
RandomHorizontalFlip = register(T.RandomHorizontalFlip)
# 删除尺寸过小的框
SanitizeBoundingBoxes = register(T.SanitizeBoundingBoxes)
# 随机颜色扰动
RandomPhotometricDistort = register(T.RandomPhotometricDistort)