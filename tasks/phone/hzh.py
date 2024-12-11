from automation import auto
from datetime import datetime
from utils.base_utils import BaseUtils
from utils.time_utils import TimeUtil
from .phone_template import PhoneTemplate


class Hzh(PhoneTemplate):
    def run(self):
        BaseUtils.copy_to_clipboard("华住会")
        if auto.find_element("./res/phone/basics/home_search.png", is_global=True):
            auto.press_keys(['ctrl', 'v'])
        if auto.click_element("./res/phone/hzh/icon.png", is_global=True):
            TimeUtil.wait_time(10)
            if auto.click_element("./res/phone/hzh/close.png", is_global=True):
                self.log.info("关闭了广告")
                TimeUtil.wait_(1)
            if auto.click_element("./res/phone/hzh/signin_icon.png", is_global=True):
                TimeUtil.wait_time(5)
                if auto.click_element("./res/phone/hzh/signin_skip.png", is_global=True):
                    self.log.info("关闭了签到首页指导")
                    TimeUtil.wait_(1)
                if auto.click_element("./res/phone/hzh/signin.png", is_global=True):
                    TimeUtil.wait_(1)
                    if auto.click_element("./res/phone/hzh/signin_true.png", is_global=True, is_save=True):
                        today_date = datetime.now().strftime('%Y_%m_%d')
                        self.log.info(f"{today_date}----华住会签到成功")
