# -*- coding:utf-8 -*-
import warnings
import pandas as pd
from functools import wraps
import chardet
import zipfile
import socket
from pyzipper import PyZipFile
import os
import platform
import json
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.config import myconfig
from mdbq.aggregation import df_types
from mdbq.config import products
from mdbq.aggregation import optimize_data
from mdbq.aggregation import query_data
import datetime
import time
import re
import shutil
import getpass

warnings.filterwarnings('ignore')


if platform.system() == 'Windows':
    # windows版本
    Data_Path = r'C:\同步空间\BaiduSyncdisk'
    D_PATH = os.path.join(f'C:\\Users\\{getpass.getuser()}\\Downloads')
    Share_Path = os.path.join(r'\\192.168.1.198\时尚事业部\01.运营部\天猫报表')  # 共享文件根目录
elif platform.system() == 'Linux':
    Data_Path = '数据中心'
    D_PATH = 'Downloads'
    if not os.path.exists(D_PATH):
        os.makedirs(D_PATH)
    Share_Path = ''  # linux 通常是远程服务器，不需要访问共享
else:
    Data_Path = f'/Users/{getpass.getuser()}/数据中心'  # 使用Mac独立网络时
    D_PATH = os.path.join(f'/Users/{getpass.getuser()}/Downloads')
    Share_Path = os.path.join('/Volumes/时尚事业部/01.运营部/天猫报表')  # 共享文件根目录

upload_path = os.path.join(D_PATH, '数据上传中心')  # 此目录位于下载文件夹
# source_path = os.path.join(Data_Path, '原始文件2')  # 此目录保存下载并清洗过的文件，作为数据库备份
source_path3 = os.path.join(Data_Path, '原始文件3')  # 此目录保存下载并清洗过的文件，作为数据库备份

username, password, host, port, service_database = None, None, None, None, None,
if socket.gethostname() in ['xigua_lx', 'xigua1', 'MacBookPro']:
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    service_database = {'xigua_lx': 'mysql'}
elif socket.gethostname() in ['company', 'Mac2.local']:
    conf = myconfig.main()
    conf_data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    service_database = {'company': 'mysql'}
if not username:
    print(f'找不到主机：')



