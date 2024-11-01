from core.automation import auto
from .template import Template


class Mail(Template):
    def run(self):
        if auto.click_element("./res/food_language/reward/email/game_email.png"):
            if auto.click_element("./res/food_language/reward/email/game_email_receive_reward.png"):
                if auto.click_element("./res/food_language/basics/game_blank_close.png"):
                    auto.click_element("./res/food_language/basics/game_close.png")