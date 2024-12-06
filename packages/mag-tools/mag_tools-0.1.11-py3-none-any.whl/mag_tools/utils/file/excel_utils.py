class ExcelUtils:
    @staticmethod
    def clear_empty(df):
        """
        清除前面空白的行和列
        :param df: Excel文件句柄
        :return:
        """
        df = df.dropna(how='all').reset_index(drop=True)
        df = df.dropna(axis=1, how='all')

        return df

    @staticmethod
    def get_cells_of_row_by_keyword(df, row, keyword):
        """
        获取指定行中匹配关键词的单元格的内容
        :param df: Excel文件句柄
        :param row: 行数
        :param keyword: 内容所包含的关键词
        :return: 指定单元格的内容，返回匹配的所有单元格内容
        """
        row_data = df.iloc[row]
        # 查找包含关键字的列
        return row_data[row_data.astype(str).str.contains(keyword, na=False)]

    @staticmethod
    def get_first_cell_of_row_by_keyword(df, row, keyword):
        """
        获取指定行中匹配关键词的首个单元格的内容
        :param df: Excel文件句柄
        :param row: 行数
        :param keyword: 内容所包含的关键词
        :return: 指定单元格的内容，返回匹配的第一个单元格内容
        """
        matching_columns = ExcelUtils.get_cells_of_row_by_keyword(df, row, keyword)
        return matching_columns.iloc[0] if not matching_columns.empty else None

    @staticmethod
    def delete_row_with_keyword(df, row, keyword):
        # 检查指定行是否包含关键词
        if row < len(df) and df.iloc[row].astype(str).str.contains(keyword, na=False).any():
            # 删除包含指定关键词的行
            df = df.drop(index=row).reset_index(drop=True)
        return df

    @staticmethod
    def get_value_from_group(group, column_name):
        value = None
        value_groups = group.groupby(column_name)
        if value_groups and len(value_groups) >= 1:
            value = list(value_groups.groups.keys())[0]

        return value
