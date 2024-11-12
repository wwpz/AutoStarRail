
from .mail import Mail
from .signin import Signin
from core.log import log
from core.automation import auto

class Reward:

    def __init__(self):
        self.game_type = None
        self.mail = Mail("邮件", "true","food_language")
        self.signin = Signin("签到", "true")

        self.reward_instances = {
            "mail": self.mail,
            "signin": self.signin,
        }

        self.reward_food_language_mapping = {
            "mail": "./res/food_language/reward/email/game_email.png",
            "signin": "./res/food_language/reward/signin/game_signin.png"
        }

        self.reward_1999_mapping = {
            "mail": "./res/1999/reward/email/game_email.png",
            "signin": "./res/1999/reward/signin/game_signin.png"
        }

    def check_and_collect_rewards(self):
        log.hr("开始领取奖励", 0)
        # 获取 game_type 的第一个参数
        if self.mail.game_type:  # 确保 game_type 不为空
            self.game_type = self.mail.game_type[0]
        else:
            self.game_type = None  # 如果为空，可以设置一个默认值或者处理逻辑

        if self.game_type == "1999":
            for reward_type, (image_path) in self.reward_1999_mapping.items():
                if self._find_reward(image_path):
                    self.reward_instances[reward_type].start()
                else:
                    reward_name = self._get_reward_name(reward_type)
                    log.info(f"未检测到{reward_name}奖励")
        elif self.game_type == "food_language":
            for reward_type, (image_path) in self.reward_food_language_mapping.items():
                if self._find_reward(image_path):
                    self.reward_instances[reward_type].start()
                else:
                    reward_name = self._get_reward_name(reward_type)
                    log.info(f"未检测到{reward_name}奖励")
        log.hr("完成", 2)

    def check_and_collect_specific_reward(self, reward_type):
        reward_name = self._get_reward_name(reward_type)
        log.hr(f"开始领取{reward_name}奖励", 0)
        if self.mail.game_type == "1999":
            if reward_type in self.reward_1999_mapping:
                image_path = self.reward_1999_mapping[reward_type]
                if self._find_reward(image_path):
                    self.reward_instances[reward_type].start()
                else:
                    log.info(f"未检测到{reward_name}奖励")
            else:
                log.error(f"未知的奖励类型: {reward_type}")
        elif self.mail.game_type == "food_language":
            if reward_type in self.reward_food_language_mapping:
                image_path = self.reward_food_language_mapping[reward_type]
                if self._find_reward(image_path):
                    self.reward_instances[reward_type].start()
                else:
                    log.info(f"未检测到{reward_name}奖励")
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