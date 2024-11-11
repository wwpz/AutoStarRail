import os
import sys
import time
import pyuac
import atexit
import core.game as game
import core.simulator_game as simulator_game
import core.launcher as launcher
import core.tasks.reward as reward

from core.log import log

# 将当前工作目录设置为程序所在的目录，确保无论从哪里执行，其工作目录都正确设置为程序本身的位置，避免路径错误。
os.chdir(
    os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

if not pyuac.isUserAdmin():
    try:
        pyuac.runAsAdmin(False)
        sys.exit(0)
    except Exception:
        sys.exit(1)


def run_main_actions():
    while True:
        game.start()

def run_simulator_start():
    simulator_game.start()

def run_reward_tasks():
    reward.start()

def first_run():
    log.info("启动成功")
    input("按回车键关闭窗口. . .")
    sys.exit(0)


def run_launcher():
    launcher.start()


def main(action=None):
    # first_run()

    # 完整运行
    if action is None or action == "main":
        run_launcher()
        time.sleep(5)
        run_reward_tasks()
        # launcher.stop(True)

    elif action == "simulator_start":
        run_simulator_start()

    elif action == "reward":
        run_reward_tasks()

    # 模拟器上的游戏完整运行
    elif action == "launcher":
        run_launcher()

    # 模拟器_1999
    elif action == "simulator_game_1999":
        run_reward_tasks()

    # 模拟器_食物语
    elif action == "simulator_game_food":
        run_reward_tasks()

    else:
        log.error(f"未知任务: {action}")
        input("按回车键关闭窗口. . .")
        sys.exit(1)


# 程序结束时的处理器
def exit_handler():
    log.error(f"程序结束...")


if __name__ == "__main__":
    try:
        atexit.register(exit_handler)
        main(sys.argv[1]) if len(sys.argv) > 1 else main()
    except KeyboardInterrupt:
        log.error("发生错误: 手动强制停止")
        input("按回车键关闭窗口. . .")
        sys.exit(1)
    except Exception as e:
        log.error("发生错误 {error}".format(error=e))
        # notif.notify(cfg.notify_template['ErrorOccurred'].format(error=e))
        input("按回车键关闭窗口. . .")
        sys.exit(1)
