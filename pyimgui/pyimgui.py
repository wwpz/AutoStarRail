import sys
import glfw
import imgui
import threading
from OpenGL.GL import *
from log import Log
from log import log
from config import cfg
from ctypes import windll
from typing import Optional
from utils.time_utils import TimeUtil
from imgui.integrations.glfw import GlfwRenderer
from utils.AESCipher import AESCipher
from .modules.food_language import account_mg as account
from .modules.food_language import daily_task as daily
from .modules.food_language import replica_task as replica
from .modules.food_language import multiple_mg as multiple
from .modules.food_language import task_queue as task
from .modules.phone import home as home
from tasks_queue import TasksQueue
import game as game
import login as login
import launcher as launcher
import tasks.reward as reward

ui_state = {
    "game_radio1": False,
    "game_radio2": False,
    "game_radio3": False,
    "opened_apps": False,
    "file_path": "./res/config/user_info.json"
}

# 初始化解密器
cipher = AESCipher(cfg.aes_password, cfg.aes_salt)
tasks_queue = TasksQueue()

def run_reward():
    user = cfg.load_json_decrypt_object(ui_state["file_path"], cipher)
    length = len(user)
    # 获取字典的键列表
    user_ids = list(user.keys())
    for i in range(length):
        user_id = user_ids[i]  # 通过索引获取用户 ID
        cfg.set_value("user_account", user_id)
        if launcher.start():
            log.info("模拟器启动流程完成")
            if game.start():
                log.info("游戏启动流程完成")
                if login.start():
                    log.info("登录启动流程完成")
                    TimeUtil.wait_time(10)
                    reward.start()
                    launcher.stop_game()


def run_phone_reward():
    print(tasks_queue.is_empty())
    # 处理任务
    if not tasks_queue.is_empty():
        tasks_queue.process_fifo_tasks()  # 现在会执行 Hzh.run()，但不会立即

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
        self.window = glfw.create_window(700, 500, "ImGui Transparent Overlay", None, None)
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
        global ui_state
        """渲染用户界面"""
        glfw.poll_events()
        self.impl.process_inputs()
        imgui.new_frame()

        # 获取 GLFW 窗口当前大小
        width, height = glfw.get_window_size(self.window)

        # 设置 ImGui 窗口与 GLFW 窗口相同大小，并贴近边缘
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Menu",
                    flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SCROLLBAR)
        # imgui.show_demo_window()
        with imgui.begin_child("LeftSide", 490, -18, True):
            with imgui.begin_tab_bar("TabBar"):
                with imgui.font(self.new_font):
                    with imgui.begin_main_menu_bar() as main_menu_bar:
                        if main_menu_bar.opened:
                            # first menu dropdown
                            with imgui.begin_menu('设置', True) as file_menu:
                                if file_menu.opened:
                                    # submenu
                                    with imgui.begin_menu('当前运行的', True) as open_recent_menu:
                                        if open_recent_menu.opened:
                                            imgui.menu_item('doc.txt', None, False, True)
                    # if imgui.begin_tab_item("游戏选项").selected:
                    #     changed1, ui_state["game_radio1"] = imgui.checkbox("重返未来:1999", ui_state["game_radio1"])
                    #     changed2, ui_state["game_radio2"] = imgui.checkbox("食物语", ui_state["game_radio2"])
                    #     changed3, ui_state["game_radio3"] = imgui.checkbox("崩坏:星穹铁道", ui_state["game_radio3"])
                    #     imgui.end_tab_item()
                    # if ui_state["game_radio1"]:
                    #     if imgui.begin_tab_item("重返未来:1999").selected:
                    #         imgui.text("1999-button...")
                    #         imgui.end_tab_item()
                    # if ui_state["game_radio2"]:
                    if imgui.begin_tab_item("食物语").selected:
                        opened_button, ui_state["opened_apps"] = imgui.checkbox("多开账户?", ui_state["opened_apps"])
                        imgui.same_line()
                        opened_button, ui_state["opened_apps"] = imgui.checkbox("需要登录?", ui_state["opened_apps"])
                        if ui_state["opened_apps"]:
                            multiple.render()
                        daily.render()
                        replica.render()
                        account.render(self.window, glfw)
                        imgui.end_tab_item()
                    if imgui.begin_tab_item("手机签到").selected:
                        home.render()
                        if imgui.button("ok"):
                            # 创建线程
                            thread = threading.Thread(target=run_phone_reward)
                            thread.start()
                        imgui.end_tab_item()
                    # if ui_state["game_radio3"]:
                    #     with imgui.begin_tab_item("崩坏:星穹铁道", opened=ui_state["game_radio3"]) as item3:
                    #         ui_state["game_radio3"] = item3.opened
                    #         if item3.selected:
                    #             imgui.text("Honkai: Star Rail-button...")
                    if imgui.begin_tab_item("日志").selected:
                        if imgui.button("测试"):
                            self.log.debug(
                                "为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：为了确保所有文本都使用加载的字体，你可以在每个需要显示中文的区域使用 with imgui.font(new_font):。例如：")
                        with imgui.begin_child("region", -1, -50, border=True):
                            for log_message in self.log.logs:
                                imgui.text_wrapped(log_message)
                            # 自动滚动到最底部
                            imgui.set_scroll_here_y(1.0)
                        imgui.end_tab_item()

        # 检查鼠标是否在 ImGui 窗口内
        # is_hovering = self.is_mouse_hovering()

        imgui.same_line()
        with imgui.begin_child("RightSide", -1, -18, True):
            with imgui.font(self.new_font):
                imgui.text("任务队列")
                # 分割线
                imgui.separator()
                task.render()
                if imgui.button("开始"):
                    # 创建线程
                    thread = threading.Thread(target=run_reward)
                    thread.start()
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
