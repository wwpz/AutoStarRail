import time
import psutil

from core.log import log
from .simulatorGame import SimulatorGame
from core.automation import auto

starrail = SimulatorGame("E:\\MuMu Player 12\\shell\\MuMuPlayer.exe", "MuMuPlayer","Simulator", "MuMu模拟器12", "Qt5156QWindowIcon",
                         log)


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

    def wait_until_retries(condition, timeout, period=1, retries=2):
        """
        等待直到条件满足或超时，最多重试retries次
        参数:
        condition: 函数，返回布尔值，表示条件是否满足
        timeout: 每次尝试的超时时间，单位为秒
        period: 每次检查条件之间的等待时间，单位为秒，默认为1秒
        retries: 最大重试次数，默认重试3次
        """
        for attempt in range(1, retries + 1):
            log.info(f"第 {attempt} 次尝试，共 {retries} 次")
            end_time = time.time() + timeout
            while time.time() < end_time:
                try:
                    if condition():
                        return True
                except Exception as e:
                    log.debug(f"等待中出现异常--忽略: {e}")
                time.sleep(period)
        return False

    def get_process_path(name):
        # 通过进程名获取运行路径
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if name in proc.info['name']:
                process = psutil.Process(proc.info['pid'])
                return process.exe()
        return None

    def check_init():
        # 检查启动模拟器时是否有广告、模拟器更新干扰
        log.info("检查模拟器启动后是否进入主页面,是否有广告、模拟器更新按钮干扰等")
        log.info("尝试全屏模拟器")
        auto.press_key("F11")
        time.sleep(2)
        # 检测是否全屏
        starrail.check_resolution_ratio(1920, 1080)
        if auto.click_element("./res/food_language/basics/power_icon.png"):
            log.info("全屏模拟器成功")
            if auto.click_element("./res/food_language/basics/close_advertising.png"):
                time.sleep(2)
            return True
        else:
            log.error("检查是否进入模拟器主界面、是否有干扰失败")
            raise Exception("检查是否进入模拟器主界面、是否有干扰失败")

    def check_and_click_enter():
        # 点击启动游戏
        log.info("正在启动" + "食物语" + "中....")
        if auto.click_element("./res/food_language/basics/startup_icon.png"):
            time.sleep(15)
            # 在正常情况下,点击游戏进入会直接有修复和资源加载的字样,通过判断则知道是否进入游戏,否则进行其它判断
            # 游戏启动动画问题?是在检测到进入游戏后的x秒后点击画面两次跳过？还是进行12+ 图片判断点击？
            # 适配用户协议和隐私政策更新提示，需要点击“接受”
            log.info("游戏是否有隐私政策更新？")
            if wait_until_retries(auto.click_element("./res/food_language/basics/accept_update.png"),5,5):
                log.info("启动游戏成功,已在游戏界面...隐私政策已点击接受")
            log.info("游戏是否有热更新？")
            # 判断是否游戏热更新，需要确认重启
            if wait_until_retries(auto.click_element("./res/food_language/basics/confirm.png"),5,5):
                log.info("启动游戏成功,已在游戏界面...游戏需已点击确定更新")
                if wait_until(auto.click_element("./res/food_language/basics/confirm_update.png"), 300, 60):
                    log.info("游戏更新成功,点击确认重启游戏中...")
                    return True
            log.info("无其它干扰,跳过动画")
            auto.mouse_click(500,500)
            time.sleep(1)
            auto.mouse_click(500, 500)
            time.sleep(5)
            if not wait_until_retries(auto.click_element("./res/food_language/basics/game_home_close.png"), 5,5,2):
                log.error("进入游戏后-主页公告栏未找到,请检查错误截图")
            auto_login()
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
        return False

    for retry in range(1, MAX_RETRY + 1):
        log.info(f"进行第 {retry} 次启动模拟器")
        try:
            if not starrail.switch_to_game():
                # 切换到前台并启动游戏进程确保在前台或者启动
                if not starrail.start_game():
                    raise Exception("通过路径启动模拟器失败")
                time.sleep(40)
                # 检查是否进入模拟器主界面、是否有干扰
                check_init()

                # 进入后进行游戏启动判断
                check_and_click_enter()

                # 启动游戏后有动画问题？

                # if not wait_until(lambda: , 600):
                #     raise TimeoutError("查找并点击进入按钮超时")
                # time.sleep(10)
                # auto.press_mouse()
            else:
                log.info("else")
                # starrail.check_resolution_ratio(1920, 1080)
                # if cfg.auto_set_game_path_enable:
                #     program_path = get_process_path(cfg.game_process_name)
                #     if program_path is not None and program_path != cfg.game_path:
                #         cfg.set_value("game_path", program_path)
                #         log.info(f"游戏路径更新成功：{program_path}")
                # time.sleep(1)
            #
            # if not wait_until(lambda: check_and_click_enter(), 10):
            #     raise TimeoutError("获取当前界面超时")

            break  # 成功启动游戏，跳出重试循环
        except Exception as e:
            log.error(f"尝试启动模拟器时发生错误：{e}")
            if retry == MAX_RETRY:
                raise  # 如果是最后一次尝试，则重新抛出异常

def auto_login():
    # 判断是否有进入游戏字样
    if auto.find_element("./res/food_language/basics/game_home_enter_game.png"):
        log.info("登录中...")
        auto.click_element("./res/food_language/basics/game_home_agree_conditions.png")
        time.sleep(2)   #防止卡顿等一会
        auto.click_element("./res/food_language/basics/game_home_enter_game.png")
        log.info("登录成功...")
    else:
        log.info("需要手动登录账号...")
        # 判断是否需要登录账号,无则需要登录
        # 登录账号方式是否为账号密码登录,是则使用账号密码

