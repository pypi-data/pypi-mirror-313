import time
import traceback
from typing import List

from tooly.logs import INFO, LOG


class BaseChecker:
    def __init__(self, 检查名称, 停止后续检查流程=False, 尝试重试次数=5, 发送恢复消息=True):
        self.停止后续检查流程 = 停止后续检查流程
        self.异常次数 = 0
        self.检查名称 = 检查名称
        self.尝试重试次数 = 尝试重试次数
        self.发送恢复消息 = 发送恢复消息

    msgList = []

    @staticmethod
    def addMsg(msg):
        """单次检查的消息可以放在消息列表中，最终可以通过消息处理函数统一发送出去"""
        BaseChecker.msgList.append(msg)

    def checkOnce(self):
        """
        检查一次，返回True则表示异常，False表示正常
        """

    def tryRecovery(self):
        pass

    def run(self):
        """
        运行一次检查、恢复流程，返回True则中断后续流程，False不中断后续流程
        """
        checkSuccess = False
        try:
            checkSuccess = self.checkOnce()
        except:
            traceback.print_exc()

        if not checkSuccess:
            self.异常次数 += 1
            msg = f"【{self.检查名称}】 异常 【{self.异常次数}】次"
            if self.异常次数 % 5 == 0:
                # 每5次异常报告一次消息
                BaseChecker.addMsg(msg)
            INFO(msg)
            try:
                if 2 <= self.异常次数 <= (self.尝试重试次数 + 1):
                    # 异常次数在[2,args.tryRecoveryTimes]之间才尝试恢复
                    # 当一次异常时，让任务尝试自行恢复
                    INFO(f"{self.检查名称} 尝试恢复中")
                    self.tryRecovery()
            except:
                traceback.print_exc()
            return self.停止后续检查流程
        else:
            if self.异常次数 > 0:
                if self.发送恢复消息:
                    BaseChecker.addMsg(f"【{self.检查名称}】恢复正常，一共异常{self.异常次数}次")
                self.异常次数 = 0
            LOG(self.检查名称 + "正常")


def runCheckers(检查列表: List[BaseChecker], 消息处理函数=None, 检查间隔周期=60, 任务之间间隔秒数=0):
    while True:
        for chker in 检查列表:
            try:
                if chker.run():
                    break
            except:
                traceback.print_exc()
            if 任务之间间隔秒数:
                time.sleep(任务之间间隔秒数)
        if 消息处理函数:
            消息处理函数(BaseChecker.msgList)
        BaseChecker.msgList = []
        time.sleep(检查间隔周期)
