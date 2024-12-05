import os
from log import log
from config import cfg
from datetime import datetime
from automation import auto
from utils.time_utils import TimeUtil
from launcher import GameLauncher
from utils.AESCipher import AESCipher

launch = GameLauncher(cfg.game_path, cfg.game_process_name, cfg.game_type, cfg.window_name, cfg.window_class, log)
# 初始化解密器
cipher = AESCipher(cfg.aes_password, cfg.aes_salt)


def start():
    log.hr("开始运行启动游戏", 0)
    if launch.game_type in ["food_language", "1999"]:
        today_date = datetime.now().strftime('%Y_%m_%d')
        os.makedirs(f'./res/reward_images/{cfg.game_type}/{cfg.user_account}/{today_date}', exist_ok=True)
        return start_simulator_game()
    else:
        print("星铁")
    log.hr("完成启动游戏", 0)


def start_simulator_game():
    MAX_RETRY = 3
    for retry in range(1, MAX_RETRY + 1):
        log.info(f"进行第 {retry} 次启动游戏")
        if launch.game_type == "food_language":
            # 点击启动游戏
            log.info("正在启动" + "食物语" + "中....")
            json_object = cfg.load_json_as_object("./res/config/user_info.json", cipher)
            user = json_object.get(cfg.user_account)
            if user is None:
                return False
            if auto.click_element(f"./res/food_language/basics/{user.icon}.png"):
                TimeUtil.wait_time(15)
                # 适配用户协议和隐私政策更新提示，需要点击“接受”
                log.debug("是否需要同意游戏隐私政策?")
                if auto.click_element("./res/food_language/basics/accept_update.png"):
                    log.debug("同意了游戏隐私政策")
                TimeUtil.wait_time(25)
                log.debug("游戏是否有热更新?")
                # 判断是否游戏热更新，需要确认重启
                if auto.click_element("./res/food_language/basics/confirm.png"):
                    if launch.wait_until_retries(
                            lambda: auto.click_element("./res/food_language/basics/confirm_update.png"),
                            300, 3):
                        log.info("游戏更新成功,点击确认重启游戏中...")
                        TimeUtil.wait_time(40)
                log.info("无其它干扰,跳过动画")
                auto.mouse_click(500, 500)
                TimeUtil.wait_time(1)
                auto.mouse_click(500, 500)
                TimeUtil.wait_time(15)
                if not launch.wait_until_retries(
                        lambda: auto.click_element("./res/food_language/basics/game_close.png"),
                        10, 3):
                    log.error("进入游戏后-主页公告栏未找到,请检查错误截图")
                else:
                    return True
            else:
                log.error("没有找到游戏启动图标...请检查错误截图")
        else:
            log.info("正在启动" + "1999" + "中....")
            if auto.click_element("./res/1999/basics/startup_icon.png"):
                TimeUtil.wait_time(50)
                # log.debug("游戏第一次启动语音资源问题?")
                # if auto.find_element("./res/1999/basics/update_1.png"):
                #     auto.click_element("./res/1999/basics/next_button.png")
                # log.debug("检查到更新?")
                # if auto.find_element("./res/1999/basics/update_2.png"):
                #     time.sleep(3)
                #     auto.click_element("./res/1999/basics/download_button.png")
            return False
    else:
        # 如果for循环中没有break，意味着所有重试都失败，可以在这处理
        log.info("所有重试均未成功")
        return False
