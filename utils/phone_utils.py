from log import log
from config import cfg
from automation import auto
from utils.time_utils import TimeUtils
from utils.base_utils import BaseUtils

params = {
    "x": None,
    "y": None
}
ui_state = {
    "task": "手机签到",
    "task_key": "每日签到",
    "file_path": "./res/config/task_queue.json"
}


class PhoneUtils:

    @staticmethod
    def go_home():
        title = auto.window_title
        window_class = BaseUtils.get_window_class_from_title(title)
        center = BaseUtils.get_window_center(title)
        if center:
            params["x"], params["y"] = center
            log.debug(f"窗口 '{title}' 的中心点坐标: x={params["x"]}, y={params["y"]}")
        else:
            log.debug(f"未找到标题为 '{title}' 的窗口")

        for i in range(3):
            if BaseUtils.switch_to_game(window_class, title):
                auto.mouse_middle(params["x"], params["y"])
                TimeUtils.wait_(1)
            if auto.find_element("./res/phone/basics/home_setting.png"):
                log.debug("在首页")
                return center

    @staticmethod
    def open_search():
        auto.mouse_move(params["x"], params["y"] + 200)
        TimeUtils.wait_(1)
        auto.mouse_dragRel(0, -150, 0.1)
        TimeUtils.wait_(1)

    @staticmethod
    def clear_background():
        auto.mouse_move(params["x"], params["y"] + 430)
        TimeUtils.wait_(1)
        auto.mouse_dragRel(0, -900, 0.5)
        if auto.click_element("./res/phone/basics/clear.png", is_global=True):
            TimeUtils.wait_(2)
        else:
            auto.mouse_middle(params["x"], params["y"])

    @staticmethod
    def update_or_del_node(custom_key, new_values=None, delete_key=None):
        try:
            # 加载现有的数据
            existing_data = cfg.load_existing_json_data(ui_state['file_path'])

            # 确保 existing_data 字典中有正确的层级结构
            task = ui_state.get("task")
            task_key = ui_state.get("task_key")

            if task is None or task_key is None:
                raise ValueError("task 或 task_key 在 ui_state 中未定义")

            # 确保 task 和 task_key 的层级结构存在
            if task not in existing_data:
                existing_data[task] = {}
            if task_key not in existing_data[task]:
                existing_data[task][task_key] = {}

            # 获取或初始化自定义数据
            custom_data = existing_data[task][task_key]
            if custom_key not in custom_data:
                custom_data[custom_key] = {}

            # 删除指定的键
            if delete_key and delete_key in custom_data[custom_key]:
                del custom_data[custom_key][delete_key]

            # 更新自定义键下的值
            if new_values is not None:
                for key, value in new_values.items():
                    custom_data[custom_key][key] = value

            # 检查 custom_key 是否为空并删除
            if not custom_data[custom_key]:
                del custom_data[custom_key]

            # 检查 task_key 是否为空并删除
            if not existing_data[task][task_key]:
                del existing_data[task][task_key]

            # 检查 task 是否为空并删除
            if not existing_data[task]:
                del existing_data[task]

            # 将更新后的数据保存到文件
            cfg.save_json(ui_state['file_path'], existing_data)
        except Exception as e:
            print(f"更新节点时发生错误: {e}")
