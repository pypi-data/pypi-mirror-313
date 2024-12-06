# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from decimal import Decimal
import re


class DataFrameConverter(object):
    def __init__(self, df=pd.DataFrame({})):
        self.df = df

    def convert_df_cols(self, df=pd.DataFrame({})):
        """
        清理 dataframe 非法值
        对数据类型进行转换(尝试将 object 类型转为 int 或 float)
        """
        if len(df) == 0:
            df = self.df
            if len(df) == 0:
                return

        def find_longest_decimal_value(number_list):
            # 取列表中小数位数最长的值
            longest_value = None
            max_decimals = 0
            for num in number_list:
                decimal_places = len(str(num).split('.')[1])
                if decimal_places > max_decimals:
                    max_decimals = decimal_places
                    longest_value = num
            return longest_value

        # dtypes = df.dtypes.apply(str).to_dict()  # 将 dataframe 数据类型转为字典形式
        df.replace([np.inf, -np.inf], '0', inplace=True)  # 清理一些非法值
        # df.replace(to_replace=['\\N', '-', '--', '', 'nan', 'NAN'], value='0', regex=False, inplace=True)  # 替换掉特殊字符
        df.replace(to_replace=['\\N', '', 'nan', 'NAN'], value='0', regex=False, inplace=True)  # 替换掉特殊字符
        # df.replace(to_replace=[','], value='', regex=True, inplace=True)
        df.replace(to_replace=['="'], value='', regex=True, inplace=True)  # ="和"不可以放在一起清洗, 因为有: id=86785565
        df.replace(to_replace=['"'], value='', regex=True, inplace=True)
        cols = df.columns.tolist()

        df.reset_index(inplace=True, drop=True)  # 重置索引，避免下面的 df.loc[0, col] 会出错

        for col in cols:
            if col.lower() == 'id':
                df.pop(col)  # 等待插入的 df 不能包含 id 列，否则可能跟现有 id 主键冲突
                continue

            try:
                # 百分比在某些数据库中不兼容, 转换百分比为小数, # 转百分比的列不能含有中文或特殊字符
                df[col] = df[col].apply(
                    lambda x: float(float((str(x).rstrip("%"))) / 100) if re.findall(r'^\d+\.?\d*%$', str(x)) else x)
            except Exception as e:
                print(f'留意错误信息: 位于列 -> {col} -> {e}')

            if (col.endswith('占比') or col.endswith('率') or col.endswith('同比')
                    or col.endswith('环比') or col.lower().endswith('roi')
                    or col.endswith('产出比')):
                df = df.astype({col: 'float64'}, errors='raise')

            # 尝试转换合适的数据类型
            if df[col].dtype == 'object':
                #  "_"符号会被错误识别
                try:
                    # 不能直接使用 int() ，对于大数，可能转为uint64，导致数据库入库可能异常
                    df[col] = df[col].apply(
                        lambda x: np.int64(str(x)) if '_' not in str(x) and '.' not in str(x) else x)  # 不含小数点尝试转整数
                    # df[col] = df[col].apply(lambda x: int(x) if '_' not in str(x) and '.' not in str(x) else x)  # 不含小数点尝试转整数
                except:
                    pass
                if df[col].dtype == 'object':
                    try:
                        df[col] = df[col].apply(lambda x: float(x) if '.' in str(x) and '_' not in str(x) else x)
                    except:
                        pass
            if df[col].dtype == 'float' or df[col].dtype == 'float64':  # 对于小数类型, 保留 6 位小数
                df[col] = df[col].fillna(0.0).apply(lambda x: round(x, 6))

            # 转换日期样式的列为日期类型
            value = df.loc[0, col]
            if value:
                res = re.match(r'\d{4}-\d{2}-\d{2}|\d{4}-\d{2}-\d{2} |\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
                               r'|\d{4}/\d{1}/\d{1}|\d{4}/\d{1}/\d{2}|\d{4}/\d{2}/\d{1}|\d{4}/\d{2}/\d{2}', str(value))
                if res:
                    try:
                        df[col] = df[col].apply(lambda x: pd.to_datetime(x))
                    except:
                        pass
            new_col = col.lower()
            new_col = re.sub(r'[()\-，,&~^、 （）\"\'“”=·/。》《><！!`]', '_', new_col, re.IGNORECASE)
            new_col = new_col.replace('）', '')
            new_col = re.sub(r'_{2,}', '_', new_col)
            new_col = re.sub(r'_+$', '', new_col)
            df.rename(columns={col: new_col}, inplace=True)
        df.fillna(0, inplace=True)
        return df


if __name__ == '__main__':
    # df = pd.DataFrame(np.random.randn(5, 3), columns=['a', 'b', 'c'])
    # converter = DataFrameConverter()
    # df = converter.convert_df_cols(df)
    # print(df['a'].dtype)
    # print(df)
    pattern = '1540%'
    pattern = re.findall(r'^\d+\.?\d*%$', pattern)
    print(pattern)