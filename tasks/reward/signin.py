from automation import auto
from utils.time_utils import TimeUtils
from ..template import Template


class Signin(Template):
    def run(self):
        if self.game_type == "1999":
            print("1999")
        elif self.game_type == "food_language":
            TimeUtils.wait_(3)
            if auto.click_element("./res/food_language/reward/signin/game_signin.png"):
                TimeUtils.wait_(3)
                if auto.click_element("./res/food_language/basics/game_blank_close.png"):
                    TimeUtils.wait_(3)
                    if auto.click_element("./res/food_language/reward/signin/game_signin_more.png"):
                        TimeUtils.wait_(3)
                        auto.find_element("./res/food_language/reward/signin/game_signin_month.png", is_save=True, screenshot_module="signin")
                        TimeUtils.wait_(3)
                    auto.mouse_click(100, 100)
                    TimeUtils.wait_(3)
