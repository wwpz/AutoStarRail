import imgui
from config import cfg
from tasks_queue import TasksQueue
from tasks.phone.hzh.hzh import Hzh
from tasks.phone.zfb.zfb import Zfb
from collections import OrderedDict

ui_state = {
    "task": "手机签到",
    "task_key": "每日签到",
    "hzh_signin": cfg.get_value("hzh_signin"),
    "mys_starRail_signin": cfg.get_value("mys_starRail_signin"),
    "mys_Genshin_signin": cfg.get_value("mys_Genshin_signin"),
    "zfb_signin": cfg.get_value("zfb_signin"),
    "zfb_mysl_signin": cfg.get_value("zfb_mysl_signin"),
    "file_path": "./res/config/task_queue.json"
}
tasks_queue = TasksQueue()
hzh_instance = Hzh("华住会")
zfb_instance = Zfb("支付宝")


def initialize_tasks():
    task_data = cfg.load_existing_json_data(ui_state["file_path"])
    # 递归遍历任务字典，查找并执行状态为 True 的任务
    def traverse_and_execute(task_dict):
        if isinstance(task_dict, dict):
            for key, value in task_dict.items():
                if isinstance(value, bool) and value is True:
                    # 直接执行任务，当状态为 True
                    execute_task(key)
                    print(key)
                elif isinstance(value, dict):
                    # 递归深入子字典
                    traverse_and_execute(value)
    # 开始遍历任务数据
    traverse_and_execute(task_data)


def execute_task(task_key):
    # 根据 task_key 执行不同的任务操作
    if task_key == "mys_starRail_signin":
        print("Executing mys_starRail_signin task...")
    elif task_key == "华住会签到":
        print("Executing hzh_signin task...")
        tasks_queue.add_task_fifo(lambda: hzh_instance.start(), "hzh_signin")
    elif task_key == "支付宝签到":
        print("Executing zfb_signin task...")
        tasks_queue.add_task_fifo(lambda: zfb_instance.start(), "zfb_signin")


def update_node(custom_key, new_values):
    existing_data = cfg.load_existing_json_data(ui_state['file_path'])
    """
    更新 existing_data 中的状态。

    :param custom_key: 自定义键
    :param new_values: 要更新的键值对字典
    """
    # 确保 existing_data 字典中有正确的层级结构
    if ui_state["task"] not in existing_data:
        existing_data[ui_state["task"]] = {}
    if ui_state["task_key"] not in existing_data[ui_state["task"]]:
        existing_data[ui_state["task"]][ui_state["task_key"]] = {}

    # 使用 OrderedDict 来维护顺序
    custom_data = existing_data[ui_state["task"]][ui_state["task_key"]]

    if custom_key not in custom_data:
        custom_data[custom_key] = OrderedDict()

    # 更新自定义键下的值
    for key, value in new_values.items():
        if key in custom_data[custom_key]:
            del custom_data[custom_key][key]  # 删除旧的条目，重新插入以保持顺序
        custom_data[custom_key][key] = value

    # 将更新后的数据保存到文件
    cfg.save_json(ui_state['file_path'], existing_data)


initialize_tasks()


def render():
    hzh_button, ui_state["hzh_signin"] = imgui.checkbox("华住会-签到",
                                                        ui_state["hzh_signin"])
    if hzh_button:
        cfg.set_value("hzh_signin", ui_state["hzh_signin"])
        # update_node("华住会", ui_state["hzh_signin"])
        update_node("华住会", {"华住会签到": ui_state["hzh_signin"]})
        if ui_state["hzh_signin"]:
            # 使用 lambda 函数将 Hzh.run 封装为可调用对象
            tasks_queue.add_task_fifo(lambda: hzh_instance.start(), "hzh_signin")
        else:
            tasks_queue.remove_task_fifo("hzh_signin")

    imgui.same_line()
    mys_starRail_button, ui_state["mys_starRail_signin"] = imgui.checkbox("米游社-星铁签到",
                                                                          ui_state["mys_starRail_signin"])
    if mys_starRail_button:
        cfg.set_value("mys_starRail_signin", ui_state["mys_starRail_signin"])
        update_node("米游社", {"星铁签到": ui_state["mys_starRail_signin"]})
        # update_node("米游社-星铁签到", ui_state["mys_starRail_signin"])
        # if ui_state["mys_starRail_signin"]:
        #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
        #     tasks_queue.add_task_fifo(lambda: hzh_instance.start(), "hzh_signin")
        # else:
        #     tasks_queue.remove_task_fifo("hzh_signin")

    imgui.same_line()
    mys_Genshin_button, ui_state["mys_Genshin_signin"] = imgui.checkbox("米游社-原神签到",
                                                                        ui_state["mys_Genshin_signin"])
    if mys_Genshin_button:
        cfg.set_value("mys_Genshin_signin", ui_state["mys_Genshin_signin"])
        update_node("米游社", {"原神签到": ui_state["mys_Genshin_signin"]})
        # update_node("米游社-原神签到", ui_state["mys_starRail_signin"])
        # if ui_state["mys_starRail_signin"]:
        #     # 使用 lambda 函数将 Hzh.run 封装为可调用对象
        #     tasks_queue.add_task_fifo(lambda: hzh_instance.start(), "hzh_signin")
        # else:
        #     tasks_queue.remove_task_fifo("hzh_signin")

    zfb_button, ui_state["zfb_signin"] = imgui.checkbox("支付宝-签到",
                                                        ui_state["zfb_signin"])
    if zfb_button:
        cfg.set_value("zfb_signin", ui_state["zfb_signin"])
        update_node("支付宝", {"支付宝签到": ui_state["zfb_signin"]})
        if ui_state["zfb_signin"]:
            tasks_queue.add_task_fifo(lambda: zfb_instance.start(), "zfb_signin")
        else:
            tasks_queue.remove_task_fifo("zfb_signin")

    zfb_mysl_button, ui_state["zfb_mysl_signin"] = imgui.checkbox("支付宝-蚂蚁森林",
                                                                  ui_state["zfb_mysl_signin"])
    if zfb_mysl_button:
        cfg.set_value("zfb_mysl_signin", ui_state["zfb_mysl_signin"])
        update_node("支付宝", {"蚂蚁森林": ui_state["zfb_mysl_signin"]})
        # if ui_state["zfb_signin"]:
        #     tasks_queue.add_task_fifo(lambda: zfb_instance.start(), "zfb_signin")
        # else:
        #     tasks_queue.remove_task_fifo("zfb_signin")

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
