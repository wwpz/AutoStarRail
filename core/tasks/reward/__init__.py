
from .mail import Mail
from .signin import Signin
from core.log import log
from core.automation import auto

class Reward:

    def __init__(self):
        self.mail = Mail("邮件", "true")
        self.signin = Signin("签到", "true")

        self.reward_instances = {
            "mail": self.mail,
            "signin": self.signin,
        }

        self.reward_mapping = {
            "mail": "./res/food_language/reward/email/game_email.png",
            "signin": "./res/food_language/reward/signin/game_signin.png"
        }

    def check_and_collect_rewards(self):
        log.hr("开始领取奖励", 0)

        for reward_type, (image_path) in self.reward_mapping.items():
            if self._find_reward(image_path):
                self.reward_instances[reward_type].start()
            else:
                reward_name = self._get_reward_name(reward_type)
                log.info(f"未检测到{reward_name}奖励")

        log.hr("完成", 2)

    def check_and_collect_specific_reward(self, reward_type):
        reward_name = self._get_reward_name(reward_type)
        log.hr(f"开始领取{reward_name}奖励", 0)

        if reward_type in self.reward_mapping:
            image_path = self.reward_mapping[reward_type]
            if self._find_reward(image_path):
                self.reward_instances[reward_type].start()
            else:
                log.info(f"未检测到{reward_name}奖励")
        else:
            log.error(f"未知的奖励类型: {reward_type}")

        log.hr("完成", 2)

    def _get_reward_name(self, reward_type):
        instance = self.reward_instances.get(reward_type)
        return instance.name if instance else "未知"

    def _find_reward(self, image_path):
        return auto.find_element(image_path)

def start():
    # if not True:
    #     log.info("领取奖励未开启")
    #     return

    reward_manager = Reward()
    reward_manager.check_and_collect_rewards()


def start_specific(reward_type):
    # if not True:
    #     log.info("领取奖励未开启")
    #     return

    reward_manager = Reward()
    reward_manager.check_and_collect_specific_reward(reward_type)