from core.config import cfg
from core.log import log
from core.launcher import GameLauncher
from core.automation import auto
from utils.time_utils import TimeUtil

launch = GameLauncher(cfg.game_path, cfg.game_process_name, cfg.game_type, cfg.window_name, cfg.window_class, log)
game_state = True

def start():
    log.hr("开始运行启动游戏", 0)
    if launch.game_type in ["food_language", "1999"]:
        return start_simulator_game()
    else:
        print("星铁")
    log.hr("完成启动游戏", 2)


def start_simulator_game():
    if launch.game_type == "food_language":
        # 点击启动游戏
        log.info("正在启动" + "食物语" + "中....")
        if auto.click_element("./res/food_language/basics/startup_icon.png"):
            TimeUtil.wait_time(40)
            # 在正常情况下,点击游戏进入会直接有修复和资源加载的字样,通过判断则知道是否进入游戏,否则进行其它判断
            # 游戏启动动画问题?是在检测到进入游戏后的x秒后点击画面两次跳过？还是进行12+ 图片判断点击？
            # 适配用户协议和隐私政策更新提示，需要点击“接受”
            # log.info("游戏是否有隐私政策更新？")
            # if launch.wait_until_retries(auto.click_element("./res/food_language/basics/accept_update.png"), 5, 5):
            #     log.info("启动游戏成功,已在游戏界面...隐私政策已点击接受")
            # log.info("游戏是否有热更新？")
            # 判断是否游戏热更新，需要确认重启
            # if launch.wait_until_retries(auto.click_element("./res/food_language/basics/confirm.png"), 5, 5):
            #     log.info("启动游戏成功,已在游戏界面...游戏需已点击确定更新")
            #     if launch.wait_until(auto.click_element("./res/food_language/basics/confirm_update.png"), 300):
            #         log.info("游戏更新成功,点击确认重启游戏中...")
            #         return True
            log.info("无其它干扰,跳过动画")
            auto.mouse_click(500, 500)
            TimeUtil.wait_time(1)
            auto.mouse_click(500, 500)
            TimeUtil.wait_time(15)
            if not launch.wait_until_retries(lambda: auto.click_element("./res/food_language/basics/game_close.png"), 10, 3):
                log.error("进入游戏后-主页公告栏未找到,请检查错误截图")
            else:
                return True
        else:
            log.error("没有找到游戏启动图标...请检查错误截图")
            return False
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