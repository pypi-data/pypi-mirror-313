from enum import Enum


class ActionType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    CLEAR = "clear"
    SUBMIT = "submit"
    SEND_KEYS = "send_keys"

    # 缺省事件
    NONE = "none"
