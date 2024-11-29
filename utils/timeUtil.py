import time
from core.log import Log

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
