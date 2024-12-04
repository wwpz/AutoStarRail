from abc import ABC, abstractmethod
from log import log


class LauncherTemplate(ABC):
    def __init__(self, name, enabled):
        self.name = name
        self.enabled = enabled

    def start(self):
        if not self.enabled:
            log.info(f"{self.name}未开启")
            return

        log.hr(f"检测到{self.name}奖励", 1)
        self.run()
        log.hr(f"{self.name}奖励完成", 2)

    @abstractmethod
    def run(self):
        pass