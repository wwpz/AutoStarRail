import sys
import json
import time
from log import Log
from typing import Optional
from ruamel.yaml import YAML
from types import SimpleNamespace
from utils.singleton import SingletonMeta


class Config(metaclass=SingletonMeta):
    """
    配置管理类，用于加载、更新和保存配置信息
    """

    def __init__(self, version_path, example_path, config_path, log: Optional[Log] = None):
        self.yaml = YAML()
        self.version = self._load_version(version_path)
        self.config = self._load_default_config(example_path)
        self.config_path = config_path
        self._load_config()
        self.log = log

    def _load_version(self, version_path):
        """加载版本信息"""
        try:
            with open(version_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            sys.exit("版本文件未找到")

    def _update_config(self, config, new_config):
        """递归更新配置信息"""
        for key, value in new_config.items():
            if key in config:
                if isinstance(config[key], dict) and isinstance(value, dict):
                    self._update_config(config[key], value)
                else:
                    config[key] = value

    def _load_default_config(self, config_example_path):
        """加载默认配置信息"""
        try:
            with open(config_example_path, 'r', encoding='utf-8') as file:
                return self.yaml.load(file) or {}
        except FileNotFoundError:
            sys.exit("默认配置文件未找到")

    def _load_config(self, path=None):
        """加载用户配置信息，如未找到则保存默认配置"""
        path = path or self.config_path
        try:
            with open(path, 'r', encoding='utf-8') as file:
                loaded_config = self.yaml.load(file)
                if loaded_config:
                    # self.configuration.update(loaded_config)
                    self._update_config(self.config, loaded_config)
                    self.save_config()
        except FileNotFoundError:
            self.save_config()
        except Exception as e:
            print(f"配置文件 {path} 加载错误: {e}")

    def save_config(self):
        """保存配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            self.yaml.dump(self.config, file)

    def get_value(self, key, default=None):
        """获取配置项的值"""
        return self.config.get(key, default)

    def set_value(self, key, value):
        """设置配置项的值并保存"""
        self.config[key] = value
        self.save_config()

    def save_timestamp(self, key):
        """保存当前时间戳到指定的配置项"""
        self.set_value(key, time.time())

    def load_value_from_json(self, file_path, key):
        try:
            # 打开并读取 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # 获取指定键的值
            return data.get(key, None)
        except (FileNotFoundError, TypeError) as e:
            self.log.debug(f"Error accessing JSON data: {e}")
            return None

    def load_json_as_object(self, file_path, cipher):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取 JSON 数据
                data = json.load(file)
                decryData = {
                    cipher.decrypt(key): SimpleNamespace(
                        user_account=cipher.decrypt(value["user_account"]),
                        user_password=cipher.decrypt(value["user_password"]),
                        icon=value["icon"]
                    )
                    for key, value in data.items()
                }
                return decryData  # 直接返回字典
        except (FileNotFoundError, TypeError, json.JSONDecodeError) as e:
            self.log.debug(f"转换json对象失败: {e}")
            return None

    def __getattr__(self, attr):
        """允许通过属性访问配置项的值"""
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(f"'{type(self).__name__}' 对象没有属性 '{attr}'")
