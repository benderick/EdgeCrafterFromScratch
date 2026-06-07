"""
Abstract Base Class
将来会有不同的parser实现，提供一个抽象基类，定义接口规范
"""
from abc import ABC
from abc import abstractmethod

class BaseParser(ABC):

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def load_image(self, index) -> all: # type: ignore
        """
        return:
            PIL.Image
        """
        pass

    @abstractmethod
    def load_target(self, index) -> dict:
        """
        Output
        ------
        {
            "boxes": Tensor[N,4],
            "labels": Tensor[N],
            "image_id": str,
            "ori_size": (H,W),
            "size": (H,W),
        }
        """
        pass

    @abstractmethod
    def get_image_id(self, index) -> int|str:
        pass