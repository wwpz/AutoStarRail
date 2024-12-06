import imgui
from config import cfg
from utils.AESCipher import AESCipher

ui_state = {
    "show_second_window": False,
    "input_example": "请输入账号...",
    "input_password_example": "请输入密码...",
    "user_account": '',
    "user_password": '',
    "icon_current": 0,
    "icon_items": ["请选择启动图标...", "startup_icon", "startup_icon_1", "startup_icon_2"],
    "file_path": "./res/config/user_info.json",
    "data": []
}

# 初始化解密器
cipher = AESCipher(cfg.aes_password, cfg.aes_salt)


# 更新数据
def update_data():
    parsed_data = cfg.load_existing_data(ui_state["file_path"])
    ui_state["data"] = [
        {
            "user_account": cipher.decrypt(value["user_account"]),
            "user_password": cipher.decrypt(value["user_password"]),
            "user_icon": cipher.decrypt(value["user_icon"])
        }
        for value in parsed_data.values()
    ]


def reset_ui_state():
    ui_state["user_account"] = ''
    ui_state["user_password"] = ''
    ui_state["show_second_window"] = False


# 初始数据加载
update_data()


def render(window, glfw):
    expanded, visible = imgui.collapsing_header("账号管理", None)
    if expanded:
        if imgui.begin_table("table", 4, imgui.TABLE_BORDERS | imgui.TABLE_RESIZABLE):
            # 表头
            imgui.table_setup_column("账号")
            imgui.table_setup_column("密码")
            imgui.table_setup_column("启动图标")
            imgui.table_headers_row()

            # 数据行
            for row in ui_state["data"]:
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(row["user_account"])

                imgui.table_set_column_index(1)
                imgui.text(row["user_password"])

                imgui.table_set_column_index(2)
                imgui.text(row["user_icon"])

                imgui.table_set_column_index(3)
                if imgui.button("删除"):
                    print("ok")

            imgui.end_table()

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
                imgui.dummy(0, 10)
                imgui.indent(20)
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
                changed, password_buffer = imgui.input_text_with_hint("##password",
                                                                      ui_state["input_password_example"],
                                                                      ui_state["user_password"], 256,
                                                                      flags=imgui.INPUT_TEXT_PASSWORD)
                if changed:
                    # 当用户输入发生变化时，处理输入的变化
                    ui_state["user_password"] = password_buffer
                imgui.unindent(99)

                # 间隔
                imgui.dummy(0, 10)
                imgui.text("绑定启动图标：")
                imgui.same_line()
                imgui.indent(99)
                clicked, ui_state["icon_current"] = imgui.combo(
                    "", ui_state["icon_current"], ui_state["icon_items"]
                )
                if clicked:
                    if ui_state["icon_current"] == 0:
                        print(ui_state["icon_current"])

                # 间隔
                imgui.dummy(0, 10)
                if imgui.button("添加"):
                    # 加密用户输入
                    encrypted_account = cipher.encrypt(ui_state["user_account"])
                    encrypted_password = cipher.encrypt(ui_state["user_password"])
                    encrypted_icon = cipher.encrypt(ui_state["icon_items"][ui_state["icon_current"]])

                    # 加载现有数据
                    existing_data = cfg.load_existing_data(ui_state["file_path"])

                    # 创建新条目
                    user_id = encrypted_account
                    new_entry = {
                        "user_account": encrypted_account,
                        "user_password": encrypted_password,
                        "user_icon": encrypted_icon
                    }
                    existing_data[user_id] = new_entry

                    # 保存新数据
                    cfg.save_json(ui_state["file_path"], existing_data)

                    # 重新加载和更新表格数据
                    update_data()

                    # 重置输入框
                    reset_ui_state()

                if not window.opened:
                    reset_ui_state()
