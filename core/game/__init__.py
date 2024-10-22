import time

from core.log import log
from .starRailGame import StarRailGame
from core.automation import auto

starrail = StarRailGame("E:\\MuMu Player 12\\shell\\MuMuPlayer.exe", "", "", 'UnityWndClass', log)


def start():
    log.hr("开始运行", 0)
    start_game()
    log.hr("完成", 2)


def start_game():
    MAX_RETRY = 3

    def wait_until(condition, timeout, period=1):
        """等待直到条件满足或超时"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if condition():
                return True
            time.sleep(period)
        return False

    def check_and_click_enter():
        # 点击进入
        if auto.find_element("./res/food_language/basics/1.png", 0.9):
            return True
        # 游戏热更新，需要确认重启
        # auto.click_element("./assets/images/zh_CN/base/confirm.png", "image", 0.9, take_screenshot=False)
        # 网络异常等问题，需要重新启动
        # auto.click_element("./assets/images/zh_CN/base/restart.png", "image", 0.9, take_screenshot=False)
        # 适配国际服，需要点击“开始游戏”
        # auto.click_element("./assets/images/screen/start_game.png", "image", 0.9, take_screenshot=False)
        # 适配B服，需要点击“登录”
        # auto.click_element("./assets/images/screen/bilibili_login.png", "image", 0.9, take_screenshot=False)
        # 适配用户协议和隐私政策更新提示，需要点击“同意”
        # auto.click_element("./assets/images/screen/agree_update.png", "image", 0.9, take_screenshot=False)
        # 登录过期
        # if auto.find_element("./assets/images/screen/account_and_password.png", "image", 0.9, take_screenshot=False):
        #     if load_acc_and_pwd(gamereg_uid()) != (None, None):
        #         log.info("检测到登录过期，尝试自动登录")
        #         auto_login()
        #     else:
        #         raise Exception("账号登录过期")
        return False

    for retry in range(MAX_RETRY):
        try:
            if not starrail.start_game():
                raise Exception("启动游戏失败")
            time.sleep(10)


            if not wait_until(lambda: check_and_click_enter(), 10):
                raise TimeoutError("获取当前界面超时")
            break  # 成功启动游戏，跳出重试循环
        except Exception as e:
            log.error(f"尝试启动游戏时发生错误：{e}")
            if retry == MAX_RETRY - 1:
                raise  # 如果是最后一次尝试，则重新抛出异常
