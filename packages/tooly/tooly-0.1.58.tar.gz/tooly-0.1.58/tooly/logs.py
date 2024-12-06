import datetime
import inspect
import logging
import os.path
from enum import IntEnum
from logging.handlers import TimedRotatingFileHandler


class LogLevel(IntEnum):
    INFO = 0
    LOG = 3
    DEBUG = 5


__logLevel = LogLevel.LOG


def setLevel(level: LogLevel):
    global __logLevel
    __logLevel = level


def __getPrintInfo(showTime, showFile):
    ret = []
    if showTime:
        t = datetime.datetime.now()
        m = int(t.microsecond / 1000)
        t = t.strftime('%m-%d %H:%M:%S')
        ret.append(f"[{t}.{m:03d}]")
    if showFile:
        caller_frame = inspect.stack()[2]
        fname = os.path.split(caller_frame.filename)[-1]
        ret.append(f"[{fname}:{caller_frame.lineno}]")
    return "".join(ret)


def DEBUG(*args, showTime=True, showFile=True, showDebug=False):
    if __logLevel >= LogLevel.DEBUG:
        print(f"{'[DEBUG]' if showDebug else ''}{__getPrintInfo(showTime, showFile)}", *args)


def LOG(*args, showTime=True, showFile=True, showDebug=False):
    if __logLevel >= LogLevel.LOG:
        print(f"{'[LOG]' if showDebug else ''}{__getPrintInfo(showTime, showFile)}", *args)


def INFO(*args, showTime=True, showFile=True, showDebug=False):
    if __logLevel >= LogLevel.INFO:
        print(f"{'[INFO]' if showDebug else ''}{__getPrintInfo(showTime, showFile)}", *args)


class __MyFormatter(logging.Formatter):
    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = ct.strftime("%Y-%m-%d %H:%M:%S")
        s = "%s.%03d" % (t, record.msecs)
        return s


def initLog(fname: str = None,
            enableConsole=True,
            level=logging.DEBUG,
            fileRotateIntervalHour=24,
            fileRotateBackupCnt=1,
            fmt: str = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"):
    """
    logging的初始化函数。
    :param fname: 日志文件的名称，如果为空则不记录日志到文件
    :param enableConsole: 是否开启控制台日志输出
    :param level: 日志级别
    :param fileRotateIntervalHour: 日志文件多久滚动一次
    :param fileRotateBackupCnt: 日志文件最大的保存数
    :param fmt: 日志的记录格式
    :return:
    """
    formatter = __MyFormatter(fmt=fmt)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(level)
    streamHandler.setFormatter(formatter)

    time_rotate_file = TimedRotatingFileHandler(filename=fname,
                                                when='S',
                                                interval=3600 * fileRotateIntervalHour,
                                                backupCount=fileRotateBackupCnt)
    time_rotate_file.setFormatter(formatter)
    time_rotate_file.setLevel(level)

    handlers = []
    if fname:
        handlers.append(time_rotate_file)
    if enableConsole:
        handlers.append(streamHandler)

    if handlers:
        logging.basicConfig(level=level, handlers=handlers)


def a():
    DEBUG("hello ")


if __name__ == '__main__':
    a()
