from core.log import log
from .starRailGame import StarRailGame

starrail = StarRailGame("E:\\MuMu Player 12\\shell\\MuMuPlayer.exe", "", "", 'UnityWndClass', log)


def start():
    log.hr("开始运行", 0)
    start_game()
    log.hr("完成", 2)


def start_game():
    MAX_RETRY = 3
    print("ok")
    for retry in range(MAX_RETRY):
        try:
            if not starrail.start_game():
                raise Exception("启动游戏失败")

            break  # 成功启动游戏，跳出重试循环
        except Exception as e:
            log.error(f"尝试启动游戏时发生错误：{e}")
            if retry == MAX_RETRY - 1:
                raise  # 如果是最后一次尝试，则重新抛出异常
