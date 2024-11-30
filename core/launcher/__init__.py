import sys
import time
from core.config import cfg
from core.log import log
from .game_launcher import GameLauncher
from core.automation import auto
from utils.time_utils import TimeUtil

launch = GameLauncher(cfg.game_path, cfg.game_process_name, cfg.game_type, cfg.window_name, cfg.window_class, log)


def start():
    log.hr("开始运行启动模拟器", 0)
    if launch.game_type in ["food_language", "1999"]:
        return launch_simulator_start()
    else:
        print("ok")
    log.hr("启动模拟器完成", 2)


def launch_simulator_start():
    MAX_RETRY = 3
    for retry in range(1, MAX_RETRY + 1):
        log.info(f"进行第 {retry} 次启动模拟器")
        try:
            # 切换到前台并启动游戏进程确保在前台或者启动
            if launch.switch_to_game():
                if check_simulator_init():
                    return True
            else:
                if not launch.start_game():
                    raise Exception("通过路径启动模拟器失败")
            TimeUtil.wait_time(40)
            if check_simulator_init():
                return True
        except Exception as e:
            log.error(f"尝试启动模拟器时发生错误：{e}")
            if retry == MAX_RETRY:
                return False


def launch_start():
    MAX_RETRY = 3
    for retry in range(1, MAX_RETRY + 1):
        log.info(f"进行第 {retry} 次启动模拟器")
        try:
            # 切换到前台并启动游戏进程确保在前台或者启动
            if not launch.switch_to_game():
                if not launch.start_game():
                    raise Exception("通过路径启动模拟器失败")
                TimeUtil.wait_time(40)
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


def check_starrail_init():
    print("星铁启动")
    return True


def check_simulator_init():
    # 检查启动模拟器时是否有广告、更新干扰
    log.info("全屏模拟器")
    auto.press_key("F11")
    time.sleep(2)
    launch.check_resolution_ratio(1920, 1080)
    if not auto.find_element("./res/food_language/basics/power_icon.png"):
        stop(True)
        log.error("未找到模拟器全屏标志,检查模拟器界面是否有干扰")
    else:
        log.info("全屏模拟器成功")
        log.info("检测是否有广告")
        auto.click_element("./res/food_language/basics/close_advertising.png")
        return True


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
        sys.exit(0)
