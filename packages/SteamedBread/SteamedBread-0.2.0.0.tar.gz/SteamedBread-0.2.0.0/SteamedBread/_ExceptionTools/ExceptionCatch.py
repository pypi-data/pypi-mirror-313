"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: _ExceptionTools.py
@Time: 2023/12/22 19:58
"""


def hook_exceptions(exceptions: (tuple, set, list) = None):
    """
    捕获异常装饰器
    若未指定捕获的非基类异常, 则默认是忽略其它异常捕获
    example: 若 exception_types = [AssertionError], 则只会捕获这个方法中抛出的AssertionError, 而会忽略类似于ValueError等其它异常
    :param exceptions: 指定的异常
    :return: None
    """
    if isinstance(exceptions, (tuple, set, list)):
        exception_types = tuple(exceptions)
    elif isinstance(exceptions, type):
        exception_types = (exceptions,)
    elif exceptions is None:
        exception_types = tuple()

    else:
        raise Exception("参数类型错误: 需要将多个异常类以元组的形式上传")

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                raise e
            except Exception as e2:
                if type(e2) not in exception_types:
                    exception_types_name = [_.__name__ for _ in exception_types]
                    print(f"""
---------------------------------------------                    
当前的执行方法名称: {func.__name__}
未捕获指定异常类型: {exception_types_name}
或是故意忽略该异常: {type(e2).__name__}
--------------------------------------------- 
                    """)

        return wrapper

    return decorator
