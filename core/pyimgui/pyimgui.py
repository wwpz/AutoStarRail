import sys
import glfw
import imgui
import threading
from OpenGL.GL import *
from core.log import Log
from ctypes import windll
from typing import Optional
from core.config import cfg
from utils.time_utils import TimeUtil
from imgui.integrations.glfw import GlfwRenderer

import core.game as game
import core.login as login
import core.launcher as launcher
import core.tasks.reward as reward

#
game_radio1 = False
game_radio2 = False
game_radio3 = False
visible = None


def run_reward():
    if launcher.start():
        if game.start():
            login.start()
            TimeUtil.wait_time(5)
            reward.start()


class PyImgui:
    def __init__(self, log: Optional[Log] = None):
        self.log = log
        self.window = None
        self.impl = None
        self.hwnd = None
        self.ex_style = None
        self.new_font = None

    def init_glfw(self):
        """初始化 GLFW 并创建窗口"""
        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        # 创建无边框和透明的窗口
        # glfw.window_hint(glfw.FLOATING, True)  # 确保窗口总是最上层
        # glfw.window_hint(glfw.DECORATED, False)
        # glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)

        # 获取主显示器的尺寸
        # monitor = glfw.get_primary_monitor()
        # mode = glfw.get_video_mode(monitor)
        # width, height = mode.size.width, mode.size.height

        # 创建窗口
        self.window = glfw.create_window(500, 200, "ImGui Transparent Overlay", None, None)
        if not self.window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

    def init_imgui(self):
        """初始化 ImGui 并设置窗口句柄和扩展样式"""
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        io = imgui.get_io()
        self.new_font = io.fonts.add_font_from_file_ttf(
            "./res/ttf/simhei.ttf", 14, glyph_ranges=io.fonts.get_glyph_ranges_chinese_full()
        )
        self.impl.refresh_font_texture()

        # 获取窗口句柄
        self.hwnd = glfw.get_win32_window(self.window)

        # 初始设置为穿透
        # self.ex_style = windll.user32.GetWindowLongW(self.hwnd, -20)
        # windll.user32.SetWindowLongW(self.hwnd, -20, self.ex_style | 0x80000 | 0x20)

    def init_py_imgui(self):
        """初始化整个 PyImgui 环境"""
        try:
            self.init_glfw()
            self.init_imgui()
        except Exception as e:
            print(f"Initialization error: {e}")
            self.cleanup()
            sys.exit(1)
        return self.window

    def render_ui(self):
        global game_radio1, game_radio2, game_radio3, visible
        """渲染用户界面"""
        glfw.poll_events()
        self.impl.process_inputs()
        imgui.new_frame()

        # 获取 GLFW 窗口当前大小
        width, height = glfw.get_window_size(self.window)

        # 设置 ImGui 窗口与 GLFW 窗口相同大小，并贴近边缘
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Menu", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SCROLLBAR)

        # imgui.begin("Menu")
        if imgui.begin_tab_bar("TabBar"):
            with imgui.font(self.new_font):
                if imgui.begin_tab_item("Game-options").selected:
                    changed1, game_radio1 = imgui.checkbox("1999", game_radio1)
                    changed2, game_radio2 = imgui.checkbox("Food Language", game_radio2)
                    changed3, game_radio3 = imgui.checkbox("Honkai: Star Rail", game_radio3)
                    if changed1:
                        cfg.set_value("1999-button",game_radio1)
                    if changed2:
                        cfg.set_value("food_language-button", game_radio2)
                    if changed3:
                        cfg.set_value("Honkai: Star Rail", game_radio3)
                    if imgui.button("Start"):
                        # 创建线程
                        thread = threading.Thread(target=run_reward)
                        thread.start()
                    imgui.end_tab_item()

                if imgui.begin_tab_item("日志").selected:
                    if imgui.button("测试"):
                        self.log.debug("为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：")
                    with imgui.begin_child("region", -1, -50, border=True):
                        for log_message in self.log.logs:
                            imgui.text_wrapped(log_message)
                        # 自动滚动到最底部
                        imgui.set_scroll_here_y(1.0)
                    imgui.end_tab_item()
                if game_radio1:
                    if imgui.begin_tab_item("1999-options").selected:
                        imgui.text("1999-button...")
                        imgui.end_tab_item()
                if game_radio2:
                    if imgui.begin_tab_item("Food Language-options").selected:
                        expanded, visible = imgui.collapsing_header("Expand me!", None)
                        if expanded:
                            imgui.button("Now you see me!")
                            imgui.button("Now you see me!")
                            imgui.button("Now you see me!")
                            imgui.button("Now you see me!")
                            imgui.button("Now you see me!")
                        imgui.end_tab_item()
                if game_radio3:
                    with imgui.begin_tab_item("Honkai: Star Rail-options", opened=game_radio3) as item3:
                        game_radio3 = item3.opened
                        if item3.selected:
                            imgui.text("Honkai: Star Rail-button...")

                imgui.end_tab_bar()

        # 检查鼠标是否在 ImGui 窗口内
        # is_hovering = self.is_mouse_hovering()

        # if imgui.button("Start"):
        #     # 创建线程
        #     thread = threading.Thread(target=run_reward)
        #     thread.start()
        # imgui.same_line()
        # if imgui.button("Exit"):
        #     glfw.set_window_should_close(self.window, True)
        imgui.end()

        # self.adjust_window_penetration(is_hovering)

    def render(self):
        """执行 OpenGL 渲染"""
        glClearColor(0.0, 0.0, 0.0, 0.0)  # 全透明背景
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)

    def adjust_window_penetration(self, is_hovering):
        """调整窗口穿透属性"""
        if is_hovering:
            self.focus_window()
            windll.user32.SetWindowLongW(self.hwnd, -20, self.ex_style & ~0x20 & ~0x80000)
        else:
            windll.user32.SetWindowLongW(self.hwnd, -20, self.ex_style | 0x80000 | 0x20)

    def is_mouse_hovering(self):
        """判断鼠标是否悬停在窗口内"""
        window_pos = imgui.get_window_position()
        window_size = imgui.get_window_size()
        mouse_x, mouse_y = glfw.get_cursor_pos(self.window)

        return (window_pos.x <= mouse_x <= window_pos.x + window_size.x) and \
            (window_pos.y <= mouse_y <= window_pos.y + window_size.y)

    def focus_window(self):
        """将窗口设置为前景"""
        windll.user32.SetForegroundWindow(self.hwnd)

    def cleanup(self):
        """清理资源"""
        if self.impl:
            self.impl.shutdown()
        glfw.terminate()

    def __enter__(self):
        self.init_py_imgui()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
