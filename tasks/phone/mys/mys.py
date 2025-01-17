from log import log
from config import cfg
from automation import auto
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils


class Mys:
    def __init__(self, name):
        self.name = name
        self.log = log
        self.count = None,
        self.center_x = None,
        self.center_y = None,

    def start(self, receive):
        left, top, right, bottom = BaseUtils.get_window_borders()
        self.center_x = (left + right) // 2
        self.center_y = (top + bottom) // 2
        log.hr(f"开始{receive}奖励", 0)
        if receive == "星铁签到":
            self.signin()
        log.hr(f"{receive}奖励完成", 0)

    def run_once(self):
        # if not self._has_run_once:
        PhoneUtils.go_home()
        PhoneUtils.clear_background()
        PhoneUtils.open_search()
        BaseUtils.paste("米游社")
        if auto.click_element("./res/phone/mys/icon.png", is_global=True):
            TimeUtils.wait_time(2)
            if auto.click_element("./res/phone/basics/select_app.png", is_global=True):
                if auto.click_element(f"./res/phone/mys/launch_icon{self.count}.png", is_global=True):
                    TimeUtils.wait_time(15)

        # self._has_run_once = True  # 设置标志为 True，表示方法已经执行过

    def signin(self):
        for i in range(1, 3):
            self.count = i
            cfg.set_value("now_run_type", "mys")
            cfg.set_value("user_account", f"{i}_app")
            self.run_once()
            if auto.click_element("./res/phone/mys/mys_home_click.png", is_global=True):
                TimeUtils.wait_time(2)
            if auto.click_element("./res/phone/mys/mys_update_no.png", is_global=True):
                TimeUtils.wait_time(2)
            if auto.find_element("./res/phone/mys/mys_home.png", is_global=True):
                TimeUtils.wait_time(2)
                if auto.click_element("./res/phone/mys/waiting_room.png", is_global=True):
                    TimeUtils.wait_time(2)
                    if auto.click_element("./res/phone/mys/clock_in.png", is_global=True):
                        TimeUtils.wait_time(2)
                for j in range(6):
                    if auto.click_element("./res/phone/mys/star_rail_text1.png",
                                          is_global=True) or auto.click_element(
                        "./res/phone/mys/star_rail_text2.png", is_global=True):
                        TimeUtils.wait_time(5)
                        if auto.click_element("./res/phone/mys/mys_like_icon.png", is_global=True):
                            TimeUtils.wait_time(5)
                            if auto.click_element("./res/phone/mys/mys_comment_icon.png",
                                                  is_global=True) or auto.click_element(
                                "./res/phone/mys/mys_comment_icon2.png", is_global=True):
                                TimeUtils.wait_time(5)
                                if j == 5:
                                    if auto.click_element("./res/phone/mys/share.png", is_global=True) or auto.click_element("./res/phone/mys/share2.png", is_global=True):
                                        TimeUtils.wait_time(2)
                                        if auto.click_element("./res/phone/mys/qq_icon.png", is_global=True):
                                            TimeUtils.wait_time(2)
                                            if auto.click_element("./res/phone/basics/cancel.png", is_global=True):
                                                TimeUtils.wait_time(2)
                                auto.mouse_right_click(self.center_x, self.center_y)
                                TimeUtils.wait_time(5)
                if auto.click_element("./res/phone/mys/star_rail_signin_icon.png", is_global=True):
                    TimeUtils.wait_time(5)
                    if auto.click_element("./res/phone/mys/star_rail_signin.png", is_global=True):
                        TimeUtils.wait_time(5)
                    auto.mouse_right_click(self.center_x, self.center_y)
            if auto.click_element("./res/phone/mys/me.png", is_global=True):
                TimeUtils.wait_time(2)
                if auto.click_element("./res/phone/mys/exchange.png", is_global=True):
                    TimeUtils.wait_time(2)
                    if auto.click_element("./res/phone/mys/gain.png", is_global=True):
                        TimeUtils.wait_time(2)
                        if auto.find_element("./res/phone/mys/gain2.png", is_global=True, is_save=True,
                                             screenshot_module="mys_gold"):
                            TimeUtils.wait_time(2)
        PhoneUtils.update_or_del_node("米游社", delete_key="星铁签到")
