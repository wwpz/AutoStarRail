import time
from config import cfg
from log import log
from automation import auto
from utils.time_utils import TimeUtils


def start():
    log.hr("开始运行登录账号", 0)
    if cfg.game_type in ["food_language", "1999"]:
        return login_simulator_game()
    else:
        print("星铁")
    log.hr("完成登录账号", 0)


def login_simulator_game():
    if cfg.game_type == "food_language":
        # 判断是否有进入游戏字样
        log.info("登录中...")
        TimeUtils.wait_time(10)
        if auto.find_element("./res/food_language/basics/game_home_login.png"):
            log.info("需要手动登录账号...")
            if auto.click_element("./res/food_language/basics/game_home_login_other.png"):
                TimeUtils.wait_time(1)
                if auto.click_element("./res/food_language/basics/game_home_login_agree.png"):
                    TimeUtils.wait_time(1)
                    if auto.click_element("./res/food_language/basics/game_home_login_logo.png"):
                        TimeUtils.wait_time(1)
                        if auto.click_element("./res/food_language/basics/game_home_login_account.png"):
                            account = cfg.get_value("user_account")
                            for number in account:
                                auto.press_key(number)
                            log.info(f'登录账号为 : {account}')
                            if auto.click_element("./res/food_language/basics/game_home_login_password.png"):
                                password = cfg.get_value("user_password")
                                for number in password:
                                    auto.press_key(number)
                                log.info(password)
                                if auto.click_element("./res/food_language/basics/game_home_login.png"):
                                    TimeUtils.wait_time(5)
        if auto.find_element("./res/food_language/basics/game_home_enter_game.png"):
            auto.click_element("./res/food_language/basics/game_home_agree_conditions.png")
            TimeUtils.wait_time(2)  # 防止卡顿等一会
            auto.click_element("./res/food_language/basics/game_home_enter_game.png")
            log.info("登录成功...")
            return True
    else:
        if auto.find_element("./res/1999/basics/login_tag.png"):
            TimeUtils.wait_time(5)
            if auto.find_element("./res/1999/basics/logout_button.png"):
                auto.mouse_click(500, 500)
                time.sleep(1)
                auto.mouse_click(500, 500)
                TimeUtils.wait_time(5)
                log.info("登录成功...")
        else:
            print("手动登录账号（暂时不确定）")