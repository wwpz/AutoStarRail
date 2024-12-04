import glfw

from log import log
from .pyimgui import PyImgui

py_imgui = PyImgui(log)


def start():
    log.hr("控制台窗口启动", 0)
    window = py_imgui.init_py_imgui()
    while not glfw.window_should_close(window):
        # 用户界面
        py_imgui.render_ui()
        # 渲染
        py_imgui.render()