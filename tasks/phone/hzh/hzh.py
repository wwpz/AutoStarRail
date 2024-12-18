from automation import auto
from datetime import datetime
from utils.base_utils import BaseUtils
from utils.phone_utils import PhoneUtils
from utils.time_utils import TimeUtils
from tasks.phone.phone_template import PhoneTemplate


class Hzh(PhoneTemplate):
    def run(self):
        BaseUtils.paste("华住会")
        if auto.click_element("./res/phone/hzh/icon.png", is_global=True):
            TimeUtils.wait_time(10)
            if auto.click_element("./res/phone/hzh/close.png", is_global=True):
                self.log.info("关闭了广告")
                TimeUtils.wait_(1)
            if auto.click_element("./res/phone/hzh/signin_icon.png", is_global=True) or auto.click_element(
                    "./res/phone/hzh/signin_icon2.png", is_global=True):
                TimeUtils.wait_time(5)
                if auto.click_element("./res/phone/hzh/signin_skip.png", is_global=True):
                    self.log.info("关闭了签到首页指导")
                    TimeUtils.wait_(1)
                if auto.click_element("./res/phone/hzh/signin.png", is_global=True) or auto.click_element(
                        "./res/phone/hzh/signin2.png", is_global=True):
                    TimeUtils.wait_time(5)
                    auto.mouse_move(self.center_x, self.bottom - 15)
                    auto.click_element("./res/phone/hzh/signed_close.png", is_global=True)
                    TimeUtils.wait_time(3)
                    if auto.click_element("./res/phone/hzh/signin_true.png", is_global=True,
                                          is_save=True) or auto.click_element("./res/phone/hzh/signed_in.png",
                                                                              is_global=True, is_save=True):
                        today_date = datetime.now().strftime('%Y_%m_%d')
                        self.log.info(f"{today_date}----华住会签到成功")
                    PhoneUtils.update_or_del_node("华住会", delete_key="华住会签到")