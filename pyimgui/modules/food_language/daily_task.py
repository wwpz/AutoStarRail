import imgui
from config import cfg

ui_state = {
    "visible": False,
    "mail_state": False,
    "signin_state": False,
    "activity_state": False,
    "queue_priority": [1, 2, 3],
    "task": "食物语",
    "task_key": "每日奖励",
    "file_path": "./res/config/task_queue.json"
}


# 读取 JSON 数据并初始化 ui_state
def load_json_init():
    data = cfg.load_existing_json_data(ui_state["file_path"])
    # 如果数据为空，使用默认值
    if not data or "食物语" not in data or "每日奖励" not in data["食物语"]:
        ui_state["mail_state"] = False  # 默认值
        ui_state["signin_state"] = False  # 默认值
        ui_state["activity_state"] = False  # 默认值
    else:
        # 更新 ui_state 根据 JSON 数据
        ui_state["mail_state"] = data["食物语"]["每日奖励"].get("邮件", False)
        ui_state["signin_state"] = data["食物语"]["每日奖励"].get("签到", False)
        ui_state["activity_state"] = data["食物语"]["每日奖励"].get("活动奖励四", False)


def update_data():
    # 加载现有数据
    existing_data = cfg.load_existing_json_data(ui_state["file_path"])

    # 确保现有数据有效且符合预期结构
    if existing_data is None or ui_state["task"] not in existing_data:
        # 初始化默认值
        ui_state["mail_state"] = False
        ui_state["signin_state"] = False
        ui_state["activity_state"] = False

        # 初始化现有数据
        existing_data = {
            ui_state["task"]: {
                ui_state["task_key"]: {
                    "邮件": ui_state["mail_state"],
                    "签到": ui_state["signin_state"],
                    "活动奖励四": ui_state["activity_state"]
                }
            }
        }
    elif ui_state["task_key"] not in existing_data[ui_state["task"]]:
        # 如果任务键不存在，初始化该键
        existing_data[ui_state["task"]][ui_state["task_key"]] = {
            "邮件": ui_state["mail_state"],
            "签到": ui_state["signin_state"],
            "活动奖励四": ui_state["activity_state"]
        }
    else:
        # 如果一切正常，更新现有条目
        existing_data[ui_state["task"]][ui_state["task_key"]] = {
            "邮件": ui_state["mail_state"],
            "签到": ui_state["signin_state"],
            "活动奖励四": ui_state["activity_state"]
        }

    # 保存更新后的数据
    cfg.save_json(ui_state["file_path"], existing_data)


load_json_init()


def render():
    expanded, visible = imgui.collapsing_header("每日奖励", None)
    if expanded:
        mail_button, ui_state["mail_state"] = imgui.checkbox("邮件", ui_state["mail_state"])
        if mail_button:
            update_data()
        imgui.same_line()
        signin_button, ui_state["signin_state"] = imgui.checkbox("签到", ui_state["signin_state"])
        if signin_button:
            update_data()
        imgui.same_line()
        activity_button, ui_state["activity_state"] = imgui.checkbox("活动奖励四", ui_state["activity_state"])
        if activity_button:
            update_data()
