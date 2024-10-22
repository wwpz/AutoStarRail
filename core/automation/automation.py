import cv2
import time
import math
import numpy as np

from .input import Input
from .screenshot import Screenshot
from typing import Optional
from core.log.log import Log
from utils.singleton import SingletonMeta
from utils.image_utils import ImageUtils


class Automation(metaclass=SingletonMeta):
    """
    自动化管理类，用于管理与游戏窗口相关的自动化操作。
    """

    def __init__(self, window_title, log: Optional[Log] = None):
        """
        :param window_title: 游戏窗口的标题。
        :param log: 用于记录日志的Logger对象，可选参数。
        """
        self.window_title = window_title
        self.log = log
        self.screenshot = None
        self._init_input()
        self.img_cache = {}

    def _init_input(self):
        """
        初始化输入处理器，将输入操作如点击、移动等绑定至实例变量。
        """
        self.input_handler = Input(self.log)
        self.mouse_click = self.input_handler.mouse_click
        self.mouse_down = self.input_handler.mouse_down
        self.mouse_up = self.input_handler.mouse_up
        self.mouse_move = self.input_handler.mouse_move
        self.mouse_scroll = self.input_handler.mouse_scroll
        self.press_key = self.input_handler.press_key
        self.secretly_press_key = self.input_handler.secretly_press_key
        self.press_mouse = self.input_handler.press_mouse

    def take_screenshot(self, crop=(0, 0, 1, 1)):
        """
        捕获游戏窗口的截图。
        :param crop: 截图的裁剪区域，格式为(x1, y1, x2, y2)，默认为全屏。
        :return: 成功时返回截图及其位置和缩放因子，失败时抛出异常。
        """
        start_time = time.time()
        while True:
            try:
                result = Screenshot.take_screenshot(self.window_title, crop=crop)
                if result:
                    self.screenshot, self.screenshot_pos, self.screenshot_scale_factor = result
                    return result
                else:
                    self.log.error("截图失败：没有找到游戏窗口")
            except Exception as e:
                self.log.error(f"截图失败：{e}")
            time.sleep(1)
            if time.time() - start_time > 60:
                raise RuntimeError("截图超时")

    def calculate_center_position(self, template, max_loc):
        """
        计算匹配位置的中心坐标。
        :param template: 模板图片。
        :param max_loc: 最佳匹配位置。
        :return: 匹配位置的中心坐标。
        """
        try:
            channels, width, height = template.shape[::-1]
        except ValueError:
            width, height = template.shape[::-1]
        center_x = int(max_loc[0] / self.screenshot_scale_factor) + int(width / (2 * self.screenshot_scale_factor))
        center_y = int(max_loc[1] / self.screenshot_scale_factor) + int(height / (2 * self.screenshot_scale_factor))
        return center_x, center_y

    def find_element(self, target, threshold=None, max_retries=1, take_screenshot=True):
        """
        查找元素，并返回中心点
        :param target: 图片路径
        :param threshold: 查找阈值，用于图像查找时的相似度匹配。
        :param max_retries: 最大重试次数。
        :param take_screenshot: 是否需要先截图。
        :return: 查找到的图像中心点位置（x,y）。
        """
        max_retries = 1 if not take_screenshot else max_retries
        for i in range(max_retries):
            if take_screenshot:
                # 捕获游戏窗口，判断是否在游戏窗口内进行截图
                screenshot_result = self.take_screenshot()
                if not screenshot_result:
                    continue  # 如果截图失败，则跳过本次循环

                try:
                    if target in self.img_cache:
                        mask = self.img_cache[target]['mask']
                        template = self.img_cache[target]['template']
                    else:
                        mask = ImageUtils.read_template_with_mask(target)  # 读取模板图片掩码
                        template = cv2.imread(target)  # 读取模板图片
                        self.img_cache[target] = {'mask': mask, 'template': template}
                    screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)  # 将截图转换为RGB
                    if mask is not None:
                        matchVal, matchLoc = ImageUtils.scale_and_match_template(screenshot, template, threshold, mask)  # 执行匹配模板
                    else:
                        matchVal, matchLoc = ImageUtils.scale_and_match_template(screenshot, template, threshold)  # 执行匹配模板

                    self.log.debug(f"目标图片：{target.replace('./assets/images/', '')} 相似度：{matchVal:.2f}")

                    # # 获取模板图像的宽度和高度
                    template_width = template.shape[1]
                    template_height = template.shape[0]

                    # 在输入图像上绘制矩形框
                    top_left = matchLoc
                    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

                    # 显示标记了匹配位置的图像
                    resized_img = cv2.resize(screenshot, (640, 480))
                    cv2.imshow('Matched Image', resized_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                    if mask is not None:
                        if not math.isinf(matchVal) and (threshold is None or matchVal <= threshold):
                            top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                            return top_left, bottom_right, matchVal
                    else:
                        if not math.isinf(matchVal) and (threshold is None or matchVal >= threshold):
                            top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                            return top_left, bottom_right, matchVal
                except Exception as e:
                    self.log.error(f"寻找图片出错：{e}")
            if i < max_retries - 1:
                time.sleep(1)  # 在重试前等待一定时间
        return None
