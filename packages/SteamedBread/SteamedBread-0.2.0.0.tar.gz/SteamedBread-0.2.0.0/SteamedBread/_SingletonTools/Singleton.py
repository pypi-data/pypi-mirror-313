"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: Singleton.py
@Time: 2023/12/9 18:00
"""


def singleton(cls):
    instance = dict()

    def inner(*args, **kwargs):
        if not instance.get(cls):
            obj = cls(*args, **kwargs)
            instance[cls] = obj
        else:
            obj = instance[cls]
        return obj

    return inner


class SingletonExample:
    instance = {}

    def __init__(self):
        self.A = "111"

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance
