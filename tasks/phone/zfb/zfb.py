from automation import auto
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils
from tasks.phone.phone_template import PhoneTemplate


class Zfb(PhoneTemplate):
    def run(self):
        BaseUtils.paste("支付宝")
        if auto.click_element("./res/phone/zfb/icon.png", is_global=True):
            TimeUtils.wait_time(10)
            if auto.click_element("./res/phone/zfb/home_me.png", is_global=True):
                TimeUtils.wait_(3)
                if auto.click_element("./res/phone/zfb/zfb_member.png", is_global=True):
                    TimeUtils.wait_(3)
                    if auto.click_element("./res/phone/zfb/signin.png", is_global=True):
                        TimeUtils.wait_(3)
                        if auto.click_element("./res/phone/zfb/close.png", is_global=True):
                            TimeUtils.wait_(3)
                        PhoneUtils.update_or_del_node("支付宝", delete_key="支付宝签到")
                        for i in range(2):
                            auto.mouse_right_click(self.x, self.y)
                            TimeUtils.wait_(2)