class DataClean:
    """ 数据分类 """

    def __init__(self, path, source_path):
        self.path = path  # 数据源位置，下载文件夹
        self.source_path = source_path  # 原始文件保存目录
        self.datas = []

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

    def sycm_tm(self, path=None, is_except=[]):
        """ 天猫 生意参谋数据 """
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': '商品排行_',  # 文件名中包含的字符
                '数据库名': '生意参谋3',
                '集合名称': '商品排行',
            },
            {
                '文件简称': '店铺来源_来源构成_',  # 文件名中包含的字符
                '数据库名': '生意参谋3',
                '集合名称': '店铺流量来源构成',
            },
            {
                '文件简称': '爱库存_商品榜单_',  # 文件名中包含的字符
                '数据库名': '爱库存2',
                '集合名称': '商品spu榜单',
            },
            {
                '文件简称': '手淘搜索_本店引流词_',  # 文件名中包含的字符
                '数据库名': '生意参谋3',
                '集合名称': '手淘搜索_本店引流词',
            },
            {
                '文件简称': '直播分场次效果_',  # 文件名中包含的字符
                '数据库名': '生意参谋3',
                '集合名称': '直播分场次效果',
            },
            {
                '文件简称': 'crm_客户列表_',  # 文件名中包含的字符
                '数据库名': '生意参谋3',
                '集合名称': 'crm成交客户',
            },
        ]
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

                # 这里排除掉非目标报表
                is_continue = False
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue
                if name.endswith('.csv') and '商品排行_' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # df = pd.read_excel(os.path.join(root, name), header=4)

                elif name.endswith('.csv') and '手淘搜索_本店引流词_' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # df = pd.read_excel(os.path.join(root, name), header=5, engine='xlrd')

                elif name.endswith('.csv') and '_来源构成_' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)

                elif name.endswith('.csv') and '爱库存_商品榜单_' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    if '店铺名称' not in df.columns.tolist():
                        df.insert(loc=1, column='店铺名称', value='爱库存平台')  # df中插入新列
                    new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    self.save_to_csv(df, root, new_name, encoding='utf-8_sig')
                    os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and '直播分场次效果' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # shop_name = re.findall(r'_([\u4e00-\u9fffA-Za-z]+店)_', name)[0]
                    # if '店铺名称' not in df.columns.tolist():
                    #     df.insert(loc=1, column='店铺名称', value=shop_name)
                    # new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    # self.save_to_csv(df, root, new_name, encoding='utf-8_sig')
                    # os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and 'crm_客户列表' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    # print(f'db_name/collection_name 不能为空')
                    continue
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                    )

    def dmp_tm(self, path=None, is_except=[]):
        """ 天猫 达摩盘 """
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': '我的人群属性',  # 文件名中包含的字符
                '数据库名': '达摩盘3',
                '集合名称': '我的人群属性',
            },
            {
                '文件简称': 'dmp人群报表_',  # 文件名中包含的字符
                '数据库名': '达摩盘3',
                '集合名称': 'dmp人群报表',
            },
            {
                '文件简称': '货品洞察_全店单品',  # 文件名中包含的字符
                '数据库名': '达摩盘3',
                '集合名称': '货品洞察_全店单品',
            },
        ]
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

                # 这里排除掉非目标报表
                is_continue = False
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue
                if name.endswith('.csv') and '人群属性_万里马官方旗舰店' in name:  # 推广类报表
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and 'dmp人群报表_' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '货品洞察_全店单品' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    # print(f'db_name/collection_name 不能为空')
                    continue
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                )

    def tg_reports(self, path=None, is_except=[]):
        """ 处理天猫淘宝推广类报表 """
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': 'tg_report_主体报表',
                '数据库名': '推广数据2',
                '集合名称': '主体报表',
            },
            {
                '文件简称': 'tg_report_创意报表_创意',
                '数据库名': '推广数据2',
                '集合名称': '创意报表_创意',
            },
            {
                '文件简称': 'tg_report_创意报表_素材',
                '数据库名': '推广数据2',
                '集合名称': '创意报表_素材',
            },
            {
                '文件简称': 'tg_report_单元报表',
                '数据库名': '推广数据2',
                '集合名称': '单元报表',
            },
            {
                '文件简称': 'tg_report_地域报表_省份',
                '数据库名': '推广数据2',
                '集合名称': '地域报表_省份',
            },
            {
                '文件简称': 'tg_report_地域报表_城市',
                '数据库名': '推广数据2',
                '集合名称': '地域报表_城市',
            },
            {
                '文件简称': 'tg_report_关键词报表',
                '数据库名': '推广数据2',
                '集合名称': '关键词报表',
            },
            {
                '文件简称': 'tg_report_计划报表',
                '数据库名': '推广数据2',
                '集合名称': '计划报表',
            },
            {
                '文件简称': 'tg_report_权益报表',
                '数据库名': '推广数据2',
                '集合名称': '权益报表',
            },
            {
                '文件简称': 'tg_report_人群报表',
                '数据库名': '推广数据2',
                '集合名称': '人群报表',
            },
            {
                '文件简称': 'tg_report_营销场景报表',
                '数据库名': '推广数据2',
                '集合名称': '营销场景报表',
            },
            {
                '文件简称': 'tg_report_超级直播报表_人群',
                '数据库名': '推广数据2',
                '集合名称': '超级直播',
            },
            {
                '文件简称': 'tg_report_品销宝_明星店铺',
                '数据库名': '推广数据2',
                '集合名称': '品销宝',
            },
            {
                '文件简称': 'tg_report_超级短视频_主体',
                '数据库名': '推广数据2',
                '集合名称': '超级短视频_主体',
            }
        ]
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue
                # if 'py_xg' in name:
                #     continue
                is_continue = False
                if is_except:
                    for item in is_except:
                        if item in os.path.join(root, name):
                            # print(name)
                            is_continue = True
                            break
                if is_continue:  # 需要排除不做处理的文件或文件夹
                    continue

                # 这里排除掉非推广类报表
                is_continue = False
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue
                # 区分淘宝和天猫的报表
                if '万里马官方旗舰店' in name:
                    pass
                elif '万里马官方企业店' in name:
                    db_name = '推广数据_淘宝店'
                else:
                    print(f'报表名称错误，不属于天猫/淘宝店：{name}')
                    continue

                if name.endswith('.csv') and '明星店铺' not in name:  # 推广类报表
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '品销宝_明星店铺' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.xlsx') and '品销宝_明星店铺' in name:
                    # 品销宝
                    sheets4 = ['账户', '推广计划', '推广单元', '创意', '品牌流量包', '定向人群']  # 品销宝
                    file_name4 = os.path.splitext(name)[0]  # 明星店铺报表
                    new_df = []
                    for sheet4 in sheets4:
                        df = pd.read_excel(os.path.join(root, name), sheet_name=sheet4, header=0, engine='openpyxl')
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            os.remove(os.path.join(root, name))
                            continue
                        if len(df) < 1:
                            print(f'{name} 跳过')
                            continue
                        else:
                            shop_name = re.findall(r'明星店铺_([\u4e00-\u9fffA-Za-z]+店)', name)[0]
                            df.insert(loc=1, column='店铺名称', value=shop_name)
                            df.insert(loc=2, column='报表类型', value=sheet4)
                            # if '访客触达率' not in df.columns.tolist():
                            #     df['访客触达率'] = '0'
                            df.fillna(0, inplace=True)
                            df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
                            # min_clm = str(df['日期'].min()).split(' ')[0]
                            # max_clm = str(df['日期'].max()).split(' ')[0]
                            new_file_name4 = f'{sheet4}_py_xg_{file_name4}.csv'
                            # 以sheet名进一步创建子文件夹
                            # root_new = os.path.join(self.source_path, '推广报表/品销宝', sheet4)
                            self.save_to_csv(df, upload_path, new_file_name4)
                            new_df.append(df)
                    df = pd.concat(new_df)  # 品销宝 1 表有 6 个 sheet
                    os.remove(os.path.join(root, name))

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    print(f'db_name/collection_name 不能为空')
                    continue
                # print(db_name, collection_name)
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                )

    def syj_reports_tm(self, path=None, is_except=[]):
        """ 生意经报表 """
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': 'baobei',
                '数据库名': '生意经3',
                '集合名称': '宝贝指标',
            },
            {
                '文件简称': 'order',
                '数据库名': '生意经3',
                '集合名称': '订单数据',
            },
            {
                '文件简称': '省份城市分析',
                '数据库名': '生意经3',
                '集合名称': '省份城市分析',
            },
            {
                '文件简称': '店铺销售指标',
                '数据库名': '生意经3',
                '集合名称': '店铺销售指标',
            },
        ]

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue
                # if 'py_xg' in name:
                #     continue
                is_continue = False
                if is_except:
                    for item in is_except:
                        if item in os.path.join(root, name):
                            # print(name)
                            is_continue = True
                            break
                if is_continue:  # 需要排除不做处理的文件或文件夹
                    continue

                # 这里排除掉非目标报表
                is_continue = False
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue

                if name.endswith('.csv') and 'baobei' in name:
                    # encoding = self.get_encoding(file_path=os.path.join(root, name))
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and 'order' in name:
                    """ 如果是手动下载的表格，这里不能使用表格原先的 gb2312， 会报错 """
                    # df = pd.read_csv(os.path.join(root, name), encoding='gb18030', header=0, na_filter=False)
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '省份城市分析' in name:
                    encoding = self.get_encoding(file_path=os.path.join(root, name))
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                    pattern = re.findall(r'(.*[\u4e00-\u9fa5])(\d{4})(\d{2})(\d{2})\W', name)[0]  # 注意后面可能有小括号 ...27 (2).csv
                    date = '-'.join(pattern[1:])
                    new_name = f'py_xg_天猫_{pattern[0]}-{date}.csv'
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
                    self.save_to_csv(df, root, new_name, encoding='utf-8_sig')
                    os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and '店铺销售指标' in name:
                    # 生意经, 店铺指标，仅限月数据，实际日指标也可以
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    # print(f'db_name/collection_name 不能为空')
                    continue
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                )

    def jd_reports(self, path=None, is_except=[]):
        """ 处理京东报表 """
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': '京东推广_点击成交',
                '数据库名': '京东数据3',
                '集合名称': '推广数据_京准通',
            },
            {
                '文件简称': '京东推广_搜索词',
                '数据库名': '京东数据3',
                '集合名称': '推广数据_搜索词报表',
            },
            {
                '文件简称': '京东推广_关键词',
                '数据库名': '京东数据3',
                '集合名称': '推广数据_关键词报表',
            },
            {
                '文件简称': 'sku_商品明细',
                '数据库名': '京东数据3',
                '集合名称': '京东商智_sku_商品明细',
            },
            {
                '文件简称': 'spu_商品明细',
                '数据库名': '京东数据3',
                '集合名称': '京东商智_spu_商品明细',
            },
            {
                '文件简称': '店铺来源_三级来源',
                '数据库名': '京东数据3',
                '集合名称': '京东商智_店铺来源',
            },
        ]

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue
                # if 'py_xg' in name:
                #     continue
                is_continue = False
                if is_except:
                    for item in is_except:
                        if item in os.path.join(root, name):
                            # print(name)
                            is_continue = True
                            break
                if is_continue:  # 需要排除不做处理的文件或文件夹
                    continue

                # 这里排除掉非目标报表
                is_continue = False
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue

                if name.endswith('.csv') and '京东推广_' in name:
                    # df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # new_name = f'py_xg_{name}'
                    # if os.path.isfile(os.path.join(root, new_name)):
                    #     os.remove(os.path.join(root, new_name))
                    # os.rename(os.path.join(root, name), os.path.join(root, new_name))
                elif name.endswith('.csv') and 'sku_商品明细' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    # df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                    # pattern = re.findall(r'_(\d{4}-\d{2}-\d{2})', name)[0]
                    # df.insert(loc=0, column='日期', value=pattern)
                    # df.insert(loc=1, column='店铺名称', value='京东箱包旗舰店')
                    # df.fillna(0, inplace=True)
                    # new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    # df.to_csv(os.path.join(root, new_name), encoding='utf-8_sig', index=False, header=True)
                    # # df.to_excel(os.path.join(upload_path, new_name),
                    # #             index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))
                    # os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and 'spu_商品明细' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    # df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                    # pattern = re.findall(r'_(\d{4}-\d{2}-\d{2})', name)[0]
                    # df.insert(loc=0, column='日期', value=pattern)
                    # df.insert(loc=1, column='店铺名称', value='京东箱包旗舰店')
                    # df.fillna(0, inplace=True)
                    # new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    # df.to_csv(os.path.join(root, new_name), encoding='utf-8_sig', index=False, header=True)
                    # # df.to_excel(os.path.join(upload_path, new_name),
                    # #             index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))
                    # os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and '店铺来源_三级来源' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    # df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    # df.replace(to_replace=['-'], value='', regex=False, inplace=True)
                    # df.rename(columns={'时间': '日期'}, inplace=True)
                    # for col in df.columns.tolist():
                    #     if '环比' in col or '同比' in col:
                    #         df.drop(col, axis=1, inplace=True)
                    # df.fillna(0, inplace=True)
                    # new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    # df.to_csv(os.path.join(root, new_name), encoding='utf-8_sig', index=False, header=True)
                    # # df.to_excel(os.path.join(upload_path, new_name),
                    # #             index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))
                    # os.remove(os.path.join(root, name))

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    # print(f'db_name/collection_name 不能为空')
                    continue
                # print(name)
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                )

    def sp_scene_clean(self, path=None, is_except=[]):
        if not path:
            path = self.path
        report_names = [
            {
                '文件简称': '商品素材_',  # 文件名中包含的字符
                '数据库名': '属性设置3',
                '集合名称': '商品素材中心',
            },
            {
                '文件简称': '商品类目属性_',  # 文件名中包含的字符
                '数据库名': '属性设置3',
                '集合名称': '商品类目属性',
            },
            {
                '文件简称': '商品主图视频_',  # 文件名中包含的字符
                '数据库名': '属性设置3',
                '集合名称': '商品主图视频',
            },
            {
                '文件简称': '商品sku属性_',  # 文件名中包含的字符
                '数据库名': '属性设置3',
                '集合名称': '商品sku',
            },
        ]

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue
                if 'py_xg' in name:
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
                db_name = None  # 初始化参数
                collection_name = None
                for item in report_names:
                    if item['文件简称'] in name:
                        db_name = item['数据库名']
                        collection_name = item['集合名称']
                        is_continue = True
                if not is_continue:
                    continue

                if name.endswith('.xlsx') and '商品素材_' in name:
                    shop_name = re.findall(r'_([\u4e00-\u9fffA-Za-z]+店)_', name)[0]
                    df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                    if '日期' not in df.columns.tolist():
                        df.insert(loc=0, column='日期', value=datetime.datetime.today().strftime('%Y-%m-%d'))
                    if '店铺名称' not in df.columns.tolist():
                        df.insert(loc=1, column='店铺名称', value=shop_name)
                    new_name = f'py_xg_{name}'
                    df.to_excel(os.path.join(upload_path, new_name),
                                index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))
                    os.remove(os.path.join(root, name))
                elif name.endswith('.csv') and ('商品类目属性' in name or '商品主图视频' in name or '商品sku属性' in name):
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    new_name = f'py_xg_{os.path.splitext(name)[0]}.csv'
                    if os.path.isfile(os.path.join(root, new_name)):
                        os.remove(os.path.join(root, new_name))
                    os.rename(os.path.join(root, name), os.path.join(root, new_name))

                # 将数据传入 self.datas 等待更新进数据库
                if not db_name or not collection_name:
                    # print(f'db_name/collection_name 不能为空')
                    continue
                self.datas.append(
                    {
                        '数据库名': db_name,
                        '集合名称': collection_name,
                        '数据主体': df,
                        '文件名': name,
                    }
                )
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
                t2 = os.path.join(t2, _date)  # 添加 年月分类
                if not os.path.exists(t2):
                    os.makedirs(t2, exist_ok=True)
        old_file = os.path.join(t2, _name)  # 检查目标位置是否已经存在该文件
        if os.path.isfile(old_file):
            os.remove(old_file)  # 如果存在则移除
        shutil.move(os.path.join(path, _name), t2)  # 将文件从下载文件夹移到目标位置

    def move_sycm(self, path=None, is_except=[]):
        """ 生意参谋 """
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and '商品排行_' in name:
                    t_path = os.path.join(self.source_path, '生意参谋', '商品排行')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '店铺来源_来源构成_' in name:
                    t_path = os.path.join(self.source_path, '生意参谋', '店铺流量来源')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and (
                        '商品类目属性' in name or '商品主图视频' in name or '商品sku属性' in name):
                    t_path = os.path.join(self.source_path, '生意参谋', '商品属性')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '爱库存_商品榜单_' in name:
                    t_path = os.path.join(self.source_path, '爱库存', '商品spu榜单')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '手淘搜索_本店引流词_' in name:
                    t_path = os.path.join(self.source_path, '生意参谋', '手淘搜索_本店引流词')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '直播分场次效果_' in name:
                    t_path = os.path.join(self.source_path, '生意参谋', '直播分场次效果')
                    bib(t_path, _as_month=True)

    def move_dmp(self, path=None, is_except=[]):
        """ 达摩盘 """
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and '人群属性_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '达摩盘', '我的人群属性')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'dmp人群报表_' in name:
                    t_path = os.path.join(self.source_path, '达摩盘', 'dmp人群报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '货品洞察_全店单品' in name:
                    t_path = os.path.join(self.source_path, '达摩盘', '货品洞察')
                    bib(t_path, _as_month=True)

    # @try_except
    def move_sjy(self, path=None, is_except=[]):
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and 'baobei' in name:
                    t_path = os.path.join(self.source_path, '生意经', '宝贝指标')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '省份城市分析' in name:
                    t_path = os.path.join(self.source_path, '生意经', '省份城市分析')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '店铺销售指标' in name:
                    t_path = os.path.join(self.source_path, '生意经', '店铺销售指标')
                    bib(t_path, _as_month=False)
                elif name.endswith('.csv') and 'order' in name:
                    t_path = os.path.join(self.source_path, '生意经', '订单数据')
                    bib(t_path, _as_month=False)

    # @try_except
    def move_jd(self, path=None, is_except=[]):
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and 'spu_商品明细' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '京东商智_spu_商品明细')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'sku_商品明细' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '京东商智_sku_商品明细')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东推广_搜索词' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '搜索词报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东推广_点击成交' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '推广报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '京东推广_关键词点击' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '关键词报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '店铺来源_三级来源' in name:
                    t_path = os.path.join(self.source_path, '京东报表', '店铺来源_三级来源')
                    bib(t_path, _as_month=True)

    # @try_except
    def move_tg_tm(self, path=None, is_except=[]):
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and 'tg_report_主体报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '主体报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_营销场景报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '营销场景报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_人群报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '人群报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_权益报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '权益报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_计划报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '计划报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_关键词报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '关键词报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_地域报表_省份_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '地域报表_省份')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_地域报表_城市_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '地域报表_城市')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_单元报表_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '单元报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_创意报表_素材粒度_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '创意报表_素材粒度')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_创意报表_创意粒度_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '创意报表_创意粒度')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_超级直播报表_人群_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '超级直播报表_人群')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and '超级短视频_主体' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '超级短视频_主体')
                    bib(t_path, _as_month=True)

                elif name.endswith('.csv') and 'tg_report_品销宝_明星店铺_' in name:
                    t_path = os.path.join(self.source_path, '天猫推广报表', '品销宝')
                    bib(t_path, _as_month=True)

                elif name.endswith('xlsx') and '商品素材_万里马官方旗舰店' in name:
                    t_path = os.path.join(self.source_path, '商品素材')
                    bib(t_path, _as_month=True)
                elif name.endswith('xlsx') and '商品素材_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '商品素材')
                    bib(t_path, _as_month=True)

    # @try_except
    def move_tg_tb(self, path=None, is_except=[]):
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

                if 'py_xg' not in name:  # 排除非目标文件
                    continue

                if name.endswith('.csv') and 'tg_report_主体报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '主体报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_营销场景报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '营销场景报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_人群报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '人群报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_权益报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '权益报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_计划报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '计划报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_关键词报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '关键词报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_地域报表_省份_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '地域报表_省份')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_地域报表_城市_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '地域报表_城市')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_单元报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '单元报表')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_创意报表_素材粒度_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '创意报表_素材粒度')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_创意报表_创意粒度_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '创意报表_创意粒度')
                    bib(t_path, _as_month=True)
                elif name.endswith('.csv') and 'tg_report_超级直播报表_万里马官方企业店' in name:
                    t_path = os.path.join(self.source_path, '淘宝推广报表', '超级直播报表')
                    bib(t_path, _as_month=True)

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
                                # 专门处理京东文件, 已过期可删
                                df = pd.read_excel(new_path, engine='xlrd')
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

    def upload_df(self, path=None):
        """
        将清洗后的 df 上传数据库, copysh.py 调用
        """
        df_to_json = df_types.DataTypes()  # json 文件, 包含数据的 dtypes 信息

        # d = mongo.UploadMongo(
        #     username=username,
        #     password=password,
        #     host=host,
        #     port=port,
        #     drop_duplicates=False,
        # )
        # for data in self.datas:
        #     db_name, collection_name, df = data['数据库名'], data['集合名称'], data['数据主体']
        #     df_to_json.get_df_types(
        #         df=df,
        #         db_name=db_name,
        #         collection_name=collection_name,
        #         is_file_dtype=True,  # 默认本地文件优先: True
        #     )
        #     d.df_to_mongo(df=df, db_name=db_name, collection_name=collection_name)
        # if d.client:
        #     d.client.close()

        m = mysql.MysqlUpload(
            username=username,
            password=password,
            host=host,
            port=port,
        )
        for data in self.datas:
            df, db_name, collection_name, rt_filename = data['数据主体'], data['数据库名'], data['集合名称'], data['文件名']
            df_to_json.get_df_types(
                df=df,
                db_name=db_name,
                collection_name=collection_name,
                is_file_dtype=True,  # 默认本地文件优先: True
            )
            m.df_to_mysql(
                df=df,
                db_name=db_name,
                table_name=collection_name,
                move_insert=False,  # 先删除，再插入，新版有多店数据，不可按日期删除
                df_sql=True,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                filename=rt_filename,  # 用来追踪处理进度
                service_database=service_database,  # 字典
            )
            df_to_json.as_json_file()  # 写入 json 文件, 包含数据的 dtypes 信息


