import cv2
import time
import math
import os
import numpy as np

import pygetwindow as gw
from config import cfg
from log.log import Log
from .input import Input
from typing import Optional
from datetime import datetime
from .screenshot import Screenshot
from utils.image_utils import ImageUtils
from utils.singleton import SingletonMeta


class Automation(metaclass=SingletonMeta):
    """
    自动化管理类，用于管理与游戏窗口相关的自动化操作。
    """

    def __init__(self, log: Optional[Log] = None):
        """
        :param log: 用于记录日志的Logger对象，可选参数。
        """
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
        self.mouse_right_click = self.input_handler.mouse_right_click
        self.mouse_down = self.input_handler.mouse_down
        self.mouse_up = self.input_handler.mouse_up
        self.mouse_move = self.input_handler.mouse_move
        self.mouse_scroll = self.input_handler.mouse_scroll
        self.mouse_middle = self.input_handler.mouse_middle
        self.mouse_dragRel = self.input_handler.mouse_dragRel
        self.press_key = self.input_handler.press_key
        self.secretly_press_key = self.input_handler.secretly_press_key
        self.press_mouse = self.input_handler.press_mouse
        self.press_keys = self.input_handler.press_keys

    def take_screenshot(self):
        """
        捕获游戏窗口的截图。
        :return: 成功时返回截图及其位置，失败时抛出异常。
        """
        start_time = time.time()
        while True:
            try:
                self.log.debug("正在捕获游戏窗口截图")
                result = Screenshot.take_screenshot(cfg.get_value("window_title"))
                # result = Screenshot.take_back_screenshot(cfg.get_value("window_title"))
                if result:
                    self.screenshot, self.screenshot_pos = result
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
        # 获取模板的宽度和高度
        width, height = template.shape[1], template.shape[0]

        # 计算中心坐标
        center_x = max_loc[0] + width // 2
        center_y = max_loc[1] + height // 2
        return center_x, center_y

    def convert_to_global(self, x, y):
        """
        将找到的中心坐标位置匹配为全局中心坐标。
        :param x: 模板图片。
        :param y: 最佳匹配位置。
        :return: 匹配位置的中心坐标。
        """
        window = gw.getWindowsWithTitle(cfg.get_value("window_title"))
        if window:
            win = window[0]
        else:
            raise Exception(f"Window with title '{cfg.get_value("window_title")}' not found.")
        return win.left + x, win.top + y

    def find_element(self, target, threshold=0.9, max_retries=2, take_screenshot=True, is_save=False,
                     screenshot_module=None, is_global=False):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        today_date = datetime.now().strftime('%Y_%m_%d')
        now_image_name = target.replace('./res/', '')
        self.log.debug(f"本次查找的图片路径为------：" + now_image_name)
        max_retries = 1 if not take_screenshot else max_retries
        for i in range(max_retries):
            if take_screenshot:
                # 捕获游戏窗口，判断是否在游戏窗口内进行截图
                screenshot_result = self.take_screenshot()
                if not screenshot_result:
                    self.log.info("截图失败")
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
                    # 测试时保存截图
                    base_name = target.replace("./res/", "").split('/')[0]
                    # 构建保存路径，包括基于时间戳的文件夹和文件名
                    save_path = os.path.join(self.log.save_dir, f'{base_name}_{timestamp}.jpg')

                    if is_save:
                        # 保存领取成功后的截图
                        self.log.debug(f"本次保存的奖励图片为------：" + screenshot_module)
                        if cfg.now_run_type in ["food_language","mys"]:
                            os.makedirs(f'./reward_images/{cfg.now_run_type}/{cfg.user_account}/{today_date}',
                                        exist_ok=True)
                            cv2.imwrite(os.path.join(f'./reward_images/{cfg.now_run_type}/{cfg.user_account}/{today_date}',
                                                     f'{screenshot_module}_{timestamp}.jpg'), screenshot)
                        else:
                            os.makedirs(f'./reward_images/{cfg.now_run_type}/{today_date}',exist_ok=True)
                            cv2.imwrite(os.path.join(f'./reward_images/{cfg.now_run_type}/{today_date}',
                                                     f'{screenshot_module}_{timestamp}.jpg'), screenshot)
                    # 使用 OpenCV 保存图像
                    cv2.imwrite(save_path, screenshot)
                    if mask is not None:
                        # 执行匹配模板
                        matchVal, matchLoc = ImageUtils.scale_and_match_template(screenshot, template, threshold, mask)
                    else:
                        # 执行匹配模板
                        matchVal, matchLoc = ImageUtils.scale_and_match_template(screenshot, template, threshold, None)
                    if matchVal > 0 and matchLoc != (-1, -1):
                        self.log.debug(f"目标图片：{target.replace('./res/', '')} 相似度：{matchVal:.2f}")

                    # # 获取模板图像的宽度和高度
                    # template_width = template.shape[1]
                    # template_height = template.shape[0]
                    #
                    # # 在输入图像上绘制矩形框
                    # top_left = matchLoc
                    # bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                    # cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                    #
                    # # 显示标记了匹配位置的图像
                    # resized_img = cv2.resize(screenshot, (640, 480))
                    # cv2.imshow('Matched Image', resized_img)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    if matchVal > 0 and matchLoc != (-1, -1):
                        if mask is not None:
                            if not math.isinf(matchVal) and (threshold is None or matchVal <= threshold):
                                if is_global:
                                    print("is_global1")
                                    top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                                    top_left, bottom_right = self.convert_to_global(top_left, bottom_right)
                                else:
                                    top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                                return top_left, bottom_right, matchVal
                        else:
                            if not math.isinf(matchVal) and (threshold is None or matchVal >= threshold):
                                if is_global:
                                    top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                                    top_left, bottom_right = self.convert_to_global(top_left, bottom_right)
                                else:
                                    top_left, bottom_right = self.calculate_center_position(template, matchLoc)
                                return top_left, bottom_right, matchVal
                except Exception as e:
                    self.log.debug(f"目标图片路径未找到------：{target.replace('./res/', '')}")
                    self.log.debug(f"寻找图片出错：{e}")
            if i < max_retries - 1:
                time.sleep(1)  # 在重试前等待一定时间
        return None

    def click_element_with_pos(self, coordinates, action="click"):
        """
        在指定坐标上执行点击操作。

        参数:
        :param coordinates: 元素的坐标。
        :param action: 执行的动作，包括'click', 'down', 'move'。

        返回:
        - 如果操作成功，则返回True；否则返回False。
        """
        x, y, matchVal = coordinates
        # 动作到方法的映射
        action_map = {
            "click": self.mouse_click,
            "down": self.mouse_down,
            "move": self.mouse_move,
            "middle": self.mouse_middle
        }

        if action in action_map:
            action_map[action](x, y)
        else:
            raise ValueError(f"未知的动作类型: {action}")

        return True

    def click_element(self, target, threshold=0.9, max_retries=2, action="click", is_save=False,
                      screenshot_module=None, is_global=False):
        """
        查找并点击屏幕上的元素。

        参数:
        :param target: 图片路径
        :param threshold: 查找阈值，用于图像查找时的相似度匹配。
        :param max_retries: 最大重试次数。
        :param action: 执行的动作。
        :param is_save: 是否保存当前截图。
        :param screenshot_module: 保存的图片模块。
        :param is_global: 是否全局中心坐标。

        返回:
        如果找到元素并点击成功，则返回True；否则返回False。
        """
        coordinates = self.find_element(target, threshold, max_retries, is_save=is_save,
                                        screenshot_module=screenshot_module, is_global=is_global)
        if coordinates:
            return self.click_element_with_pos(coordinates, action)
        return False

    def mysl_click_element(self, max_retries=2, startX=None, startY=None,
                           endX=None, endY=None):
        max_retries = 1 if not max_retries else max_retries
        for i in range(max_retries):
            # 捕获游戏窗口，判断是否在游戏窗口内进行截图
            screenshot_result = self.take_screenshot()
            if not screenshot_result:
                self.log.info("截图失败")
                continue  # 如果截图失败，则跳过本次循环
            try:
                # 将截取的屏幕区域转换为OpenCV图像格式
                image = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
                # 裁剪图像
                cropped_image = image[startY:endY, startX:endX]
                # 转换为灰度图像
                gray_cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                # 使用Canny边缘检测
                edges = cv2.Canny(gray_cropped_image, 100, 200)
                # 使用霍夫变换进行圆形检测
                circles = cv2.HoughCircles(
                    edges,
                    cv2.HOUGH_GRADIENT,
                    dp=1,
                    minDist=30,
                    param1=50,
                    param2=30,
                    minRadius=10,
                    maxRadius=50
                )
                # 如果检测到圆形，则返回坐标
                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")
                    for (x, y, r) in circles:
                        circle_center = (x, y)
                        if circle_center:
                            global_x, global_y = self.convert_to_global(x, y)
                            self.mouse_click(global_x, global_y + startY)
                            # 保存领取成功后的截图
                            # self.log.debug(f"本次保存的奖励图片为------：" + "蚂蚁森林领取能量")
                            # cv2.imwrite(
                            #     os.path.join(f'./res/reward_images/{cfg.game_type}/{cfg.user_account}/{today_date}',
                            #                  f'{screenshot_module}_{timestamp}.jpg'), screenshot)
                            time.sleep(3)
            except Exception as e:
                self.log.debug(f"寻找图片出错：{e}")
            if i < max_retries - 1:
                time.sleep(1)  # 在重试前等待一定时间
        return None
