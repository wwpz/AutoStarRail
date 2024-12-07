import imgui

ui_state = {
    "activity_state": False,
}

def render():
    expanded, visible = imgui.collapsing_header("战斗", None)
    if expanded:
        activity_button, ui_state["activity_state"] = imgui.checkbox("活动",
                                                                     ui_state["activity_state"])
