# -*- coding:utf-8 -*-
import datetime
import platform
import re
import time
from functools import wraps
import warnings
import pymysql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar
from mdbq.config import get_myconf
from mdbq.dataframe import converter

warnings.filterwarnings('ignore')
"""
程序专门用来下载数据库数据, 并返回 df, 不做清洗数据操作;
"""


class QueryDatas:
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.config = {
            'host': self.host,
            'port': int(self.port),
            'user': self.username,
            'password': self.password,
            'charset': charset,  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }

    def check_condition(self, db_name, table_name, condition):
        """ 按指定条件查询数据库，并返回 """
        if self.check_infos(db_name, table_name) == False:
            return

        self.config.update({'database': db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        with connection.cursor() as cursor:
            sql = f"SELECT 更新时间 FROM {table_name} WHERE {condition}"
            # print(sql)
            cursor.execute(sql)
            columns = cursor.fetchall()
            return columns

    def data_to_df(self, db_name, table_name, start_date, end_date, projection: dict=[]):

        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        df = pd.DataFrame()  # 初始化df

        if self.check_infos(db_name, table_name) == False:
            return df

        self.config.update({'database': db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库

        with connection.cursor() as cursor:
            # 3. 获取数据表的所有列信息
            sql = 'SELECT `COLUMN_NAME` FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
            cursor.execute(sql, (db_name, {table_name}))
            columns = cursor.fetchall()
            cols_exist = [col['COLUMN_NAME'] for col in columns]  # 数据表的所有列, 返回 list

            # 4. 构建 SQL 查询语句
            if projection:  # 获取指定列
                columns_in = []
                for key, value in projection.items():
                    if value == 1 and key in cols_exist:
                        columns_in.append(key)  # 提取值为 1 的键并清理不在数据表的键
                columns_in = [f"`{item}`" for item in columns_in]
                if not columns_in:
                    print(f'传递的参数 projection，在数据库中没有找到匹配的列，请检查 projection： {projection}')
                    return df
                columns_in = ', '.join(columns_in)
                if '日期' in cols_exist:  # 不论是否指定, 只要数据表有日期，则执行
                    sql = (f"SELECT {columns_in} FROM `{db_name}`.`{table_name}` "
                           f"WHERE {'日期'} BETWEEN '{start_date}' AND '{end_date}'")
                else:  # 数据表没有日期列时，返回指定列的所有数据
                    sql = f"SELECT {columns_in} FROM `{db_name}`.`{table_name}`"
            else:  # 没有指定获取列时
                if '日期' in cols_exist:  # 但数据表有日期，仍然执行
                    cols_exist = [f"`{item}`" for item in cols_exist]
                    columns_in = ', '.join(cols_exist)
                    sql = (f"SELECT {columns_in} FROM `{db_name}`.`{table_name}` "
                           f"WHERE {'日期'} BETWEEN '{start_date}' AND '{end_date}'")
                else:  # 没有指定获取列，且数据表也没有日期列，则返回全部列的全部数据
                    all_col = ', '.join([f"`{item}`" for item in cols_exist if item != 'id'])
                    sql = f"SELECT %s FROM `%s`.`%s`" % (all_col, db_name, table_name)
            # print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()  # 获取查询结果
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)  # 转为 df
            if 'id' in df.columns.tolist():
                df.pop('id')  # 默认不返回 id 列
            if len(df) == 0:
                print(f'database: {db_name}, table: {table_name} 查询的数据为空1')
            connection.close()
            return df

        # if len(df) == 0:
        #     print(f'database: {db_name}, table: {table_name} 查询的数据为空2')
        #     return pd.DataFrame()
        # cv = converter.DataFrameConverter()
        # df = cv.convert_df_cols(df)
        # if 'id' in df.columns.tolist():
        #     df.pop('id')  # 默认不返回 id 列
        # return df

    def columns_to_list(self, db_name, table_name,  columns_name) -> list:
        """
        获取数据表的指定列, 返回列表
        [{'视频bv号': 'BV1Dm4y1S7BU', '下载进度': 1}, {'视频bv号': 'BV1ov411c7US', '下载进度': 1}]
        """
        if self.check_infos(db_name, table_name) == False:  # 检查传入的数据库和数据表是否存在
            return []

        self.config.update({'database': db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        with connection.cursor() as cursor:
            # 3. 获取数据表的所有列信息
            sql = 'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
            cursor.execute(sql, (db_name, {table_name}))
            columns = cursor.fetchall()
            cols_exist = [col['COLUMN_NAME'] for col in columns]  # 数据表的所有列, 返回 list
            columns_name = [item for item in columns_name if item in cols_exist]
            if len(columns_name) == 0:
                return []
            columns_in = ', '.join(columns_name)
            sql = (f"SELECT {columns_in} FROM {db_name}.{table_name} ")
            cursor.execute(sql)
            column_values = cursor.fetchall()  # 返回指定列，结果是[dict, dict, dict, ...]
            # column_values = [item[column_name] for item in column_values]  # 提取字典的值, 组成列表
        connection.close()
        return column_values

    def dtypes_to_list(self, db_name, table_name) -> list:
        """
        获取数据表的指定列, 返回列表
        [{'视频bv号': 'BV1Dm4y1S7BU', '下载进度': 1}, {'视频bv号': 'BV1ov411c7US', '下载进度': 1}]
        """
        if self.check_infos(db_name, table_name) == False:  # 检查传入的数据库和数据表是否存在
            return []

        self.config.update({'database': db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        with connection.cursor() as cursor:
            # 3. 获取数据表的所有列信息
            sql = 'SELECT COLUMN_NAME, COLUMN_TYPE FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
            cursor.execute(sql, (db_name, {table_name}))
            column_name_and_type = cursor.fetchall()
        connection.close()
        return column_name_and_type

    def check_infos(self, db_name, table_name) -> bool:
        """ 检查数据库、数据表是否存在 """
        connection = pymysql.connect(**self.config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                # 1. 检查数据库是否存在
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    print(f"Database <{db_name}>: 数据库不存在")
                    return False
        finally:
            connection.close()  # 这里要断开连接

        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        try:
            with connection.cursor() as cursor:
                # 2. 查询表是否存在
                sql = f"SHOW TABLES LIKE '{table_name}'"
                cursor.execute(sql)
                if not cursor.fetchone():
                    print(f'{db_name} -> <{table_name}>: 表不存在')
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()  # 断开连接


if __name__ == '__main__':
    conf = ConfigTxt()
    data = conf.config_datas['Windows']['xigua_lx']['mysql']['remoto']
    username, password, host, port = data['username'], data['password'], data['host'], data['port']

    q = QueryDatas(username, password, host, port)
    res = q.columns_to_list(db_name='视频数据', table_name='bilibili视频', columns_name=['视频bv号', '下载进度'])
    print(res)
