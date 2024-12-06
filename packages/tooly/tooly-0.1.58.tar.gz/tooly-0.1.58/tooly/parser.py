import argparse, argcomplete

# argcomplete的安装方法：
# 1. pip install argcomplete
# 2. 配置全局的自动帮助信息：activate-global-python-argcomplete
# 3. 确认脚本的前1024字节中有PYTHON_ARGCOMPLETE_OK
# 4. .bashrc中增加如下行：
# . /etc/bash_completion.d/python-argcomplete
__tasks__ = {}

from typing import TypeVar, Generic

T = TypeVar('T')
from tooly.sh import CustomHelpFormatter


class __NoDefaultValue:
    pass


def define_arg(prefix="--", default=__NoDefaultValue, choices=__NoDefaultValue, help=__NoDefaultValue,
               **kwargs):
    """
    定义参数，最终的参数会透传进入parser.add_argument
    参数名为：prefix+类中的变量名
    注意：task的变量名的choices会被默认的注解值覆盖
    """
    args = {}
    if default != __NoDefaultValue:
        args['default'] = default
    if choices != __NoDefaultValue:
        args['choices'] = choices
    if help != __NoDefaultValue:
        args['help'] = help
    return (prefix, {**kwargs, **args})


def parse_args(argDef: Generic[T], description=None, formatter_class=CustomHelpFormatter) -> Generic[T]:
    p = argparse.ArgumentParser(description=description, formatter_class=formatter_class)
    for k in dir(argDef):
        if k.startswith("_"):
            continue
        v = getattr(argDef, k)
        if k == 'task' and v[0] == '':
            v[1]['choices'] = __tasks__.keys()
        p.add_argument(v[0] + k, **v[1])
    argcomplete.autocomplete(p)
    return p.parse_args()


def register_action(*otherNames):
    """
    默认以函数名为key，写入__tasks__的map中（key为函数名，value为函数对应的函数列表）
    @param otherNames: 其他的函数名
    """
    if otherNames and callable(otherNames[0]):  # 判断是否有额外参数传递进来
        # 当作无参数装饰器处理
        func = otherNames[0]
        __tasks__[func.__name__] = [func]

        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator
    else:
        # 当作带参数装饰器处理，维持原来的逻辑
        class _Action:
            def __init__(self, func):
                self.fun = func
                for k in [func.__name__, *otherNames]:
                    if k not in __tasks__:
                        __tasks__[k] = []
                    __tasks__[k].append(self.fun)

            def __call__(self, *args, **kwds):
                return self.fun(*args, **kwds)

        return _Action


def runTasks(taskName: str):
    for i in __tasks__[taskName]:
        i()
