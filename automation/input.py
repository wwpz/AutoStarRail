import pyautogui
import time


class Input:
    # 禁用pyautogui的失败安全特性，防止意外中断
    pyautogui.FAILSAFE = False

    def __init__(self, logger):
        self.logger = logger  # 初始化日志记录器

    def mouse_click(self, x, y):
        '''在屏幕上的（x，y）位置执行鼠标点击操作'''
        try:
            pyautogui.click(x, y)
            self.logger.debug(f"鼠标点击 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"鼠标点击出错：{e}")

    def mouse_right_click(self, x, y):
        """在屏幕上的 (x, y) 位置执行鼠标右键点击操作"""
        try:
            pyautogui.click(x, y, button='right')
            self.logger.debug(f"鼠标右键点击 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"鼠标右键点击出错：{e}")

    def mouse_down(self, x, y):
        '''在屏幕上的（x，y）位置按下鼠标按钮'''
        try:
            pyautogui.mouseDown(x, y)
            self.logger.debug(f"鼠标按下 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"鼠标按下出错：{e}")

    def mouse_up(self):
        '''释放鼠标按钮'''
        try:
            pyautogui.mouseUp()
            self.logger.debug("鼠标释放")
        except Exception as e:
            self.logger.error(f"鼠标释放出错：{e}")

    def mouse_move(self, x, y):
        '''将鼠标光标移动到屏幕上的（x，y）位置'''
        try:
            pyautogui.moveTo(x, y, 1)
            self.logger.debug(f"鼠标移动 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"鼠标移动出错：{e}")

    def mouse_scroll(self, count, direction=-1, pause=True):
        '''滚动鼠标滚轮，方向和次数由参数指定'''
        for _ in range(count):
            pyautogui.scroll(direction, _pause=pause)
        self.logger.debug(f"滚轮滚动 {count * direction} 次")

    def mouse_middle(self, x, y):
        '''在屏幕上的（x，y）位置执行鼠标中键点击操作'''
        try:
            pyautogui.click(x, y, button='middle')
            self.logger.debug(f"鼠标中键点击 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"鼠标点击出错：{e}")

    def mouse_dragRel(self, x_offset, y_offset, duration=1):
        """
       在屏幕上滑动鼠标。
       :param x_offset: 水平方向滑动的像素距离（正值向右，负值向左）
       :param y_offset: 垂直方向滑动的像素距离（正值向下，负值向上）
       :param duration: 滑动的持续时间（秒）
        mouse_dragRel(300, 0, 1)  # 向右滑动300像素，持续1秒
        mouse_dragRel(-300, 0, 1)  # 向左滑动300像素，持续1秒
        mouse_dragRel(0, 300, 1)  # 向下滑动300像素，持续1秒
        mouse_dragRel(0, -300, 1)  # 向上滑动300像素，持续1秒
       """
        try:
            # 获取当前鼠标位置
            start_x, start_y = pyautogui.position()
            self.logger.debug(f"初始鼠标位置: ({start_x}, {start_y})")

            # 使用 dragRel 方法
            self.logger.debug(f"开始滑动鼠标：相对偏移 ({x_offset}, {y_offset})，持续时间：{duration} 秒")
            pyautogui.dragRel(x_offset, y_offset, duration=duration, button='left')

            # 获取结束位置
            end_x, end_y = pyautogui.position()
            self.logger.debug(f"滑动结束，鼠标结束位置：({end_x}, {end_y})")
        except Exception as e:
            self.logger.error(f"鼠标滑动出错：{e}")

    def press_key(self, key, wait_time=0.2):
        '''模拟键盘按键，可以指定按下的时间'''
        try:
            pyautogui.keyDown(key)
            time.sleep(wait_time)  # 等待指定的时间
            pyautogui.keyUp(key)
            self.logger.debug(f"键盘按下 {key}")
        except Exception as e:
            self.logger.error(f"键盘按下 {key} 出错：{e}")

    def press_keys(self, keys, wait_time=0.2):
        '''模拟键盘按键，可以指定按下的时间。如果是组合键，keys 应该是一个列表或元组。'''
        try:
            if isinstance(keys, (list, tuple)):
                # 使用 hotkey 方法同时按下和释放多个键
                pyautogui.hotkey(*keys)
                self.logger.debug(f"组合键按下 {'+'.join(keys)}")
            else:
                # 单个按键的情况
                pyautogui.keyDown(keys)
                time.sleep(wait_time)  # 等待指定的时间
                pyautogui.keyUp(keys)
                self.logger.debug(f"键盘按下 {keys}")
        except Exception as e:
            self.logger.error(f"键盘按下 {keys} 出错：{e}")

    def secretly_press_key(self, key, wait_time=0.2):
        '''(不输出具体键位)模拟键盘按键，可以指定按下的时间'''
        try:
            pyautogui.write
            pyautogui.keyDown(key)
            time.sleep(wait_time)  # 等待指定的时间
            pyautogui.keyUp(key)
            self.logger.debug("键盘按下 *")
        except Exception as e:
            self.logger.error(f"键盘按下 * 出错：{e}")

    def press_mouse(self, wait_time=0.2):
        '''模拟鼠标左键的点击操作，可以指定按下的时间'''
        try:
            pyautogui.mouseDown()
            time.sleep(wait_time)  # 等待指定的时间
            pyautogui.mouseUp()
            self.logger.debug("按下鼠标左键")
        except Exception as e:
            self.logger.error(f"按下鼠标左键出错：{e}")
