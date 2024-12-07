import imgui

ui_state = {
    "opened_apps": False,
}

def render():
    expanded, visible = imgui.collapsing_header("多开管理", None)
    if expanded:
        opened_button, ui_state["opened_apps"] = imgui.checkbox("同步任务", ui_state["opened_apps"])
        if opened_button:
            print("ojk")
