import numpy as np


class ArrayUtils:
    @staticmethod
    def assign_array_2d(array2, i1, i2, j1, j2, value):
        """
        给数组指定区域的元素赋值
        :param array2: 二维数组
        :param i1: 行数1
        :param i2: 行数2
        :param j1: 列数1
        :param j2: 列数2
        :param value: 数值
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                if i < len(array2) and j < len(array2[i]):
                    array2[i][j]= value
                else:
                    raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array2


    @staticmethod
    def multiply_array_2d(array2, i1, i2, j1, j2, factor):
        """
        给数组指定区域的元素乘以系数
        :param array2: 二维数组
        :param i1: 行数1
        :param i2: 行数2
        :param j1: 列数1
        :param j2: 列数2
        :param factor: 系数
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                if i < len(array2) and j < len(array2[i]):
                    array2[i][j] *= factor
                else:
                    raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array2

    @staticmethod
    def add_array_2d(array2, i1, i2, j1, j2, value):
        """
        给数组指定区域的元素增加数值
        :param array2: 二维数组
        :param i1: 行数1
        :param i2: 行数2
        :param j1: 列数1
        :param j2: 列数2
        :param value: 数值
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                if i < len(array2) and j < len(array2[i]):
                    array2[i][j] += value
                else:
                    raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array2

    @staticmethod
    def assign_array_3d(array3, i1, i2, j1, j2, k1, k2, value):
        """
        给数组指定区域的元素赋值
        :param array3: 三维数组
        :param i1: 层数1
        :param i2: 层数2
        :param j1: 行数1
        :param j2: 行数2
        :param k1: 列数1
        :param k2: 列数2
        :param value: 数值
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                for k in range(k1, k2 + 1):
                    if i < len(array3) and j < len(array3[i]) and k < len(array3[i][j]):
                        array3[i][j][k] = value
                    else:
                        raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array3

    @staticmethod
    def multiply_array_3d(array3, i1, i2, j1, j2, k1, k2, factor):
        """
        给数组指定区域的元素乘以系数
        :param array3: 三维数组
        :param i1: 层数1
        :param i2: 层数2
        :param j1: 行数1
        :param j2: 行数2
        :param k1: 列数1
        :param k2: 列数2
        :param factor: 系数
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                for k in range(k1, k2 + 1):
                    if i < len(array3) and j < len(array3[i]) and k < len(array3[i][j]):
                        array3[i][j][k] *= factor
                    else:
                        raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array3

    @staticmethod
    def add_array_3d(array3, i1, i2, j1, j2, k1, k2, value):
        """
        给数组指定区域的元素增加数值
        :param array3: 三维数组
        :param i1: 层数1
        :param i2: 层数2
        :param j1: 行数1
        :param j2: 行数2
        :param k1: 列数1
        :param k2: 列数2
        :param value: 数值
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                for k in range(k1, k2 + 1):
                    if i < len(array3) and j < len(array3[i]) and k < len(array3[i][j]):
                        array3[i][j][k] += value
                    else:
                        raise IndexError("Index out of range for the provided 3D array dimensions.")
        return array3


    @staticmethod
    def copy_array_3d(source_array, target_array, i1, i2, j1, j2, k1, k2):
        """
        复制源数组指定区域到目标数组
        :param source_array: 源数组
        :param target_array: 目标数组
        :param i1: 层数1
        :param i2: 层数2
        :param j1: 行数1
        :param j2: 行数2
        :param k1: 列数1
        :param k2: 列数2
        """
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                for k in range(k1, k2 + 1):
                    if i < len(source_array) and j < len(source_array[i]) and k < len(source_array[i][j]):
                        target_array[i][j][k] = source_array[i][j][k]
                    else:
                        raise IndexError("Index out of range for the provided 3D array dimensions.")
        return target_array

    @staticmethod
    def init_array_3d(x, y, z):
        """
        初始化三维数据
        :x: 层数
        :y: 行数
        :z: 列数
        """
        return np.empty((x, y, z), dtype=object)

    @staticmethod
    def init_array_2d(x, y):
        """
        初始化二维数据
        :x: 行数
        :y: 列数
        """
        return np.empty((x, y), dtype=object)

if __name__ == '__main__':
    # 示例用法
    _array3 = [[[0 for _ in range(5)] for _ in range(4)] for _ in range(3)]

    _values = list(range(1, 19))  # 示例数据，共18个值
    ArrayUtils.assign_array_3d(_array3, 1, 2, 1, 3, 1, 3, _values)

    for layer in _array3:
        print(layer)

    ArrayUtils.multiply_array_3d(_array3, 1, 2, 1, 3, 1, 3, 2)
    print("\n数组乘以系数后：")
    for layer in _array3:
        print(layer)


    ArrayUtils.add_array_3d(_array3, 1, 2, 1, 3, 1, 3, 100.0)
    print("\n数组加数值后：")
    for layer in _array3:
        print(layer)