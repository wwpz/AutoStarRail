from log import log
from automation import auto
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils


class Zfb:
    def __init__(self, name):
        self.name = name
        self.log = log
        self.x = None,
        self.y = None,
        self._has_run_once = False  # 初始化标志为 False

    def start(self, receive):
        left, top, right, bottom = BaseUtils.get_window_borders()
        self.x = (left + right) // 2
        self.y = (top + bottom) // 2
        log.hr(f"开始{receive}奖励", 0)
        if receive == "支付宝签到":
            self.signin()
        elif receive == "蚂蚁森林":
            self.mysl()
        elif receive == "蚂蚁庄园":
            self.myzy()
        elif receive == "芭芭农场":
            self.bbnc()
        log.hr(f"{receive}奖励完成", 0)

    def init(self):
        if auto.click_element("./res/phone/zfb/home_icon.png", is_global=True) or auto.click_element(
                "./res/phone/zfb/home_icon2.png", is_global=True):
            TimeUtils.wait_time(5)
        else:
            self.run_once()

    def run_once(self):
        # if not self._has_run_once:
        PhoneUtils.go_home()
        PhoneUtils.clear_background()
        PhoneUtils.open_search()
        BaseUtils.paste("支付宝")
        if auto.click_element("./res/phone/zfb/icon.png", is_global=True):
            TimeUtils.wait_time(10)
            # self._has_run_once = True  # 设置标志为 True，表示方法已经执行过

    def signin(self):
        self.init()
        if auto.click_element("./res/phone/zfb/zfb_home_me.png", is_global=True):
            TimeUtils.wait_(3)
            if auto.click_element("./res/phone/zfb/zfb_member.png", is_global=True):
                TimeUtils.wait_(3)
                auto.mysl_click_element(startX=0, startY=710, endX=2000, endY=760)
                if auto.click_element("./res/phone/zfb/zfb_all_receive.png", is_global=True):
                    TimeUtils.wait_time(5)
                if auto.click_element("./res/phone/zfb/zfb_signin.png", is_global=True):
                    TimeUtils.wait_(3)
                    # if auto.click_element("./res/phone/zfb/close.png", is_global=True):
                    #     TimeUtils.wait_(3)
                    for i in range(2):
                        auto.mouse_right_click(self.x, self.y)
                        TimeUtils.wait_(2)
        PhoneUtils.update_or_del_node("支付宝", delete_key="支付宝签到")

    def mysl(self):
        self.init()
        if auto.click_element("./res/phone/zfb/mysl.png", is_global=True):
            TimeUtils.wait_time(10)
            if auto.click_element("./res/phone/zfb/mysl_close.png", is_global=True) or auto.click_element(
                    "./res/phone/zfb/mysl_close2.png", is_global=True):
                TimeUtils.wait_(3)
            if auto.click_element("./res/phone/zfb/mysl_close2.png", is_global=True) or auto.click_element(
                    "./res/phone/zfb/mysl_close.png", is_global=True):
                TimeUtils.wait_(3)
            auto.mysl_click_element(startX=0, startY=200, endX=2000, endY=320)
            TimeUtils.wait_(3)
            while auto.click_element("./res/phone/zfb/mysl_find_power.png", is_global=True):
                TimeUtils.wait_(3)
                if auto.click_element("./res/phone/zfb/mysl_receive_award.png", is_global=True):
                    TimeUtils.wait_(3)
            if auto.click_element("./res/phone/zfb/mysl_back_to_home.png", is_global=True):
                TimeUtils.wait_time(10)
                auto.mysl_click_element(startX=0, startY=140, endX=2000, endY=280)
                if auto.click_element("./res/phone/zfb/mysl_reward.png", is_global=True):
                    TimeUtils.wait_(3)
                    if auto.click_element("./res/phone/zfb/mysl_receive.png", is_global=True):
                        TimeUtils.wait_(3)
                        if auto.click_element("./res/phone/zfb/mysl_receive_back.png", is_global=True):
                            TimeUtils.wait_(3)
            if auto.click_element("./res/phone/zfb/mysl_back.png", is_global=True):
                TimeUtils.wait_time(5)
        PhoneUtils.update_or_del_node("支付宝", delete_key="蚂蚁森林")

    def myzy(self):
        self.init()
        if auto.click_element("./res/phone/zfb/myzy.png", is_global=True):
            TimeUtils.wait_time(10)
        if auto.click_element("./res/phone/zfb/myzy_close.png", is_global=True) or auto.click_element(
                "./res/phone/zfb/myzy_close2.png", is_global=True):
            TimeUtils.wait_time(10)
        if auto.click_element("./res/phone/zfb/myzy_thief_chicken.png", is_global=True):
            TimeUtils.wait_time(3)
            if auto.click_element("./res/phone/zfb/myzy_drive_away.png", is_global=True):
                TimeUtils.wait_time(3)
        if auto.click_element("./res/phone/zfb/myzy_get_feed.png", is_global=True):
            TimeUtils.wait_time(3)
            if auto.click_element("./res/phone/zfb/myzy_get.png", is_global=True):
                TimeUtils.wait_time(3)
                if auto.click_element("./res/phone/zfb/myzy_get_feed_close.png", is_global=True):
                    TimeUtils.wait_time(3)
        if auto.click_element("./res/phone/zfb/myzy_find_chicken.png", is_global=True):
            TimeUtils.wait_(5)
            if auto.click_element("./res/phone/zfb/myzy_my_chicken.png", is_global=True):
                TimeUtils.wait_(5)
        if auto.click_element("./res/phone/zfb/myzy_feed.png", is_global=True):
            TimeUtils.wait_time(3)
        if auto.click_element("./res/phone/zfb/myzy_home.png", is_global=True):
            TimeUtils.wait_time(5)
            if auto.click_element("./res/phone/zfb/myzy_home_signin.png", is_global=True):
                TimeUtils.wait_time(5)
            if auto.click_element("./res/phone/zfb/myzy_home_back.png", is_global=True):
                TimeUtils.wait_time(5)
        if auto.click_element("./res/phone/zfb/myzy_back.png", is_global=True):
            TimeUtils.wait_time(3)
        PhoneUtils.update_or_del_node("支付宝", delete_key="蚂蚁庄园")

    def bbnc(self):
        self.init()
        if auto.click_element("./res/phone/zfb/bbnc.png", is_global=True):
            TimeUtils.wait_time(10)
            if auto.click_element("./res/phone/zfb/bbnc_get_apply_fertilizer.png", is_global=True):
                TimeUtils.wait_time(5)
                while auto.click_element("./res/phone/zfb/bbnc_apply_fertilizer_receive.png", is_global=True):
                    TimeUtils.wait_time(5)
                    if auto.click_element("./res/phone/zfb/bbnc_isee.png", is_global=True):
                        TimeUtils.wait_time(5)
                if auto.click_element("./res/phone/zfb/bbnc_apply_fertilizer_close.png", is_global=True):
                    TimeUtils.wait_time(5)
            if auto.click_element("./res/phone/zfb/bbnc_back.png", is_global=True):
                TimeUtils.wait_time(5)
        PhoneUtils.update_or_del_node("支付宝", delete_key="芭芭农场")