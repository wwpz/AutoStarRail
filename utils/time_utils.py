import time
from log import Log
from datetime import datetime

log = Log()


class TimeUtil:
    @staticmethod
    def wait_time(timeout, print_interval=5):
        """等待指定时间，并每隔 print_interval 秒打印剩余时间。"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())  # 更新剩余时间
            if remaining_time % print_interval == 0:
                log.debug(f"剩余等待时间: {remaining_time} seconds")
            time.sleep(1)  # 添加一个延迟，以避免快速循环

    @staticmethod
    def wait_(timeout):
        """等待指定时间，每秒打印剩余时间。"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())  # 更新剩余时间
            log.debug(f"剩余等待时间: {remaining_time} seconds")  # 每秒打印剩余时间
            time.sleep(1)  # 添加一个延迟，以避免快速循环

    @staticmethod
    def check_time(target_hour, target_minute):
        """
        检查当前时间是否到达指定的时间，并返回 True 或 False。

        :param target_hour: 指定的目标小时（24小时制）
        :param target_minute: 指定的目标分钟
        :return: 如果当前时间到达或超过目标时间，返回 True；否则返回 False。
        """
        # 获取当前时间
        now = datetime.now()

        # 创建今天的目标时间对象
        target_time_today = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        if now >= target_time_today:
            # 如果当前时间已经超过或等于目标时间
            return True
        else:
            # 否则返回 False
            return False
