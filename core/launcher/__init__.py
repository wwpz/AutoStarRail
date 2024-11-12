import os
import sys
import time

from core.log import log
from .game_launcher import GameLauncher
from core.automation import auto

launch = GameLauncher("E:\\MuMu Player 12\\shell\\MuMuPlayer.exe", "MuMuPlayer", "food_language", "MuMu模拟器12",
                      "Qt5156QWindowIcon",log)


def start():
    log.hr("开始运行", 0)
    launch_start()
    if launch.game_type in ["food_language", "1999"]:
        launcher_simulator_game()
    login_simulator_game()
    log.hr("完成", 2)


def launch_start():
    MAX_RETRY = 3

    for retry in range(1, MAX_RETRY + 1):
        log.info(f"进行第 {retry} 次启动模拟器")
        try:
            # 切换到前台并启动游戏进程确保在前台或者启动
            if not launch.switch_to_game():
                if not launch.start_game():
                    raise Exception("通过路径启动模拟器失败")
                time.sleep(40)
            # 检查是否进入模拟器主界面、是否有干扰
            if launch.game_type in ["food_language", "1999"]:
                check_simulator_init()
            else:
                check_starrail_init()
            break  # 成功启动游戏，跳出重试循环
        except Exception as e:
            log.error(f"尝试启动模拟器时发生错误：{e}")
            if retry == MAX_RETRY:
                raise  # 如果是最后一次尝试，则重新抛出异常


def launcher_simulator_game():
    if launch.game_type == "food_language":
        # 点击启动游戏
        log.info("正在启动" + "食物语" + "中....")
        if auto.click_element("./res/food_language/basics/startup_icon.png"):
            time.sleep(15)
            # 在正常情况下,点击游戏进入会直接有修复和资源加载的字样,通过判断则知道是否进入游戏,否则进行其它判断
            # 游戏启动动画问题?是在检测到进入游戏后的x秒后点击画面两次跳过？还是进行12+ 图片判断点击？
            # 适配用户协议和隐私政策更新提示，需要点击“接受”
            log.info("游戏是否有隐私政策更新？")
            if launch.wait_until_retries(auto.click_element("./res/food_language/basics/accept_update.png"), 5, 5):
                log.info("启动游戏成功,已在游戏界面...隐私政策已点击接受")
            log.info("游戏是否有热更新？")
            # 判断是否游戏热更新，需要确认重启
            if launch.wait_until_retries(auto.click_element("./res/food_language/basics/confirm.png"), 5, 5):
                log.info("启动游戏成功,已在游戏界面...游戏需已点击确定更新")
                if launch.wait_until(auto.click_element("./res/food_language/basics/confirm_update.png"), 300, 60):
                    log.info("游戏更新成功,点击确认重启游戏中...")
                    return True
            log.info("无其它干扰,跳过动画")
            auto.mouse_click(500, 500)
            time.sleep(1)
            auto.mouse_click(500, 500)
            time.sleep(5)
            if not launch.wait_until_retries(auto.click_element("./res/food_language/basics/game_close.png"), 5, 5, 2):
                log.error("进入游戏后-主页公告栏未找到,请检查错误截图")
        else:
            log.error("没有找到游戏启动图标...请检查错误截图")

        # 网络异常等问题，需要重新启动
        # auto.click_element("./assets/images/zh_CN/base/restart.png", "image", 0.9, take_screenshot=False)
        # 适配国际服，需要点击“开始游戏”
        # auto.click_element("./assets/images/screen/start_game.png", "image", 0.9, take_screenshot=False)
        # 适配B服，需要点击“登录”
        # auto.click_element("./assets/images/screen/bilibili_login.png", "image", 0.9, take_screenshot=False)
        # 登录过期
        # if auto.find_element("./assets/images/screen/account_and_password.png", "image", 0.9, take_screenshot=False):
        #     if load_acc_and_pwd(gamereg_uid()) != (None, None):
        #         log.info("检测到登录过期，尝试自动登录")
        #         auto_login()
        #     else:
        #         raise Exception("账号登录过期")
    else:
        log.info("正在启动" + "1999" + "中....")
        if auto.click_element("./res/1999/basics/startup_icon.png"):
            time.sleep(40)
                # log.debug("游戏第一次启动语音资源问题?")
                # if auto.find_element("./res/1999/basics/update_1.png"):
                #     auto.click_element("./res/1999/basics/next_button.png")
                # log.debug("检查到更新?")
                # if auto.find_element("./res/1999/basics/update_2.png"):
                #     time.sleep(3)
                #     auto.click_element("./res/1999/basics/download_button.png")
        return False


def login_simulator_game():
    if launch.game_type == "food_language":
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

def check_starrail_init():
    print("星铁启动")
    return True


def check_simulator_init():
    # 检查启动模拟器时是否有广告、更新干扰
    log.info("检查模拟器启动后是否进入主页面,是否有广告、更新按钮等干扰")
    log.info("尝试全屏模拟器")
    auto.press_key("F11")
    time.sleep(2)
    # 检测是否全屏
    launch.check_resolution_ratio(1920, 1080)
    if auto.find_element("./res/food_language/basics/power_icon.png"):
        log.info("全屏模拟器成功")
        log.info("检测是否有广告")
        if auto.click_element("./res/food_language/basics/close_advertising.png"):
            log.info("检测是否有更新")
            if auto.click_element("./res/food_language/basics/power_icon.png"):
                return True
    else:
        raise Exception("进入模拟器主界面失败、检查模拟器界面是否有干扰")


def stop(detect_loop=False):
    log.hr("停止运行", 0)

    if detect_loop and "cfg.after_finish" == "Loop":
        print("Loop")
        # after_finish_is_loop()
    else:
        if detect_loop:
            print("notify_after_finish_not_loop()")
        if "Exit" in ["Exit", "Loop", "Shutdown", "Hibernate", "Sleep", "Logoff"]:
            launch.shutdown("Exit")
        log.hr("完成", 2)
        if "Exit" not in ["Shutdown", "Hibernate", "Sleep", "Logoff"]:
            input("按回车键关闭窗口. . .")
        sys.exit(0)
