### 导入常用系统库 ###
import os
import sys
###################

### 配置根路径 #####################
# 路径配置是我们项目的重要合约，许多逻辑基于此合约构建
# 将项目根目录设置为ROOT变量值、设置为当前工作目录、
# 设置为环境变量PROJECT_ROOT、加入sys.path、
# 将根目录下的.env文件加载到环境变量中
from PIL import Image
import rootutils
ROOT = rootutils.setup_root(__file__, project_root_env_var=True, 
                            dotenv=True, pythonpath=True, cwd=True)
##################################

### 导入引擎，完成注册 ###
import engine
#########################

### 导入日志系统 ###
from engine.utils import log
#################

### 导入系统配置库 ###
from omegaconf import DictConfig, OmegaConf
import hydra
#####################

### 导入全局注册表 ###
from engine.core.workspace import REGISTRY
from engine.core.omega_config import OmegaExpConfig
######################

@hydra.main(version_base="1.3", config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    log.rule("项目启动")
    # log.use_loggerfile(".") # 在工作目录下创建日志文件
    # log.rule(f"工作目录：{os.getcwd()}")
    # log.panel(sys.path, "导包列表")
    # log.panel(sys.modules, "模块缓存")
    log.panel(REGISTRY, "注册表内容")
    # log.panel(OmegaConf.to_container(cfg), "配置内容")
    
    exp = OmegaExpConfig(cfg.exp)
    dl = exp.dataloader
    for images, targets in dl:
        log.info(images.shape)
        log.panel(targets)
        break    
if __name__ == "__main__":
    main()