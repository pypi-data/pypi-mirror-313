# -*- coding:utf-8 -*-
import datetime
import os
import re
import warnings
import time
import pandas as pd
import numpy as np
import pymongo
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from mdbq.config import get_myconf
from mdbq.dataframe import converter

warnings.filterwarnings('ignore')


def rename_col(username, password, host, db_name, collection_name, old_name, new_name, port: int = 27017,):
    """ 修改mongodb数据源 某集合的某个字段名 """
    # 连接到MongoDB
    _link = f'mongodb://{username}:{password}@{host}:{port}/'
    client = pymongo.MongoClient(_link)
    db = client[db_name]  # 数据库名
    collection = db[collection_name]  # 集合名

    rename_operation = {"$rename": {old_name: new_name}}  # 修改字段名的操作

    collection.update_many({}, rename_operation)
    if new_name == '日期':
        collection.create_index([(new_name, -1)], background=True)  # 必须, 创建索引


class CreateUser:
    """
    通过python 创建 mongodb 管理员账户
    """
    def __init__(self, username, password, host, port: int = 27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None

        self.db_roles = [{'市场数据2': 'read'}]
        self.user_infos = []  # 现有用户信息
        self.root = False
        self.add_permission = True  # 更新权限时, 默认新增, 设置为False 则减去权限

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @try_except
    def create_user(self):
        """
        role: read(只读), readAnyDatabase(读取所有), readWriteAnyDatabase(读写所有), userAdminAnyDatabase(用户管理权限)

        """

        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        db = self.client['admin']  # 切换到admin数据库
        users = db.system.users.find()  # 获取所有用户
        for user in users:
            self.user_infos.append({user['user']: user['roles']})

        add_roles = []
        for db_role in self.db_roles:
            for key, value in db_role.items():
                add_roles.append({
                    'role': value,
                    'db': key
                })
        # root_roles = ['root'],  # root 权限用户, 正常情况下不要创建 root
        root_roles = [
                {'role': 'userAdminAnyDatabase', 'db': 'admin'},  # 赋予所有数据库的用户管理权限
                {'role': 'readWriteAnyDatabase', 'db': 'admin'}  # 赋予所有数据库的读写权限
            ]

        user_list = []  # 现有用户列表
        i = 0
        for user_info in self.user_infos:
            for key, value in user_info.items():
                user_list.append(key)
                if self.username == key:
                    print(f'{self.username}: 用户已存在, 权限为: {value}')
                    if self.root:
                        print(f'不支持直接升级管理员权限, 请先删除用户再重新创建root角色, 设置 self.root = True ')
                    if self.add_permission:  # 新增权限
                        roles = value + add_roles
                    else:  # 减去权限
                        roles = [item for item in value if item['db'] != add_roles[0]['db']]
                    db.command('updateUser', self.username, roles=roles)  # 更新权限
                    i += 1
                    break
                if self.root:  # 设置超级管理员
                    db.command(command='createUser', value=self.username, pwd=self.password, roles=root_roles)
                    print(f'管理员创建成功: {self.username}, 权限为: {root_roles}')
                    self.client.close()
                    return
            if i > 0:
                self.client.close()
                return
        admin_user = db.command(command='createUser', value=self.username, pwd=self.password, roles=add_roles)
        if admin_user['ok'] > 0:
            print(f'普通用户创建成功: {self.username}, 权限为: {add_roles}')
        self.client.close()

    def delete_user(self):
        """ 删除指定用户: self.username """
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        db = self.client['admin']  # 切换到admin数据库
        users = db.system.users.find()  # 获取所有用户
        for user in users:
            self.user_infos.append({user['user']: user['roles']})

        user_list = []  # 现有用户列表
        i = 0
        for user_info in self.user_infos:
            for key, value in user_info.items():
                user_list.append(key)
                if self.username == key:
                    db.command("dropUser", self.username)
                    print(f'已删除用户: {self.username}')
                    i += 1
        if i == 0:
            print(f'不存在的用户: {self.username}, 无需执行删除操作')
        self.client.close()


class DownMongo:
    """  下载数据 """
    def __init__(self, save_path, username, password, host, port: int = 27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None
        self.db_name = None
        self.collection_name = None
        self.days = 5
        self.start_date = None
        self.end_date = datetime.datetime.now()
        self.save_path = save_path
        self.projection = {'_id': 0}  # 读取数据库指定字段

    def data_to_df(self, db_name, collection_name, projection: dict):
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        self.db_name = db_name
        self.collection_name = collection_name
        collection = self.client[self.db_name][self.collection_name]  # 连接集合
        if not self.start_date:
            self.start_date = datetime.datetime.now() - datetime.timedelta(days=self.days)
            self.end_date = datetime.datetime.now()
        else:
            self.start_date = pd.to_datetime(self.start_date)  # 对日期进行格式化并赋值
            self.end_date = pd.to_datetime(self.end_date)
        # print(self.start_date, '->', self.end_date)

        self.projection.update(projection)  # 指定字段
        pipeline = [
            {'$match': {'日期': {'$gte': self.start_date, '$lte': self.end_date}}},
            {'$project': projection},
        ]
        results = collection.aggregate(pipeline)
        # print(results)
        # 输出结果
        datas = []
        for doc in results:
            # print(doc)
            datas.append(doc)
        if len(datas) == 0:
            return pd.DataFrame()
        df = pd.DataFrame(datas)
        for col in df.columns.tolist():
            if '日期' in col:
                try:
                    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='ignore')  # 转换日期列
                except ValueError as v:
                    print(f'{name}: {v}')
            else:
                df[col] = pd.to_numeric(df[col], errors='ignore').fillna(0)  # 尝试转换数据类型
        # self.client.close()
        return df



    def data_to_file(self, file_type, db_name, collection_name):
        """
        用于 GUI 的函数
        将 mongodb 数据保存本地
        db_name: 数据库名
        collections 集合名
        file_type: 保存的文件类型 csv, json, xlsx, xls
        """
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        self.db_name = db_name
        self.collection_name = collection_name
        _collection = self.client[self.db_name][self.collection_name]  # 连接集合
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        if not self.start_date:
            print(f'{now}正在下载 ({self.host}) {self.db_name}: {self.collection_name}, 区间: 近 {self.days} 天\n...')
        else:
            print(f'{now}正在下载 ({self.host}) {self.db_name}: {self.collection_name}, 区间: {self.start_date}~{self.end_date}')

        if not self.start_date:
            self.start_date = datetime.datetime.now() - datetime.timedelta(days=self.days)
            self.end_date = datetime.datetime.now()
        else:
            self.start_date = pd.to_datetime(self.start_date)  # 对日期进行格式化并赋值
            self.end_date = pd.to_datetime(self.end_date)
        pipeline = [
            {'$match': {'日期': {'$gte': self.start_date, '$lte': self.end_date}}},
            {'$project': {'_id': 0}},  # 不保留 id 字段
        ]
        results = _collection.aggregate(pipeline)

        # 输出结果
        datas = []
        for doc in results:
            datas.append(doc)
        _df = pd.DataFrame(datas)
        if len(_df) == 0:
            print(f'查询的数据量: {len(_df)}, 森么都米有花生')
            self.client.close()
            return
        if '_id' in _df.columns.tolist():
            _df.drop('_id', axis=1, inplace=True)

        print(f'查询的数据量: {len(_df)}')
        cv = converter.DataFrameConverter()
        _df = cv.convert_df_cols(_df)
        s_date = re.findall(r'(\d{4}-\d{2}-\d{2})', str(_df['日期'].values.min()))[0]
        e_date = re.findall(r'(\d{4}-\d{2}-\d{2})', str(_df['日期'].values.max()))[0]
        if not file_type.startswith('.'):
            file_type = '.' + file_type
        _path = os.path.join(self.save_path, f'{self.db_name}_{self.collection_name}_{s_date}_{e_date}{file_type}')
        if file_type.endswith('json'):
            _df.to_json(_path, orient='records', force_ascii=False)
        elif file_type.endswith('csv'):
            _df.to_csv(_path, encoding='utf-8_sig', index=False, header=True)
        elif file_type.endswith('xlsx') or file_type.endswith('xls'):
            _df.to_excel(_path, index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))  # freeze_ 冻结列索引
        else:
            print(f'{file_type}: 未支持的文件类型')
        print(f'<{self.collection_name}> 导出: {_path}, 数据完成！')
        self.client.close()


