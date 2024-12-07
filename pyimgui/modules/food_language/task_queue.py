import imgui
from config import cfg

ui_state = {
    "file_path": "./res/config/task_queue.json",
    "task_queue": []
}


def render():
    ui_state["task_queue"] = cfg.load_existing_json_data(ui_state["file_path"])
    if not ui_state["task_queue"]:
        imgui.text("没有可用的任务。")
    else:
        # 定义一个递归函数来显示任务
        def display_tasks(task_dict, indent=""):
            if isinstance(task_dict, dict):  # 检查是否是字典
                for key, value in task_dict.items():
                    if isinstance(value, dict):  # 如果值是字典
                        # 检查字典中是否有任何值为 True
                        if any(v for v in value.values() if v):
                            imgui.text(f"{indent}{key}:")  # 打印当前键
                            display_tasks(value, indent + "  ")  # 递归调用并增加缩进
                    elif value:  # 如果值不是字典并且为 True
                        imgui.text(f"{indent}- {key}")  # 打印子键
            elif isinstance(task_dict, list):  # 检查是否是列表
                for item in task_dict:
                    display_tasks(item, indent)  # 对列表中的每个项递归调用

        # 调用递归函数来显示任务队列
        display_tasks(ui_state["task_queue"])
