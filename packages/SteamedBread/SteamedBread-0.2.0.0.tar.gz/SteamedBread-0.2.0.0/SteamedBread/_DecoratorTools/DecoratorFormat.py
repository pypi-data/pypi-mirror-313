"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: DecoratorFormat.py
@Time: 2023/12/9 18:00
"""

import functools
import inspect
import json
import os
from pathlib import Path

import allure
import pytest
import yaml


def timer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        import time
        from SteamedBread import logger

        __start_time = time.time()
        resp = func(*args, **kwargs)
        logger.info(msg=f'{func.__name__}() 共耗时: %.3f秒' % (time.time() - __start_time))
        return resp

    return inner


class Decorators:
    """"""

    @staticmethod
    def load_json_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.loads(f.read())

    @staticmethod
    def load_yaml_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            data = yaml.safe_load(f.read())
            if isinstance(data, dict):
                if 'param_data' not in data:
                    raise Exception('yaml 文件中至少要有 param_data 的 key')
                return data['param_data']
            return data

    @staticmethod
    def get_test_data_file_by_env(path, suffix='yaml'):
        # 只有 filename 不带 相应 后缀才会自动根据执行环境做自动识别
        if not path.endswith(suffix):
            # 遵循 SteamedBread 模块为任意地方可以 import 的原则，使用局部 import Config
            # if "test" in ("test", "ppe"):
            from SteamedBread import SetEnvironment
            env = SetEnvironment()
            if env.current_env not in ["tce", "ppe", "online"]:
                real_file = path + f'.test.{suffix}'
            else:
                real_file = path + f'.online.{suffix}'
            # 如果用例不区分boe|tce，直接取对应的 json 后缀的文件
            if not os.path.exists(real_file):
                real_file = path + f'.{suffix}'
        else:
            real_file = path
        return real_file

    @staticmethod
    def _parameterized_func(case, parameter_data, enable_index=None, *args, **kwargs):
        p = []
        for index, each in enumerate(parameter_data):
            # 如果设置了 enable_index，并且没有指定当前参数化，则跳过当前
            # 主要用于调试用例时进行 debug
            if enable_index is not None and index not in enable_index:
                continue
            p.append(each)

        return pytest.mark.parametrize('param', p, *args, **kwargs)(case)

    @classmethod
    def param_file(cls, filename: str, enable_index=None, enable_envs=None,
                   disable_envs=None, suffix='yaml', *args, **kwargs):
        def inner(func):
            case_dir = Path(inspect.getfile(func)).parent
            parameter_file = str(case_dir.joinpath(filename))
            if enable_envs is not None and "test" not in enable_envs \
                    or disable_envs is not None and "test" in disable_envs:
                return pytest.mark.skip(f'Case not run in test ! 当前环境下没有对应的测试文件')
            real_file = cls.get_test_data_file_by_env(parameter_file, suffix=suffix)

            try:
                if suffix == 'yaml':
                    parameter_data = cls.load_yaml_file(real_file)
                elif suffix == 'json':
                    parameter_data = cls.load_json_file(real_file)
                else:
                    raise Exception('没有对应的类型文件')
                if not isinstance(parameter_data, (list, tuple)):
                    return pytest.mark.skip('参数化json文件 {} 不是数组！'.format(parameter_file))
                return cls._parameterized_func(func, parameter_data, enable_index, *args, **kwargs)
            except FileNotFoundError:
                from SteamedBread import SetEnvironment
                raise FileNotFoundError(f'当前环境: {SetEnvironment().current_env}, 缺少对应的参数化文件: {parameter_file}')

        return inner

    @classmethod
    def param_data(cls, parameter_data: list, enable_index=None, *args, **kwargs):
        def inner(func):
            if not isinstance(parameter_data, (list, tuple)):
                return pytest.mark.skip('参数化json数据 {} 不是数组！'.format(parameter_data))
            return cls._parameterized_func(func, parameter_data, enable_index, *args, **kwargs)

        return inner


param_file = Decorators.param_file
param_data = Decorators.param_data

