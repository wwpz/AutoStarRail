
from .mail import Mail
from log import log
from automation import auto

class Phone:

    def __init__(self):
        self.hzh = Mail("华住会", "true", "hzh")
        # self.signin = Signin("签到", "true", "signin")

        self.phone_instances = {
            "hzh": self.hzh,
            # "signin": self.signin,
        }

        self.phone_mapping = {
            "mail": "./res/food_language/phone/email/game_email.png",
            # "signin": "./res/food_language/phone/signin/game_signin.png"
        }

    def check_and_collect_phones(self):
        log.hr("开始领取奖励", 0)

        for phone_type, (image_path) in self.phone_mapping.items():
            if self._find_phone(image_path):
                self.phone_instances[phone_type].start()
            else:
                phone_name = self._get_phone_name(phone_type)
                log.info(f"未检测到{phone_name}奖励")

        log.hr("完成", 2)

    def check_and_collect_specific_phone(self, phone_type):
        phone_name = self._get_phone_name(phone_type)
        log.hr(f"开始领取{phone_name}奖励", 0)

        if phone_type in self.phone_mapping:
            image_path = self.phone_mapping[phone_type]
            if self._find_phone(image_path):
                self.phone_instances[phone_type].start()
            else:
                log.info(f"未检测到{phone_name}奖励")
        else:
            log.error(f"未知的奖励类型: {phone_type}")

        log.hr("完成", 2)

    def _get_phone_name(self, phone_type):
        instance = self.phone_instances.get(phone_type)
        return instance.name if instance else "未知"

    def _find_phone(self, image_path):
        return auto.find_element(image_path)

def start():
    # if not True:
    #     log.info("领取奖励未开启")
    #     return

    phone_manager = phone()
    phone_manager.check_and_collect_phones()


def start_specific(phone_type):
    # if not True:
    #     log.info("领取奖励未开启")
    #     return

    phone_manager = phone()
    phone_manager.check_and_collect_specific_phone(phone_type)