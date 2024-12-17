from log import log
from automation import auto
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils


class Zfb:
    def __init__(self, name):
        self.name = name
        self.log = log
        self.x = 0,
        self.y = 0,
        self._has_run_once = False  # 初始化标志为 False

    def start(self, receive):
        log.hr(f"开始{receive}奖励", 0)
        if receive == "支付宝签到":
            self.signin()
        elif receive == "蚂蚁森林":
            self.mysl()
        log.hr(f"{receive}奖励完成", 0)

    def run_once(self):
        if not self._has_run_once:
            self.x, self.y = PhoneUtils.go_home()
            PhoneUtils.clear_background()
            PhoneUtils.open_search()
            BaseUtils.paste("支付宝")
            if auto.click_element("./res/phone/zfb/icon.png", is_global=True):
                TimeUtils.wait_time(10)
            self._has_run_once = True  # 设置标志为 True，表示方法已经执行过

    def signin(self):
        self.run_once()
        if auto.click_element("./res/phone/zfb/home_me.png", is_global=True):
            TimeUtils.wait_(3)
            if auto.click_element("./res/phone/zfb/zfb_member.png", is_global=True):
                TimeUtils.wait_(3)
                if auto.click_element("./res/phone/zfb/signin.png", is_global=True):
                    TimeUtils.wait_(3)
                    if auto.click_element("./res/phone/zfb/close.png", is_global=True):
                        TimeUtils.wait_(3)
                    for i in range(2):
                        auto.mouse_right_click(self.x, self.y)
                        TimeUtils.wait_(2)
        PhoneUtils.update_or_del_node("支付宝", delete_key="支付宝签到")

    def mysl(self):
        self.run_once()
        if auto.click_element("./res/phone/zfb/home_icon.png", is_global=True) or auto.click_element(
                "./res/phone/zfb/home_icon2.png", is_global=True):
            TimeUtils.wait_time(5)
            if auto.click_element("./res/phone/zfb/mysl.png", is_global=True):
                TimeUtils.wait_time(10)
                # if auto.click_element("./res/phone/zfb/mysl_close.png", is_global=True):
                #     TimeUtils.wait_(3)
                auto.mysl_click_element(startX=0, startY=140, endX=2000, endY=280)
                TimeUtils.wait_(3)
                while auto.click_element("./res/phone/zfb/mysl_find_power.png", is_global=True):
                    TimeUtils.wait_(3)
                    if auto.click_element("./res/phone/zfb/mysl_receive_award.png", is_global=True):
                        TimeUtils.wait_(3)
                if auto.click_element("./res/phone/zfb/back_to_home.png", is_global=True):
                    TimeUtils.wait_time(10)
                    if auto.click_element("./res/phone/zfb/reward.png", is_global=True):
                        TimeUtils.wait_(3)
                        # while auto.click_element("./res/phone/zfb/receive.png", is_global=True):
                        #     TimeUtils.wait_(3)
        PhoneUtils.update_or_del_node("支付宝", delete_key="蚂蚁森林")
