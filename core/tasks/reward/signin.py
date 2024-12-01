import time

from core.automation import auto
from ..template import Template


class Signin(Template):
    def run(self):
        if self.game_type == "1999":
            print("1999")
        elif self.game_type == "food_language":
            if auto.click_element("./res/food_language/reward/signin/game_signin.png"):
                time.sleep(3)
                if auto.click_element("./res/food_language/basics/game_blank_close.png"):
                    time.sleep(3)
                    if auto.click_element("./res/food_language/reward/signin/game_signin_more.png"):
                        time.sleep(3)
                        auto.click_element("./res/food_language/reward/signin/game_signin_month.png")
                    auto.mouse_click(100, 100)
                    time.sleep(3)