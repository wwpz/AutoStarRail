from automation import auto
from datetime import datetime
from utils.base_utils import BaseUtils
from utils.time_utils import TimeUtils
from tasks.phone.phone_template import PhoneTemplate


class Zfb(PhoneTemplate):
    def run(self):
        BaseUtils.copy_to_clipboard("支付宝")
        if auto.find_element("./res/phone/basics/home_search.png", is_global=True):
            auto.press_keys(['ctrl', 'v'])
            TimeUtils.wait_(1)
        if auto.click_element("./res/phone/zfb/icon.png", is_global=True):
            TimeUtils.wait_time(10)
            if auto.click_element("./res/phone/hzh/home_me.png", is_global=True):
                TimeUtils.wait_(1)
                if auto.click_element("./res/phone/hzh/zfb_member.png", is_global=True):
                    TimeUtils.wait_(1)
                    if auto.click_element("./res/phone/hzh/signin.png", is_global=True):
                        TimeUtils.wait_(1)
                        if auto.click_element("./res/phone/hzh/close.png", is_global=True):
                            TimeUtils.wait_(1)
                        for i in range(3):
                            auto.mouse_right_click(self.x, self.y)
                            TimeUtils.wait_(1)
