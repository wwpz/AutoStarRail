import imgui
from config import cfg

ui_state = {
    "visible": False,
    "mail_state": False,
    "signin_state": False,
    "activity_state": False,
    "queue_priority": [1, 2, 3],
    "task": "food_language",
    "task_key": "daily_task",
    "file_path": "./res/config/task_queue.json"
}


def update_data():
    # 加载现有数据
    existing_data = cfg.load_existing_data(ui_state["file_path"])
    if existing_data and ui_state["task"] in existing_data and ui_state["task_key"] in existing_data[ui_state["task"]]:
        # 创建新条目
        new_entry = {
            "mail": ui_state["mail_state"],
            "signin": ui_state["signin_state"],
            "activity": ui_state["activity_state"]
        }
        existing_data[ui_state["task"]][ui_state["task_key"]] = new_entry
        cfg.save_json(ui_state["file_path"], existing_data)


def render():
    expanded, visible = imgui.collapsing_header("日常任务", None)
    if expanded:
        mail_button, ui_state["mail_state"] = imgui.checkbox("每日邮件", ui_state["mail_state"])
        if mail_button:
            update_data()
        imgui.same_line()
        signin_button, ui_state["signin_state"] = imgui.checkbox("签到奖励", ui_state["signin_state"])
        if signin_button:
            update_data()
        imgui.same_line()
        activity_button, ui_state["activity_state"] = imgui.checkbox("活动", ui_state["activity_state"])
        if activity_button:
            update_data()
