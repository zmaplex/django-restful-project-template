import os
import importlib

from base.basemodel import BaseModel

# 获取当前目录
current_dir = os.path.dirname(__file__)

# 遍历当前目录中的所有文件
for file in os.listdir(current_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]  # 去除文件名的 ".py" 后缀
        module = importlib.import_module("." + module_name, __package__)
        for name in dir(module):
            obj = getattr(module, name)
            if (
                isinstance(obj, type)
                and issubclass(obj, BaseModel)
                and obj is not BaseModel
            ):
                globals()[name] = obj
