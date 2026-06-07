from engine.core._config import ExpConfig
from engine.core.workspace import REGISTRY
from omegaconf import DictConfig, OmegaConf
from hydra.utils import instantiate
from engine.utils import log


class OmegaExpConfig(ExpConfig):
    """OmegaConf配置类，支持从字典初始化属性"""
    def __init__(self, cfg : DictConfig):
        super().__init__()
                        
        # 检查cfg中的字段是否在ExpConfig中已定义
        self._check_cfg(cfg)
        
        # 递归地将cfg中的带_target_字段的对象转换成GLOBAL_CONFIG中的完整模块路径
        self._target_cfg(cfg)
        
        # 将targetd cfg转换成普通字典存储在self.auto_generated_cfg中，方便后续访问，未经实例化
        self.auto_generated_cfg = OmegaConf.to_container(cfg, resolve=True) # type: ignore
        
        # 实例化cfg中带_target_字段的对象，并转为dict存储在temp_cfg中
        temp_cfg : dict = OmegaConf.to_container(instantiate(cfg, _recursive_=True), resolve=True) # type: ignore
        
        # 将temp_cfg中的字段赋值到ExpConfig中，方便后续访问
        for key, value in temp_cfg.items():
            setattr(self, key, value)
            log.info(f"{key:<5} 已实例化并做准备")
            
    def _check_cfg(self, cfg):
        for key in cfg:
            assert key in self.__dict__, f"YAML 中实验配置字段 {key} 在 ExpConfig 主类中陌生"
    
    def _target_cfg(self, cfg):
        """
        1. 检查所有字段准为ExpConfig中已配置字段
        2. 递归地将cfg中的带_target_字段的对象，将其值转换成GLOBAL_CONFIG中的完整模块路径，
        方便之后的动态实例化。
        要求
        """
        for key, value in cfg.items():            
            if isinstance(value, DictConfig):
                self._target_cfg(value) # 递归检查子配置
                if '_target_' in value: 
                    # 如果是待实例化字段，获取其完整模块路径并更新_target_
                    # 如果待实例化字段值未注册，抛出断言错误
                    info = REGISTRY.get(value['_target_'], None)
                    assert info is not None, f"{value['_target_']} 未在全局注册表中注册"
                    if isinstance(info, dict) and '_pymodule' in info:
                        pymodule = info['_pymodule']
                        value["_target_"] = pymodule
                    else:
                        value["_target_"] = info