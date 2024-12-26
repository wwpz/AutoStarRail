from log import log
from config import cfg
from automation import auto
from utils.time_utils import TimeUtils
from utils.base_utils import BaseUtils

params = {
    "center_x ": None,
    "center_y": None,
    "left": None,
    "top": None,
    "right": None,
    "bottom": None,
}
ui_state = {
    "task": "手机签到",
    "task_key": "每日签到",
    "file_path": "./res/config/task_queue.json"
}


class PhoneUtils:

    @staticmethod
    def go_home():
        params["left"], params["top"], params["right"], params["bottom"] = BaseUtils.get_window_borders()
        params["center_x"] = params["left"] + (params["right"] - params["left"]) // 2
        params["center_y"] = params["top"] + (params["bottom"] - params["top"]) // 2
        title = cfg.get_value("window_title")
        window_class = BaseUtils.get_window_class_from_title(title)

        for i in range(3):
            if BaseUtils.switch_to_game(window_class, title):
                auto.mouse_middle(params["center_x"], params["center_y"])
                TimeUtils.wait_(1)
            if auto.find_element("./res/phone/basics/home_setting.png"):
                log.debug("在首页")
                break

    @staticmethod
    def clear_background():
        TimeUtils.wait_(1)
        auto.mouse_move(params["center_x"], params["bottom"] - 15)
        TimeUtils.wait_(1)
        auto.mouse_dragRel(0, -600, 0.8)
        if auto.click_element("./res/phone/basics/clear.png", is_global=True):
            TimeUtils.wait_(2)
        else:
            auto.mouse_middle(params["center_x"], params["center_y"])

    @staticmethod
    def open_search():
        if auto.click_element("./res/phone/basics/home_search.png", is_global=True):
            TimeUtils.wait_(1)

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
