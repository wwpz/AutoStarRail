import pyautogui
import win32gui
import win32ui
import win32con
import cv2
import numpy as np


class Screenshot:
    @staticmethod
    def is_application_fullscreen(window):
        screen_width, screen_height = pyautogui.size()
        return (window.width, window.height) == (screen_width, screen_height)

    @staticmethod
    def get_window_real_resolution(window):
        left, top, right, bottom = win32gui.GetClientRect(window._hWnd)
        return right - left, bottom - top

    @staticmethod
    def get_window_region(window):
        if Screenshot.is_application_fullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            real_width, real_height = Screenshot.get_window_real_resolution(window)
            other_border = (window.width - real_width) // 2
            up_border = window.height - real_height - other_border
            return (window.left + other_border, window.top + up_border, window.width - other_border - other_border, window.height - up_border - other_border)

    @staticmethod
    def get_window(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window
        return False

    @staticmethod
    def get_window_hWnd(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window._hWnd  # 获取窗口句柄
        return False

    @staticmethod
    def take_screenshot(title):
        window = Screenshot.get_window(title)
        if window:
            left, top, width, height = Screenshot.get_window_region(window)
            # 截取整个窗口的截图
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot_pos = (left, top, width, height)
            return screenshot, screenshot_pos
        return False

    @staticmethod
    def take_back_screenshot(title):
        window = Screenshot.get_window_hWnd(title)
        # 获取窗口的设备上下文
        hwindc = win32gui.GetWindowDC(window)
        left, top, right, bot = win32gui.GetClientRect(window)
        width = right - left
        height = bot - top
        screenshot_pos = (left, top, width, height)

        # 创建一个内存设备上下文
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()

        # 创建一个位图对象
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)

        # 将窗口的内容拷贝到位图中
        memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

        # 获取位图信息
        bmp_info = bmp.GetInfo()
        bmp_str = bmp.GetBitmapBits(True)

        # 释放设备上下文
        memdc.DeleteDC()
        win32gui.ReleaseDC(window, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        # 将位图转换为OpenCV格式
        img = np.frombuffer(bmp_str, dtype='uint8')
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

        # 转换为BGR格式
        screenshot = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return screenshot, screenshot_pos, window