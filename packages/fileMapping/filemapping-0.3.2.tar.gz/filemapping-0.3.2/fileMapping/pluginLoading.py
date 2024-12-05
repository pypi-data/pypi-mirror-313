"""
这个文件用于加载插件
plugIns
"""
import os
import ast
import importlib
import importlib.util
from typing import Any

import inspect as inspectKB

from rich import inspect

from . import config


"""
empty 一个空 函数/方法
    - 当导入错误时，触发空函数，为了防止调用错误

method 公共方法

packageMethod(method)  包类
    
fileMethod(method)  文件类

f 调用函数
"""
class blacklist:
    ...


class empty:
    # 一个空函数/方法
    class main:
        def __init__(self):
            pass

    def __init__(self):
        self.main = self.main()

class method:
    def __init__(self, path):
        self.pointer = None
        self.pack: Any| empty
        self.magicParameters: dict[str: Any] = {}
        # 调用对象
        self.path: str = path
        self.absolutePath = self.path if os.path.isabs(self.path) == True else os.path.realpath(self.path)
        # 相对路径 & 绝对路径
        self.importThePackage()
        # 导入包

    def run(self, *args, **kwargs):
        """
        运行包
        :return:
        """
        if self.pointer == None:
            #
            return False

        else:
            #
            self.list = []

        try:
            sig = inspectKB.signature(self.pointer)
            parameter_list = [
                key for key, data in sig.parameters.items()
            ]
            if args == [] and kwargs == {}:
                # 获取参数
                if len(parameter_list) != 0:
                    # 需要参数
                    parameter = {
                        parameter_list[i]: self.list[i] for i in range(len(self.list))
                    }

                else:
                    # 不需要参数
                    parameter = {}

            else:
                return self.pointer(*args, **kwargs)

            return self.pointer(**parameter)

        except TypeError as e:
            return False

    def importThePackage(self): ...


def impo(file_path: os.path, callObject: str):
        """
        :param callObject: 'main'
        :param file_path: 绝对路径
        :return:
        """
        spec = importlib.util.spec_from_file_location(callObject, file_path)
        the_api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(the_api)
        return the_api


class packageMethod(method):
    """包方法"""
    __name__ = 'packageMethod'

    def importThePackage(self):
        """
        导入包
        :return:
        """
        def get(module, name, data = False):
            return getattr(module, name) if name in dir(module) else data

        try:
            self.pack = impo(f"{self.absolutePath}\\__init__.py", '')
            # 导入 __init__.py 获取保留参数
            fs = {
                key: get(self.pack, key, data) for key, data in config.functionsKeepParameters.items()
            }
            if fs['__file__'] == '':
                fs['__file__'] = '__init__.py'
            self.pack = impo(f"{self.absolutePath}\\{fs['__file__']}", fs['__function__'])
            # 导入包
        except (ModuleNotFoundError, TypeError, ImportError) as e:
            # 导入错误
            print(f"\n\033[1;31m file: {self.path}\n导入错误 log: {e}\033[0m")
            self.pack = empty()

        for i in dir(self.pack):
            if not i in dir(blacklist):
                self.magicParameters[i] = getattr(self.pack, i)
                if i == 'main':
                    self.pointer = getattr(self.pack, i)

        else:
            if self.pointer == None:
                # 无 main
                print(f"\n\033[1;31m file: {self.path}\n导入错误 main函数: py文件没有main函数\033[0m")
                return False

class fileMethod(method):
    """文件方法"""
    __name__ = 'fileMethod'

    def importThePackage(self):
        """
        导入包
        :return:
        """
        if not (os.path.isfile(self.absolutePath) and self.absolutePath.split('.')[-1] == 'py'):
            return False

        try:
            self.pack = impo(self.absolutePath, 'main')
            # 导入包
        except ModuleNotFoundError or TypeError as e:
            # 导入错误
            print(f"\n\033[1;31m file: {self.path}\n导入错误 log: {e}\033[0m")
            self.pack = empty()

        for i in dir(self.pack):
            if not i in dir(blacklist):
                self.magicParameters[i] = getattr(self.pack, i)
                if i == 'main':
                    self.pointer = getattr(self.pack, i)

        else:
            print(15, self.pointer)
            if self.pointer == None:
                # 无 main
                print(f"\n\033[1;31m file: {self.path}\n导入错误 main函数: py文件没有main函数\033[0m")
                return False


def f(path: os.path) -> packageMethod | fileMethod | bool:
    """
    判断 path 是否为 包/文件
    :return: 包 packageMethod 文件 fileMethod
    """
    def package(path: os.path, ) -> bool:
        """
        判断是否为包
        __init__.py & main.py
        :return: bool
        """
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "__init__.py")):
            # 判断函数是否是为包
            return True

        return False

    def file(path: os.path) -> bool:
        """
        判断是否 是一个可调用文件
        :return: bool
        """
        if os.path.isfile(path) and path.split('.')[-1] == 'py':
            with open(path, encoding='utf-8') as f:
                tree = ast.parse(f.read())

            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            # 获取类型和函数
            if 'main' in functions:
                return True

        print(f"\n\033[1;31m file: {path}\n导入错误 main函数: py文件没有main函数\033[0m")
        return False

    if os.path.isdir(path) and package(path):
        return packageMethod(path)

    elif os.path.isfile(path) and file(path):
        return fileMethod(path)

    else:
        return False

