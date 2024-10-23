from PIL import Image
import pyautogui
import win32gui


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
    def take_screenshot(title):
        window = Screenshot.get_window(title)
        if window:
            left, top, width, height = Screenshot.get_window_region(window)
            # 截取整个窗口的截图
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot_pos = (left, top, width, height)
            return screenshot, screenshot_pos
        return False
