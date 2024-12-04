import os
import sys
import pyuac
import atexit
import game as game
import pyimgui as py_imgui


from log import log

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

# def run_simulator_start():
#     simulator_game.start()
#
# def run_reward_tasks():
#     reward.start()

def first_run():
    log.info("启动成功")
    input("按回车键关闭窗口. . .")
    sys.exit(0)


# def run_launcher():
#     launcher.start()


def main():

    # thread2 = threading.Thread(target=task, args=("线程2", 4))
    #
    # # 启动线程
    # thread1.start()
    # thread2.start()
    #
    # # 等待所有线程完成
    # thread1.join()
    # thread2.join()
    #
    # print("所有线程已完成")


    py_imgui.start()
    # launcher.start()
    # time.sleep(5)
    # reward.start()
    # launcher.stop(True)

# 程序结束时的处理器
def exit_handler():
    log.error(f"程序结束...")


if __name__ == "__main__":
    try:
        atexit.register(exit_handler)
        main()
    except KeyboardInterrupt:
        log.error("发生错误: 手动强制停止")
        # input("按回车键关闭窗口. . .")
        sys.exit(1)
    except Exception as e:
        log.error("发生错误 {error}".format(error=e))
        # notif.notify(cfg.notify_template['ErrorOccurred'].format(error=e))
        # input("按回车键关闭窗口. . .")
        sys.exit(1)
