from abc import ABC, abstractmethod
from core.log import log


class Template(ABC):
    def __init__(self, name, enabled, screen):
        self.name = name
        self.enabled = enabled
        self.screen = screen

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
