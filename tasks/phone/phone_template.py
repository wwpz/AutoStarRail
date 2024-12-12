from log import log
from automation import auto
from abc import ABC, abstractmethod

from utils.time_utils import TimeUtils
from utils.base_utils import BaseUtils

params = {
    "x": None,
    "y": None
}


def go_home():
    title = auto.window_title
    window_class = BaseUtils.get_window_class_from_title(title)
    center = BaseUtils.get_window_center(title)
    if center:
        params["x"], params["y"] = center
        log.debug(f"窗口 '{title}' 的中心点坐标: x={params["x"]}, y={params["y"]}")
    else:
        log.debug(f"未找到标题为 '{title}' 的窗口")

    for i in range(3):
        if BaseUtils.switch_to_game(window_class, title):
            auto.mouse_middle(params["x"], params["y"])
            TimeUtils.wait_(1)
        if auto.find_element("./res/phone/basics/home_setting.png"):
            log.debug("在首页")
            break


def open_search():
    auto.mouse_move(params["x"], params["y"] + 200)
    TimeUtils.wait_(1)
    auto.mouse_dragRel(0, -150, 0.1)
    TimeUtils.wait_(1)


def clear_background():
    auto.mouse_move(params["x"], params["y"] + 430)
    TimeUtils.wait_(1)
    auto.mouse_dragRel(0, -900, 0.5)
    if auto.click_element("./res/phone/basics/clear.png", is_global=True):
        TimeUtils.wait_(2)


class PhoneTemplate(ABC):
    def __init__(self, name):
        self.name = name
        self.log = log

    def start(self):
        log.hr(f"开始{self.name}奖励", 0)
        go_home()
        clear_background()
        open_search()
        self.run()
        log.hr(f"{self.name}奖励完成", 0)

    @abstractmethod
    def run(self):
        pass
