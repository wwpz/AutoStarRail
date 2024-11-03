import time

from core.automation import auto
from .template import Template


class Signin(Template):
    def run(self):
        if auto.click_element("./res/food_language/reward/signin/game_signin.png"):
            time.sleep(3)
            if auto.click_element("./res/food_language/basics/game_blank_close.png"):
                time.sleep(3)
                auto.mouse_click(500,500)