import importlib
import os
import traceback

# 核心：定义节点映射和显示名称映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 获取当前插件所在目录
current_dir = os.path.dirname(__file__)

# 遍历目录加载所有 .py 节点模块
# 这样即便你以后添加了新的英文名 .py 文件，它也会自动加载
for file in os.listdir(current_dir):
    if file.endswith(".py") and file != "__init__.py":
        # 移除后缀获取模块名
        module_name = file[:-3]
        try:
            # 使用相对导入方式
            module = importlib.import_module(f".{module_name}", package=__name__)
            
            # 自动读取子模块中的 MAPPINGS 并合并
            if hasattr(module, "NODE_CLASS_MAPPINGS"):
                NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                
        except Exception as e:
            # 专业处理：即便其中一个节点写错了，也不会导致整个 ComfyUI 启动崩溃
            print(f" [ComfyUI_Text_Processing] Failed to load module '{module_name}': {e}")
            traceback.print_exc()

# 导出映射供 ComfyUI 后台调用
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]