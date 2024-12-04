import time

from automation import auto
from ..template import Template


class Activity(Template):
    def run(self):
        if self.game_type == "1999":
            print("ok")
        elif self.game_type == "food_language":
            time.sleep(2)
            if auto.click_element("./res/food_language/reward/activity/game_activity.png"):
                time.sleep(2)
                if auto.click_element("./res/food_language/reward/activity/game_activity_4.png"):
                    time.sleep(2)
                    if auto.click_element("./res/food_language/reward/activity/game_activity_reward.png"):
                        time.sleep(2)
                        if auto.click_element("./res/food_language/basics/game_blank_close.png", is_save=True, screenshot_module="activity"):
                            time.sleep(2)
                if auto.click_element("./res/food_language/basics/game_close.png"):
                    time.sleep(2)
