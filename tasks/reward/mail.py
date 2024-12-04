import time

from automation import auto
from ..template import Template


class Mail(Template):
    def run(self):
        if self.game_type == "1999":
            if auto.click_element("./res/1999/reward/email/game_email.png"):
                if auto.click_element("./res/1999/reward/game_email_receive_reward.png"):
                    print("ok")
        elif self.game_type == "food_language":
            time.sleep(3)
            if auto.click_element("./res/food_language/reward/email/game_email.png"):
                time.sleep(3)
                if auto.click_element("./res/food_language/reward/email/game_email_receive_reward.png"):
                    time.sleep(3)
                    if auto.click_element("./res/food_language/basics/game_blank_close.png", is_save=True, screenshot_module="mail"):
                        time.sleep(3)
                        auto.click_element("./res/food_language/basics/game_close.png")
                        time.sleep(3)
