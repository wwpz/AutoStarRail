from log import log
from abc import ABC, abstractmethod
from utils.phone_utils import PhoneUtils

params = {
    "x": None,
    "y": None
}


class PhoneTemplate(ABC):
    def __init__(self, name, is_go_home=True):
        self.name = name
        self.x = params["x"]
        self.y = params["y"]
        self.log = log
        self.go_home = is_go_home

    def start(self):
        log.hr(f"开始{self.name}奖励", 0)
        if self.go_home:
            params["x"], params["y"] = PhoneUtils.go_home()
            PhoneUtils.clear_background()
            PhoneUtils.open_search()
        self.run()
        log.hr(f"{self.name}奖励完成", 0)

    @abstractmethod
    def run(self):
        pass
