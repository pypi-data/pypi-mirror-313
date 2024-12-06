# -*- coding:utf-8 -*-
import warnings
import pandas as pd
import os
import platform
import json
import pymysql
import socket
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.mysql import s_query
from mdbq.config import myconfig
from mdbq.config import set_support
from mdbq.dataframe import converter
import datetime
import time
import re

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
    def __init__(self, path=None, service_name=None):
        self.datas = {
            '_json统计':
                {
                    '分类': 0,
                    '数据库量': 0,
                    '集合数量': 0,
                    '字段量': 0,
                    '数据简介': '记录数据库各表的数据类型信息',
                }
        }
        self.path = path
        if not self.path:
            self.path = set_support.SetSupport(dirname='support').dirname
        self.service_name = service_name
        if not self.service_name:
            self.service_name = 'xigua_lx'
        self.json_file = os.path.join(self.path, f'mysql_types_{self.service_name}.json')
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

    def get_mysql_types(self, cl, dtypes, db_name, table_name, is_file_dtype=True):
        """ 更新 mysql 的 types 信息到 json 文件 """
        if cl in self.datas.keys():
            if db_name in list(self.datas[cl].keys()):  # ['京东数据2', '推广数据2', '生意参谋2', '生意经3']
                if table_name in list(self.datas[cl][db_name].keys()):
                    if is_file_dtype:  # 旧数据优先
                        # # 用 dtypes 更新, 允许手动指定 json 文件里面的数据类型
                        dtypes[cl][db_name][table_name].update(self.datas[cl][db_name][table_name])
                        # 将 dtypes 更新进去，使 self.datas 包含新旧信息
                        self.datas[cl][db_name][table_name].update(dtypes[cl][db_name][table_name])
                    else:  # 新数据优先
                        self.datas[cl][db_name][table_name].update(dtypes[cl][db_name][table_name])
                else:
                    if is_file_dtype:  # 旧数据优先
                        dtypes[cl][db_name].update(self.datas[cl][db_name])
                        self.datas[cl][db_name].update(dtypes[cl][db_name])
                    else:
                        self.datas[cl][db_name].update(dtypes[cl][db_name])
            else:
                # dtypes.update(self.datas)  # 可以注释掉, 因为旧数据 self.datas 是空的
                self.datas[cl].update(dtypes[cl])
        else:
            self.datas.update(dtypes)

        cif = 0  # 分类
        dbs = 0  # 数据库
        collections = 0  # 集合
        cols = 0  # 字段
        for k, v in self.datas.items():
            if k == '_json统计':
                continue  # 不统计头信息
            cif += 1
            for t, g in v.items():
                dbs += 1
                for d, j in g.items():
                    collections += 1
                    for t, p in j.items():
                        cols += 1
        tips = {'分类': cif, '数据库量': dbs, '集合数量': collections, '字段量': cols}
        self.datas['_json统计'].update(tips)
        # with open(json_file, 'w', encoding='utf-8_sig') as f:
        #     json.dump(
        #         self.datas,
        #         f,
        #         ensure_ascii=False,  # 默认True，非ASCII字符将被转义。如为False，则非ASCII字符会以\uXXXX输出
        #         sort_keys=True,  # 默认为False。如果为True，则字典的输出将按键排序。
        #         indent=4,
        #     )

    def as_json_file(self):
        """ 保存为本地 json 文件 """
        with open(self.json_file, 'w', encoding='utf-8_sig') as f:
            json.dump(
                self.datas,
                f,
                ensure_ascii=False,  # 默认True，非ASCII字符将被转义。如为False，则非ASCII字符会以\uXXXX输出
                sort_keys=True,  # 默认为False。如果为True，则字典的输出将按键排序。
                indent=4,
            )
        print(f'已更新 json 文件: {self.json_file}')
        time.sleep(1)

    def load_dtypes(self, db_name, table_name, cl='mysql', ):
        """
        mysql.py 程序从本地文件中读取 dtype 信息
        如果缺失 dtypes 信息，则执行 mysql_all_dtypes 以便更新所有数据库 dtypes 信息到 json 文件
        """
        if cl in self.datas.keys():
            if db_name in list(self.datas[cl].keys()):
                if table_name in list(self.datas[cl][db_name].keys()):
                    return self.datas[cl][db_name][table_name], None, None, None
                else:
                    print(f'不存在的集合名信息: {table_name}, 文件位置: {self.json_file}')
                    # mysql_all_dtypes(db_name=db_name, table_name=table_name)   # 更新一个表的 dtypes
                    return {}, cl, db_name, table_name
            else:
                print(f'不存在的数据库信息: {db_name}, 文件位置: {self.json_file}')
                # mysql_all_dtypes(db_name=db_name)  # 更新一个数据库的 dtypes
                return {}, cl, db_name, None
        else:
            print(f'不存在的数据分类: {cl}, 文件位置: {self.json_file}')
            # mysql_all_dtypes()  # 更新所有数据库所有数据表的 dtypes 信息到本地 json
            return {}, cl, None, None  # 返回这些结果的目的是等添加完列再写 json 文件才能读到 types 信息


