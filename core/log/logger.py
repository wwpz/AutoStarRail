import os
import logging
from datetime import datetime
from typing import Literal
import unicodedata
from utils.singleton import SingletonMeta

from .coloredformatter import ColoredFormatter
from .colorcodefilter import ColorCodeFilter


class Logger(metaclass=SingletonMeta):
    """
    日志管理类
    """

    def __init__(self, level="INFO"):
        self._level = level
        self._init_logger()
        self._initialized = True

    def _init_logger(self):
        """根据提供的日志级别初始化日志器及其配置。"""
        self._create_logger()
        self._create_logger_title()

    def _current_datetime(self):
        """获取当前日期，格式为YYYY-MM-DD."""
        return datetime.now().strftime("%Y-%m-%d")

    def _create_logger(self):
        """创建并配置日志器，包括控制台和文件输出."""
        self.logger = logging.getLogger('StarRailAuto')
        self.logger.propagate = False
        self.logger.setLevel(self._level)

        # 控制台日志
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # 文件日志
        self._ensure_log_directory_exists()
        file_handler = logging.FileHandler(f"./logs/{self._current_datetime()}.log", encoding="utf-8")
        file_formatter = ColorCodeFilter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def _create_logger_title(self):
        """创建专用于标题日志的日志器."""
        self.logger_title = logging.getLogger('StarRailAuto_title')
        self.logger_title.propagate = False
        self.logger_title.setLevel(self._level)

        # 控制台日志
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger_title.addHandler(console_handler)

        # 文件日志
        self._ensure_log_directory_exists()
        file_handler = logging.FileHandler(f"./logs/{self._current_datetime()}.log", encoding="utf-8")
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger_title.addHandler(file_handler)

    def _ensure_log_directory_exists(self):
        """确保日志目录存在，不存在则创建."""
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def info(self, message):
        """记录INFO级别的日志."""
        self.logger.info(message)

    def debug(self, message):
        """记录DEBUG级别的日志."""
        self.logger.debug(message)

    def warning(self, message):
        """记录WARNING级别的日志."""
        self.logger.warning(message)

    def error(self, message):
        """记录ERROR级别的日志."""
        self.logger.error(message)

    def critical(self, message):
        """记录CRITICAL级别的日志."""
        self.logger.critical(message)

    def hr(self, title, level: Literal[0, 1, 2] = 0, write=True):
        """
        格式化标题并打印或写入文件.

        level: 0
        +--------------------------+
        |       这是一个标题        |
        +--------------------------+

        level: 1
        ======= 这是一个标题 =======

        level: 2
        ------- 这是一个标题 -------     
        """
        try:
            separator_length = 115
            title_lines = title.split('\n')
            separator = '+' + '-' * separator_length + '+'
            title_length = self._custom_len(title)
            half_separator_left = (separator_length - title_length) // 2
            half_separator_right = separator_length - title_length - half_separator_left

            if level == 0:
                formatted_title_lines = []

                for line in title_lines:
                    title_length_ = self._custom_len(line)
                    half_separator_left_ = (separator_length - title_length_) // 2
                    half_separator_right_ = separator_length - title_length_ - half_separator_left_

                    formatted_title_line = '|' + ' ' * half_separator_left_ + line + ' ' * half_separator_right_ + '|'
                    formatted_title_lines.append(formatted_title_line)

                formatted_title = f"{separator}\n" + "\n".join(formatted_title_lines) + f"\n{separator}"
            elif level == 1:
                formatted_title = '=' * half_separator_left + ' ' + title + ' ' + '=' * half_separator_right
            elif level == 2:
                formatted_title = '-' * half_separator_left + ' ' + title + ' ' + '-' * half_separator_right
            self._print_title(formatted_title, write)
        except:
            pass

    def _custom_len(self, text):
        """
        计算字符串的自定义长度，考虑到某些字符可能占用更多的显示宽度。
        """
        return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in text)

    def _print_title(self, title, write):
        """打印标题."""
        if write:
            self.logger_title.info(title)
        else:
            print(title)
