import imgui
from config import cfg
from tasks_queue import TasksQueue
from tasks.phone.hzh import Hzh

ui_state = {
    "task": "手机签到",
    "task_key": "每日签到",
    "mys_starRail_signin": False,
    "hzh_signin": cfg.get_value("hzh_signin"),
    "file_path": "./res/config/task_queue.json"
}
tasks_queue = TasksQueue()
hzh_instance = Hzh("华住会")  # 创建 Hzh 的实例

existing_data = cfg.load_existing_json_data(ui_state['file_path'])


def update_node(button_name, state):
    """
    更新 existing_data 中的状态。

    :param button_name: 按钮的名称
    :param state: 按钮的新状态
    """
    # 确保 existing_data 字典中有正确的层级结构
    if ui_state["task"] not in existing_data:
        existing_data[ui_state["task"]] = {}
    if ui_state["task_key"] not in existing_data[ui_state["task"]]:
        existing_data[ui_state["task"]][ui_state["task_key"]] = {}
    # 更新对应按钮的状态
    existing_data[ui_state["task"]][ui_state["task_key"]][button_name] = state
    cfg.save_json(ui_state['file_path'], existing_data)


# 读取配置文件数据,并初始化json
# def load_json_init():
#
#     # 如果数据为空，使用默认值
#     if not data or "食物语" not in data or "每日奖励" not in data["食物语"]:
#         ui_state["mail_state"] = False  # 默认值
#         ui_state["signin_state"] = False  # 默认值
#         ui_state["activity_state"] = False  # 默认值
#     else:
#         # 更新 ui_state 根据 JSON 数据
#         ui_state["mail_state"] = data["食物语"]["每日奖励"].get("邮件", False)
#         ui_state["signin_state"] = data["食物语"]["每日奖励"].get("签到", False)
#         ui_state["activity_state"] = data["食物语"]["每日奖励"].get("活动奖励四", False)


def render():
    hzh_button, ui_state["hzh_signin"] = imgui.checkbox("华住会-签到",
                                                        ui_state["hzh_signin"])
    if hzh_button:
        cfg.set_value("hzh_signin", ui_state["hzh_signin"])
        update_node("华住会", ui_state["hzh_signin"])
        if ui_state["hzh_signin"]:
            # 使用 lambda 函数将 Hzh.run 封装为可调用对象
            tasks_queue.add_task_fifo(lambda: hzh_instance.start(),"hzh_signin")
        else:
            print(tasks_queue.queue_len())
            tasks_queue.remove_task_fifo("hzh_signin")
            print(tasks_queue.queue_len())

    imgui.same_line()
    mys_starRail_button, ui_state["mys_starRail_signin"] = imgui.checkbox("米游社-星铁签到",
                                                                          ui_state["mys_starRail_signin"])
    if mys_starRail_button:
        cfg.set_value("mys_starRail_signin", ui_state["mys_starRail_signin"])
        update_node("米游社-星铁签到", ui_state["mys_starRail_signin"])
        # if ui_state["hzh_signin"]:
            # 使用 lambda 函数将 Hzh.run 封装为可调用对象
            # tasks_queue.add_task_fifo(lambda: hzh_instance.start())

    # imgui.same_line()
    # activity_button2, ui_state["mys_starRail_signin"] = imgui.checkbox("米游社-原神签到",
    #                                                                    ui_state["mys_starRail_signin"])
    # if ui_state["mys_starRail_signin"]:
    #     print(ui_state["mys_starRail_signin"])
    #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
    #     # tasks_queue.add_task_fifo(lambda: mail_instance.run())
    #
    # activity_button2, ui_state["mys_starRail_signin"] = imgui.checkbox("支付宝-签到",
    #                                                                    ui_state["mys_starRail_signin"])
    # if ui_state["mys_starRail_signin"]:
    #     print(ui_state["mys_starRail_signin"])
    #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
    #     # tasks_queue.add_task_fifo(lambda: mail_instance.run())
    #
    # imgui.same_line()
    # activity_button2, ui_state["mys_starRail_signin"] = imgui.checkbox("支付宝-蚂蚁森林",
    #                                                                    ui_state["mys_starRail_signin"])
    # if ui_state["mys_starRail_signin"]:
    #     print(ui_state["mys_starRail_signin"])
    #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
    #     # tasks_queue.add_task_fifo(lambda: mail_instance.run())
    #
    # imgui.same_line()
    # activity_button2, ui_state["mys_starRail_signin"] = imgui.checkbox("支付宝-蚂蚁庄园",
    #                                                                    ui_state["mys_starRail_signin"])
    # if ui_state["mys_starRail_signin"]:
    #     print(ui_state["mys_starRail_signin"])
    #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
    #     # tasks_queue.add_task_fifo(lambda: mail_instance.run())
    #
    # activity_button2, ui_state["mys_starRail_signin"] = imgui.checkbox("支付宝-芭芭农场",
    #                                                                    ui_state["mys_starRail_signin"])
    # if ui_state["mys_starRail_signin"]:
    #     print(ui_state["mys_starRail_signin"])
    #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
    #     # tasks_queue.add_task_fifo(lambda: mail_instance.run())