def mysql_all_dtypes(db_name=None, table_name=None, path=None):
    """
    更新 mysql 中所有数据库的 dtypes 信息到本地 json
    """
    username, password, host, port, service_name = None, None, None, None, None
    conf = myconfig.main()
    if socket.gethostname() in ['xigua_lx', 'xigua1', 'MacBookPro']:
        data = conf['Windows']['xigua_lx']['mysql']['local']
        username, password, host, port = data['username'], data['password'], data['host'], data['port']
        service_name = 'xigua_lx'  # 影响 mysql_types_xigua_lx.json 文件名
    elif socket.gethostname() in ['company', 'Mac2.local']:
        data = conf['Windows']['company']['mysql']['local']
        username, password, host, port = data['username'], data['password'], data['host'], data['port']
        service_name = 'company'  # 影响 mysql_types_company.json 文件名
    if not username or not service_name:
        return

    config = {
        'host': host,
        'port': int(port),
        'user': username,
        'password': password,
        'charset': 'utf8mb4',  # utf8mb4 支持存储四字节的UTF-8字符集
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)  # 连接数据库
    with connection.cursor() as cursor:
        sql = "SHOW DATABASES;"
        cursor.execute(sql)
        db_name_lists = cursor.fetchall()
        db_name_lists = [item['Database'] for item in db_name_lists]
        connection.close()

    sys_lists = ['information_schema', 'mysql', 'performance_schema', 'sakila', 'sys']
    db_name_lists = [item for item in db_name_lists if item not in sys_lists]

    results = []  # 返回结果示例: [{'云电影': '电影更新'}, {'生意经3': 'e3_零售明细统计'}]
    for db_ in db_name_lists:
        config.update({'database': db_})  # 添加更新 config 字段
        connection = pymysql.connect(**config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                sql = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_}';"
                sql = "SHOW TABLES;"
                cursor.execute(sql)
                res_tables = cursor.fetchall()
                for res_table in res_tables:
                    for k, v in res_table.items():
                        results.append({db_: v})
        except:
            pass
        finally:
            connection.close()
        time.sleep(0.5)

    d = DataTypes(path=path, service_name=service_name)
    for result in results:
        for db_n, table_n in result.items():
            # print(db_n, table_n, db_name, table_name)
            if db_name and table_name:  # 下载一个指定的数据表
                if db_name != db_n or table_name != table_n:
                    continue
            elif db_name:  # 下载一个数据库的所有数据表
                if db_name != db_n:
                    continue
            # 如果 db_name 和 table_name 都不指定，则下载所有数据库的所有数据表
            print(f'获取列信息 数据库: < {db_n} >, 数据表: < {table_n} >')
            sq = s_query.QueryDatas(username=username, password=password, host=host, port=port)
            # 获取数据表的指定列, 返回列表
            # [{'视频bv号': 'BV1Dm4y1S7BU', '下载进度': 1}, {'视频bv号': 'BV1ov411c7US', '下载进度': 1}]
            name_type = sq.dtypes_to_list(db_name=db_n, table_name=table_n)
            if name_type:
                dtypes = {item['COLUMN_NAME']: item['COLUMN_TYPE'] for item in name_type}
                dtypes = {'mysql': {db_n: {table_n: dtypes}}}
                d.get_mysql_types(
                    dtypes=dtypes,
                    cl='mysql',
                    db_name=db_n,
                    table_name=table_n,
                    is_file_dtype=True  # True表示旧文件有限
                )
            else:
                print(f'数据库回传数据(name_type)为空')
        # print(d.datas)
    d.as_json_file()  # 2024.11.05 改


if __name__ == '__main__':
    # 更新 mysql 中所有数据库的 dtypes 信息到本地 json
    mysql_all_dtypes(
        path='/Users/xigua/Downloads',
    )
