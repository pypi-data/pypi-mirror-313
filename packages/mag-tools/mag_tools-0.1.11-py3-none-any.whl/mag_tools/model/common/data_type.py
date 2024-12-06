from enum import Enum


class DataType(Enum):
    INTEGER = 1
    FLOAT = 2
    STRING = 3
    BOOLEAN = 4
    LIST = 5
    DICTIONARY = 6

    @classmethod
    def get_type(cls, text):
        # 尝试判断是否为整数
        try:
            int(text)
            return DataType.INTEGER
        except ValueError:
            pass

        # 尝试判断是否为浮点数
        try:
            float(text)
            return DataType.FLOAT
        except ValueError:
            pass

        # 判断是否为布尔值
        if text.lower() in ['true', 'false']:
            return DataType.BOOLEAN

        # 判断是否为列表
        if text.startswith('[') and text.endswith(']'):
            return DataType.LIST

        # 判断是否为字典
        if text.startswith('{') and text.endswith('}'):
            return DataType.DICTIONARY

        # 默认返回字符串类型
        return DataType.STRING