import imgui
from config import cfg

ui_state = {
    "file_path": "./res/config/task_queue.json",
    "task_queue": {},
    "cleared_once": False  # 新增标记用于记录是否已清空过
}

# 定义用于控制显示的键列表
control_keys = ["华住会", "米游社", "支付宝"]

def render():
    # 加载现有的任务队列数据
    ui_state["task_queue"] = cfg.load_existing_json_data(ui_state["file_path"])

    # 预检查所有控制键的状态
    def all_controls_inactive(task_dict):
        if isinstance(task_dict, dict):
            for task, task_value in task_dict.items():
                for task_key, task_key_value in task_value.items():
                    for control_key in control_keys:
                        if control_key in task_key_value:
                            # 检查 control_key 下所有的子项是否全为 False
                            if any(task_key_value[control_key].values()):
                                return False
        return True

    # 检查并显示文本信息
    if (not ui_state["task_queue"] or all_controls_inactive(ui_state["task_queue"])):
        if not ui_state["cleared_once"]:
            ui_state["task_queue"] = {}
            cfg.save_json(ui_state["file_path"], ui_state["task_queue"])
            ui_state["cleared_once"] = True  # 设置标记为已清空
        imgui.text("没有可用的任务。")
    else:
        # 如果 task_queue 中有内容且符合条件，则重置标记
        if ui_state["task_queue"]:
            ui_state["cleared_once"] = False

        # 定义一个递归函数来显示任务
        def display_tasks(task_dict, indent=""):
            if isinstance(task_dict, dict):
                for task, task_value in task_dict.items():
                    imgui.text(f"{indent}{task}:")  # 显示 task
                    for task_key, task_key_value in task_value.items():
                        imgui.text(f"{indent}  {task_key}:")  # 显示 task_key
                        for custom_key, custom_values in task_key_value.items():
                            # 如果所有控制键都为False，则跳过该 custom_key
                            if custom_key in control_keys and not any(custom_values.values()):
                                continue
                            if any(v for v in custom_values.values() if v):
                                imgui.text(f"{indent}    {custom_key}:")  # 显示 custom_key
                                for key, value in custom_values.items():
                                    if value:
                                        imgui.text(f"{indent}      - {key}")  # 显示 custom_key 的子项
            elif isinstance(task_dict, list):
                for item in task_dict:
                    display_tasks(item, indent)

        # 调用递归函数来显示任务队列
        display_tasks(ui_state["task_queue"])
