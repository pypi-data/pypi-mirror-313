import random
import re
from datetime import date, datetime

import unicodedata

from mag_tools.bean.common.data_format import DataFormat
from mag_tools.utils.common.random_utils import RandomUtils
from mag_tools.model.common.data_type import DataType


class StringUtils:
    @staticmethod
    def get_before_keyword(s, keyword):
        return s.split(keyword)[0]

    @staticmethod
    def get_after_keyword(s, keyword):
        array = s.split(keyword)
        return array[1] if len(array) > 1 else None

    @staticmethod
    def split_name_id(text):
        """
        将 名称(标识)字符串分为{名称, 标识}
        :param text: 名称(标识)字符串
        :return: {名称, 标识}
        """
        match = re.match(r"(.+)[(（](.+)[)）]", text)
        if match:
            _name = match.group(1)
            _id = match.group(2)
            return _name, _id
        else:
            return text, None

    @staticmethod
    def parse_function(function_name):
        """
        解析字符串，将其分解为方法名和参数
        :param function_name: 字符串，格式如：test(arg1, arg2)
        :return: 方法名和参数列表
        """
        pattern = r'(\w+)\((.*)\)'
        match = re.match(pattern, function_name)

        if not match:
            raise ValueError("字符串格式不正确")

        method_name = match.group(1)
        args = match.group(2).split(',') if match.group(2) else []

        # 去除参数两端的空格
        args = [arg.strip() for arg in args]

        return method_name, args

    @staticmethod
    def to_chinese_number(num):
        units = ["", "十", "百", "千", "万", "十", "百", "千", "亿"]
        digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

        if num == 0:
            return "零"

        result = ""
        unit_position = 0
        while num > 0:
            digit = num % 10
            if digit != 0:
                result = digits[digit] + units[unit_position] + result
            elif result and result[0] != "零":
                result = "零" + result
            num //= 10
            unit_position += 1

        # 处理 "一十" 的情况
        if result.startswith("一十"):
            result = result[1:]

        return result

    @staticmethod
    def pad_text(text, pad_length, right_justify = True):
        """
        将字符串用空格补充到指定长度，空格添加在字符串前。
        参数：
        :param right_justify: 是否右对齐，空格填补在字符串前，否则填补在结尾
        :param text: 原始字符串
        :param pad_length: 目标长度
        :return: 补充空格后的字符串
        """
        if DataType.get_type(text) != DataType.STRING:
            text = str(text)

        if len(text) >= pad_length:
            return text
        padding_length = pad_length - len(text)
        return ' ' * padding_length + text if right_justify else text + ' ' * padding_length

    @staticmethod
    def pad_texts(strings, separator, pad_length, right_justify=True):
        strings = [StringUtils.pad_text(text, pad_length, right_justify) + separator for text in strings]
        return ''.join(strings)

    @staticmethod
    def split_by_keyword(lines, keyword):
        """
        根据关键字或空行将字符串数组切分成若干块。

        参数：
        :param lines: 字符串数组
        :param keyword: 关键字
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        blocks = []
        current_block = []

        for line in lines:
            if keyword in line:
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks

    @staticmethod
    def split_by_empty_line(lines):
        """
        根据空行将字符串数组切分成若干块，并删除空行。

        参数：
        :param lines: 字符串数组
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        blocks = []
        current_block = []

        for line in lines:
            if line.strip() == "":
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks

    @staticmethod
    def format(template):
        """
            格式化字符串，处理{}中的特定函数
        """
        if template is None: return template

        while '{' in template and '}' in template:
            start = template.index('{')
            end = template.index('}', start)
            expression = template[start + 1:end]

            # 解析函数名和参数
            func_name, args = StringUtils.parse_function(expression)

            # 调用相应的函数
            if func_name == 'random_text':
                result = RandomUtils.random_text(int(args[0]))
            elif func_name == 'random_string':
                result = RandomUtils.random_string(int(args[0]))
            elif func_name == 'random_chinese':
                length = int(args[0]) if args[0] else random.randint(1, 100)
                result = RandomUtils.random_chinese(length)
            elif func_name == 'random_number':
                result = RandomUtils.random_number(int(args[0]))
            elif func_name == 'random_int':
                result = str(random.randint(1, int(args[0])))
            elif func_name == 'random_date':
                year = int(args[0]) if len(args) > 0 else date.today().year
                fmt = args[1] if len(args) > 1 else "%Y%m%d"
                result = RandomUtils.random_date(year).strftime(fmt)
            elif func_name == 'today':
                fmt = args[0] if len(args) > 0 else "%Y%m%d"
                result = date.today().strftime(fmt)
            elif func_name == 'current':
                fmt = args[0] if len(args) > 0 else "%Y-%m-%d %H:%M:%S"
                result = datetime.now().strftime(fmt)
            else:
                raise ValueError(f"未知的函数: {func_name}")

            # 替换模板中的表达式
            template = template[:start] + result + template[end + 1:]

        return template

    @staticmethod
    def parse_lines_to_map(lines):
        """
        将字符串数组解析为字典。

        参数：
        :param lines: 字符串数组
        :return: 字典
        """
        data_map = {}
        for line in lines:
            key, value = line.split()
            data_map[key] = value
        return data_map

    @staticmethod
    def to_value(text, data_type=None):
        """
        将文本转换为数值
        :param text: 文本
        :param data_type: 数据类型
        """
        if data_type is None:
            data_type = DataType.get_type(text)

        if data_type == DataType.INTEGER:
            return int(text)
        elif data_type == DataType.FLOAT:
            return float(text)
        elif data_type == DataType.BOOLEAN:
            text = text.lower()
            return text == 'true' or text == 'yes' or text == 't' or text == 'y' or text == '1'
        elif data_type == DataType.LIST:
            return eval(text)
        elif data_type == DataType.DICTIONARY:
            return eval(text)
        else:
            return text

    @staticmethod
    def format_value(value, data_format=None):
        if data_format is None:
            data_type = DataType.get_type(value)
            data_format = DataFormat(data_type)

        if data_format.data_type == DataType.FLOAT:
            if value.is_integer():
                return f"{value:.{data_format.decimal_places_of_zero}f}"
            elif abs(value) >= 1e8 or abs(value) < 1e-3:
                # 手动构建科学计数法的字符串表示
                exponent = int(f"{value:e}".split('e')[1])
                coefficient = f"{value / (10 ** exponent):.6f}".rstrip('0').rstrip('.')
                return f"{coefficient}e{exponent}"
            else:
                formatted_value = f"{value:.{data_format.decimal_places}f}"
                # 确保小数位末尾的零的个数符合要求
                if '.' in formatted_value:
                    integer_part, decimal_part = formatted_value.split('.')
                    decimal_part = decimal_part.rstrip('0')
                    if len(decimal_part) < data_format.decimal_places_of_zero:
                        decimal_part += '0' * (data_format.decimal_places_of_zero - len(decimal_part))
                    formatted_value = f"{integer_part}.{decimal_part}"
                return formatted_value
        elif data_format.data_type == DataType.INTEGER:
            return f"{round(value)}"

    @staticmethod
    def get_print_width(s, chines_width=1.67):
        width = 0
        for char in s:
            if unicodedata.east_asian_width(char) in ('F', 'W'):
                width += chines_width
            else:
                width += 1
        return int(width)

    @staticmethod
    def remove_keywords(text, keyword_begin, keyword_end):
        # 使用正则表达式去除keyword_begin和keyword_end之间的内容，包括这两个关键词
        pattern = re.escape(keyword_begin) + '.*?' + re.escape(keyword_end)
        result = re.sub(pattern, '', text, flags=re.DOTALL)
        return result

if __name__ == '__main__':
    # 创建DataFormat对象
    _data_format = DataFormat(DataType.FLOAT, decimal_places=6, decimal_places_of_zero=3)

    # 测试format_value方法
    print(StringUtils.format_value(1.5, _data_format))  # 输出: 1.500000
    print(StringUtils.format_value(1.53e-005, _data_format))  # 输出: 1.550000
    print(StringUtils.format_value(155, _data_format))  # 输出: 155.000000