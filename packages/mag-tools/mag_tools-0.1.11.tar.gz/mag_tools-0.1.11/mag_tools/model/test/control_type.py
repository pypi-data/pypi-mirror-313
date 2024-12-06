from enum import Enum

from mag_tools.utils.common.string_utils import StringUtils


class ControlType(Enum):
    """
        控件类型枚举
        枚举值为不包含前缀的控件类型名，如：ControlType.EDIT
    """

    #
    EDIT = "Edit"  # 文本框 TextBox
    DOC = "Document"  # 文档 Document
    #
    BUTTON = "Button"  # 按钮 Button
    SPLIT_BUTTON = "SplitButton" # 拆分按钮 SplitButton
    CHECKBOX = "CheckBox"  # 复选框 CheckBox
    RADIO = "RadioButton"  # 单选按钮 RadioButton
    #
    MENU_BAR = "MenuBar"  # 菜单栏 MenuBar
    MENU = "Menu"  # 菜单 Menu
    MENU_ITEM = "MenuItem"  # 菜单项 MenuItem
    #
    CONTEXT_MENU = "ContextMenu"  # 上下文菜单 ContextMenu
    #
    WINDOW = "Window"   # 主窗口 Main Window
    DIALOG = "Dialog"   # 对话框
    MESSAGE = "MessageBox"  # 消息框
    #
    LABEL = "Text"  # 标签 Label
    #
    LIST = "List"  # 列表框 ListBox
    LIST_VIEW = "ListView"  # 列表视图 ListView
    LIST_ITEM = "ListItem"  # 列表项， ListBox/ListView包含ListItem
    #
    COMBO_BOX = "ComboBox"  # 组合框 ComboBox
    #
    TREE = "Tree"  # 树视图 TreeView
    TREE_ITEM = "TreeItem"  # 树节点
    #
    TAB = "Tab"  # 选项卡 TabControl
    TAB_ITEM = "TabItem"    # Tab项
    GROUP_TAB = "GroupTab"  # 组TabItem
    #
    DATETIME = "SysDateTimePick32"   # 日期时间控件，类名为 SysDateTimePick32
    PROGRESS = "ProgressBar"  # 进度条 ProgressBar
    TITLE = "TitleBar"         # 标题栏 TitleBar
    SLIDER = "Slider"  # 滑块 Slider
    STATUS = "StatusBar"  # 状态条 StatusBar
    TOOL = "ToolBar"      # 工具栏 ToolBar
    GROUP = "Group" # 组Group
    PANEL = "Panel"  # Panel 分组和布局
    PANE = "Pane"  # Panel 分组框或面板

    @classmethod
    def get_by_value(cls, value):
        for type in cls:
            if type.value == value:
                return type
        return None

    @classmethod
    def type(cls, element):
        if element is None:
            return None

        type_name = StringUtils.get_after_keyword(element.tag_name, ".")
        return ControlType.get_by_value(type_name)

    def is_composite(self):
        return self in {ControlType.BUTTON, ControlType.SPLIT_BUTTON, ControlType.MENU, ControlType.COMBO_BOX,
                                 ControlType.LIST, ControlType.LIST_VIEW, ControlType.TREE, ControlType.PANE,
                                 ControlType.TOOL,
                                 ControlType.DATETIME, ControlType.WINDOW}

    @classmethod
    def get_name_by_chinese(cls, name_cn):
        _dict = {"文本框": "EDIT",
                 "文档": "DOC",
                 "按钮": "BUTTON",
                 "拆分按钮": "SPLIT_BUTTON",
                 "复选框": "CHECKBOX",
                 "单选按钮": "RADIO",
                 "菜单栏": "MENU_BAR",
                 "菜单": "MENU",
                 "菜单项": "MENU_ITEM",
                 "上下文菜单": "CONTEXT_MENU",
                 "主窗口": "WINDOW",
                 "对话框": "DIALOG",
                 "消息框": "MESSAGE",
                 "标签": "LABEL",
                 "列表框": "LIST",
                 "列表视图": "LIST_VIEW",
                 "列表项": "LIST_ITEM",
                 "组合框": "COMBO_BOX",
                 "树视图": "TREE",
                 "树节点": "TREE_ITEM",
                 "TAB": "TAB",
                 "TAB项": "TAB_ITEM",
                 "TAB组": "GROUP_TAB",
                 "工具栏": "TOOL",
                 "GROUP": "GROUP",
                 "PANE": "PANE",
                 "PANEL": "PANEL",
                 "标题栏": "TITLE",
                 "进度条": "PROGRESS",
                 "滑块": "SLIDER",
                 "状态条": "STATUS",
                 "日期时间": "DATETIME",
                 "组": "GROUP"}
        return _dict.get(name_cn)

    @classmethod
    def get_type_by_chinese(cls, name_ch):
        name = ControlType.get_name_by_chinese(name_ch)
        try:
            return cls[name]
        except KeyError:
            return None