def date_table():
    """
    生成 pbix 使用的日期表
    """
    start_date = '2022-01-01'  # 日期表的起始日期
    yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
    dic = pd.date_range(start=start_date, end=yesterday)
    df = pd.DataFrame(dic, columns=['日期'])
    df.sort_values('日期', ascending=True, ignore_index=True, inplace=True)
    df.reset_index(inplace=True)
    # inplace 添加索引到 df
    p = df.pop('index')
    df['月2'] = df['日期']
    df['月2'] = df['月2'].dt.month
    df['日期'] = df['日期'].dt.date  # 日期格式保留年月日，去掉时分秒
    df['年'] = df['日期'].apply(lambda x: str(x).split('-')[0] + '年')
    df['月'] = df['月2'].apply(lambda x: str(x) + '月')
    # df.drop('月2', axis=1, inplace=True)
    mon = df.pop('月2')
    df['日'] = df['日期'].apply(lambda x: str(x).split('-')[2])
    df['年月'] = df.apply(lambda x: x['年'] + x['月'], axis=1)
    df['月日'] = df.apply(lambda x: x['月'] + x['日'] + '日', axis=1)
    df['第n周'] = df['日期'].apply(lambda x: x.strftime('第%W周'))
    df['索引'] = p
    df['月索引'] = mon
    df.sort_values('日期', ascending=False, ignore_index=True, inplace=True)

    m = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
    )
    m.df_to_mysql(
        df=df,
        db_name='聚合数据',
        table_name='日期表',
        move_insert=True,  # 先删除，再插入
        df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
        drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
        filename=None,  # 用来追踪处理进度
        service_database=service_database,  # 用来追踪处理进度
    )


