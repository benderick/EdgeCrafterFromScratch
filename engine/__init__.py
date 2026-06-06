import os
import importlib

def auto_import_recursive(pkg_path, pkg_name):
    """
    递归遍历包目录下所有 .py 文件并导入执行（只执行，不导出）
    :param pkg_path: 包的物理路径
    :param pkg_name: 包名（如 engine.core）
    """
    for filename in os.listdir(pkg_path):
        file_path = os.path.join(pkg_path, filename)

        # 如果是目录 → 递归进去
        if os.path.isdir(file_path):
            auto_import_recursive(file_path, f"{pkg_name}.{filename}")

        # 如果是 py 文件，且不是 __init__.py → 导入执行
        elif filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                # 绝对导入
                importlib.import_module(f"{pkg_name}.{module_name}")
            except Exception as e:
                print(f"[自动导入警告] 导入失败: {pkg_name}.{module_name}, {e}")

# 入口：从当前包开始递归
current_dir = os.path.dirname(__file__)
auto_import_recursive(current_dir, __name__)