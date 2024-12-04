import imgui

ui_state = {
    "show_second_window": False,
    "input_example": "请输入账号...",
    "input_password_example": "请输入密码...",
    "user_account": '',
    "user_password": '',
}


def renderAccount(window, glfw):
    if imgui.button("添加账号"):
        ui_state["show_second_window"] = True
    if ui_state["show_second_window"]:
        # 获取 GLFW 窗口当前大小
        width, height = glfw.get_window_size(window)
        # 设置 ImGui 窗口与 GLFW 窗口相同大小，并贴近边缘
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        # 开始一个新的窗口
        with imgui.begin("添加账号", closable=True,
                         flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_ALWAYS_USE_WINDOW_PADDING) as window:
            imgui.text("账号/手机号：")
            imgui.same_line()
            # 创建一个输入框
            changed, user_buffer = imgui.input_text_with_hint("##input",
                                                              ui_state["input_example"],
                                                              ui_state["user_account"], 256)
            if changed:
                # 当用户输入发生变化时，处理输入的变化
                ui_state["user_account"] = user_buffer
            # 间隔
            imgui.dummy(0, 10)
            imgui.text("密码：")
            imgui.same_line()
            # 增加缩进
            imgui.indent(99)
            # 创建密码输入框
            changed, password_buffer = imgui.input_text_with_hint("##password", ui_state[
                "input_password_example"], ui_state["user_password"], 256,
                                                                  flags=imgui.INPUT_TEXT_PASSWORD)
            if changed:
                # 当用户输入发生变化时，处理输入的变化
                ui_state["user_password"] = password_buffer
            if not window.opened:
                ui_state["show_second_window"] = False
