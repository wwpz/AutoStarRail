from abc import ABC, abstractmethod
from log import log
from config import cfg


class Template(ABC):
    def __init__(self, name, enabled):
        self.name = name
        self.enabled = enabled
        self.game_type = cfg.game_type

    def start(self):
        if not self.enabled:
            log.info(f"{self.name}未开启")
            log.hr(f"{self.name}未开启", 0)
            return

        log.hr(f"检测到{self.name}奖励", 0)
        cfg.set_value("now_run_type", self.game_type)
        self.run()
        log.hr(f"{self.name}奖励完成", 0)

    @abstractmethod
    def run(self):
        pass
