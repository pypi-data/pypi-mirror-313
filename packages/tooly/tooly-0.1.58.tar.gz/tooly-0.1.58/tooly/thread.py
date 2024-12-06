import math
from threading import Thread
from typing import List, Any, Callable


class Result:
    def __init__(self, result: Any, exception: Exception = None):
        self.result = result
        self.exception = exception

    def __repr__(self):
        return f"[result = {self.result}, exception = {self.exception}]"


def runInMultiThread(threadCnt: int, func: Callable, args: List[List[Any]]) -> List[Result]:
    """
    启动threadCnt个线程，循环运行func函数
    :param threadCnt: 线程数量
    :param func: 线程中要运行的函数
    :param args: List<List>
    :return: List<Result>
    """
    threadResultList = [None] * threadCnt

    def f(i, arg):
        resList = []
        for a in arg:
            try:
                res = func(*a)
                resList.append(Result(res))
            except Exception as e:
                resList.append(Result(None, e))
        threadResultList[i] = resList

    thList = []
    argSize = math.ceil(len(args) / threadCnt)
    for i in range(threadCnt):
        th = Thread(target=f, args=(i, args[i * argSize:(i + 1) * argSize]))
        th.start()
        thList.append(th)

    for th in thList:
        th.join()
    result = []
    for res in threadResultList:
        result += res
    return result


if __name__ == '__main__':
    def f(i):
        return f"i = {i}, 1/i = {1 / i}"


    thArgs = [[1], [2], [3], [4], [0]]

    for i in runInMultiThread(3, f, thArgs):
        print(i)
