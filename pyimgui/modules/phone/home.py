import imgui
from tasks_queue import TasksQueue
from tasks.phone.hzh import Hzh
from tasks.phone.mail import Mail

ui_state = {
    "activity_state": False,
    "activity_stat2": False,
}
tasks_queue = TasksQueue()
hzh_instance = Hzh("画质",True)  # 创建 Hzh 的实例
mail_instance = Mail("画质",True)  # 创建 Hzh 的实例

def render():

    activity_button, ui_state["activity_state"] = imgui.checkbox("sss",
                                                                 ui_state["activity_state"])
    if activity_button:
        print(ui_state["activity_state"])
        # 使用 lambda 函数将 Hzh.run 封装为可调用对象
        tasks_queue.add_task_fifo(lambda: hzh_instance.run())

    activity_button2, ui_state["activity_stat2"] = imgui.checkbox("额哦哦饿哦额",
                                                                 ui_state["activity_stat2"])
    if activity_button2:
        print(ui_state["activity_stat2"])
        # 使用 lambda 函数将 Hzh.run 封装为可调用对象
        tasks_queue.add_task_fifo(lambda: mail_instance.run())