def main(is_mysql=False, is_company=False):
    """
    is_mysql: 调试时加，False: 是否后续的聚合数据
    is_company: 公司电脑不需要移动文件到原始文件
    """

    cn = DataClean(
        path=upload_path,  # 源文件目录，下载文件夹
        source_path=source_path3,  # 原始文件保存目录
    )
    cn.new_unzip(is_move=True)  # 解压文件， is_move 解压后是否删除原 zip 压缩文件
    cn.sycm_tm(is_except=['except'])  # 天猫生意参谋
    cn.dmp_tm(is_except=['except'])  # 达摩盘
    cn.tg_reports(is_except=['except'])  # 推广报表，天猫淘宝共同清洗
    cn.syj_reports_tm(is_except=['except'])  # 天猫生意经

    cn.jd_reports(is_except=['except'])  # 清洗京东报表
    cn.sp_scene_clean(is_except=['except'])  # 商品素材
    cn.upload_df()  # 上传数据库

    if is_company:  # 公司移除所有文件
        files = os.listdir(upload_path)
        for file in files:
            os.remove(os.path.join(upload_path, file))
    else:  # 其他主机则进行文件分类
        cn.move_sycm(is_except=['临时文件', ])  # 生意参谋，移到文件到原始文件夹
        cn.move_dmp(is_except=['临时文件', ])  # 达摩盘
        cn.move_sjy(is_except=['临时文件',])  # 生意经，移到文件到原始文件夹
        cn.move_jd(is_except=['临时文件', ])  # 京东，移到文件到原始文件夹
        cn.move_tg_tm(is_except=['临时文件', ])  # 天猫，移到文件到原始文件夹
        cn.move_tg_tb(is_except=['临时文件', ])  # 淘宝店，移到文件到原始文件夹

    if not is_mysql:
        return

    # 更新日期表
    date_table()
    # 更新货品年份基准表， 属性设置 3 - 货品年份基准
    p = products.Products()
    p.to_mysql()

    conf = myconfig.main()
    data = conf['Windows']['xigua_lx']['mysql']['local']
    db_list = conf['Windows']['xigua_lx']['mysql']['数据库集']
    db_list = [item for item in db_list if item != '聚合数据']
    # 清理所有非聚合数据的库
    optimize_data.op_data(
        db_name_lists=db_list,
        days=5,
        is_mongo=True,
        is_mysql=True,
    )

    # 数据聚合
    query_data.data_aggregation(months=3)
    time.sleep(60)

    # 清理聚合数据, mongodb 中没有聚合数据，所以只需要清理 mysql 即可
    optimize_data.op_data(
        db_name_lists=['聚合数据'],
        days=100,
        is_mongo=False,
        is_mysql=True,
    )


if __name__ == '__main__':
    main(is_mysql=False)
