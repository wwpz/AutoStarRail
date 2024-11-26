import time
from core.config import cfg
from core.log import log
from core.automation import auto


def start():
    log.hr("开始运行", 0)
    if cfg.game_type in ["food_language", "1999"]:
        login_simulator_game()
    else:
        print("星铁")
    log.hr("完成", 2)


def login_simulator_game():
    if cfg.game_type == "food_language":
        # 判断是否有进入游戏字样
        if auto.find_element("./res/food_language/basics/game_home_enter_game.png"):
            log.info("登录中...")
            auto.click_element("./res/food_language/basics/game_home_agree_conditions.png")
            time.sleep(2)  # 防止卡顿等一会
            auto.click_element("./res/food_language/basics/game_home_enter_game.png")
            log.info("登录成功...")
        else:
            log.info("需要手动登录账号...")
            # 判断是否需要登录账号,无则需要登录
            # 登录账号方式是否为账号密码登录,是则使用账号密码
    else:
        if auto.find_element("./res/1999/basics/login_tag.png"):
            time.sleep(5)
            if auto.find_element("./res/1999/basics/logout_button.png"):
                auto.mouse_click(500, 500)
                time.sleep(1)
                auto.mouse_click(500, 500)
                time.sleep(5)
                log.info("登录成功...")
        else:
            print("手动登录账号（暂时不确定）")
