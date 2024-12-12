import imgui
from config import cfg

ui_state = {
    "file_path": "./res/config/task_queue.json",
    "task_queue": []
}

# 定义用于控制显示的键列表
control_keys = ["华住会", "米游社-星铁签到"]


def render():
    ui_state["task_queue"] = cfg.load_existing_json_data(ui_state["file_path"])

    # 预检查所有控制键的状态
    def all_controls_inactive(task_dict):
        if isinstance(task_dict, dict):
            for key, value in task_dict.items():
                if isinstance(value, dict):
                    # 如果找到任何控制键值为True，立即返回False
                    if any(value.get(k, False) for k in control_keys):
                        return False
                    # 递归检查子字典
                    if not all_controls_inactive(value):
                        return False
        return True

    if not ui_state["task_queue"] or all_controls_inactive(ui_state["task_queue"]):
        imgui.text("没有可用的任务。")
    else:
        # 定义一个递归函数来显示任务
        def display_tasks(task_dict, indent=""):
            if isinstance(task_dict, dict):
                for key, value in task_dict.items():
                    if isinstance(value, dict):
                        if all(k in value and not value[k] for k in control_keys):
                            continue
                        if any(v for v in value.values() if v):
                            imgui.text(f"{indent}{key}:")
                            display_tasks(value, indent + "  ")
                    elif value:
                        imgui.text(f"{indent}- {key}")
            elif isinstance(task_dict, list):
                for item in task_dict:
                    display_tasks(item, indent)

        # 调用递归函数来显示任务队列
        display_tasks(ui_state["task_queue"])
