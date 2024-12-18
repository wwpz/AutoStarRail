import random
from automation import auto
from datetime import datetime
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils
from tasks.phone.phone_template import PhoneTemplate


class Xmsc(PhoneTemplate):
    def run(self):
        BaseUtils.paste("小米商城")
        if auto.click_element("./res/phone/xmsc/icon.png", is_global=True):
            TimeUtils.wait_time(15)
            # if auto.click_element("./res/phone/hzh/close.png", is_global=True):
            #     self.log.info("关闭了广告")
            #     TimeUtils.wait_(1)
            if auto.click_element("./res/phone/xmsc/home_me.png", is_global=True):
                TimeUtils.wait_time(5)
                if auto.click_element("./res/phone/xmsc/gold.png", is_global=True):
                    TimeUtils.wait_(3)
                while auto.click_element("./res/phone/xmsc/go_signin.png", is_global=True):
                    TimeUtils.wait_time(5)
                    if auto.click_element("./res/phone/xmsc/signin.png", is_global=True):
                        today_date = datetime.now().strftime('%Y_%m_%d')
                        self.log.info(f"{today_date}----小米商城签到成功")
                        TimeUtils.wait_time(3)
                    if auto.click_element("./res/phone/xmsc/go_browse.png", is_global=True):
                        for i in range(3):
                            auto.mouse_move(self.center_x, self.bottom - 50)
                            random_float = random.uniform(250, 450)
                            auto.mouse_dragRel(0, random_float, 0.8)
                            TimeUtils.wait_(2)
                    if auto.click_element("./res/phone/xmsc/receive_award.png", is_global=True):
                        TimeUtils.wait_(3)
                PhoneUtils.update_or_del_node("小米商城", delete_key="小米商城签到")
