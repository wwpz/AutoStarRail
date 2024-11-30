import time

from core.automation import auto
from ..template import Template


class Activity(Template):
    def run(self):
        if self.game_type == "1999":
                    print("ok")
        elif self.game_type == "food_language":
            time.sleep(5)
            if auto.click_element("./res/food_language/reward/activity/game_activity.png"):
                if auto.click_element("./res/food_language/reward/activity/game_activity_4.png"):
                    if auto.click_element("./res/food_language/reward/activity/game_activity_reward.png"):
                        time.sleep(3)
                        if auto.click_element("./res/food_language/basics/game_blank_close.png"):
                            time.sleep(3)
                            if auto.click_element("./res/food_language/basics/game_close.png"):
                                time.sleep(3)