import sys
import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer
# 保存表单状态的字典
form_state = {
    "username": "",
    "email": "",
    "password": "",
    "remember_me": False,
    "gender": 0,  # 0: Male, 1: Female, 2: Other
}

# 示例数据
data = [
    {"ID": 1, "Name": "Alice", "Age": 30},
    {"ID": 2, "Name": "Bob", "Age": 25},
    {"ID": 3, "Name": "Charlie", "Age": 35},
    {"ID": 4, "Name": "David", "Age": 40},
    {"ID": 5, "Name": "Eva", "Age": 22},
]

def main():
    # 初始化glfw
    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # 设置OpenGL版本
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # 创建窗口
    window = glfw.create_window(1280, 720, "ImGui with PyOpenGL", None, None)
    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    # 设置上下文
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    # 初始化imgui
    imgui.create_context()
    impl = GlfwRenderer(window)

    # 主循环
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # 开始新一帧
        imgui.new_frame()

        # 添加一个窗口
        imgui.begin("Hello, World!")
        imgui.text("This is a simple text inside the ImGui window.")

        # 创建用户名输入框
        changed, form_state["username"] = imgui.input_text(
            "Username", form_state["username"], 256
        )

        # 创建电子邮件输入框
        changed, form_state["email"] = imgui.input_text(
            "Email", form_state["email"], 256
        )

        # 创建密码输入框
        changed, form_state["password"] = imgui.input_text(
            "Password", form_state["password"], 256, imgui.INPUT_TEXT_PASSWORD
        )

        # 创建性别单选按钮
        imgui.text("Gender")
        imgui.radio_button("Male", form_state["gender"])
        imgui.same_line()
        imgui.radio_button("Female", form_state["gender"])
        imgui.same_line()
        imgui.radio_button("Other", form_state["gender"])

        # 创建“记住我”复选框
        changed, form_state["remember_me"] = imgui.checkbox(
            "Remember Me", form_state["remember_me"]
        )

        # 创建提交按钮
        if imgui.button("Submit"):
            # 当用户点击提交按钮时，处理表单数据
            print("Form Submitted")
            print("Username:", form_state["username"])
            print("Email:", form_state["email"])
            print("Password:", form_state["password"])
            print("Gender:", ["Male", "Female", "Other"][form_state["gender"]])
            print("Remember Me:", form_state["remember_me"])

        # 使用表格 API 创建一个展示表格
        if imgui.begin_table("table", 3, imgui.TABLE_BORDERS | imgui.TABLE_RESIZABLE):
            # 表头
            imgui.table_setup_column("ID")
            imgui.table_setup_column("Name")
            imgui.table_setup_column("Age")
            imgui.table_headers_row()

            # Data rows
            for row in data:
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(str(row["ID"]))

                imgui.table_set_column_index(1)
                imgui.text(row["Name"])

                imgui.table_set_column_index(2)
                imgui.text(str(row["Age"]))

            imgui.end_table()


        imgui.end()

        # 渲染
        glClearColor(0.1, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    # 结束
    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