class UploadMongo:
    """
    上传更新数据库
    目前有两类, 一类上传原始文件, 一类上传pandas数据源
    单独调用 df_to_mongo 方法，最后必须手动关闭数据库连接
    self.drop_duplicates: 原始文件不需要删除旧数据, pandas数据源则应删除旧数据
    """

    def __init__(self, username, password, host, port: int = 27017, drop_duplicates=False):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None
        self.db_name = None  # 上传到数据库时的数据库名
        self.collection_name = None  # 上传到数据库时的集合名, 这个类实际是以文件夹或者文件名作为集合名
        self.data_days = 5  # 更新近期的数据, 不宜过大, 这个参数主要用于 pandas数据源, 其他不要设置
        self.start_date = None
        self.encoding = 'utf-8_sig'
        self.drop_duplicates = drop_duplicates

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @try_except
    def upload_file(self, path):
        if '.DS_Store' in path or '.ini' in path or 'desktop' in path or 'baiduyun' in path or 'xunlei' in path:
            return
        if not path.endswith('csv') or path.endswith('年.csv'):  # 跳过特定文件
            return
        df = pd.read_csv(path, encoding=self.encoding, header=0, na_filter=False)
        if '日期' in df.columns.tolist():
            df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else pd.to_datetime('2099-01-01'))
            self.start_date = pd.to_datetime(datetime.date.today() - datetime.timedelta(days=self.data_days))
            df = df[df['日期'] >= self.start_date]
            if len(df) == 0:
                # 有些跨月报表可能空数据, 所以读取近35天
                df = df[df['日期'] >= pd.to_datetime(datetime.date.today() - datetime.timedelta(35))]
            else:
                df = df[df['日期'] >= self.start_date]  # 选取大于该时间点的数据

        if len(df) == 0:  # 如果依然是空表，则不上传更新
            return
        self.df_to_mongo(df=df)

    @try_except
    def upload_dir(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if str(self.collection_name) not in name:  # 理论上文件夹名必然在文件名中
                    continue
                new_path = os.path.join(root, name)
                self.upload_file(new_path)

    def upload_pandas(self, upload_path, select_files: str = None, skip_files: str = '其他数据'):
        """
        专门用于上传pandas数据源到数据库, 跳过 '其他数据'  or '京东数据集'
        要检查 db_name, 不检查 collection
        select_files: 仅更新此文件
        skip_files: 跳过文件
        """
        if not self.db_name:
            print(f' {self.host}/{self.port}  未设置 self.db_name ')
            return

        pd_files = os.listdir(upload_path)
        for file in pd_files:
            if select_files:
                if select_files not in file:
                    continue
            if skip_files:
                if skip_files in file:
                    continue
            path = os.path.join(upload_path, file)
            if os.path.isfile(path):  # path: 单文件
                self.collection_name = f'{os.path.splitext(file)[0]}_f'
                self.upload_file(path=path)
            elif os.path.isdir(path):  # path: 文件夹
                if '其他数据' in path or '京东数据集' in path:
                    continue  # 跳过的文件夹
                self.collection_name = f'{os.path.splitext(file)[0]}'
                self.upload_dir(path=path)

    @staticmethod
    def split_list(lst, _num=None):
        """
        传入列表，并将其 _num 等分
        """
        length = len(lst)
        if not _num:
            if length > 20000:
                _num = 30
            elif length > 10000:
                _num = 20
            elif length > 1000:
                _num = 15
            elif length > 200:
                _num = 5
            else:
                _num = 2
        if length % _num == 0:
            # print(length, _num)
            sublist_length = length // _num
            return [lst[i:i + sublist_length] for i in range(0, length, sublist_length)]
        else:
            sublist_length = length // _num
            extra = length % _num
            return [lst[i * sublist_length:i * sublist_length + sublist_length] for i in range(_num)] + \
                [lst[-extra:]]  # 添加剩余文档到列表末尾

    @staticmethod
    def duplicates_list(_datas):
        """
        <mongodb> 对传进来的 _datas 排重，数据量大时将消耗大量系统资源
        """
        if len(_datas) > 100 * 1000:
            print(f'数据量太大，可能大量消耗系统资源，谨慎执行!!! {len(_datas)}')
        _my_list = []
        for _data in _datas:
            if _data in _my_list:
                continue
            else:
                _my_list.append(_data)
        return _my_list

    def df_to_mongo(self, df, db_name=None, collection_name=None):
        """
        需要检查 self.db_name 和 self.collection_name
        df: 待插入数据, dataframe 格式
        可以初始化时指定 db_name 和 collection_name 或者在这个函数指定
        """

        if db_name:
            self.db_name = db_name
        if collection_name:
            self.collection_name = collection_name
        if not self.db_name or not self.collection_name:
            print(f'{self.host}/{self.port} 未指定 self.db_name/collection: {self.db_name}/{self.collection_name}')
            return

        self.db_name = re.sub(r'[\',，（）()/=<>+\-*^"’\[\]~#|&% .]', '_', self.db_name)
        self.collection_name = re.sub(r'[\',，（）()/=<>+\-*^"’\[\]~#|&% .]', '_', self.collection_name)
        self.client = pymongo.MongoClient(self.link)
        collections = self.client[self.db_name][self.collection_name]  # 连接数据库
        start_date = None
        end_date = None

        cv = converter.DataFrameConverter()
        df = cv.convert_df_cols(df=df)  # 清理列名中的不合规字符
        if '日期' in df.columns.tolist():
            # df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
            collections.create_index([('日期', -1)], background=True)  # 必须, 创建索引, background 不阻塞
            start_date = pd.to_datetime(df['日期'].values.min())
            end_date = pd.to_datetime(df['日期'].values.max())

        # for col in df.columns.tolist():  # 除日期列外，所有数据类型转为 str 再上传
        #     if '日期' not in col:
        #         df[col] = df[col].astype(str)

        datas = df.to_dict('records')  # 待插入的数据, [dict, dict, ....]

        new_list = self.split_list(datas, )
        # new_list: map 多线程只能传迭代对象，不能直接传其他参数, 所以将 _collection 封装到 list 内
        # new_list: [[_collection, [dict, dict, ...]], [_collection, [dict, dict, ...]]]
        new_list = [[collections, item] for item in new_list]

        def delete_data(data_list):
            """ data_list: [_collection, [dict, dict, ...]]
                delete_many 接受入参是 dict 文档, 所以需要将 data_list 的第二个参数遍历出来 """
            for my_datas in data_list[1]:
                data_list[0].delete_many(my_datas)

        if self.drop_duplicates:
            # 如果有日期列，按日期范围删除旧数据，没有日期，则直接删除旧数据
            if '日期' in df.columns.tolist():
                query = {
                    '日期': {
                        '$gte': start_date,
                        '$lt': end_date + datetime.timedelta(days=1)
                    }
                }
                collections.delete_many(query)
            else:
                with ThreadPoolExecutor() as pool:  # 删除重复数据
                    pool.map(delete_data, new_list)

        def insert_data(data_list):  # insert_many 可以直接传入列表，表中包含一堆 dict
            data_list[0].insert_many(data_list[1])

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        print(f'{now}正在更新 mongoDB ({self.host}:{self.port}) {self.db_name}/{self.collection_name}')

        with ThreadPoolExecutor() as pool:  # 插入新数据
            pool.map(insert_data, new_list)

        self.client.close()  #


class OptimizeDatas:
    """
    数据维护 删除 mongodb 的冗余数据
    更新过程:
    1. 读取所有数据库和集合
    2. 遍历所有集合, 遍历列, 如果存在日期列则按天遍历所有日期, 不存在则全表读取
    3. 按天删除所有冗余数据(存在日期列时)
    tips: 查找冗余数据的方式是创建一个临时迭代器, 逐行读取数据并添加到迭代器, 出现重复时将重复数据的 id 添加到临时列表, 按列表 id 执行删除
    """
    def __init__(self, username: str, password: str, host: str, port: int, drop_duplicates=False):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None
        self.db_name = None  # 数据库名称
        self.db_name_lists = []  # 更新多个数据库 删除重复数据
        self.collection_name = None  # 集合名, 实际应是以文件夹或者文件名作为集合名
        self.days: int = 60  # 处理近 N 天数据
        self.end_date = None
        self.start_date = None

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    # @try_except
    def optimize_list(self):
        """
        更新多个数据库 移除冗余数据
        需要设置 self.db_name_lists
        """
        if not self.db_name_lists:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            print(f'{now}尚未设置参数: self.db_name_lists')
            return
        for db_name in self.db_name_lists:
            self.db_name = db_name
            self.optimize()

    # @try_except
    def my_collection_names(self, db_name) -> list:
        """ 获取指定数据库的所有集合 """
        database_names = self.client.list_database_names()  # 所有数据库名称
        if db_name not in database_names:
            print(f'{self.host}/{self.port} 数据库: {database_names}, 不存在的数据库: {db_name}')
        results = self.client[db_name].list_collection_names()
        return results

    # @try_except
    def optimize(self):
        """ 获取指定集合的数据 """
        if not self.db_name:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            print(f'{now}{self.host}/{self.port} 尚未设置参数: self.db_name')
            return
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        database_names = self.client.list_database_names()  # 所有数据库名称
        if self.db_name not in database_names:
            print(f'{self.host}/{self.port} 当前数据库: {database_names}, 不存在的数据库: {self.db_name}')
            return

        # 日期初始化
        if not self.end_date:
            self.end_date = pd.to_datetime(datetime.datetime.today())
        else:
            self.end_date = pd.to_datetime(self.end_date)
        if self.days:
            self.start_date = pd.to_datetime(self.end_date - datetime.timedelta(days=self.days))
        if not self.start_date:
            self.start_date = self.end_date
        else:
            self.start_date = pd.to_datetime(self.start_date)
        start_date_before = self.start_date
        end_date_before = self.end_date
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        print(f'{now}mongodb({self.host}: {self.port}) {self.db_name} 数据库优化中(日期长度: {self.days} 天)...')

        collections = self.my_collection_names(db_name=self.db_name)  # 所有集合名称
        for collection_name in collections:
            collection = self.client[self.db_name].get_collection(collection_name)
            # 查询集合中是否包含日期列
            has_date_field = collection.find_one({'日期': {'$exists': True}}) is not None
            if not has_date_field:  # 没有日期则全集更新
                self.delete_duplicate2(collection_name=collection_name)
                continue
            pipeline = [
                {"$group": {"_id": None, "min_date": {"$min": "$日期"}, "max_date": {"$max": "$日期"}}}
            ]
            results = collection.aggregate(pipeline)
            for result in results:  # {'_id': None, 'min_date': datetime.datetime(2023, 1, 1, 0, 0)}
                start_date = pd.to_datetime(result['min_date'])  # 当前集合中的最小日期
                end_date = pd.to_datetime(result['max_date'])  # 当前集合中的最大日期
                if self.start_date < start_date:  # 匹配修改为合适的起始和结束日期
                    self.start_date = start_date
                if self.end_date > end_date:
                    self.end_date = end_date
                break
            # print(collection_name, self.start_date, start_date, self.end_date, end_date)
            dates_list = self.day_list(start_date=self.start_date, end_date=self.end_date)
            for date in dates_list:
                self.delete_duplicate(collection_name=collection_name, date=date)
            self.start_date = start_date_before  # 重置，不然日期错乱
            self.end_date = end_date_before

        # self.client.close()  # 断开连接
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        print(f'{now}mongodb({self.host}: {self.port}) {self.db_name} 数据库优化完成!')

    def delete_duplicate(self, collection_name, date,):
        """ 更新数据 集合中有日期列的情况 """
        collection = self.client[self.db_name].get_collection(collection_name)
        pipeline = [
            {'$match': {'日期': {'$gte': date, '$lte': date}}},
            # {'$project': {'_id': 0}},  # 不保留 id 字段
        ]
        docs = collection.aggregate(pipeline)
        datas = []
        for doc in docs:
            datas.append(doc)
        duplicate_id = []  # 出现重复的 id
        all_datas = []  # 迭代器
        for data in datas:
            delete_id = data['_id']
            del data['_id']
            data = re.sub(r'\.0+\', ', '\', ', str(data))  # 统一移除小数点后面的 0
            if data in all_datas:  # 数据出现重复时
                duplicate_id.append(delete_id)  # 添加 id 到 duplicate_id
                continue
            all_datas.append(data)  # 数据没有重复
        del all_datas

        if not duplicate_id:  # 如果没有重复数据，则跳过
            return
        collection.delete_many({'_id': {'$in': duplicate_id}})
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        print(f'{now}{collection_name} -> {date.strftime("%Y-%m-%d")} '
              f'before: {len(datas)}, remove: {len(duplicate_id)}')

    def delete_duplicate2(self, collection_name,):
        """ 更新数据 正常按日期逐天检查，如果没有日期列的情况"""
        collection = self.client[self.db_name].get_collection(collection_name)
        docs = collection.find({})
        datas = []
        for doc in docs:
            datas.append(doc)
        duplicate_id = []  # 出现重复的 id
        all_datas = []  # 迭代器
        for data in datas:
            delete_id = data['_id']
            del data['_id']
            data = re.sub(r'\.0+\', ', '\', ', str(data))  # 统一移除小数点后面的 0
            if data in all_datas:  # 数据出现重复时
                duplicate_id.append(delete_id)  # 添加 id 到 duplicate_id
                continue
            all_datas.append(data)  # 数据没有重复
        del all_datas

        if not duplicate_id:  # 如果没有重复数据，则跳过
            return
        collection.delete_many({'_id': {'$in': duplicate_id}})
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        print(f'{now}{collection_name} -> before: {len(datas)}, remove: {len(duplicate_id)}')

    def get_collection_datas_bak(self, db_name, collection_name):
        database_names = self.client.list_database_names()  # 所有数据库名称
        if db_name not in database_names:
            print(f'{self.host}/{self.port} 当前数据库: {database_names}, 不存在的数据库: {db_name}')
        collection = self.client[self.db_name].get_collection(collection_name)
        batch_size = 1000  # 设置批次大小
        cursor = collection.find().batch_size(batch_size)  # 获取游标
        results = []
        for doc in cursor:
            results.append(doc)
        return results

    def day_list(self, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        date_list = []
        while start_date <= end_date:
            date_list.append(pd.to_datetime(start_date.date()))
            start_date += datetime.timedelta(days=1)
        return date_list

    def rename_column(self):
        """ 批量修改数据库的列名 """
        """
        # for db_name in ['京东数据2', '推广数据2', '市场数据2', '生意参谋2', '生意经2', '属性设置2',]:
        #     s = OptimizeDatas(username=username, password=password, host=host, port=port)
        #     s.db_name = db_name
        #     s.rename_column()
        #     s.client.close()
        """
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        database_names = self.client.list_database_names()  # 所有数据库名称
        collections = self.my_collection_names(db_name=self.db_name)  # 所有集合名称
        for collection_name in collections:
            collection = self.client[self.db_name].get_collection(collection_name)
            has_date_field = collection.find_one({})
            for key, value in has_date_field.items():
                if key.endswith('_'):
                    new_name = re.sub(r'_+$', '', key)
                    query = {key: {'$exists': True}}
                    update = {'$rename': {key: new_name}}
                    collection.update_many(query, update)


def upload_one_dir():
    username, password, host, port = get_myconf.select_config_values(target_service='home_lx', database='mongodb')
    p = UploadMongo(username=username, password=password, host=host, port=port, drop_duplicates=False)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    print(f'{now}数据处理中...')

    p.db_name = ''
    p.collection_name = f''
    path = os.path.join('C:\\同步空间', 'BaiduSyncdisk', '原始文件2', r'京东报表', 'JD流量来源')

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if '按天_' not in name:
                continue
            if name.endswith('.csv') and 'baidu' not in name:
                df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                for col in df.columns.tolist():
                    if '日期' in col:
                        df[col] = df[col].apply(lambda x: pd.to_datetime(x) if x else pd.to_datetime('2099-01-01'))
                p.df_to_mongo(df=df)
    if p.client:
        p.client.close()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    print(f'{now}数据完成!')


def main():
    pass


if __name__ == '__main__':
    # main()
    username, password, host, port = get_myconf.select_config_values(target_service='home_lx', database='mongodb')
    print(username, password, host, port)

    # for db_name in [
    #         '京东数据2',
    #         '推广数据2',
    #         '市场数据2',
    #         '生意参谋2',
    #         '生意经2',
    #         '属性设置2',
    #     ]:
    #     s = OptimizeDatas(username=username, password=password, host=host, port=port)
    #     s.db_name = db_name
    #     s.rename_column()
    # s.client.close()
