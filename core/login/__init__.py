import time
from core.config import cfg
from core.log import log
from core.automation import auto
from utils.time_utils import TimeUtil


def start():
    log.hr("开始运行登录账号", 0)
    if cfg.game_type in ["food_language", "1999"]:
        login_simulator_game()
    else:
        print("星铁")
    log.hr("完成登录账号", 0)


def login_simulator_game():
    if cfg.game_type == "food_language":
        # 判断是否有进入游戏字样
        log.info("登录中...")
        TimeUtil.wait_time(10)
        if auto.find_element("./res/food_language/basics/game_home_enter_game.png"):
            auto.click_element("./res/food_language/basics/game_home_agree_conditions.png")
            TimeUtil.wait_time(2)  # 防止卡顿等一会
            auto.click_element("./res/food_language/basics/game_home_enter_game.png")
            log.info("登录成功...")
        else:
            log.info("需要手动登录账号...")
            # 判断是否需要登录账号,无则需要登录
            # 登录账号方式是否为账号密码登录,是则使用账号密码
    else:
        if auto.find_element("./res/1999/basics/login_tag.png"):
            TimeUtil.wait_time(5)
            if auto.find_element("./res/1999/basics/logout_button.png"):
                auto.mouse_click(500, 500)
                time.sleep(1)
                auto.mouse_click(500, 500)
                TimeUtil.wait_time(5)
                log.info("登录成功...")
        else:
            print("手动登录账号（暂时不确定）")
log.info("登录启动流程完成")