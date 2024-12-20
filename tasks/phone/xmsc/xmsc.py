import random
from automation import auto
from datetime import datetime
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils
from tasks.phone.phone_template import PhoneTemplate


class Xmsc(PhoneTemplate):
    def run(self):
        self.log.info("开始小米商城签到")
        BaseUtils.paste("小米商城")

        if not auto.click_element("./res/phone/xmsc/icon.png", is_global=True):
            self.log.error("未能找到小米商城图标")
            return

        TimeUtils.wait_time(15)

        if not auto.click_element("./res/phone/xmsc/home_me.png", is_global=True):
            self.log.error("未能进入小米商城个人主页")
            return

        TimeUtils.wait_time(5)

        if not auto.click_element("./res/phone/xmsc/gold.png", is_global=True):
            self.log.error("未能找到金币图标")
            return

        for attempt in range(3):
            if self.perform_signin():
                break

        self.log.info("小米商城签到完成")
        PhoneUtils.update_or_del_node("小米商城", delete_key="小米商城签到")

    def perform_signin(self):
        if auto.click_element("./res/phone/xmsc/go_signin.png", is_global=True):
            TimeUtils.wait_time(5)
            if auto.click_element("./res/phone/xmsc/signin.png", is_global=True):
                today_date = datetime.now().strftime('%Y_%m_%d')
                self.log.info(f"{today_date}----小米商城签到成功")
                TimeUtils.wait_time(3)
                return True
        return False

    def browse_items(self):
        if auto.click_element("./res/phone/xmsc/go_browse.png", is_global=True):
            for _ in range(3):
                auto.mouse_move(self.center_x, self.bottom - 50)
                random_float = random.uniform(250, 450)
                auto.mouse_dragRel(0, -random_float, 0.8)
                TimeUtils.wait_(2)

    def receive_award(self):
        if auto.click_element("./res/phone/xmsc/receive_award.png", is_global=True):
            TimeUtils.wait_(3)
