# -*- coding:utf-8 -*-
import warnings
import pandas as pd
import numpy as np
import chardet
import zipfile

from numpy import dtype
from pandas.tseries.holiday import next_monday
from pyzipper import PyZipFile
import os
import platform
import json
import pymysql
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.mysql import s_query
from mdbq.config import get_myconf
from mdbq.config import set_support
from mdbq.dataframe import converter
import datetime
import time
import re
import shutil
import getpass

from sqlalchemy.dialects.postgresql.pg_catalog import pg_get_serial_sequence

warnings.filterwarnings('ignore')
"""
1. 记录 dataframe 或者数据库的列信息(dtypes)
2. 更新 mysql 中所有数据库的 dtypes 信息到本地 json
"""


class DataTypes:
    """
     数据简介: 记录 dataframe 或者数据库的列信息(dtypes)，可以记录其信息或者加载相关信息用于入库使用，
     第一字段为分类(如 dataframe/mysql)，第二字段为数据库名，第三字段为集合名，第四段列名及其数据类型
    """
    def __init__(self, path=None):
        self.datas = {
            "json统计":
                {
                    "字段量": 0,
                    "数据库量": 0,
                    "集合数量": 0
                }
        }
        self.path = path
        if not self.path:
            self.path = set_support.SetSupport(dirname='support').dirname
        self.json_file = os.path.join(self.path, 'df_types.json')
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if not os.path.isfile(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8_sig') as f:
                json.dump(self.datas, f, ensure_ascii=False, sort_keys=True, indent=4)
        self.json_before()

    def json_before(self):
        """ 本地 json 文件的 dtypes 信息, 初始化更新给 self.datas """
        with open(self.json_file, 'r', encoding='utf-8_sig') as f:
            json_ = json.load(f)
            self.datas.update(json_)

    def get_df_types(self, db_name, collection_name, df=pd.DataFrame(), is_file_dtype=True):
        """
        读取 df 的 dtypes, 并更新本地 json 文件
        期间会 清理不合规的列名, 并对数据类型进行转换(尝试将 object 类型转为 int 或 float)
        返回: df 的 dtypes, 后续使用示例: df = df.astype(dtypes, errors='ignore')
        is_file_dtype=True: 默认情况下以旧 json 优先, 即允许手动指定 json 文件里面的数据类型
        """
        if len(df) == 0:
            return
        cv = converter.DataFrameConverter()
        df = cv.convert_df_cols(df=df)  # 清理 dataframe 非法值
        dtypes = df.dtypes.apply(str).to_dict()
        dtypes = {db_name: {collection_name: dtypes}}

        if not self.datas:  # 如果不存在本地 json 文件, 直接返回即可
            self.datas.update(dtypes)
            return self.datas[db_name][collection_name]
        else:  # 存在则读取，并更新 df 的 dtypes
            if db_name in list(self.datas.keys()):  # ['京东数据2', '推广数据2', '生意参谋2', '生意经2']
                if collection_name in list(self.datas[db_name].keys()):
                    if is_file_dtype:  # 旧数据优先
                        # # 用 dtypes 更新, 允许手动指定 json 文件里面的数据类型
                        dtypes[db_name][collection_name].update(self.datas[db_name][collection_name])
                        # 将 dtypes 更新进去，使 self.datas 包含新旧信息
                        self.datas[db_name][collection_name].update(dtypes[db_name][collection_name])
                    else:  # 新数据优先
                        self.datas[db_name][collection_name].update(dtypes[db_name][collection_name])
                else:
                    if is_file_dtype:  # 旧数据优先
                        dtypes[db_name].update(self.datas[db_name])
                        self.datas[db_name].update(dtypes[db_name])
                    else:
                        self.datas[db_name].update(dtypes[db_name])
            else:
                # dtypes.update(self.datas)  # 可以注释掉, 因为旧数据 self.datas 是空的
                self.datas.update(dtypes)
            dbs = 0
            collections = 0
            cols = 0
            # self.datas.pop('json统计')
            for k, v in self.datas.items():
                if k == 'json统计':
                    continue
                dbs += 1
                for d, j in v.items():
                    collections += 1
                    for t, p in j.items():
                        cols += 1
            tips = {'json统计': {'数据库量': dbs, '集合数量': collections, '字段量': cols}}
            self.datas.update(tips)
            return self.datas[db_name][collection_name]  # 返回 df 的 dtypes

    def as_json_file(self):
        """ 保存为本地 json 文件 """
        self.datas = {k: 'null' if v is None else v for k, v in self.datas.items()}  # 替换字典中，值存在空值的值
        self.datas = {k if k != None else 'null': v for k, v in self.datas.items()}  # 替换字典中，键存在空值的键
        if 'null' in str(self.datas):
            print(f'self.datas 数据中存在空值，可能有未匹配的数据库名或数据表名，请检查 《标题对照表.csv》，已取消写入 df_types.json ')
            print('self.datas: ', self.datas)
            return
        with open(self.json_file, 'w', encoding='utf-8_sig') as f:
            json.dump(
                self.datas,
                f,
                ensure_ascii=False,  # 默认True，非ASCII字符将被转义。如为False，则非ASCII字符会以\uXXXX输出
                sort_keys=True,  # 默认为False。如果为True，则字典的输出将按键排序。
                indent=4,
            )
        time.sleep(1)

    def df_dtypes_to_json(self, db_name, collection_name, path, df=pd.DataFrame(), is_file_dtype=True):
        if len(df) == 0:
            return
        cv = converter.DataFrameConverter()
        df = cv.convert_df_cols(df=df)  # 清理 dataframe 列名的不合规字符
        dtypes = df.dtypes.apply(str).to_dict()
        dtypes = {'dataframe': {db_name: {collection_name: dtypes}}}
        self.dtypes_to_json(dtypes=dtypes, cl='dataframe', db_name=db_name, collection_name=collection_name, path=path, is_file_dtype=is_file_dtype)

    def load_dtypes(self, db_name, collection_name):
        if db_name in list(self.datas.keys()):
            if collection_name in list(self.datas[db_name].keys()):
                return self.datas[db_name][collection_name]
            else:
                print(f'不存在的集合名信息: {collection_name}, 文件位置: {self.json_file}')
                return {}
        else:
            print(f'不存在的数据库信息: {db_name}, 文件位置: {self.json_file}')
            return {}


def update_df_types_to_json(file, db_name, collection_name, is_file_dtype=True):
    """ 更新一个文件的 dtype 信息到 json 文件 """
    df = pd.read_csv(file, encoding='utf-8_sig', header=0, na_filter=False)
    df_to_json = DataTypes()
    df_to_json.get_df_types(
        df=df,
        db_name=db_name,
        collection_name=collection_name,
        is_file_dtype=is_file_dtype,  # 日常需开启文件优先, 正常不要让新文件修改 json 已有的类型
    )
    df_to_json.as_json_file()
    print(f'json文件已存储: {df_to_json.json_file}')


def test_load_dtypes(db_name, collection_name):
    d = DataTypes()
    res = d.load_dtypes(db_name=db_name, collection_name=collection_name)
    print(res)


if __name__ == '__main__':
    file = '/Users/xigua/数据中心/pandas数据源/店铺日报.csv'
    update_df_types_to_json(
        file=file,
        db_name='pandas数据源',
        collection_name='店铺日报',
        is_file_dtype=True,
    )
    # test_load_dtypes(db_name='pandas数据源', collection_name='店铺日报')


