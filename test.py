import subprocess
import pyautogui
import win32gui
import cv2
import numpy as np
import ctypes
from ctypes import windll
from PIL import ImageGrab
import time
from core.automation.screenshot import Screenshot
from core.automation import auto

# 获取桌面窗口句柄
hwndChildList = []
hd = win32gui.GetDesktopWindow()
win32gui.EnumChildWindows(hd, lambda hwnd, param: param.append(hwnd), hwndChildList)

# 遍历子窗口句柄列表，查找标题为"MuMu模拟器12"的窗口
target_hwnd = None
for hwnd in hwndChildList:
    title = win32gui.GetWindowText(hwnd)
    if title == "MuMu模拟器12":
        target_hwnd = hwnd
        break  # 找到后退出循环

# 检查是否找到目标窗口
if target_hwnd:
    # 获取窗口的类名
    window_class = win32gui.GetClassName(target_hwnd)
    # 获取窗口的标题（已经获取过，可以直接使用）
    window_name = win32gui.GetWindowText(target_hwnd)

    print(f"Window Handle: {target_hwnd}")
    print(f"Window Name: {window_name}")
    print(f"Window Class: {window_class}")
else:
    print("未找到标题为 'MuMu模拟器12' 的窗口")


def get_window_rect(hwnd):
    # 如果使用高 DPI 显示器（或 > 100% 缩放尺寸），添加下面一行，否则注释掉
    windll.user32.SetProcessDPIAware()
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        if rect[2] > rect[0] and rect[3] > rect[1]:  # 确保宽度和高度是正数
            return rect
    print("无法获取有效的窗口矩形或窗口不可见")
    return None


# 展示窗口
# rect = get_window_rect(target_hwnd)
# time.sleep(2)
# if rect is not None:
#     x1, y1, x2, y2 = rect
#     print(f"捕获的窗口矩形: ({x1}, {y1}, {x2}, {y2})")
#
#     # 找home
#     target = './res/food_language/basics/game_home_close.png'
#     template = cv2.imread(target)  # 读取模板图片
#     # 获取模板图像的宽度和高度
#     template_width = template.shape[1]
#     template_height = template.shape[0]
#
#     while True:
#         img = ImageGrab.grab(bbox=rect)
#
#         screenshot = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)  # 将截图转换为RGB
#         result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#         _, max_val, _, max_loc = cv2.minMaxLoc(result)
#         print(max_val)
#         if max_val > 0.9:
#             print("找打了")
#             # 将截图中的坐标转换为屏幕坐标
#             screen_x = rect[0] + max_loc[0]
#             screen_y = rect[1] + max_loc[1]
#             # 计算中心点在屏幕上的坐标
#             center_screen_x = screen_x + (template_width // 2)
#             center_screen_y = screen_y + (template_height // 2)
#             cv2.circle(screenshot, (center_screen_x, center_screen_y), 1, (0, 0, 255), -1)
#             # pyautogui.click(center_screen_x,center_screen_y)
#         top_left = max_loc
#         # 获取模板图像的宽度和高度
#         bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
#         cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
#
#         # 显示标记了匹配位置的图像
#         resized_img = cv2.resize(screenshot, (640, 480))
#
#         cv2.imshow('Matched Image', resized_img)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):  # 添加退出条件，按'q'键退出
#             break
#
#     cv2.destroyAllWindows()  # 销毁所有窗口
# else:
#     print("无法获取窗口矩形")

def set_foreground_window_with_retry(hwnd):
    """尝试将窗口设置为前台，失败时先最小化再恢复。"""

    def toggle_window_state(hwnd, minimize=False):
        """最小化或恢复窗口。"""
        state = 6 if minimize else 9
        ctypes.windll.user32.ShowWindow(hwnd, state)

    toggle_window_state(hwnd, minimize=False)
    if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
        toggle_window_state(hwnd, minimize=True)
        toggle_window_state(hwnd, minimize=False)
        if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
            raise Exception("设置窗口前景失败")


import psutil
import win32gui
import win32process
import os

def get_process_name_from_hwnd(hwnd):
    try:
        # 获取窗口句柄对应的进程ID
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        # 使用psutil获取进程信息
        process = psutil.Process(pid)
        return process.name()
    except Exception as e:
        print(f"Error: {e}")
        return None


# 示例用法
hwnd = target_hwnd  # 替换为你要查询的窗口句柄
process_name = get_process_name_from_hwnd(hwnd)

if process_name:
    print(f"Process name for HWND {hwnd}: {process_name}")
else:
    print(f"No process found for HWND {hwnd} or an error occurred.")


def terminate_named_process(target_process_name, termination_timeout=10):
    """
    根据进程名终止属于当前用户的进程。

    参数:
    - target_process_name (str): 要终止的进程名。
    - termination_timeout (int, optional): 终止进程前等待的超时时间（秒）。

    返回值:
    - bool: 如果成功终止进程则返回True，否则返回False。
    """
    system_username = os.getlogin()  # 获取当前系统用户名
    # 遍历所有运行中的进程
    for process in psutil.process_iter(attrs=["pid", "name"]):
        # 检查当前进程名是否匹配并属于当前用户
        if target_process_name in process.info["name"]:
            process_username = process.username().split("\\")[-1]  # 从进程所有者中提取用户名
            if system_username == process_username:
                proc_to_terminate = psutil.Process(process.info["pid"])
                proc_to_terminate.terminate()  # 尝试终止进程
                proc_to_terminate.wait(termination_timeout)  # 等待进程终止


def stop_game():
    """终止游戏"""
    try:
        # os.system(f'taskkill /f /im {self.process_name}')
        terminate_named_process("MuMuPlayer")
        print(f"游戏终止：MuMuPlayer")
        return True
    except Exception as e:
        print(f"终止游戏时发生错误：{e}")
        return False

stop_game()


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
        print(f"第 {attempt} 次尝试，共 {retries} 次")
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                if condition():
                    return True
            except Exception as e:
                print(f"等待中出现异常--忽略: {e}")
            time.sleep(period)
        return False

# set_foreground_window_with_retry(target_hwnd)
# time.sleep(2)
# auto.press_key("f11")
# def take_screenshot(title):
#     window = Screenshot.get_window(title)
#     if window:
#         left, top, width, height = Screenshot.get_window_region(window)
#         # 截取整个窗口的截图
#         screenshot = pyautogui.screenshot(region=(left, top, width, height))
#         screenshot_pos = (left, top, width, height)
#         return screenshot, screenshot_pos
#     return False
#
# time.sleep(5)
# screenshot,screenshot_pos = take_screenshot("MuMu模拟器12")
# print(take_screenshot("MuMu模拟器12"))
#
#
# # 显示标记了匹配位置的图像
# screenshot1 = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)  # 将截图转换为RGB
# resized_img = cv2.resize(screenshot1, (640, 480))
# cv2.imshow('Matched Image', resized_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def testPin():
    print("Ok")
    re

wait_until_retries(testPin,5,5)