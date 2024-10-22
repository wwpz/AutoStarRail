import subprocess
import pyautogui
import win32gui
import cv2
import numpy as np
from PIL import ImageGrab
import time
from core.automation.screenshot import Screenshot

print(pyautogui.getWindowsWithTitle("MuMu模拟器12"))


def take_screenshot(title, crop=(0, 0, 1, 1)):
    window = Screenshot.get_window(title)
    if window:
        left, top, width, height = Screenshot.get_window_region(window)

        screenshot = pyautogui.screenshot(region=(
            int(left + width * crop[0]),
            int(top + height * crop[1]),
            int(width * crop[2]),
            int(height * crop[3])
        ))

        real_width, _ = Screenshot.get_window_real_resolution(window)
        if real_width > 1920:
            screenshot_scale_factor = 1920 / real_width
            screenshot = screenshot.resize((int(1920 * crop[2]), int(1080 * crop[3])))
        else:
            screenshot_scale_factor = 1

        screenshot_pos = (
            int(left + width * crop[0]),
            int(top + height * crop[1]),
            int(width * crop[2] * screenshot_scale_factor),
            int(height * crop[3] * screenshot_scale_factor)
        )

        return screenshot, screenshot_pos, screenshot_scale_factor

    return False


if win32gui.IsWindow(67454) and win32gui.IsWindowVisible(67454):
    rect = win32gui.GetWindowRect(67454)
x1, y1, x2, y2 = rect
print(f"捕获的窗口矩形: ({x1}, {y1}, {x2}, {y2})")
time.sleep(3)
# while True:
#     img = ImageGrab.grab(bbox=rect)
#
#     screenshot = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)  # 将截图转换为RGB
#     resized_img = cv2.resize(screenshot, (640, 480))
#     cv2.imshow('Matched Image', resized_img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # 添加退出条件，按'q'键退出
#         break
screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)  # 将截图转换为RGB
result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
