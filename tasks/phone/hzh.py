import time

from automation import auto
from ..template import Template


class Hzh(Template):
    def run(self):
        print("ok")
        time.sleep(3)
        print("完成")
        # if auto.click_element("./res/food_language/reward/email/game_email.png"):
        #     if auto.click_element("./res/food_language/reward/email/game_email_receive_reward.png"):
        #         if auto.click_element("./res/food_language/basics/game_blank_close.png"):
        #             time.sleep(3)
        #             auto.click_element("./res/food_language/basics/game_close.png")