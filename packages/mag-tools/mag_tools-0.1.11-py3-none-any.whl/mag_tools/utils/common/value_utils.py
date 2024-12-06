import numpy as np

from mag_tools.model.common.data_type import DataType
from mag_tools.utils.common.string_utils import StringUtils


class ValueUtils:
    @staticmethod
    def text_to_array_1d(text, data_type=DataType.INTEGER):
        """
        从一行文本中获取数值数组[]
        :param text: 文本，由 "数值" 或 "数值个数*数值"构成
        :param data_type: 数据类型
        :return: 数值数组
        """
        data = []

        for part in text.split():
            if '*' in part:
                count, value = part.split('*')
                data.extend([StringUtils.to_value(value, data_type)] * int(count))
            else:
                data.append(StringUtils.to_value(part, data_type))

        return data

    @staticmethod
    def lines_to_array_1d(lines, data_type=DataType.INTEGER):
        """
        从多行文本中获取数值数组[]
        :param lines: 文本段，每行由 "数值" 或 "数值个数*数值"构成
        :param data_type: 数据类型
        :return: 数值数组
        """
        array_1d = []
        for line in lines:
            array_1d.extend(ValueUtils.text_to_array_1d(line, data_type))
        return array_1d

    @staticmethod
    def lines_to_array_2d(block_lines, nx, ny, data_type=DataType.INTEGER):
        """
        从文本块获取数值列表
        :param block_lines: 文本块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        :param nx: 行数
        :param ny: 列数
        :param data_type: 数据类型
        :return: Values
        """
        array_1d = ValueUtils.lines_to_array_1d(block_lines, data_type)

        return np.array(array_1d).reshape((nx, ny))

    @staticmethod
    def lines_to_array_3d(block_lines, nx, ny, nz, data_type=DataType.INTEGER):
        """
        从文本块获取数值列表
        :param block_lines: 文本块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        :param nx: 行数
        :param ny: 列数
        :param nz: 层数
        :param data_type: 数据类型
        :return: Values
        """
        array_1d = ValueUtils.lines_to_array_1d(block_lines, data_type)

        return np.array(array_1d).reshape((nz, nx, ny))

    @staticmethod
    def array_1d_to_lines(array_1d, data_format):
        if array_1d is None:
            return []

        result = []
        count = 1
        current_value = array_1d[0]

        max_len = 2
        for i in range(1, len(array_1d)):
            if array_1d[i] == current_value:
                count += 1
            else:
                current_text = StringUtils.format_value(current_value, data_format)
                txt = f"{count}*{current_text}" if count > 1 else f"{current_text}"
                max_len = max(max_len, len(txt))
                result.append(txt)

                current_value = array_1d[i]
                count = 1

        # 处理最后一组数据
        current_text = StringUtils.format_value(current_value, data_format)
        txt = f"{count}*{current_text}" if count > 1 else f"{current_text}"
        max_len = max(max_len, len(txt))
        result.append(txt)

        # 将结果按行分隔，每行包含data_format.number_per_line个数值
        lines = []
        for i in range(0, len(result), data_format.number_per_line):
            txt = StringUtils.pad_texts(result[i:i + data_format.number_per_line], ' ', max_len, data_format.right_justify)
            lines.append(f'{data_format.at_header}{txt}')

        return lines

    @staticmethod
    def array_2d_to_lines(array_2d, data_format):
        """
        生成数值块
        :param array_2d: 二维数组
        :param data_format: 数据格式
        :return: 数值块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        """

        # 将其展平为一维数组后添加到列表中
        layer = array_2d.flatten()
        return ValueUtils.array_1d_to_lines(layer, data_format)

    @staticmethod
    def array_3d_to_lines(array_3d, data_format):
        """
        生成数值块
        :param array_3d: 三维数组
        :param data_format: 数据格式
        :return: 数值块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        """
        lines = []

        # 遍历每一层并将其展平为一维数组后添加到列表中
        layers = []
        num_layers = array_3d.shape[0]  # 层数
        for i in range(num_layers):
            layers.append(array_3d[i, :, :].flatten())

        for layer in layers:
            lines.extend(ValueUtils.array_1d_to_lines(layer, data_format))
        return lines

if __name__ == '__main__':
    _lines = ['60*0.087', '60*0.097']
    # _lines = ['1.18379        2.26189        2.61705        5.99524       10.31299',
    #           '15.17937       32.40075       33.90037      109.47345      261.72995',
    #           '238.24753      206.15742',
    #           '238.24753      206.15742      121.33305      242.47713      166.94165',
    #           '146.50681       13.91259        7.39986        5.83849        6.06996',
    #           '7.95473        8.99119']
    dt = ValueUtils.lines_to_array_3d(_lines, 20, 3, 2)

    te = ValueUtils.array_3d_to_lines(dt, 5)
    print("\n".join(te))