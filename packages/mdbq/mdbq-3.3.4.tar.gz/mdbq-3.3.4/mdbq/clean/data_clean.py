# -*- coding:utf-8 -*-
import warnings
import pandas as pd
from functools import wraps
import chardet
import zipfile
from pyzipper import PyZipFile
import os
import platform
import pathlib
import json
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.config import get_myconf
import datetime
import time
import re
import shutil
import getpass

warnings.filterwarnings('ignore')


class DataClean:
    """ 数据分类 """

    def __init__(self, path, source_path):
        self.path = path
        self.source_path = source_path
        self.set_up_to_mogo: bool = True  # 不设置则不上传 mongodb
        self.set_up_to_mysql: bool = True  # 不设置则不上传 mysql

    def __call__(self, *args, **kwargs):
        self.new_unzip(path=self.path, is_move=True)  # 解压文件
        self.change_and_sort(path=self.path)

        self.move_all(path=self.path)  # 移到文件到原始文件夹
        self.attribute(path=self.path)  # 商品素材重命名和分类

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @staticmethod
    def get_encoding(file_path):
        """
        获取文件的编码方式, 读取速度比较慢，非必要不要使用
        """
        with open(file_path, 'rb') as f:
            f1 = f.read()
            encod = chardet.detect(f1).get('encoding')
        return encod

    @staticmethod
    def save_to_csv(_df, _save_paths, filenames, encoding='utf-8_sig'):
        if '.csv' not in filenames:
            filenames = f'{filenames}.csv'
        if not os.path.exists(_save_paths):
            os.makedirs(_save_paths, exist_ok=True)
        _df.to_csv(os.path.join(_save_paths, filenames), encoding=encoding, index=False, header=True)

    # @try_except
    def change_and_sort(self, path=None, is_except=[]):
        """数据转换"""
        if not path:
            path = self.path

        if self.set_up_to_mogo:
            username, password, host, port = get_myconf.select_config_values(target_service='home_lx',
                                                                             database='mongodb')
            d = mongo.UploadMongo(username=username, password=password, host=host, port=port,
                                         drop_duplicates=False
                                         )
        if self.set_up_to_mysql:
            username, password, host, port = get_myconf.select_config_values(target_service='home_lx', database='mysql')
            m = mysql.MysqlUpload(username=username, password=password, host=host, port=port)

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue

                is_continue = False
                if is_except:
                    for item in is_except:
                        if item in os.path.join(root, name):
                            # print(name)
                            is_continue = True
                            break
                if is_continue:  # 需要排除不做处理的文件或文件夹
                    continue

                try:
                    encoding = self.get_encoding(file_path=pathlib.Path(root, name))
                    # ----------------- 推广报表 分割线 -----------------
                    tg_names = [
                        '账户报表',  # 旧版，后来改成 营销场景报表了，C 店还是旧版
                        '营销场景报表',
                        '计划报表',
                        '单元报表',
                        '关键词报表',
                        '人群报表',
                        '主体报表',
                        '其他主体报表',
                        '创意报表',
                        '地域报表',
                        '权益报表',
                    ]
                    for tg_name in tg_names:
                        if tg_name in name and '汇总' not in name and name.endswith('.csv'):  # 人群报表排除达摩盘报表： 人群报表汇总
                            pattern = re.findall(r'(.*_)\d{8}_\d{6}', name)
                            if not pattern:  # 说明已经转换过
                                continue
                            shop_name = re.findall(r'\d{8}_\d{6}_(.*)\W', name)
                            if shop_name:
                                shop_name = shop_name[0]
                            else:
                                shop_name = ''
                            df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                            if '地域' not in name:  # 除了地域报表, 检查数据的字段是否包含“场景名字”,如果没有,说明没有选“pbix” 数据模块下载
                                ck = df.columns.tolist()
                                if '场景名字' not in ck:
                                    print(f'{name} 报表字段缺失, 请选择Pbix数据模板下载')
                                    continue
                            if len(df) == 0:
                                print(f'{name} 报表是空的, 请重新下载, 此报表已移除')
                                os.remove(os.path.join(root, name))
                                continue

                            df.replace(to_replace=['\\N'], value=0, regex=False, inplace=True)  # 替换掉特殊字符
                            df.fillna(0, inplace=True)
                            col_ids = [
                                # '场景ID',  # 2024.10.5 改为不加 =""
                                '计划ID',
                                '单元ID',
                                '主体ID',
                                '宝贝ID',
                                '词ID/词包ID',
                                '创意ID',
                            ]
                            sb = df.columns.tolist()
                            if '日期' not in sb:
                                print(f'{name} 注意：该报表不包含分日数据，数据不会保存，请重新下载！')
                                continue
                            if '省' in sb:
                                if '市' not in sb:
                                    print(
                                        f'{name} 注意：请下载市级地域报表，而不是省报表，数据不会保存，请重新下载！')
                                    continue
                            for col_id in col_ids:
                                if col_id in sb:
                                    df[col_id] = df[col_id].apply(
                                        lambda x: f'="{x}"' if x and '=' not in str(x) else x
                                    )
                            date_min = f'_{df["日期"].values.min()}_'
                            date_max = f'{df["日期"].values.max()}.csv'
                            if '万里马' in name:
                                tm_s_name = pattern[0] + shop_name + date_min + date_max
                                if shop_name == '广东万里马':
                                    new_root_p = pathlib.Path(self.source_path, '推广报表_淘宝店', tg_name)  # 文件夹，未包括文件名
                                else:
                                    new_root_p = pathlib.Path(self.source_path, '推广报表', tg_name)  # 文件夹，未包括文件名
                                df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                                if '省' in df.columns.tolist() and '场景名字' in df.columns.tolist() and '完整' in name:
                                    if shop_name == '广东万里马':
                                        new_root_p = pathlib.Path(self.source_path, '推广报表_淘宝店', f'完整_{tg_name}')
                                    else:
                                        new_root_p = pathlib.Path(self.source_path, '推广报表', f'完整_{tg_name}')
                                    tm_s_name = f'完整_{tm_s_name}'
                                self.save_to_csv(df, new_root_p, tm_s_name)
                                # if self.set_up_to_mogo:
                                #     d.df_to_mongo(df=df, db_name='天猫数据1', collection_name=f'天猫_推广_{tg_name}')
                                # if self.set_up_to_mysql:
                                #     m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name=f'天猫_推广_{tg_name}')
                                os.remove(os.path.join(root, name))
                            else:
                                print(f'{name} 文件名不含"万里马", 不属于爬虫下载，您可以手动进行分类，但不会上传数据库')

                    if name.endswith('.csv') and '超级直播' in name:
                        # 超级直播
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        pattern = re.findall(r'(.*_)\d{8}_\d{6}', name)
                        shop_name = re.findall(r'\d{8}_\d{6}_(.*)\W', name)
                        if shop_name:
                            shop_name = shop_name[0]
                        else:
                            shop_name = ''
                        cols = [
                            # '场景ID',  # 2024.10.5 改为不加 =""
                            '计划ID',
                        ]
                        for col in cols:
                            df[col] = df[col].apply(lambda x: f'="{x}"' if x and '=' not in str(x) else x)
                        df.replace(to_replace=['\\N'], value=0, regex=False, inplace=True)  # 替换掉特殊字符
                        root_new = pathlib.Path(self.source_path, '推广报表', '超级直播')
                        date_min = f'_{df["日期"].values.min()}_'  # 仅适用于日期列未转换之前, 还是整数，转换后不能用这个函数
                        date_max = f'{df["日期"].values.max()}.csv'
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        new_name = pattern[0] + shop_name + date_min + date_max
                        self.save_to_csv(df, root_new, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='天猫_推广_超级直播')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='天猫_推广_超级直播')
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.xls') and '短直联投' in name:
                        # 短直联投
                        df = pd.read_excel(os.path.join(root, name), sheet_name=None, header=0)
                        df = pd.concat(df)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        new_name2 = os.path.splitext(name)[0] + '.csv'
                        df['订单Id'] = df['订单Id'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        root_new = pathlib.Path(self.source_path, '推广报表/短直联投')
                        self.save_to_csv(df, root_new, new_name2)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='天猫_推广_短直联投')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='天猫_推广_短直联投')
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.xls') and '视频加速推广' in name:
                        # 超级短视频
                        df = pd.read_excel(os.path.join(root, name), sheet_name=None, header=0)
                        df = pd.concat(df)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        new_name2 = os.path.splitext(name)[0] + '.csv'
                        df['计划ID'] = df['计划ID'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        df['视频id'] = df['视频id'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        root_new = pathlib.Path(self.source_path, '推广报表/超级短视频')
                        self.save_to_csv(df, root_new, new_name2)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='天猫_推广_超级短视频')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='天猫_推广_超级短视频')
                        os.remove(os.path.join(root, name))
                    if '人群报表汇总' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=1, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        min_clm = df.min()['日期']
                        max_clm = df.max()['日期']
                        new_name = '{}{}{}'.format(min_clm, '_', max_clm)
                        df['点击率'] = df['点击率'].apply(lambda x: format(x, '.2%') if x > 0 else '')  # 格式化成百分比
                        df['UV点击率'] = df['UV点击率'].apply(lambda x: format(x, '.2%') if x > 0 else '')
                        df['收藏加购率'] = df['收藏加购率'].apply(lambda x: format(x, '.2%') if x > 0 else '')
                        df['UV收藏加购率'] = df['UV收藏加购率'].apply(lambda x: format(x, '.2%') if x > 0 else '')
                        df['点击转化率'] = df['点击转化率'].apply(lambda x: format(x, '.2%') if x > 0 else '')
                        df['UV点击转化率'] = df['UV点击转化率'].apply(lambda x: format(x, '.2%') if x > 0 else '')
                        df.replace(to_replace=[0], value='', regex=False, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        df.to_csv(os.path.join(self.path, 'DMP报表_' + new_name + '.csv'), encoding='utf-8_sig',
                                  index=False, header=True)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='天猫_达摩盘_DMP报表',)
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='天猫_达摩盘_DMP报表')
                        os.remove(os.path.join(root, name))
                    # ----------------- 推广报表 分割线 -----------------
                    # ----------------- 推广报表 分割线 -----------------

                    date01 = re.findall(r'(\d{4}-\d{2}-\d{2})_\d{4}-\d{2}-\d{2}', str(name))
                    date02 = re.findall(r'\d{4}-\d{2}-\d{2}_(\d{4}-\d{2}-\d{2})', str(name))
                    if name.endswith('.xls') and '生意参谋' in name and '无线店铺流量来源' in name:
                        # 无线店铺流量来源
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=5)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        if date01[0] != date02[0]:
                            data_lis = date01[0] + '_' + date02[0]
                            df.insert(loc=0, column='数据周期', value=data_lis)
                        df.insert(loc=0, column='日期', value=date01[0])
                        # 2024-2-19 官方更新了推广渠道来源名称
                        # df['三级来源'] = df['三级来源'].apply(
                        #     lambda x: '精准人群推广' if x == '精准人群推广(原引力魔方)'
                        #     else '关键词推广' if x == '关键词推广(原直通车)'
                        #     else '智能场景' if x == '智能场景(原万相台)'
                        #     else x
                        # )
                        df['三级来源'] = df['三级来源'].apply(
                            lambda x: re.sub('(.*)', '', str(x) if x else x)
                        )
                        # df = df[df['访客数'] != '0']
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        for col in df.columns.tolist():
                            df[col] = df[col].apply(lambda x: 0 if not x else 0 if x == '' else x)
                        if '经营优势' in df['一级来源'].tolist():  # 新版流量
                            new_name = re.sub(r'\s?\(.*\)', '', new_name)  # 删除小括号
                            new_name = os.path.splitext(new_name)[0] + '_新版.csv'

                        self.save_to_csv(df, root, new_name)  # 因为 mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if '经营优势' in df['一级来源'].tolist():  # 新版流量
                            if '数据周期' in df.columns.tolist():
                                if self.set_up_to_mogo:
                                    d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_店铺来源_月数据')
                                if self.set_up_to_mysql:
                                    m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_店铺来源_月数据')
                            else:
                                if self.set_up_to_mogo:
                                    d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_店铺来源_日数据')
                                if self.set_up_to_mysql:
                                    m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_店铺来源_日数据')
                        else:  # 旧版流量
                            if '数据周期' in df.columns.tolist():
                                if self.set_up_to_mogo:
                                    d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_店铺来源_月数据_旧版')
                                if self.set_up_to_mysql:
                                    m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_店铺来源_月数据_旧版')
                            else:
                                if self.set_up_to_mogo:
                                    d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_店铺来源_日数据_旧版')
                                if self.set_up_to_mysql:
                                    m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_店铺来源_日数据_旧版')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '生意参谋' in name and '无线店铺三级流量来源详情' in name:
                        # 店铺来源，手淘搜索，关键词
                        pattern = re.findall(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', name)
                        df = pd.read_excel(os.path.join(root, name), header=5)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            continue
                        df.replace(to_replace=[','], value='', regex=True, inplace=True)
                        df.insert(loc=0, column='日期', value=pattern[0][1])
                        df.rename(columns={
                            '来源名称': '关键词',
                            '收藏商品-支付买家数': '收藏商品_支付买家数',
                            '加购商品-支付买家数': '加购商品_支付买家数',
                        }, inplace=True)
                        if pattern[0][0] != pattern[0][1]:
                            data_lis = pattern[0][0] + '_' + pattern[0][1]
                            df.insert(loc=1, column='数据周期', value=data_lis)
                        new_name = os.path.splitext(name)[0] + '.csv'
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '生意参谋' in name and '商品_全部' in name:
                        # 店铺商品排行
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=4)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        df['商品ID'] = df['商品ID'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        df['货号'] = df['货号'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        df.rename(columns={'统计日期': '日期', '商品ID': '商品id'}, inplace=True)
                        if date01[0] != date02[0]:
                            data_lis = date01[0] + '_' + date02[0]
                            df.insert(loc=1, column='数据周期', value=data_lis)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_商品排行')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_商品排行')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '参谋店铺整体日报' in name:
                        # 自助取数，店铺日报
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=7)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={'统计日期': '日期'}, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='生意参谋2', collection_name='生意参谋_自助取数_整体日报')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_自助取数_整体日报')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '参谋每日流量_自助取数_新版' in name:
                        # 自助取数，每日流量
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=7)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={'统计日期': '日期'}, inplace=True)
                        # 2024-2-19 官方更新了推广渠道来源名称，自助取数没有更新，这里强制更改
                        df['三级来源'] = df['三级来源'].apply(
                            lambda x: '精准人群推广' if x == '引力魔方'
                            else '关键词推广' if x == '直通车'
                            else '智能场景' if x == '万相台'
                            else '精准人群推广' if x == '精准人群推广(原引力魔方)'
                            else '关键词推广' if x == '关键词推广(原直通车)'
                            else '智能场景' if x == '智能场景(原万相台)'
                            else x
                        )
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_自助取数_每日流量')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_自助取数_每日流量')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '商品sku' in name:
                        # 自助取数，商品sku
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=7)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={
                            '统计日期': '日期',
                            '商品ID': '商品id',
                            'SKU ID': 'sku id',
                            '商品SKU': '商品sku',
                        }, inplace=True)
                        for _i in ['商品id', 'sku id']:
                            df[_i] = df[_i].astype(str).apply(lambda x: f'="{x}"')
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_自助取数_商品sku')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_自助取数_商品sku')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '参谋店铺流量来源（月）' in name:
                        # 自助取数，月店铺流量来源
                        new_name = os.path.splitext(name)[0] + '.csv'
                        df = pd.read_excel(os.path.join(root, name), header=7)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={'统计日期': '数据周期'}, inplace=True)
                        # 2024-2-19 官方更新了推广渠道来源名称，自助取数没有更新，这里强制更改
                        df['三级来源'] = df['三级来源'].apply(
                            lambda x: '精准人群推广' if x == '引力魔方'
                            else '关键词推广' if x == '直通车'
                            else '智能场景' if x == '万相台'
                            else '精准人群推广' if x == '精准人群推广(原引力魔方)'
                            else '关键词推广' if x == '关键词推广(原直通车)'
                            else '智能场景' if x == '智能场景(原万相台)'
                            else x
                        )
                        df['日期'] = df['数据周期'].apply(lambda x: re.findall('(.*) ~', x)[0])
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_自助取数_店铺流量_月数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_自助取数_店铺流量_月数据')
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.xlsx') and '直播分场次效果' in name:
                        pattern = re.findall(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', name)
                        if pattern:
                            continue
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            continue
                        df.replace(to_replace=['--'], value='0', regex=False, inplace=True)
                        df.replace(to_replace=[','], value='', regex=True, inplace=True)
                        df['直播开播时间'] = pd.to_datetime(df['直播开播时间'], format='%Y-%m-%d %H:%M:%S', errors='ignore')
                        df.insert(loc=0, column='日期', value=df['直播开播时间'])
                        df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(str(x).split(' ')[0], format='%Y-%m-%d', errors='ignore') if x else x)
                        df.insert(loc=1, column='店铺', value='万里马官方旗舰店')
                        min_clm = str(df.min()['直播开播时间']).split(' ')[0]
                        max_clm = str(df.max()['直播开播时间']).split(' ')[0]
                        new_name = f'{os.path.splitext(name)[0]}_{min_clm}_{max_clm}.csv'
                        new_name = re.sub(r' ?(\(\d+\))', '',new_name)
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.csv') and '分天数据-计划_活动类型-推广概览-数据汇总' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        df['日期'].replace(to_replace=['\\t'], value='', regex=True, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        min_clm = str(df['日期'].min()).split(' ')[0]
                        max_clm = str(df['日期'].max()).split(' ')[0]
                        new_name = f'淘宝联盟_分天数据_计划_活动类型_推广概览_数据汇总_{min_clm}_{max_clm}'
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.csv') and 'baobei' in name:
                        # 生意经宝贝指标日数据
                        # print(name)
                        date = re.findall(r's-(\d{4})(\d{2})(\d{2})\.', str(name))
                        if not date:  # 阻止月数据及已转换的表格
                            print(f'{name}  不支持或是已转换的表格')
                            os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                            continue
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        if '日期' in df.columns.tolist():
                            df.pop('日期')
                        new_date = '-'.join(date[0])
                        df.insert(loc=0, column='日期', value=new_date)
                        df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                        df['宝贝ID'] = df['宝贝ID'].apply(
                            lambda x: f'="{x}"' if x and '=' not in str(x) else x
                        )
                        df['商家编码'] = df['商家编码'].apply(
                            lambda x: f'="{x}"' if x and '=' not in str(x) else x
                        )
                        name_st = re.findall(r'(.*)\d{4}\d{2}\d{2}\.', str(name))  # baobeitrans-
                        new_name = f'{name_st[0]}{new_date}.csv'
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意经1', collection_name='生意经_宝贝指标')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意经1', tabel_name='生意经_宝贝指标')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.csv') and '店铺销售指标' in name:
                        # 生意经, 店铺指标，仅限月数据，实际日指标也可以
                        name_st = re.findall(r'(.*)\(分日', name)
                        if not name_st:
                            print(f'{name}  已转换的表格')
                            continue
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df['日期'] = df['日期'].astype(str).apply(
                            lambda x: '-'.join(re.findall(r'(\d{4})(\d{2})(\d{2})', x)[0]) if x else x)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
                        # min_clm = str(df.min()['日期']).split(' ')[0]
                        # max_clm = str(df.max()['日期']).split(' ')[0]
                        min_clm = str(df['日期'].min()).split(' ')[0]
                        max_clm = str(df['日期'].max()).split(' ')[0]
                        new_name = f'{name_st[0]}-{min_clm}_{max_clm}.csv'  # 保存时将(分日)去掉
                        df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意经1', collection_name='生意经_店铺指标')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意经1', tabel_name='生意经_店铺指标')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('csv') and '省份' in name:
                        # 生意经，地域分布, 仅限日数据
                        pattern = re.findall(r'(.*[\u4e00-\u9fa5])(\d{4})(\d{2})(\d{2})\.', name)
                        if not pattern or '省份城市分析2' not in name:
                            print(f'{name}  不支持或已转换的表格')
                            os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                            continue
                        date = pattern[0][1:]
                        date = '-'.join(date)
                        new_name = f'{pattern[0][0]}-{date}.csv'
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df['省'] = df['省份'].apply(lambda x: x if ' ├─ ' not in x and ' └─ ' not in x else None)
                        df['城市'] = df[['省份', '省']].apply(lambda x: '汇总' if x['省'] else x['省份'], axis=1)
                        df['省'].fillna(method='ffill', inplace=True)
                        df['城市'].replace(to_replace=[' ├─ | └─ '], value='', regex=True, inplace=True)
                        pov = df.pop('省')
                        city = df.pop('城市')
                        df['省+市'] = df['省份']
                        df['省份'] = pov
                        df.insert(loc=1, column='城市', value=city)
                        df.insert(loc=0, column='日期', value=date)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意经1', collection_name='生意经_地域分布_省份城市分析')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意经1', tabel_name='生意经_地域分布_省份城市分析')
                        os.remove(os.path.join(root, name))  # 移除已转换的原文件

                    elif name.endswith('csv') and 'order' in name:
                        # 生意经，订单数据，仅限月数据
                        pattern = re.findall(r'(.*)(\d{4})(\d{2})(\d{2})-(\d{4})(\d{2})(\d{2})', name)
                        if not pattern:
                            print(f'{name}  不支持或已转换的表格')
                            os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                            continue
                        date1 = pattern[0][1:4]
                        date1 = '-'.join(date1)
                        date2 = pattern[0][4:]
                        date2 = '-'.join(date2)
                        date = f'{date1}_{date2}'
                        new_name = f'{pattern[0][0]}{date}.csv'
                        df = pd.read_csv(os.path.join(root, name), encoding='gb18030', header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.insert(loc=0, column='日期', value=date1)
                        df.insert(loc=1, column='数据周期', value=date)
                        df['商品id'] = df['宝贝链接'].apply(
                            lambda x: f'=\"{"".join(re.findall("id=(.*)", str(x))[0])}\"' if x else x)
                        df.rename(columns={'宝贝标题': '商品标题', '宝贝链接': '商品链接'}, inplace=True)
                        df['颜色编码'] = df['商家编码'].apply(
                            lambda x: ''.join(re.findall(r' .*(\d{4})$', str(x))) if x else x)
                        df['商家编码'] = df['商家编码'].apply(lambda x: f'="{x}"' if x else x)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意经1', collection_name='生意经_订单数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意经1', tabel_name='生意经_订单数据')
                        os.remove(os.path.join(root, name))  # 移除已转换的原文件

                    elif name.endswith('.xlsx') and '直播间成交订单明细' in name:
                        # 直播间成交订单明细
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={'场次ID': '场次id', '商品ID': '商品id'}, inplace=True)
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        cols = ['开播时间', '下单时间', '支付时间', '确认收货时间']
                        for col in cols:
                            df[col] = pd.to_datetime(df[col])  # 转换日期列
                        for col2 in ['支付金额', '确认收货金额']:
                            df[col2] = pd.to_numeric(df[col2], errors='ignore')
                        df['日期'] = df['支付时间'].apply(lambda x: x.strftime('%Y-%m-%d'))
                        date_min = df['日期'].values.min() + '_'
                        date_max = df['日期'].values.max()
                        new_name = '直播间成交订单明细_' + date_min + date_max + '.csv'
                        for col3 in ['场次id', '商品id', '父订单', '子订单']:
                            df[col3] = df[col3].apply(
                                lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                            )
                        col4 = ['日期', '直播标题', '开播时间', '场次id', '支付时间', '支付金额', '商品id', '商品标题',
                                '商品一级类目', '父订单', '子订单', '下单时间', '确认收货时间', '确认收货金额']
                        df_lin = df[col4]
                        # 调整列顺序
                        df = pd.merge(df_lin, df, how='outer', on=col4)
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_直播间成交订单明细')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_直播间成交订单明细')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '直播间大盘数据' in name:
                        # 直播间大盘数据
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        df.rename(columns={'统计日期': '日期'}, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        df['日期'] = df['日期'].apply(lambda x: x.strftime('%Y-%m-%d'))
                        date_min = df['日期'].values.min() + '_'
                        date_max = df['日期'].values.max()
                        new_name = '直播间大盘数据_' + date_min + date_max + '.csv'
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_直播间大盘数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_直播间大盘数据')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '直播业绩-成交拆解' in name:
                        # 直播业绩-成交拆解
                        df = pd.read_excel(os.path.join(root, name), header=5)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        df.replace(to_replace=[','], value='', regex=True, inplace=True)
                        df.rename(columns={'统计日期': '日期'}, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        df['日期'] = df['日期'].apply(lambda x: x.strftime('%Y-%m-%d'))
                        date_min = df['日期'].values.min() + '_'
                        date_max = df['日期'].values.max()
                        new_name = '直播业绩_成交拆解_' + date_min + date_max + '.csv'
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意参谋2', collection_name='生意参谋_直播业绩')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意参谋2', tabel_name='生意参谋_直播业绩')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '明星店铺' in name:
                        # 品销宝
                        pattern = re.findall(r'_(\d{4}-\d{2}-\d{2})_', name)
                        if pattern:
                            continue
                        sheets4 = ['账户', '推广计划', '推广单元', '创意', '品牌流量包', '定向人群']  # 品销宝
                        file_name4 = os.path.splitext(name)[0]  # 明星店铺报表
                        for sheet4 in sheets4:
                            df = pd.read_excel(os.path.join(root, name), sheet_name=sheet4, header=0, engine='openpyxl')
                            # print(sheet4)
                            if len(df) == 0:
                                print(f'{name} 报表数据为空')
                                os.remove(os.path.join(root, name))
                                continue
                            if len(df) < 1:
                                print(f'{name} 跳过')
                                continue
                            else:
                                df.insert(loc=1, column='报表类型', value=sheet4)
                                df.fillna(0, inplace=True)
                                df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
                                min_clm = str(df['日期'].min()).split(' ')[0]
                                max_clm = str(df['日期'].max()).split(' ')[0]
                                new_file_name4 = f'{sheet4}_{file_name4}_{min_clm}_{max_clm}.csv'
                                # 以sheet名进一步创建子文件夹
                                root_new = str(pathlib.Path(self.source_path, '推广报表/品销宝', sheet4))
                                self.save_to_csv(df, root_new, new_file_name4)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                                if self.set_up_to_mogo:
                                    d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='天猫_推广_品销宝')
                                if self.set_up_to_mysql:
                                    m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='天猫_推广_品销宝')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.csv') and '淘宝店铺数据' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='市场数据1', collection_name='淘宝店铺数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='市场数据1', tabel_name='淘宝店铺数据')

                    elif name.endswith('.csv') and '人群洞察' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                        df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                        df = df[df['人群规模'] != '']
                        if len(df) == 0:
                            os.remove(os.path.join(root, name))
                            print(f'{name}: 数据为空, 已移除: {os.path.join(root, name)}')
                            continue
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='天猫数据1', collection_name='万相台_人群洞察')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='天猫数据1', tabel_name='万相台_人群洞察')

                    # ----------------------- 京东数据处理分界线 -----------------------
                    elif name.endswith('.csv') and '关键词点击成交报表_pbix同步_勿删改' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                        for col in df.columns.tolist():
                            if '（' in col:
                                new_col = re.sub('[（）]', '_', col)
                                new_col = new_col.strip('_')
                                df.rename(columns={col: new_col}, inplace=True)
                        df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        min_clm = str(df['日期'].min()).split(' ')[0]
                        max_clm = str(df['日期'].max()).split(' ')[0]
                        new_name = f'京东推广关键词点击成交报表_{min_clm}_{max_clm}.csv'
                        self.save_to_csv(df, root, new_name)
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.csv') and '营销概况_全站营销' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=1, na_filter=False)
                        df = df[(df['日期'] != '日期') & (df['日期'] != '汇总') & (df['日期'] != '0') & (df['花费'] != '0') & (df['花费'] != '0.00')]
                        df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                        df.drop("'当前时间'", axis=1, inplace=True)
                        df.rename(columns={'全站ROI': '全站roi'}, inplace=True)
                        df.insert(loc=1, column='产品线', value='全站营销')
                        new_name = re.sub('至', '_', name)
                        self.save_to_csv(df, root, new_name)
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.xlsx') and '店铺来源_流量来源' in name:
                        # 京东店铺来源
                        if '按天' not in name:
                            print(f'{name} 京东流量请按天下载')
                            continue
                        new_name = name.split(r'__20')[0]
                        date01 = re.findall(r'(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2})', str(name))
                        new_date01 = f'{date01[0][0]}-{date01[0][1]}-{date01[0][2]}'
                        new_date02 = f'{date01[0][3]}-{date01[0][4]}-{date01[0][5]}'
                        new_date03 = f'{new_date01}_{new_date02}'
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        df.insert(loc=0, column='日期', value=new_date01)
                        if new_date01 != new_date02:
                            df.insert(loc=1, column='数据周期', value=new_date03)
                        cols = df.columns.tolist()
                        if '三级来源' in cols:
                            source = '三级来源'
                        elif '二级来源' in cols:
                            source = '二级来源'
                        else:
                            source = '一级来源'

                        new_name = f'{new_name}_{source}_{new_date03}.csv'
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name)  # csv 文件仍然保留这些列
                        for col_2024 in cols:  # 京东这个表有字段加了去年日期，删除这些同比数据字段，不然列数量爆炸
                            if '20' in col_2024 and '流量来源' in name:
                                df.drop(col_2024, axis=1, inplace=True)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_流量来源_日数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_流量来源_日数据')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '全部渠道_商品明细' in name:
                        # 京东商品明细 文件转换
                        date1 = re.findall(r'_(\d{4})(\d{2})(\d{2})_全部', str(name))
                        if not date1[0]:
                            print(f'{name}: 仅支持日数据')
                            continue
                        if date1:
                            date1 = f'{date1[0][0]}-{date1[0][1]}-{date1[0][2]}'
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        if '10035975359247' in df['商品ID'].values or '10056642622343' in df['商品ID'].values:
                            new_name = f'sku_{date1}_全部渠道_商品明细.csv'
                        elif '10021440233518' in df['商品ID'].values or '10022867813485' in df['商品ID'].values:
                            new_name = f'spu_{date1}_全部渠道_商品明细.csv'
                        else:
                            new_name = f'未分类_{date1}_全部渠道_商品明细.csv'
                        df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                        df.rename(columns={'商品ID': '商品id'}, inplace=True)
                        df['商品id'] = df['商品id'].apply(lambda x: f'="{x}"' if x else x)
                        df['货号'] = df['货号'].apply(lambda x: f'="{x}"' if x else x)
                        df.insert(loc=0, column='日期', value=date1)

                        self.save_to_csv(df, root, new_name)
                        if self.set_up_to_mogo:
                            if 'sku' in new_name:
                                d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_sku_商品明细')
                            elif 'spu' in new_name:
                                d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_spu_商品明细')
                        if self.set_up_to_mysql:
                            if 'sku' in new_name:
                                m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_sku_商品明细')
                            elif 'spu' in new_name:
                                m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_spu_商品明细')
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.xlsx') and '搜索分析-排名定位-商品词下排名' in name:
                        # 京东商品词下排名
                        pattern = re.findall(r'(\d{4}-\d{2}-\d{2})-(\d{4}-\d{2}-\d{2})', name)
                        if not pattern:
                            os.remove(os.path.join(root, name))
                            continue
                        if pattern[0][0] == pattern[0][1]:
                            print(f'{name}: 检测到数据周期异常，仅支持7天数据')
                            os.remove(os.path.join(root, name))
                            continue
                        new_name = os.path.splitext(name)[0] + '.csv'
                        # print(name)
                        df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        if len(df.columns.tolist()) < 20:
                            print(f'{name}: 报表可能缺失诊断数据')
                            os.remove(os.path.join(root, name))
                            continue
                        df.rename(columns={'商品的ID': 'skuid'}, inplace=True)
                        df['skuid'] = df['skuid'].apply(lambda x: f'="{x}"' if x and '=' not in str(x) else x)
                        self.save_to_csv(df, root, new_name)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_商品词下排名')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_商品词下排名')
                        os.remove(os.path.join(root, name))  # 移除已转换的原文件

                    elif name.endswith('.xlsx') and '搜索分析-排名定位-商品排名' in name:
                        # 京东商品排名
                        new_name = os.path.splitext(name)[0] + '.csv'
                        date_in = re.findall(r'(\d{4}-\d{2}-\d{2})-搜索', str(name))[0]
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.insert(0, '日期', date_in)  # 插入新列
                        df.rename(columns={'SKU': 'skuid'}, inplace=True)
                        df['skuid'] = df['skuid'].apply(lambda x: f'="{x}"' if x and '=' not in str(x) else x)
                        self.save_to_csv(df, root, new_name, encoding='utf-8_sig')
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_商品排名')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_商品排名')
                        os.remove(os.path.join(root, name))  # 移除已转换的原文件

                    elif name.endswith('.xls') and '竞店概况_竞店详情' in name:
                        # 京东，竞争-竞店概况-竞店详情-全部渠道
                        date01 = re.findall(r'全部渠道_(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2})', str(name))
                        start_date = f'{date01[0][0]}-{date01[0][1]}-{date01[0][2]}'
                        end_date = f'{date01[0][3]}-{date01[0][4]}-{date01[0][5]}'
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df.replace(to_replace=[','], value='', regex=True, inplace=True)
                        df.insert(loc=0, column='日期', value=start_date)
                        new_name = f'{os.path.splitext(name)[0]}'
                        new_name = re.sub(r'\d{8}_\d{8}', f'{start_date}_{end_date}', new_name)
                        self.save_to_csv(df, root, new_name)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_竞店监控_日数据')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_竞店监控_日数据')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and ('JD店铺日报_店铺' in name or '店铺_20' in name):
                        # 京东 自助报表  店铺日报
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        if '访客数-全部渠道' not in df.columns.tolist():  # 识别是否真的京东日报
                            continue
                        df['日期'] = df['日期'].apply(
                            lambda x: '-'.join(re.findall(r'(\d{4})(\d{2})(\d{2})', str(x))[0])
                        )
                        date_min = df['日期'].values.min()
                        date_max = df['日期'].values.max()
                        # df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        new_name = f'JD店铺日报_' + re.findall(r"(.*)\d{8}_\d{8}", name)[0] + f'_{date_min}_{date_max}.csv'
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='京东数据1', collection_name='京东_自助取数_店铺日报')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_自助取数_店铺日报')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xls') and '商家榜单_女包_整体' in name:
                        # 京东 行业 商家榜单
                        date2 = re.findall(r'_\d{8}-\d+', name)
                        if date2:
                            print(f'{name}: 请下载日数据，不支持其他周期')
                            os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                            continue
                        date1 = re.findall(r'_(\d{4})(\d{2})(\d{2})', name)
                        date1 = f'{date1[0][0]}-{date1[0][1]}-{date1[0][2]}'
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df['日期'] = df['日期'].astype(str).apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:8]}')
                        df.insert(loc=0, column='类型', value='商家榜单')
                        new_name = f'{os.path.splitext(name)[0]}_{date1}.csv'
                        self.save_to_csv(df, root, new_name)
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df,db_name='京东数据1', collection_name='京东_商家榜单')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_商家榜单')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '批量SKU导出-批量任务' in name:
                        # 京东 sku 导出
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        d_time = datetime.datetime.today().strftime('%Y-%m-%d')
                        df.insert(loc=0, column='日期', value=d_time)
                        for col in ['SKUID', '商品编码', '商家SKU', '货号']:
                            df[col] = df[col].apply(lambda x: f'="{x}"' if x else x)
                        df['商品链接'] = df['商品链接'].apply(lambda x: f'https://{x}' if x else x)
                        new_name = f'京东商品信息_{os.path.splitext(name)[0]}_{d_time}.csv'
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='属性设置1', collection_name='京东商品信息')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='属性设置1', tabel_name='京东商品信息')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '批量SPU导出-批量任务' in name:
                        # 京东 spu 导出
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        d_time = datetime.datetime.today().strftime('%Y-%m-%d')
                        df.insert(loc=0, column='日期', value=d_time)
                        for col in ['商品编码', '货号']:
                            df[col] = df[col].apply(lambda x: f'="{x}"' if x else x)
                        new_name = f'京东商品信息_{os.path.splitext(name)[0]}_{d_time}.csv'

                        self.save_to_csv(df, root, new_name)
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.csv') and '万里马箱包推广1_完整点击成交' in name:
                        # 京东推广数据
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        pic_list = df['日期'].tolist()
                        pic = []
                        for i in pic_list:
                            pics = re.findall(pattern=r'(\d{4})(\d{2})(\d{2})', string=str(i))
                            if pics:
                                pics = '-'.join(pics[0])
                                pic.append(pics)
                            else:
                                pic.append(i)
                        df['日期'] = pd.Series(pic)
                        date_min = df['日期'].values.min() + '_'
                        date_max = df['日期'].values.max()
                        new_name2 = '京东点击成交报表_' + date_min + date_max + '.csv'
                        for col in ['计划ID', '触发SKU ID', '跟单SKU ID',  'SPU ID']:
                            df[col] = df[col].astype(str).apply(lambda x: f'="{x}"' if x and '=' not in x else x)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        self.save_to_csv(df, root, new_name2)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='京东数据1', collection_name='京东_推广_京准通')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_推广_京准通')
                        os.remove(os.path.join(root, name))
                    elif name.endswith('.csv') and '万里马箱包推广1_京东推广搜索词_pbix同步不要' in name:
                        df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        pic_list = df['日期'].tolist()
                        pic = []
                        for i in pic_list:
                            pics = re.findall(pattern=r'(\d{4})(\d{2})(\d{2})', string=str(i))
                            if pics:
                                pics = '-'.join(pics[0])
                                pic.append(pics)
                            else:
                                pic.append(i)
                        df['日期'] = pd.Series(pic)
                        date_min = df['日期'].values.min() + '_'
                        date_max = df['日期'].values.max()
                        new_name2 = '京东推广搜索词_' + date_min + date_max + '.csv'
                        df.replace(to_replace=[0], value='', regex=False, inplace=True)
                        df['是否品牌词'] = df['搜索词'].str.contains('万里马|wanlima', regex=True)
                        df['是否品牌词'] = df['是否品牌词'].apply(lambda x: '品牌词' if x else '')
                        self.save_to_csv(df, root, new_name2)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='京东数据1', collection_name='京东_推广_搜索词报表')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='京东数据1', tabel_name='京东_推广_搜索词报表')
                        os.remove(os.path.join(root, name))

                    elif name.endswith('.xlsx') and '零售明细统计' in name:
                        #
                        df = pd.read_excel(os.path.join(root, name), header=0)
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        df['摘要'] = df['摘要'].apply(lambda x: re.sub('\'', '', str(x)) if x else x)
                        for col in ['原单号', '商品代码', '摘要']:
                            df[col] = df[col].apply(lambda x: f'="{re.sub(".0", "", str(x))}"' if x else x)
                        df = df[df['缩略图'] != '合计']
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        date_min = f'_{re.sub("T.*", "", str(df["日期"].values.min()))}_'
                        date_max = f'{re.sub("T.*", "", str(df["日期"].values.max()))}.csv'
                        new_name = re.findall(r'(.*)_\d{4}-\d{2}-\d{2}', name)[0]
                        new_name = f'{new_name}{date_min}{date_max}'
                        self.save_to_csv(df, root, new_name)  # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        if self.set_up_to_mogo:
                            d.df_to_mongo(df=df, db_name='生意经1', collection_name='E3_零售明细统计')
                        if self.set_up_to_mysql:
                            m.df_to_mysql(df=df, db_name='生意经1', tabel_name='E3_零售明细统计')
                        os.remove(os.path.join(root, name))
                except Exception as e:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
                    print(f'{now}{name}: 报错: {e}')
        if self.set_up_to_mogo:
            if d.client:
                d.client.close()  # 必须手动关闭数据库连接

    """
    {文件分类}
    将已处理完的文件 分类移到原始文件夹下
    此处t_path参数定义了子文件夹的生成名称
    """

    @staticmethod
    def move_files(path, _name, target_path, _as_month=None):
        """
        name: 移动的文件名，
        target_path: 目标位置
        """
        t2 = target_path  # t2 赋值有用, 不能省略
        if not os.path.exists(t2):  # 如果目录不存在则创建
            os.makedirs(t2, exist_ok=True)
        if _as_month:
            _date = re.findall(r'(\d{4}-\d{2})-\d{2}', str(_name))
            if _date:
                _date = _date[0]
                t2 = pathlib.Path(t2, _date)  # 添加 年月分类
                if not os.path.exists(t2):
                    os.makedirs(t2, exist_ok=True)
        old_file = os.path.join(t2, _name)  # 检查目标位置是否已经存在该文件
        if os.path.isfile(old_file):
            os.remove(old_file)  # 如果存在则移除
        shutil.move(os.path.join(path, _name), t2)  # 将文件从下载文件夹移到目标位置

    # @try_except
    def move_all(self, path=None, is_except=[]):
        if not path:
            path = self.path
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                # print(name)
                is_continue = False
                if is_except:
                    for item in is_except:
                        # print(item, f'-----', os.path.join(root, name))
                        if item in os.path.join(root, name):
                            # print(name)
                            is_continue = True
                            break
                if is_continue:  # 需要排除不做处理的文件或文件夹
                    continue
                # print(is_except, is_continue)
                def bib(paths, _as_month=None):
                    """闭包函数"""
                    self.move_files(path=path, _name=name, target_path=paths, _as_month=_as_month)

                if name.endswith('.csv') and '无线店铺流量来源' in name:
                    date01 = re.findall(r'\d{4}-\d{2}-(\d{2})_\d{4}-\d{2}-(\d{2})', name)

                    if int(date01[0][1]) - int(date01[0][0]) > 15:
                        t_path = str(pathlib.Path(self.source_path, '月数据/流量来源_旧版'))
                        bib(t_path)
                    elif '_新版' in name:
                        t_path = str(pathlib.Path(self.source_path, '生意参谋/流量来源'))
                        bib(t_path, _as_month=True)
                    else:
                        t_path = str(pathlib.Path(self.source_path, '生意参谋/流量来源_旧版'))
                        bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '生意参谋' in name and '无线店铺三级流量来源详情' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/手淘搜索来源'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '商品_全部' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/商品排行'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '参谋店铺整体日报' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/全店数据-自助取数'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '参谋每日流量_自助取数' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/流量来源-自助取数'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '商品sku' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/商品sku-自助取数'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '参谋店铺流量来源（月）' in name:
                    t_path = str(pathlib.Path(self.source_path, '月数据/流量来源-自助取数-月数据'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '淘宝联盟_分天数据_计划_活动类型_推广概览_数据汇总' in name:
                    t_path = str(pathlib.Path(self.source_path, '月数据/淘宝联盟'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '竞店分析' in name and '来源分析-入店来源' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/竞店分析/来源分析/入店来源'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '竞店分析' in name and '来源分析-入店搜索词' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/竞店分析/来源分析/入店搜索词'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '竞店分析' in name and '销售分析-关键指标对比' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/竞店分析/销售分析/关键指标对比'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '竞店分析' in name and '销售分析-top商品榜' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/竞店分析/销售分析/top商品榜'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '监控店铺数据' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/监控店铺数据'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '监控商品' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/监控商品数据'))
                    bib(t_path, _as_month=True)
                # elif name.endswith('.csv') and '竞店分析-流量分析' in name:
                #     t_path = str(pathlib.Path(self.source_path, '市场数据/竞店流量构成'))
                #     bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '类目洞察' in name and '属性分析_分析明细_汇总' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/类目洞察/属性分析/汇总'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '类目洞察' in name and '属性分析_分析明细_商品发现' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/类目洞察/属性分析/商品发现'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '类目洞察' in name and '价格分析_分析明细_汇总' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/类目洞察/价格分析/汇总'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '类目洞察' in name and '价格分析_分析明细_商品发现' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/类目洞察/价格分析/商品发现'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '搜索排行_搜索' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/搜索排行'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '市场排行_店铺排行' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/市场二级类目店铺'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'baobei' in name:
                    date = re.findall(r's-(\d{4})-(\d{2})-(\d{2})\.', str(name))
                    if not date:  # 阻止月数据及未转换的表格
                        continue
                    t_path = str(pathlib.Path(self.source_path, '生意经/宝贝指标'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '省份城市分析' in name:
                    date = re.findall(r'(\d{4})-(\d{2})-(\d{2})\.', str(name))
                    if not date:  # 阻止未转换的表格
                        continue
                    t_path = str(pathlib.Path(self.source_path, '生意经/地域分布'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '店铺销售指标' in name:
                    date = re.findall(r'(\d{4})-(\d{2})-(\d{2})\.', str(name))
                    if not date:  # 阻止未转换的表格
                        continue
                    t_path = str(pathlib.Path(self.source_path, '生意经/店铺指标'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and 'order' in name:
                    date = re.findall(r'(\d{4})-(\d{2})-(\d{2})\.', str(name))
                    if not date:  # 阻止未转换的表格
                        continue
                    t_path = str(pathlib.Path(self.source_path, '生意经/订单数据'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '直播间成交订单明细' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/直播订单明细'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '直播间大盘数据' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/直播间大盘数据'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '直播业绩_成交拆解' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/直播业绩_成交拆解'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'DMP报表' in name:
                    t_path = str(pathlib.Path(self.source_path, '推广报表/DMP报表'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '人群洞察' in name:
                    t_path = str(pathlib.Path(self.source_path, '推广报表/人群洞察'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '客户_客户概况_画像' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/客户_客户概况_画像'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '市场排行_店铺' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/市场排行'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '淘宝店铺数据' in name:
                    t_path = str(pathlib.Path(self.source_path, '市场数据/其他数据'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '零售明细统计' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意经/E3零售明细统计'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '客户运营平台_客户列表' in name:
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/客户运营平台'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '直播分场次效果' in name:
                    pattern = re.findall(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', name)
                    if not pattern:
                        continue
                    t_path = str(pathlib.Path(self.source_path, '生意参谋/直播场次分析'))
                    bib(t_path, _as_month=True)
                #  京东分界线   ------- 开始标记
                #  京东分界线
                elif name.endswith('.csv') and '全部渠道_商品明细' in name:
                    if 'sku' in name:
                        t_path = str(pathlib.Path(self.source_path, '京东报表/JD商品明细sku'))
                    elif 'spu' in name:
                        t_path = str(pathlib.Path(self.source_path, '京东报表/JD商品明细spu'))
                    else:
                        t_path = str(pathlib.Path(self.source_path, '京东报表/未找到分类数据'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '竞店概况_竞店详情' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD竞店监控数据'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东推广搜索词' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD推广搜索词报表'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东点击成交报表' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD推广报表'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '搜索分析-排名定位-商品词下排名' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD排名定位/商品词下排名'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '搜索分析-排名定位-商品排名' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD排名定位/商品排名'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '按天_店铺来源_流量来源' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD流量来源'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'JD店铺日报' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD店铺日报'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '商家榜单_女包_整体' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD商家榜单'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '导出-批量任务' in name:
                    if 'SKU' in name:
                        t_path = str(pathlib.Path(self.source_path, '京东报表/商品信息导出/sku'))
                        bib(t_path, _as_month=False)
                    elif 'SPU' in name:
                        t_path = str(pathlib.Path(self.source_path, '京东报表/商品信息导出/spu'))
                        bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '_行业分析_竞争分析' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/行业竞争分析'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '付费广告_行业分析_行业大盘' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/行业大盘_流量排行'))
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and '营销概况_全站营销' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD推广_全站营销报表'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东推广关键词点击成交报表' in name:
                    t_path = str(pathlib.Path(self.source_path, '京东报表/JD推广_关键词报表'))
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '爱库存_商品榜单_spu_' in name:
                    t_path = str(pathlib.Path(self.source_path, '爱库存/商品榜单'))
                    bib(t_path, _as_month=True)
                #  京东分界线   ------- 结束标记

    def attribute(self, path=None, _str='商品素材导出', ):
        """
        从天猫商品素材库中下载的文件，将文件修改日期添加到DF 和文件名中
        """
        db_name = '属性设置2'
        collection_name = '商品素材导出'
        if not path:
            path = self.path

        # if self.set_up_to_mogo:
        #     username, password, host, port = get_myconf.select_config_values(target_service='home_lx',
        #                                                                      database='mongodb')
        #     d = mongo.UploadMongo(username=username, password=password, host=host, port=port,
        #                                  drop_duplicates=False
        #                                  )
        # if self.set_up_to_mysql:
        #     username, password, host, port = get_myconf.select_config_values(target_service='home_lx', database='mysql')
        #     m = mysql.MysqlUpload(username=username, password=password, host=host, port=port)
        new_save_path = os.path.join(self.source_path, '属性设置', '商品素材')
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith('.xlsx') and '~' not in name:
                    pattern = re.findall('([\u4e00-\u9fa5])', name)
                    if pattern:
                        continue
                    if '~$' in name or 'DS_Store' in name:
                        continue
                    df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    col = df.columns.tolist()
                    if '商品白底图' in col and '方版场景图' in col:
                        f_info = os.stat(os.path.join(root, name))  # 读取文件的 stat 信息
                        mtime = time.strftime('%Y-%m-%d', time.localtime(f_info.st_mtime))  # 读取文件创建日期
                        df['日期'] = mtime
                        df.rename(columns={'商品ID': '商品id'}, inplace=True)
                        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                        if (652737455554 in df['商品id'].tolist()
                                or 683449516249 in df['商品id'].tolist()
                                or 37114359548 in df['商品id'].tolist()
                                or 570735930393 in df['商品id'].tolist()):
                            df.insert(0, '店铺名称', '万里马官方旗舰店')  # 插入新列
                            new_name = 'tm_' + os.path.splitext(name)[0] + f'_{_str}_' + mtime + '.csv'
                        elif (704624764420 in df['商品id'].tolist()
                              or 701781021639 in df['商品id'].tolist()
                              or 520380314717 in df['商品id'].tolist()):
                            df.insert(0, '店铺名称', '万里马官方企业店')  # 插入新列
                            new_name = 'tb_' + os.path.splitext(name)[0] + f'_{_str}_' + mtime + '.csv'
                        else:
                            df.insert(0, '店铺名称', 'coome旗舰店')  # 插入新列
                            new_name = 'coome_' + os.path.splitext(name)[0] + f'_{_str}_' + mtime + '.csv'
                        df['商品id'] = df['商品id'].apply(
                            lambda x: "{0}{1}{2}".format('="', x, '"') if x and '=' not in str(x) else x
                        )
                        # mysql 可能改变 df 列名，所以在上传 mysql 前保存 csv
                        self.save_to_csv(df, new_save_path, new_name, encoding='utf-8_sig')
                        # try:
                        #     if self.set_up_to_mogo:
                        #         d.df_to_mongo(df=df, db_name=db_name, collection_name=collection_name)
                        #     if self.set_up_to_mysql:
                        #         m.df_to_mysql(df=df, db_name=db_name, tabel_name=collection_name)
                        # except Exception as e:
                        #     print(e)
                        os.remove(os.path.join(root, name))
        # if self.set_up_to_mogo:
        #     if d.client:
        #         d.client.close()  # 必须手动关闭数据库连接

    # @try_except
    def new_unzip(self, path=None, is_move=None):
        """
        {解压并移除zip文件}
        如果是京东的商品明细，处理过程：
        1. 读取 zip包的文件名
        2. 组合完整路径，判断文件夹下是否已经有同名文件
        3. 如果有，则将该同名文件改名，（从文件名中提取日期，重新拼接文件名）
        4. 然后解压 zip包
        5. 需要用 _jd_rename 继续重命名刚解压的文件
        is_move 参数,  是否移除 下载目录的所有zip 文件
        """
        if not path:
            path = self.path
        res_names = []  # 需要移除的压缩文件
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or 'DS_Store' in name:
                    continue
                if name.endswith('.zip'):
                    old_file = os.path.join(root, name)
                    f = zipfile.ZipFile(old_file, 'r')
                    if len(f.namelist()) == 1:  # 压缩包只有一个文件的情况
                        for zip_name in f.namelist():  # 读取zip内的文件名称
                            # zip_name_1 = zip_name.encode('cp437').decode('utf-8')
                            try:
                                zip_name_1 = zip_name.encode('utf-8').decode('utf-8')
                            except:
                                zip_name_1 = zip_name.encode('cp437').decode('utf-8')
                            new_path = os.path.join(root, zip_name_1)  # 拼接解压后的文件路径
                            if os.path.isfile(new_path) and '全部渠道_商品明细' in new_path:  # 是否存在和包内同名的文件
                                # 专门处理京东文件
                                df = pd.read_excel(new_path)
                                try:
                                    pattern1 = re.findall(r'\d{8}_(\d{4})(\d{2})(\d{2})_全部渠道_商品明细',
                                                          name)
                                    pattern2 = re.findall(
                                        r'\d{8}_(\d{4})(\d{2})(\d{2})-(\d{4})(\d{2})(\d{2})_全部渠道_商品明细',
                                        name)
                                    if pattern1:
                                        year_date = '-'.join(list(pattern1[0])) + '_' + '-'.join(list(pattern1[0]))
                                    elif pattern2:
                                        year_date = '-'.join(list(pattern2[0])[0:3]) + '_' + '-'.join(
                                            list(pattern2[0])[3:7])
                                    else:
                                        year_date = '无法提取日期'
                                        print(f'{name} 无法从文件名中提取日期，请检查pattern或文件')
                                    if ('10035975359247' in df['商品ID'].values or '10056642622343' in
                                            df['商品ID'].values):
                                        os.rename(new_path,
                                                  os.path.join(root, 'sku_' + year_date + '_全部渠道_商品明细.xls'))
                                        f.extract(zip_name_1, root)
                                    elif ('10021440233518' in df['商品ID'].values or '10022867813485' in
                                          df['商品ID'].values):
                                        os.rename(new_path,
                                                  os.path.join(root, 'spu_' + year_date + '_全部渠道_商品明细.xls'))
                                        f.extract(zip_name_1, root)
                                    if is_move:
                                        os.remove(os.path.join(root, name))
                                except Exception as e:
                                    print(e)
                                    continue
                            else:
                                f.extract(zip_name, root)
                                if zip_name_1 != zip_name:
                                    os.rename(os.path.join(root, zip_name), os.path.join(root, zip_name_1))
                                if is_move:
                                    res_names.append(name)
                                    # os.remove(os.path.join(root, name))  # 这里不能移除，会提示文件被占用
                        f.close()
                    else:  # 压缩包内包含多个文件的情况
                        f.close()
                        self.unzip_all(path=old_file, save_path=path)

        if is_move:
            for name in res_names:
                os.remove(os.path.join(path, name))
                print(f'移除{os.path.join(path, name)}')

    @staticmethod
    def unzip_all(path, save_path):
        """
        遍历目录， 重命名有乱码的文件
        2. 如果压缩包是文件夹， 则保存到新文件夹，并删除有乱码的文件夹
        3. 删除MAC系统的临时文件夹__MACOSX
        """
        with PyZipFile(path) as _f:
            _f.extractall(save_path)
            _f.close()
        for _root, _dirs, _files in os.walk(save_path, topdown=False):
            for _name in _files:
                if '~$' in _name or 'DS_Store' in _name:
                    continue
                try:
                    _new_root = _root.encode('cp437').decode('utf-8')
                    _new_name = _name.encode('cp437').decode('utf-8')
                except:
                    _new_root = _root.encode('utf-8').decode('utf-8')
                    _new_name = _name.encode('utf-8').decode('utf-8')
                _old = os.path.join(_root, _name)
                _new = os.path.join(_new_root, _new_name)
                if _new_root != _root:  # 目录乱码，创建新目录
                    os.makedirs(_new_root, exist_ok=True)
                os.rename(_old, _new)
            try:
                _new_root = _root.encode('cp437').decode('utf-8')
            except:
                _new_root = _root.encode('utf-8').decode('utf-8')
            if _new_root != _root or '__MACOSX' in _root:
                shutil.rmtree(_root)


def main():
    # 数据分类

    d_path = '/Users/xigua/Downloads'
    source_path = '/Users/xigua/数据中心/原始文件2'
    c = DataClean(path=d_path, source_path=source_path)
    c.set_up_to_mogo = False
    c.set_up_to_mysql = False
    c.new_unzip(is_move=True)  # 解压文件
    c.change_and_sort()
    c.move_all()  # 移到文件到原始文件夹
    # c.attribute()  # 商品素材重命名和分类


if __name__ == '__main__':
    main()
    username, password, host, port = get_myconf.select_config_values(target_service='aliyun', database='mongodb')
    print(username, password, host, port)
