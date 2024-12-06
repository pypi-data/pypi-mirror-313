from mag_tools.model.common.data_type import DataType


class DataFormat:
    def __init__(self, data_type, number_per_line = 1, right_justify = True, at_header = '', decimal_places=2, decimal_places_of_zero=1):
        """
        数据格式
        :param data_type: 数据类型
        :param number_per_line: 每行显示的数据个数
        :param right_justify: 是否右对齐
        :param at_header: 句首添加的字符串
        :param decimal_places: 小数位数
        :param decimal_places_of_zero: 小数为0时的小数位数
        """
        self.data_type = data_type
        self.number_per_line = number_per_line
        self.right_justify = right_justify
        self.at_header = at_header
        self.decimal_places = decimal_places if data_type == DataType.FLOAT else 0
        self.decimal_places_of_zero = decimal_places_of_zero if data_type == DataType.FLOAT else 0
        self.number_per_line = number_per_line
        self.right_justify = right_justify