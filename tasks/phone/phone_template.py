from log import log
from abc import ABC, abstractmethod
from utils.phone_utils import PhoneUtils
from utils.base_utils import BaseUtils


class PhoneTemplate(ABC):
    def __init__(self, name):
        self.name = name
        self.log = log
        self.left = None
        self.top = None
        self.right = None
        self.bottom = None
        self.center_x = None
        self.center_y = None

    def start(self):
        self.left, self.top, self.right, self.bottom = BaseUtils.get_window_borders()
        self.center_x = self.left + (self.right - self.left) // 2
        self.center_y = self.top + (self.bottom - self.top) // 2

        log.hr(f"开始{self.name}奖励", 0)
        PhoneUtils.go_home()
        PhoneUtils.clear_background()
        PhoneUtils.open_search()
        self.run()
        log.hr(f"{self.name}奖励完成", 0)

    @abstractmethod
    def run(self):
        pass
