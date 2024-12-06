# -*- coding: UTF-8 –*-
import re
import socket
from mdbq.mysql import mysql
from mdbq.mysql import s_query
from mdbq.aggregation import optimize_data
from mdbq.config import myconfig
from mdbq.config import products
from mdbq.config import set_support
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from functools import wraps
import platform
import getpass
import json
import os
import time
import calendar
import concurrent.futures
import traceback

"""

"""
error_file = os.path.join(set_support.SetSupport(dirname='support').dirname, 'error.log')
m_engine = mysql.MysqlUpload(username='', password='', host='', port=0, charset='utf8mb4')
company_engine = mysql.MysqlUpload(username='', password='', host='', port=0, charset='utf8mb4')

if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['remoto']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    m_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    conf_data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    company_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    targe_host = 'company'

else:
    conf = myconfig.main()

    conf_data = conf['Windows']['company']['mysql']['remoto']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    company_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )

    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    m_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    targe_host = 'xigua_lx'


class MysqlDatasQuery:
    """
    从数据库中下载数据
    """
    def __init__(self):
        # target_service 从哪个服务器下载数据
        self.months = 0  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今
        # 实例化一个下载类
        self.download = s_query.QueryDatas(username=username, password=password, host=host, port=port)
        self.update_service = True  # 调试时加，true: 将数据写入 mysql 服务器
        self.pf_datas = []
        self.pf_datas_jd = []  # 京东聚合销售表
        self.output = set_support.SetSupport(dirname='support')

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回
                with open(error_file, 'a') as f:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f'\n{now}\n')
                    # f.write(f'报错的文件:\n{e.__traceback__.tb_frame.f_globals["__file__"]}\n')  # 发生异常所在的文件
                traceback.print_exc(file=open(error_file, 'a'))  # 返回完整的堆栈信息
                print(f'更多信息请查看日志文件: {error_file}')

        return wrapper

    # @try_except
    def tg_wxt(self, db_name='聚合数据', table_name='天猫_主体报表', is_maximize=True):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year+1):
            df = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'主体报表_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df.rename(columns={
            '场景名字': '营销场景',
            '主体id': '商品id',
            '总购物车数': '加购量',
            '总成交笔数': '成交笔数',
            '总成交金额': '成交金额'
        }, inplace=True)
        df = df.astype({
            '商品id': str,
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'float64',
            '自然流量曝光量': 'int64',
            '直接成交笔数': 'int64',
            '直接成交金额': 'float64',
        }, errors='raise')
        if is_maximize:
            df = df.groupby(['日期', '店铺名称', '营销场景', '商品id', '花费', '点击量'], as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '加购量': ('加购量', np.max),
                   '成交笔数': ('成交笔数', np.max),
                   '成交金额': ('成交金额', np.max),
                   '自然流量曝光量': ('自然流量曝光量', np.max),
                   '直接成交笔数': ('直接成交笔数', np.max),
                   '直接成交金额': ('直接成交金额', np.max)
                   }
            )
        else:
            df = df.groupby(['日期', '店铺名称', '营销场景', '商品id', '花费', '点击量'], as_index=False).agg(
                **{
                    '展现量': ('展现量', np.min),
                    '加购量': ('加购量', np.min),
                    '成交笔数': ('成交笔数', np.min),
                    '成交金额': ('成交金额', np.min),
                    '自然流量曝光量': ('自然流量曝光量', np.min),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max)
                }
            )
        df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '商品id': 'bigint',
            '花费': 'decimal(12,2)',
            '展现量': 'int',
            '点击量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '自然流量曝光量': 'int',
            '直接成交笔数': 'int',
            '直接成交金额': 'decimal(12,2)',
        }
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['日期', '店铺名称', '商品id', '花费', '成交金额', '直接成交金额']]
            }
        )  # 制作其他聚合表
        self.pf_datas.append(
            {
                '集合名称': '天猫汇总表调用',
                '数据主体': df[
                    ['日期', '店铺名称', '推广渠道', '营销场景', '商品id', '花费', '展现量', '点击量', '加购量',
                     '成交笔数', '成交金额', '直接成交笔数', '直接成交金额', '自然流量曝光量']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )

        # df_pic：商品排序索引表, 给 powerbi 中的主推款排序用的,(从上月1号到今天的总花费进行排序)
        today = datetime.date.today()
        last_month = today - datetime.timedelta(days=30)
        if last_month.month == 12:
            year_my = today.year - 1
        else:
            year_my = today.year
        # 截取 从上月1日 至 今天的花费数据, 推广款式按此数据从高到低排序（商品图+排序）
        # df_pic_lin = df[df['店铺名称'] == '万里马官方旗舰店']
        df_pic = df.groupby(['日期', '店铺名称', '商品id'], as_index=False).agg({'花费': 'sum'})
        if len(df_pic) == 0:
            return True
        df_pic = df_pic[~df_pic['商品id'].isin([''])]  # 指定列中删除包含空值的行
        date_obj = datetime.datetime.strptime(f'{year_my}-{last_month.month}-01', '%Y-%m-%d').date()
        df_pic = df_pic[(df_pic['日期'] >= date_obj)]
        df_pic = df_pic.groupby(['店铺名称', '商品id'], as_index=False).agg({'花费': 'sum'})
        df_pic.sort_values('花费', ascending=False, ignore_index=True, inplace=True)
        df_pic.reset_index(inplace=True)
        df_pic['index'] = df_pic['index'] + 100
        df_pic.rename(columns={'index': '商品索引'}, inplace=True)
        df_pic['商品索引'].fillna(1000, inplace=True)
        df_pic.pop('花费')
        p= df_pic.pop('商品索引')
        df_pic.insert(loc=2, column='商品索引', value=p)  # df中插入新列
        df_pic['更新时间'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_typ = {
            '商品id': 'bigint',
            '店铺名称': 'varchar(100)',
            '商品索引': 'smallint',
            '花费': 'decimal(12,2)',
            '更新时间': 'timestamp',
        }
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) 属性设置3/商品索引表_主推排序调用')
        m_engine.df_to_mysql(
            df=df_pic,
            db_name='属性设置3',
            table_name='商品索引表_主推排序调用',
            icm_update=['商品id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df_pic,
            db_name='属性设置3',
            table_name='商品索引表_主推排序调用',
            icm_update=['商品id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def syj(self, db_name='聚合数据', table_name='生意经_宝贝指标'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '宝贝id': 1,
            '商家编码': 1,
            '行业类目': 1,
            '销售额': 1,
            '销售量': 1,
            '订单数': 1,
            '退货量': 1,
            '退款额': 1,
            '退款额_发货后': 1,
            '退货量_发货后': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='生意经3',
                table_name=f'宝贝指标_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df['宝贝id'] = df['宝贝id'].astype(str)
        df = df.groupby(['日期', '店铺名称', '宝贝id', '行业类目'], as_index=False).agg(
            **{
                '销售额': ('销售额', np.min),
                '销售量': ('销售量', np.min),
                '订单数': ('订单数', np.min),
                '退货量': ('退货量', np.max),
                '退款额': ('退款额', np.max),
                '退款额_发货后': ('退款额_发货后', np.max),
                '退货量_发货后': ('退货量_发货后', np.max),
               }
        )
        df['件均价'] = df.apply(lambda x: x['销售额'] / x['销售量'] if x['销售量'] > 0 else 0, axis=1).round(
            0)  # 两列运算, 避免除以0
        df['价格带'] = df['件均价'].apply(
            lambda x: '2000+' if x >= 2000
            else '1000+' if x >= 1000
            else '500+' if x >= 500
            else '300+' if x >= 300
            else '300以下'
        )
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '宝贝id': 'bigint',
            '行业类目': 'varchar(255)',
            '销售额': 'decimal(12,2)',
            '销售量': 'int',
            '订单数': 'int',
            '退货量': 'int',
            '退款额': 'decimal(12,2)',
            '退款额_发货后': 'decimal(12,2)',
            '退货量_发货后': 'int',
            '件均价': 'mediumint',
            '价格带': 'varchar(100)',
        }
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['日期', '店铺名称', '宝贝id', '销售额', '销售量', '退款额_发货后', '退货量_发货后']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '宝贝id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '宝贝id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def tg_rqbb(self, db_name='聚合数据', table_name='天猫_人群报表', is_maximize=True):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
            '人群名字': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'人群报表_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df.rename(columns={
            '场景名字': '营销场景',
            '主体id': '商品id',
            '总购物车数': '加购量',
            '总成交笔数': '成交笔数',
            '总成交金额': '成交金额'
        }, inplace=True)
        df.fillna(0, inplace=True)
        df = df.astype({
            '商品id': str,
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'int64',
            '直接成交笔数': 'int64',
            '直接成交金额': 'float64',
        }, errors='raise')
        if is_maximize:
            df = df.groupby(['日期', '店铺名称', '营销场景', '商品id', '花费', '点击量', '人群名字'],
                            as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '加购量': ('加购量', np.max),
                    '成交笔数': ('成交笔数', np.max),
                    '成交金额': ('成交金额', np.max),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max)
                }
            )
        else:
            df = df.groupby(['日期', '店铺名称', '营销场景', '商品id', '花费', '点击量', '人群名字'],
                            as_index=False).agg(
                **{
                    '展现量': ('展现量', np.min),
                    '加购量': ('加购量', np.min),
                    '成交笔数': ('成交笔数', np.min),
                    '成交金额': ('成交金额', np.min),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max)
                }
            )
        df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
        # 1. 匹配 L后面接 2 个或以上数字，不区分大小写，示例：L345
        # 2. 其余情况，L 后面接多个数字的都会被第一条 if 命中，不区分大小写
        df['消费力层级'] = df.apply(
            lambda x:
            ''.join(re.findall(r'(l\d+)', x['人群名字'].upper(), re.IGNORECASE)) if re.findall(r'(l\d{2,})',
                                                                                               x['人群名字'],
                                                                                               re.IGNORECASE)
            else 'L5' if re.findall(r'(l\d*5)', x['人群名字'], re.IGNORECASE)
            else 'L4' if re.findall(r'(l\d*4)', x['人群名字'], re.IGNORECASE)
            else 'L3' if re.findall(r'(l\d*3)', x['人群名字'], re.IGNORECASE)
            else 'L2' if re.findall(r'(l\d*2)', x['人群名字'], re.IGNORECASE)
            else 'L1' if re.findall(r'(l\d*1)', x['人群名字'], re.IGNORECASE)
            else '', axis=1)
        # 1. 匹配连续的 4 个数字且后面不能接数字或"元"或汉字，筛掉的人群示例：月均消费6000元｜受众20240729175213｜xxx2024真皮公文包
        # 2. 匹配 2数字_2数字且前面不能是数字，合法匹配：人群_30_50_促； 非法示例：L345_3040 避免识别出 35～20 岁用户的情况
        # pattern = r'(\d{4})(?!\d|[\u4e00-\u9fa5])'  # 匹配 4 个数字，后面不能接数字或汉字
        # pattern = r'(?<![\d\u4e00-\u9fa5])(\d{4})' # 匹配前面不是数字或汉字的 4 个连续数字

        # 匹配 4 个数字，前面和后面都不能是数字或汉字
        pattern1 = r'(?<![\d\u4e00-\u9fa5])(\d{4})(?!\d|[\u4e00-\u9fa5])'
        # 匹配指定字符，前面不能是数字或 l 或 L 开头
        pattern2 = r'(?<![\dlL])(\d{2}_\d{2})'
        df['用户年龄'] = df.apply(
            lambda x:
            ''.join(re.findall(pattern1, x['人群名字'].upper())) if re.findall(pattern1, x['人群名字'])
            # else ''.join(re.findall(r'[^\d|l|L](\d{2}_\d{2})', x['人群名字'].upper())) if re.findall(r'[^\d|l|L](\d{2}_\d{2})', x['人群名字'])
            else ''.join(re.findall(pattern2, x['人群名字'].upper())) if re.findall(pattern2, x['人群名字'])
            else ''.join(re.findall(r'(\d{2}-\d{2})岁', x['人群名字'].upper())) if re.findall(r'(\d{2}-\d{2})岁',
                                                                                              x['人群名字'])
            else '', axis=1)
        df['用户年龄'] = df['用户年龄'].apply(
            lambda x: f'{x[:2]}~{x[2:4]}' if str(x).isdigit()
            else str(x).replace('_', '~') if '_' in x
            else str(x).replace('-', '~') if '-' in x
            else x
        )
        # 年龄层不能是 0 开头
        df['用户年龄'] = df['用户年龄'].apply(
            lambda x: '' if str(x).startswith('0') else x)
        # df = df.head(1000)
        # df.to_csv('/Users/xigua/Downloads/test.csv', index=False, header=True, encoding='utf-8_sig')
        # breakpoint()

        # 下面是添加人群 AIPL 分类
        dir_file = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新\\分类配置文件.xlsx'
        dir_file2 = '/Volumes/时尚事业部/01.运营部/0-电商周报-每周五更新/分类配置文件.xlsx'
        if platform.system() == 'Windows':
            dir_file3 = 'C:\\同步空间\\BaiduSyncdisk\\原始文件3\\分类配置文件.xlsx'
        else:
            dir_file3 = '/Users/xigua/数据中心/原始文件3/分类配置文件.xlsx'
        if not os.path.isfile(dir_file):
            dir_file = dir_file2
        if not os.path.isfile(dir_file):
            dir_file = dir_file3
        if os.path.isfile(dir_file):
            df_fl = pd.read_excel(dir_file, sheet_name='人群分类', header=0)
            df_fl = df_fl[['人群名字', '人群分类']]
            # 合并并获取分类信息
            df = pd.merge(df, df_fl, left_on=['人群名字'], right_on=['人群名字'], how='left')
            df['人群分类'].fillna('', inplace=True)
        if '人群分类' in df.columns.tolist():
            # 这行决定了，从文件中读取的分类信息优先级高于内部函数的分类规则
            # 这个 lambda 适配人群名字中带有特定标识的分类，强匹配，自定义命名
            df['人群分类'] = df.apply(
                lambda x: self.set_crowd(keyword=str(x['人群名字']), as_file=False) if x['人群分类'] == ''
                else x['人群分类'], axis=1
            )
            # 这个 lambda 适配人群名字中聚类的特征字符，弱匹配
            df['人群分类'] = df.apply(
                lambda x: self.set_crowd2(keyword=str(x['人群名字']), as_file=False) if x['人群分类'] == ''
                else x['人群分类'], axis=1
            )
        else:
            df['人群分类'] = df['人群名字'].apply(lambda x: self.set_crowd(keyword=str(x), as_file=False))
            df['人群分类'] = df.apply(
                lambda x: self.set_crowd2(keyword=str(x['人群名字']), as_file=False) if x['人群分类'] == ''
                else x['人群分类'], axis=1
            )
        df['人群分类'] = df['人群分类'].apply(lambda x: str(x).upper() if x else x)
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '商品id': 'bigint',
            '花费': 'decimal(10,2)',
            '展现量': 'int',
            '点击量': 'int',
            '人群名字': 'varchar(255)',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '直接成交笔数': 'int',
            '直接成交金额': 'decimal(12,2)',
            '消费力层级': 'varchar(100)',
            '用户年龄': 'varchar(100)',
            '人群分类': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费', '人群名字'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费', '人群名字'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def tg_gjc(self, db_name='聚合数据', table_name='天猫_关键词报表', is_maximize=True):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '宝贝id': 1,
            '词类型': 1,
            '词名字_词包名字': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'关键词报表_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df.rename(columns={
            '场景名字': '营销场景',
            '宝贝id': '商品id',
            '总购物车数': '加购量',
            '总成交笔数': '成交笔数',
            '总成交金额': '成交金额'
        }, inplace=True)
        df.fillna(0, inplace=True)
        df = df.astype({
            '商品id': str,
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'float64',
            '直接成交笔数': 'int64',
            '直接成交金额': 'float64',
        }, errors='raise')
        if is_maximize:
            df = df.groupby(
                ['日期', '店铺名称', '营销场景', '商品id', '词类型', '词名字_词包名字', '花费', '点击量'],
                as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '加购量': ('加购量', np.max),
                    '成交笔数': ('成交笔数', np.max),
                    '成交金额': ('成交金额', np.max),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max)
                }
            )
        else:
            df = df.groupby(
                ['日期', '店铺名称', '营销场景', '商品id', '词类型', '词名字_词包名字', '花费', '点击量'],
                as_index=False).agg(
                **{
                    '展现量': ('展现量', np.min),
                    '加购量': ('加购量', np.min),
                    '成交笔数': ('成交笔数', np.min),
                    '成交金额': ('成交金额', np.min),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max)
                }
            )
        df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
        df['是否品牌词'] = df['词名字_词包名字'].str.contains('万里马|wanlima', regex=True)
        df['是否品牌词'] = df['是否品牌词'].apply(lambda x: '品牌词' if x else '')
        dir_file = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新\\分类配置文件.xlsx'
        dir_file2 = '/Volumes/时尚事业部/01.运营部/0-电商周报-每周五更新/分类配置文件.xlsx'
        if not os.path.isfile(dir_file):
            dir_file = dir_file2
        if os.path.isfile(dir_file):
            df_fl = pd.read_excel(dir_file, sheet_name='关键词分类', header=0)
            # df_fl.rename(columns={'分类1': '词分类'}, inplace=True)
            df_fl = df_fl[['关键词', '词分类']]
            # 合并并获取词分类信息
            df = pd.merge(df, df_fl, left_on=['词名字_词包名字'], right_on=['关键词'], how='left')
            df.pop('关键词')
            df['词分类'].fillna('', inplace=True)
        if '词分类' in df.columns.tolist():
            # 这行决定了，从文件中读取的词分类信息优先级高于 ret_keyword 函数的词分类
            df['词分类'] = df.apply(
                lambda x: self.ret_keyword(keyword=str(x['词名字_词包名字']), as_file=False) if x['词分类'] == ''
                else x['词分类'], axis=1
            )
        else:
            df['词分类'] = df['词名字_词包名字'].apply(lambda x: self.ret_keyword(keyword=str(x), as_file=False))
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '商品id': 'bigint',
            '词类型': 'varchar(100)',
            '词名字_词包名字': 'varchar(255)',
            '花费': 'decimal(10,2)',
            '展现量': 'int',
            '点击量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '直接成交笔数': 'int',
            '直接成交金额': 'decimal(12,2)',
            '是否品牌词': 'varchar(100)',
            '词分类': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费', '词类型', '词名字_词包名字',],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '商品id', '花费', '词类型', '词名字_词包名字',],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def tg_cjzb(self, db_name='聚合数据', table_name='天猫_超级直播', is_maximize=True):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '人群名字': 1,
            '计划名字': 1,
            '花费': 1,
            '展现量': 1,
            '进店量': 1,
            '粉丝关注量': 1,
            '观看次数': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'超级直播报表_人群_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df.rename(columns={
            '观看次数': '观看次数',
            '总购物车数': '加购量',
            '总成交笔数': '成交笔数',
            '总成交金额': '成交金额',
            '场景名字': '营销场景',
        }, inplace=True)
        df['营销场景'] = '超级直播'
        df.fillna(0, inplace=True)
        df = df.astype({
            '花费': 'float64',
            # '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'float64',
            '进店量': 'int64',
            '粉丝关注量': 'int64',
            '观看次数': 'int64',
        }, errors='raise')
        if is_maximize:
            df = df.groupby(['日期', '店铺名称', '营销场景', '人群名字', '计划名字', '花费', '观看次数'],
                            as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '进店量': ('进店量', np.max),
                    '粉丝关注量': ('粉丝关注量', np.max),
                    '加购量': ('加购量', np.max),
                    '成交笔数': ('成交笔数', np.max),
                    '成交金额': ('成交金额', np.max),
                    '直接成交笔数': ('直接成交笔数', np.max),
                    '直接成交金额': ('直接成交金额', np.max),
                }
            )
        else:
            df = df.groupby(['日期', '店铺名称', '营销场景', '人群名字', '计划名字', '花费', '观看次数'],
                            as_index=False).agg(
                **{
                    '展现量': ('展现量', np.min),
                    '进店量': ('进店量', np.min),
                    '粉丝关注量': ('粉丝关注量', np.min),
                    '加购量': ('加购量', np.min),
                    '成交笔数': ('成交笔数', np.min),
                    '成交金额': ('成交金额', np.min),
                    '直接成交笔数': ('直接成交笔数', np.min),
                    '直接成交金额': ('直接成交金额', np.min),
                }
            )
        df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['日期', '店铺名称', '推广渠道', '营销场景', '花费', '展现量', '观看次数', '加购量', '成交笔数', '成交金额', '直接成交笔数', '直接成交金额']]
            },
        )  # 制作其他聚合表
        if not self.update_service:
            return
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '人群名字': 'varchar(255)',
            '计划名字': 'varchar(255)',
            '花费': 'decimal(10,2)',
            '观看次数': 'int',
            '展现量': 'int',
            '进店量': 'int',
            '粉丝关注量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '直接成交笔数': 'int',
            '直接成交金额': 'decimal(12,2)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '推广渠道', '营销场景', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def pxb_zh(self, db_name='聚合数据', table_name='天猫_品销宝账户报表', is_maximize=True):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '报表类型': 1,
            '搜索量': 1,
            '搜索访客数': 1,
            '展现量': 1,
            # '自然流量增量曝光': 1,
            '消耗': 1,
            '点击量': 1,
            '宝贝加购数': 1,
            '成交笔数': 1,
            '成交金额': 1,
            # '成交访客数': 1
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'品销宝_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df = df[df['报表类型'] == '账户']
        df.fillna(value=0, inplace=True)
        df.rename(columns={
            '消耗': '花费',
            '宝贝加购数': '加购量',
            '搜索量': '品牌搜索量',
            '搜索访客数': '品牌搜索人数'
        }, inplace=True)
        df = df.astype({
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'int64',
            '品牌搜索量': 'int64',
            '品牌搜索人数': 'int64',
        }, errors='raise')
        if is_maximize:
            df = df.groupby(['日期', '店铺名称', '报表类型', '花费', '点击量'], as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '加购量': ('加购量', np.max),
                    '成交笔数': ('成交笔数', np.max),
                    '成交金额': ('成交金额', np.max),
                    '品牌搜索量': ('品牌搜索量', np.max),
                    '品牌搜索人数': ('品牌搜索人数', np.max),
                }
            )
        else:
            df = df.groupby(['日期', '店铺名称', '报表类型', '花费', '点击量'], as_index=False).agg(
                **{
                    '展现量': ('展现量', np.min),
                    '加购量': ('加购量', np.min),
                    '成交笔数': ('成交笔数', np.min),
                    '成交金额': ('成交金额', np.min),
                    '品牌搜索量': ('品牌搜索量', np.min),
                    '品牌搜索人数': ('品牌搜索人数', np.min),
                }
            )
        df.insert(loc=1, column='推广渠道', value='品销宝')  # df中插入新列
        df.insert(loc=2, column='营销场景', value='品销宝')  # df中插入新列
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['日期', '店铺名称', '推广渠道', '营销场景', '花费', '展现量', '点击量', '加购量', '成交笔数', '成交金额']]
            },
        )  # 制作其他聚合表
        if not self.update_service:
            return
        set_typ = {
            '日期': 'date',
            '推广渠道': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '报表类型': 'varchar(100)',
            '花费': 'decimal(10,2)',
            '展现量': 'int',
            '点击量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '品牌搜索量': 'int',
            '品牌搜索人数': 'int',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '报表类型', '推广渠道', '营销场景', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '报表类型', '推广渠道', '营销场景', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def idbm(self, db_name='聚合数据', table_name='商品id编码表'):
        """ 用生意经日数据制作商品 id 和编码对照表 """
        year = datetime.datetime.today().year
        data_values = []
        for year in range(2022, year+1):
            data_values += self.download.columns_to_list(
                db_name='生意经3',
                table_name=f'宝贝指标_{year}',
                columns_name=['宝贝id', '商家编码', '行业类目'],
            )
        df = pd.DataFrame(data=data_values)
        df['宝贝id'] = df['宝贝id'].astype(str)
        df.drop_duplicates(subset='宝贝id', keep='last', inplace=True, ignore_index=True)
        # df['行业类目'] = df['行业类目'].apply(lambda x: re.sub(' ', '', x))
        try:
            df[['一级类目', '二级类目', '三级类目']] = df['行业类目'].str.split(' -> ', expand=True).loc[:, 0:2]
        except:
            try:
                df[['一级类目', '二级类目']] = df['行业类目'].str.split(' -> ', expand=True).loc[:, 0:1]
            except:
                df['一级类目'] = df['行业类目']
        df.drop('行业类目', axis=1, inplace=True)
        df.sort_values('宝贝id', ascending=False, inplace=True)
        df = df[(df['宝贝id'] != '973') & (df['宝贝id'] != 973) & (df['宝贝id'] != '0')]
        set_typ = {
            '宝贝id': 'bigint',
            '商家编码': 'varchar(100)',
            '一级类目': 'varchar(100)',
            '二级类目': 'varchar(100)',
            '三级类目': 'varchar(100)',
        }
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['宝贝id', '商家编码']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['宝贝id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['宝贝id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def sp_picture(self, db_name='聚合数据', table_name='商品id图片对照表'):
        """ 用生意经日数据制作商品 id 和编码对照表 """
        data_values = self.download.columns_to_list(
            db_name='属性设置3',
            table_name='商品素材中心',
            columns_name=['日期', '商品id', '商品白底图', '方版场景图'],
        )
        df = pd.DataFrame(data=data_values)
        df['商品id'] = df['商品id'].astype('int64')
        df['日期'] = df['日期'].astype('datetime64[ns]')
        df = df[(df['商品白底图'] != '0') | (df['方版场景图'] != '0')]
        # 白底图优先
        df['商品图片'] = df[['商品白底图', '方版场景图']].apply(
            lambda x: x['商品白底图'] if x['商品白底图'] != '0' else x['方版场景图'], axis=1)
        # # 方版场景图优先
        # df['商品图片'] = df[['商品白底图', '方版场景图']].apply(
        #     lambda x: x['方版场景图'] if x['方版场景图'] != '0' else x['商品白底图'], axis=1)
        df.sort_values(by=['商品id', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
        df.drop_duplicates(subset=['商品id'], keep='last', inplace=True, ignore_index=True)
        df = df[['商品id', '商品图片', '日期']]
        df['商品图片'] = df['商品图片'].apply(lambda x: x if 'http' in x else None)  # 检查是否是 http 链接
        df.dropna(how='all', subset=['商品图片'], axis=0, inplace=True)  # 删除指定列含有空值的行
        df['商品链接'] = df['商品id'].apply(
            lambda x: f'https://detail.tmall.com/item.htm?id={str(x)}' if x and '.com' not in str(x) else x)
        df.sort_values(by='商品id', ascending=False, ignore_index=True, inplace=True)  # ascending=False 降序排列
        set_typ = {
            '商品id': 'bigint',
            '商品图片': 'varchar(255)',
            '日期': 'date',
            '商品链接': 'varchar(255)',
        }
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['商品id', '商品图片']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['商品id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['商品id'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    # @try_except
    def dplyd(self, db_name='聚合数据', table_name='店铺流量来源构成'):
        """ 新旧版取的字段是一样的 """
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '店铺名称': 1,
            '类别': 1,
            '来源构成': 1,
            '一级来源': 1,
            '二级来源': 1,
            '三级来源': 1,
            '访客数': 1,
            '支付金额': 1,
            '支付买家数': 1,
            '支付转化率': 1,
            '加购人数': 1,
            '加购件数': 1,
            '下单买家数': 1,
            '关注店铺人数': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year+1):
            df = self.download.data_to_df(
                db_name='生意参谋3',
                table_name=f'店铺流量来源构成_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df.drop_duplicates(subset=['日期', '店铺名称', '类别', '来源构成', '一级来源', '二级来源', '三级来源', '访客数'], keep='last', inplace=True, ignore_index=True)
        # 包含三级来源名称和预设索引值列
        # 截取 从上月1日 至 今天的花费数据, 推广款式按此数据从高到低排序（商品图+排序）
        last_month, ii = get_day_of_month(1)
        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
        df_visitor3 = df[df['日期'] >= pd.to_datetime(last_month)]
        df_visitor3 = df_visitor3[(df_visitor3['三级来源'] != '汇总') & (df_visitor3['三级来源'] != '0')]
        df_visitor3 = df_visitor3.groupby(['三级来源'], as_index=False).agg({'访客数': 'sum'})
        df_visitor3.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
        df_visitor3.reset_index(inplace=True)
        df_visitor3['index'] = df_visitor3['index'] + 100
        df_visitor3.rename(columns={'index': '三级来源索引'}, inplace=True)
        df_visitor3 = df_visitor3[['三级来源', '三级来源索引']]

        # 包含二级来源名称和预设索引值列
        df_visitor2 = df[df['日期'] >= pd.to_datetime(last_month)]
        df_visitor2 = df_visitor2[(df_visitor2['二级来源'] != '汇总') & (df_visitor2['二级来源'] != '0')]
        df_visitor2 = df_visitor2.groupby(['二级来源'], as_index=False).agg({'访客数': 'sum'})
        df_visitor2.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
        df_visitor2.reset_index(inplace=True)
        df_visitor2['index'] = df_visitor2['index'] + 100
        df_visitor2.rename(columns={'index': '二级来源索引'}, inplace=True)
        df_visitor2 = df_visitor2[['二级来源', '二级来源索引']]

        # 包含一级来源名称和预设索引值列
        df_visitor1 = df[df['日期'] >= pd.to_datetime(last_month)]
        df_visitor1 = df_visitor1[(df_visitor1['一级来源'] != '汇总') & (df_visitor1['一级来源'] != '0')]
        df_visitor1 = df_visitor1.groupby(['一级来源'], as_index=False).agg({'访客数': 'sum'})
        df_visitor1.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
        df_visitor1.reset_index(inplace=True)
        df_visitor1['index'] = df_visitor1['index'] + 100
        df_visitor1.rename(columns={'index': '一级来源索引'}, inplace=True)
        df_visitor1 = df_visitor1[['一级来源', '一级来源索引']]

        df = pd.merge(df, df_visitor1, how='left', left_on='一级来源', right_on='一级来源')
        df = pd.merge(df, df_visitor2, how='left', left_on='二级来源', right_on='二级来源')
        df = pd.merge(df, df_visitor3, how='left', left_on='三级来源', right_on='三级来源')
        for col in ['一级来源索引', '二级来源索引', '三级来源索引']:
            df[col] = df[col].apply(lambda x: 1000 if str(x) == 'nan' else x)
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '类别': 'varchar(100)',
            '来源构成': 'varchar(100)',
            '一级来源': 'varchar(100)',
            '二级来源': 'varchar(100)',
            '三级来源': 'varchar(100)',
            '访客数': 'int',
            '支付金额': 'decimal(12,2)',
            '支付买家数': 'int',
            '支付转化率': 'decimal(10,4)',
            '加购人数': 'int',
            '一级来源索引': 'smallint',
            '二级来源索引': 'smallint',
            '三级来源索引': 'smallint',
        }
        # df.to_csv('/Users/xigua/Downloads/ll.csv', index=False, header=True, encoding='utf-8_sig')
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '一级来源', '二级来源', '三级来源', '访客数'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '一级来源', '二级来源', '三级来源', '访客数'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def sp_cost(self, db_name='聚合数据', table_name='商品成本'):
        """ 电商定价 """
        data_values = self.download.columns_to_list(
            db_name='属性设置3',
            table_name='电商定价',
            columns_name=['日期', '款号', '年份季节', '吊牌价', '商家平台', '成本价', '天猫页面价', '天猫中促价'],
        )
        df = pd.DataFrame(data=data_values)
        df.sort_values(by=['款号', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
        df.drop_duplicates(subset=['款号'], keep='last', inplace=True, ignore_index=True)
        set_typ = {
            '日期': 'date',
            '款号': 'varchar(100)',
            '年份季节': 'varchar(100)',
            '吊牌价': 'decimal(10,2)',
            '成本价': 'decimal(10,2)',
            '天猫页面价': 'decimal(10,2)',
            '天猫中促价': 'decimal(10,2)',
        }
        self.pf_datas.append(
            {
                '集合名称': table_name,
                '数据主体': df[['款号', '成本价']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        min_date = pd.to_datetime(df['日期'].min()).strftime('%Y-%m-%d')
        max_date = pd.to_datetime(df['日期'].max()).strftime('%Y-%m-%d')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['款号'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=['款号'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=False,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=False,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    # @try_except
    def jdjzt(self, db_name='聚合数据', table_name='京东_京准通'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '产品线': 1,
            '触发sku_id': 1,
            '跟单sku_id': 1,
            '花费': 1,
            '展现数': 1,
            '点击数': 1,
            '直接订单行': 1,
            '直接订单金额': 1,
            '总订单行': 1,
            '总订单金额': 1,
            '直接加购数': 1,
            '总加购数': 1,
            'spu_id': 1,
            '店铺名称':1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                    db_name='京东数据3',
                    table_name=f'推广数据_京准通_{year}',
                    start_date=start_date,
                    end_date=end_date,
                    projection=projection,
                )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df = df.groupby(
            ['日期', '店铺名称', '产品线', '触发sku_id', '跟单sku_id', 'spu_id', '花费', '展现数', '点击数'],
            as_index=False).agg(
            **{
                '直接订单行': ('直接订单行', np.max),
                '直接订单金额': ('直接订单金额', np.max),
                '总订单行': ('总订单行', np.max),
                '总订单金额': ('总订单金额', np.max),
                '直接加购数': ('直接加购数', np.max),
                '总加购数': ('总加购数', np.max),
            }
        )
        df = df[df['花费'] > 0]
        projection={
            'sku_id': 1,
            'spu_id': 1,
        }
        df_sku = self.download.data_to_df(
            db_name='属性设置3',
            table_name='京东商品属性',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df.pop('spu_id')  # 删除推广表的 spu id
        df = pd.merge(df, df_sku, how='left', left_on='跟单sku_id', right_on='sku_id')
        df.pop('sku_id')  # 删除聚合后合并进来的 sku id，实际使用 跟单sku_id
        p = df.pop('spu_id')
        df.insert(loc=3, column='spu_id', value=p)

        self.pf_datas_jd.append(
            {
                '集合名称': table_name,
                '数据主体': df[['日期', '产品线', '触发sku_id', '跟单sku_id', '花费']]
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '产品线': 'varchar(100)',
            '触发sku_id': 'bigint',
            '跟单sku_id': 'bigint',
            'spu_id': 'bigint',
            '花费': 'decimal(10,2)',
            '展现数': 'int',
            '点击数': 'int',
            '直接订单行': 'int',
            '直接订单金额': 'decimal(10,2)',
            '总订单行': 'int',
            '总订单金额': 'decimal(10,2)',
            '直接加购数': 'int',
            '总加购数': 'int',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '触发sku_id', '跟单sku_id', '花费', ],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '触发sku_id', '跟单sku_id', '花费', ],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )

        # # 按照 spu 聚合
        # df = df.groupby(
        #     ['日期', '店铺名称', 'spu_id'],
        #     as_index=False).agg(
        #     **{
        #         '花费': ('花费', np.sum),
        #         '展现数': ('展现数', np.sum),
        #         '点击数': ('点击数', np.sum),
        #         '直接订单行': ('直接订单行', np.sum),
        #         '直接订单金额': ('直接订单金额', np.sum),
        #         '总订单行': ('总订单行', np.sum),
        #         '总订单金额': ('总订单金额', np.sum),
        #         '直接加购数': ('直接加购数', np.sum),
        #         '总加购数': ('总加购数', np.sum),
        #     }
        # )
        # min_date = df['日期'].min()
        # max_date = df['日期'].max()
        # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/京东_京准通_按spu -> {min_date}~{max_date}')
        # m_engine.df_to_mysql(
        #     df=df,
        #     db_name=db_name,
        #     table_name='京东_京准通_按spu',
        #     # icm_update=['日期', '产品线', '触发sku_id', '跟单sku_id', '花费', ],  # 增量更新, 在聚合数据中使用，其他不要用
        #     move_insert=True,  # 先删除，再插入
        #     df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
        #     drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
        #     count=None,
        #     filename=None,  # 用来追踪处理进度
        #     reset_id=True,  # 是否重置自增列
        #     set_typ=set_typ
        # )
        # company_engine.df_to_mysql(
        #     df=df,
        #     db_name=db_name,
        #     table_name='京东_京准通_按spu',
        #     # icm_update=['日期', '产品线', '触发sku_id', '跟单sku_id', '花费', ],  # 增量更新, 在聚合数据中使用，其他不要用
        #     move_insert=True,  # 先删除，再插入
        #     df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
        #     drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
        #     count=None,
        #     filename=None,  # 用来追踪处理进度
        #     reset_id=True,  # 是否重置自增列
        #     set_typ=set_typ
        # )

        return True

    @try_except
    def jdqzyx(self, db_name='聚合数据', table_name='京东_京准通_全站营销'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '店铺名称': 1,
            '产品线': 1,
            '花费': 1,
            '全站投产比': 1,
            '全站交易额': 1,
            '全站订单行': 1,
            '全站订单成本': 1,
            '全站费比': 1,
            '核心位置展现量': 1,
            '核心位置点击量': 1,
        }
        df = self.download.data_to_df(
            db_name='京东数据3',
            table_name='推广数据_全站营销',  # 暂缺
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df = df.groupby(['日期', '店铺名称', '产品线', '花费'], as_index=False).agg(
            **{
                '全站投产比': ('全站投产比', np.max),
                '全站交易额': ('全站交易额', np.max),
                '全站订单行': ('全站订单行', np.max),
                '全站订单成本': ('全站订单成本', np.max),
                '全站费比': ('全站费比', np.max),
                '核心位置展现量': ('核心位置展现量', np.max),
                '核心位置点击量': ('核心位置点击量', np.max),
            }
        )
        df = df[df['花费'] > 0]
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '产品线': 'varchar(100)',
            '花费': 'decimal(10,2)',
            '全站投产比': 'decimal(10,2)',
            '全站交易额': 'decimal(10,2)',
            '全站订单行': 'decimal(10,2)',
            '全站订单成本': 'decimal(10,2)',
            '全站费比': 'decimal(8,4)',
            '核心位置展现量': 'int',
            '核心位置点击量': 'int',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    @try_except
    def jd_gjc(self, db_name='聚合数据', table_name='京东_关键词报表'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '产品线': 1,
            '计划类型': 1,
            '计划id': 1,
            '推广计划': 1,
            '搜索词': 1,
            '关键词': 1,
            '关键词购买类型': 1,
            '广告定向类型': 1,
            '花费': 1,
            '展现数': 1,
            '点击数': 1,
            '直接订单行': 1,
            '直接订单金额': 1,
            '总订单行': 1,
            '总订单金额': 1,
            '总加购数': 1,
            '领券数': 1,
            '商品关注数': 1,
            '店铺关注数': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                    db_name='京东数据3',
                    table_name=f'推广数据_关键词报表_{year}',
                    start_date=start_date,
                    end_date=end_date,
                    projection=projection,
                )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df_lin = df[['计划id', '推广计划']]
        df_lin.drop_duplicates(subset=['计划id'], keep='last', inplace=True, ignore_index=True)
        df = df.groupby(
            ['日期', '产品线', '计划类型', '计划id', '搜索词', '关键词', '关键词购买类型', '广告定向类型', '展现数',
             '点击数', '花费'],
            as_index=False).agg(
            **{
                '直接订单行': ('直接订单行', np.max),
                '直接订单金额': ('直接订单金额', np.max),
                '总订单行': ('总订单行', np.max),
                '总订单金额': ('总订单金额', np.max),
                '总加购数': ('总加购数', np.max),
                '领券数': ('领券数', np.max),
                '商品关注数': ('商品关注数', np.max),
                '店铺关注数': ('店铺关注数', np.max)
            }
        )
        df = pd.merge(df, df_lin, how='left', left_on='计划id', right_on='计划id')
        df['k_是否品牌词'] = df['关键词'].str.contains('万里马|wanlima', regex=True)
        df['k_是否品牌词'] = df['k_是否品牌词'].apply(lambda x: '品牌词' if x else '')
        df['s_是否品牌词'] = df['搜索词'].str.contains('万里马|wanlima', regex=True)
        df['s_是否品牌词'] = df['s_是否品牌词'].apply(lambda x: '品牌词' if x else '')
        set_typ = {
            '日期': 'date',
            '产品线': 'varchar(100)',
            '计划类型': 'varchar(100)',
            '计划id': 'varchar(100)',
            '搜索词': 'varchar(100)',
            '关键词': 'varchar(100)',
            '关键词购买类型': 'varchar(100)',
            '广告定向类型': 'varchar(100)',
            '展现数': 'int',
            '点击数': 'int',
            '花费': 'decimal(10,2)',
            '直接订单行': 'int',
            '直接订单金额': 'decimal(12,2)',
            '总订单行': 'int',
            '总订单金额': 'decimal(12,2)',
            '总加购数': 'int',
            '领券数': 'int',
            '商品关注数': 'int',
            '店铺关注数': 'int',
            '推广计划': 'varchar(100)',
            'k_是否品牌词': 'varchar(100)',
            's_是否品牌词': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '搜索词',  '关键词', '展现数', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '产品线', '搜索词',  '关键词', '展现数', '花费'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    @try_except
    def sku_sales(self, db_name='聚合数据', table_name='京东_sku_商品明细'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '店铺名称': 1,
            '商品id': 1,
            '货号': 1,
            '成交单量': 1,
            '成交金额': 1,
            '访客数': 1,
            '成交客户数': 1,
            '加购商品件数': 1,
            '加购人数': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='京东数据3',
                table_name=f'京东商智_sku_商品明细_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df = df[df['商品id'] != '合计']
        df = df.groupby(['日期', '店铺名称', '商品id', '货号', '访客数', '成交客户数', '加购商品件数', '加购人数'],
                        as_index=False).agg(
            **{
                '成交单量': ('成交单量', np.max),
                '成交金额': ('成交金额', np.max),
            }
        )
        self.pf_datas_jd.append(
            {
                '集合名称': table_name,
                '数据主体': df
            }
        )  # 制作其他聚合表
        if not self.update_service:
            return
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '商品id': 'varchar(100)',
            '货号': 'varchar(100)',
            '访客数': 'int',
            '成交客户数': 'int',
            '加购商品件数': 'int',
            '加购人数': 'int',
            '成交单量': 'int',
            '成交金额': 'decimal(10,2)',
            'sku_id': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '商品id', '成交单量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '商品id', '成交单量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def spu_sales(self, db_name='聚合数据', table_name='京东_spu_商品明细'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '店铺名称': 1,
            '商品id': 1,
            '货号': 1,
            '成交单量': 1,
            '成交金额': 1,
            '访客数': 1,
            '成交客户数': 1,
            '加购商品件数': 1,
            '加购人数': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = self.download.data_to_df(
                db_name='京东数据3',
                table_name=f'京东商智_spu_商品明细_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df = df[df['商品id'] != '合计']
        df = df.groupby(['日期', '店铺名称', '商品id', '货号', '访客数', '成交客户数', '加购商品件数', '加购人数'],
                        as_index=False).agg(
            **{
                '成交单量': ('成交单量', np.max),
                '成交金额': ('成交金额', np.max),
            }
        )
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '商品id': 'varchar(100)',
            '货号': 'varchar(100)',
            '访客数': 'int',
            '成交客户数': 'int',
            '加购商品件数': 'int',
            '加购人数': 'int',
            '成交单量': 'int',
            '成交金额': 'decimal(10,2)',
            'spu_id': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '商品id', '成交单量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '商品id', '成交单量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    @try_except
    def se_search(self, db_name='聚合数据', table_name='天猫店铺来源_手淘搜索'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '店铺名称': 1,
            '搜索词': 1,
            '词类型': 1,
            '访客数': 1,
            '加购人数': 1,
            '商品收藏人数': 1,
            '支付转化率': 1,
            '支付买家数': 1,
            '支付金额': 1,
            '新访客': 1,
            '客单价': 1,
            'uv价值': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year+1):
            df = self.download.data_to_df(
                db_name='生意参谋3',
                table_name=f'手淘搜索_本店引流词_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        df = df.groupby(
            ['日期', '店铺名称', '词类型', '搜索词'],
            as_index=False).agg(
            **{
                '访客数': ('访客数', np.max),
                '加购人数': ('加购人数', np.max),
                '支付金额': ('支付金额', np.max),
                '支付转化率': ('支付转化率', np.max),
                '支付买家数': ('支付买家数', np.max),
                '客单价': ('客单价', np.max),
                'uv价值': ('uv价值', np.max)
            }
        )
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '词类型': 'varchar(100)',
            '搜索词': 'varchar(100)',
            '访客数': 'int',
            '加购人数': 'int',
            '支付金额': 'decimal(10,2)',
            '支付转化率': 'decimal(10,4)',
            '支付买家数': 'int',
            '客单价': 'decimal(10,2)',
            'uv价值': 'decimal(10,2)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '店铺名称', '词类型', '搜索词'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '店铺名称', '词类型', '搜索词'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def zb_ccfx(self, db_name='聚合数据', table_name='生意参谋_直播场次分析'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            # '日期': 1,
            # '店铺': 1,
            # '场次信息': 1,
            # '场次id': 1,
            # '直播开播时间': 1,
            # '开播时长': 1,
            # '封面图点击率': 1,
            # '观看人数': 1,
            # '观看次数': 1,
            # '新增粉丝数': 1,
            # '流量券消耗': 1,
            # '观看总时长（秒）': 1,
            # '人均观看时长（秒）': 1,
            # '次均观看时长（秒）': 1,
            # '商品点击人数': 1,
            # '商品点击次数': 1,
            # '商品点击率': 1,
            # '加购人数': 1,
            # '加购件数': 1,
            # '加购次数': 1,
            # '成交金额（元）': 1,
            # '成交人数': 1,
            # '成交件数': 1,
            # '成交笔数': 1,
            # '成交转化率': 1,
            # '退款人数': 1,
            # '退款笔数': 1,
            # '退款件数': 1,
            # '退款金额': 1,
            # '预售定金支付金额': 1,
            # '预售预估总金额': 1,
            # '店铺名称': 1,
        }
        df = self.download.data_to_df(
            db_name='生意参谋3',
            table_name='直播分场次效果',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df.drop_duplicates(subset=['场次id'], keep='first', inplace=True, ignore_index=True)
        set_typ = {
            '日期': 'DATE',
            '店铺名称': 'varchar(100)',
            'fvr_pv': 'int',
            '封面图点击率': 'decimal(10,4)',
            'itrt_pv    ': 'int',
            '开播时长': 'smallint',
            '成交笔数': 'smallint',
            'aov': 'decimal(10,2)',
            '退款金额': 'decimal(12,2)',
            '曝光pv': 'int',
            '场次信息': 'varchar(255)',
            'cmt_uv': 'int',
            '退款件数占比': 'decimal(10,4)',
            'reward_gift_cnt': 'smallint',
            '观看人数': 'int',
            '开播时长_f': 'varchar(100)',
            'reward_uv_rate': 'smallint',
            'fvr_uv': 'int',
            '直播开播时间': 'datetime',
            '商品点击率': 'decimal(10,4)',
            '加购次数': 'smallint',
            '成交转化率': 'decimal(10,4)',
            'atv': 'decimal(10,2)',
            '成交金额': 'decimal(12,2)',
            '退款人数': 'smallint',
            'index': 'smallint',
            '预售定金支付人数': 'smallint',
            '加购访客': 'smallint',
            '商品点击次数': 'int',
            '退款笔数': 'smallint',
            'itrt_uv': 'smallint',
            '成交人数': 'smallint',
            '观看总时长': 'varchar(100)',
            '加购访客转化率': 'decimal(10,4)',
            'subpay_order_cnt': 'smallint',
            'cmt_pv': 'int',
            '商品点击人数': 'int',
            'status': 'int',
            '商品曝光uv': 'int',
            '预售定金支付件数': 'smallint',
            '预售预估总金额': 'decimal(12,2)',
            '退款笔数占比': 'decimal(10,4)',
            'reward_pv': 'int',
            '访客点击量': 'int',
            'aiv': 'decimal(10,2)',
            'shr_uv': 'int',
            '浏览点击量': 'int',
            '场次图片': 'text',
            'user_role': 'varchar(100)',
            '退款人数占比': 'decimal(10,4)',
            '退款件数': 'smallint',
            '新增粉丝数': 'smallint',
            '场均观看时长': 'decimal(10,2)',
            '人均观看时长': 'decimal(10,2)',
            '加购人数': 'smallint',
            'reward_uv': 'smallint',
            '直播结束时间': 'datetime',
            '商品曝光pv': 'int',
            'shr_pv': 'int',
            '场次id': 'bigint',
            'look_pv_flowcontrol': 'smallint',
            '退款率': 'decimal(10,4)',
            'is_delete': 'varchar(50)',
            'atn_uv_rate': 'decimal(10,4)',
            '成交件数': 'smallint',
            '最大在线人数': 'int',
            '曝光uv': 'int',
            '加购件数': 'smallint',
            '预售定金支付金额': 'decimal(12,2)',
            '观看次数': 'int',
            '封面图': 'text',
            '更新时间': 'timestamp',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        new_dict = {
            '日期': '',
            '店铺名称': '',
            '场次信息': '',
            '场次id': '',
            '直播开播时间': '',
            '开播时长': '',
            '封面图点击率': '',
            '观看人数': '',
            '观看次数': '',
            '新增粉丝数': '',
            '流量券消耗': '',
            '观看总时长': '',
            '人均观看时长': '',
            '次均观看时长': '',
            '商品点击人数': '',
            '商品点击次数': '',
            '商品点击率': '',
            '加购人数': '',
            '加购件数': '',
            '加购次数': '',
            '成交金额': '',
            '成交人数': '',
            '成交件数': '',
            '成交笔数': '',
            '成交转化率': '',
            '退款人数': '',
            '退款笔数': '',
            '退款件数': '',
            '退款金额': '',
            '预售定金支付金额': '',
            '预售预估总金额': '',
        }
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        for dict_data in df.to_dict(orient='records'):
            new_dict.update(dict_data)
            m_engine.dict_to_mysql(
                db_name=db_name,
                table_name=table_name,
                dict_data=new_dict,
                unique_main_key=None,
                icm_update=['场次id'],  # 唯一组合键
                main_key=None,  # 指定索引列, 通常用日期列，默认会设置日期为索引
                set_typ=set_typ,  # 指定数据类型
            )
            company_engine.dict_to_mysql(
                db_name=db_name,
                table_name=table_name,
                dict_data=new_dict,
                unique_main_key=None,
                icm_update=['场次id'],  # 唯一组合键
                main_key=None,  # 指定索引列, 通常用日期列，默认会设置日期为索引
                set_typ=set_typ,  # 指定数据类型
            )
        return True

    # @try_except
    def tg_by_day(self, db_name='聚合数据', table_name='多店推广场景_按日聚合'):
        """
        汇总各个店铺的推广数据，按日汇总
        """
        df_tm = pd.DataFrame()  # 天猫营销场景
        df_tb = pd.DataFrame()  # 淘宝营销场景
        df_tb_qzt = pd.DataFrame()  # 淘宝全站推广
        df_tm_pxb = pd.DataFrame()  # 天猫品销宝
        df_tm_living = pd.DataFrame()  # 天猫超级直播
        df_jd = pd.DataFrame()  # 京东推广
        df_jd_qzyx = pd.DataFrame()  # 京东全站推广

        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景id': 1,
            '场景名字': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df_tm = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'营销场景报表_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df_tm)
        df_tm = pd.concat(__res, ignore_index=True)
        if len(df_tm) > 0:
            df_tm.rename(columns={'场景名字': '营销场景'}, inplace=True)
            df_tm = df_tm.groupby(
                ['日期', '店铺名称', '场景id', '营销场景', '花费', '展现量'],
                as_index=False).agg(
                **{
                    # '展现量': ('展现量', np.max),
                    '点击量': ('点击量', np.max),
                    '加购量': ('总购物车数', np.max),
                    '成交笔数': ('总成交笔数', np.max),
                    '成交金额': ('总成交金额', np.max)
                }
            )
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df_tb = self.download.data_to_df(
                db_name='推广数据_淘宝店',
                table_name=f'营销场景报表_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df_tb)
        df_tb = pd.concat(__res, ignore_index=True)
        if len(df_tb) > 0:
            df_tb.rename(columns={'场景名字': '营销场景'}, inplace=True)
            df_tb = df_tb.groupby(
                ['日期', '店铺名称', '场景id', '营销场景', '花费', '展现量'],
                as_index=False).agg(
                **{
                    # '展现量': ('展现量', np.max),
                    '点击量': ('点击量', np.max),
                    '加购量': ('总购物车数', np.max),
                    '成交笔数': ('总成交笔数', np.max),
                    '成交金额': ('总成交金额', np.max)
                }
            )

        #  天猫的全站推广包含在营销场景报表中，淘宝店不包含
        df_tb_qzt = pd.DataFrame()
        if '全站推广' not in df_tb['营销场景'].tolist():
            projection = {
                '日期': 1,
                '主体id': 1,
                '花费': 1,
                '展现量': 1,
                '点击量': 1,
                '总购物车数': 1,
                '总成交笔数': 1,
                '总成交金额': 1,
                '店铺名称': 1,
            }
            __res = []
            for year in range(2024, datetime.datetime.today().year + 1):
                df_tb_qzt = self.download.data_to_df(
                    db_name='推广数据_淘宝店',
                    table_name=f'全站推广报表_{year}',
                    start_date=start_date,
                    end_date=end_date,
                    projection=projection,
                )
                __res.append(df_tb_qzt)
            df_tb_qzt = pd.concat(__res, ignore_index=True)
            if len(df_tb_qzt) > 0:
                # 这一步是排重
                df_tb_qzt = df_tb_qzt.groupby(
                    ['日期', '店铺名称', '主体id', '花费'],
                    as_index=False).agg(
                    **{
                        '展现量': ('展现量', np.max),
                        '点击量': ('点击量', np.max),
                        '加购量': ('总购物车数', np.max),
                        '成交笔数': ('总成交笔数', np.max),
                        '成交金额': ('总成交金额', np.max)
                    }
                )
                # 这一步是继续聚合，因为这个报表统计的是场景维度，不需要商品维度
                df_tb_qzt = df_tb_qzt.groupby(
                    ['日期', '店铺名称', '花费'],
                    as_index=False).agg(
                    **{
                        '展现量': ('展现量', np.sum),
                        '点击量': ('点击量', np.sum),
                        '加购量': ('加购量', np.sum),
                        '成交笔数': ('成交笔数', np.sum),
                        '成交金额': ('成交金额', np.sum)
                    }
                )
                df_tb_qzt['营销场景'] = '全站推广'

        # 品销宝报表
        projection = {
            '日期': 1,
            '报表类型': 1,
            '消耗': 1,
            '展现量': 1,
            '点击量': 1,
            '宝贝加购数': 1,
            '成交笔数': 1,
            '成交金额': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df_tm_pxb = self.download.data_to_df(
                db_name='推广数据2',
                table_name=f'品销宝_{year}',
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df_tm_pxb)
        df_tm_pxb = pd.concat(__res, ignore_index=True)
        if len(df_tm_pxb) > 0:
            df_tm_pxb = df_tm_pxb[df_tm_pxb['报表类型'] == '账户']
            df_tm_pxb = df_tm_pxb.groupby(
                ['日期', '店铺名称', '报表类型', '消耗'],
                as_index=False).agg(
                **{
                    '展现量': ('展现量', np.max),
                    '点击量': ('点击量', np.max),
                    '加购量': ('宝贝加购数', np.max),
                    '成交笔数': ('成交笔数', np.max),
                    '成交金额': ('成交金额', np.max)
                }
            )
            df_tm_pxb.rename(columns={'报表类型': '营销场景', '消耗': '花费'}, inplace=True)
            df_tm_pxb['营销场景'] = '品销宝'

        # 因为 2024.04.16及之前的营销场景报表不含超级直播，所以在此添加
        if start_date < pd.to_datetime('2024-04-17'):
            projection = {
                '日期': 1,
                '场景名字': 1,
                '花费': 1,
                '展现量': 1,
                '观看次数': 1,
                '总购物车数': 1,
                '总成交笔数': 1,
                '总成交金额': 1,
                '店铺名称': 1,
            }
            __res = []
            for year in range(2024, datetime.datetime.today().year + 1):
                df_tm_living = self.download.data_to_df(
                    db_name='推广数据2',
                    table_name=f'超级直播报表_人群_{year}',
                    start_date=start_date,
                    end_date=pd.to_datetime('2024-04-16'),  # 只可以取此日期之前的数据
                    projection=projection,
                )
                __res.append(df_tm_living)
            df_tm_living = pd.concat(__res, ignore_index=True)
            if len(df_tm_living) > 0:
                df_tm_living.rename(columns={'场景名字': '营销场景'}, inplace=True)
                df_tm_living = df_tm_living.groupby(
                    ['日期', '店铺名称', '营销场景', '花费'],
                    as_index=False).agg(
                    **{
                        '展现量': ('展现量', np.max),
                        '点击量': ('观看次数', np.max),
                        '加购量': ('总购物车数', np.max),
                        '成交笔数': ('总成交笔数', np.max),
                        '成交金额': ('总成交金额', np.max)
                    }
                )

        projection = {
            '日期': 1,
            '产品线': 1,
            '触发sku_id': 1,
            '跟单sku_id': 1,
            '花费': 1,
            '展现数': 1,
            '点击数': 1,
            '直接订单行': 1,
            '直接订单金额': 1,
            '总订单行': 1,
            '总订单金额': 1,
            '直接加购数': 1,
            '总加购数': 1,
            'spu_id': 1,
            '店铺名称': 1,
        }
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df_jd = self.download.data_to_df(
                    db_name='京东数据3',
                    table_name=f'推广数据_京准通_{year}',
                    start_date=start_date,
                    end_date=end_date,
                    projection=projection,
                )
            __res.append(df_jd)
        df_jd = pd.concat(__res, ignore_index=True)
        if len(df_jd) > 0:
            df_jd = df_jd.groupby(['日期', '店铺名称', '产品线', '触发sku_id', '跟单sku_id', 'spu_id', '花费', '展现数', '点击数'],
                            as_index=False).agg(
                **{
                    '直接订单行': ('直接订单行', np.max),
                    '直接订单金额': ('直接订单金额', np.max),
                    '成交笔数': ('总订单行', np.max),
                    '成交金额': ('总订单金额', np.max),
                    '直接加购数': ('直接加购数', np.max),
                    '加购量': ('总加购数', np.max),
                }
            )
            df_jd = df_jd[['日期', '店铺名称', '产品线', '花费', '展现数', '点击数', '加购量', '成交笔数', '成交金额']]
            df_jd.rename(columns={'产品线': '营销场景', '展现数': '展现量', '点击数': '点击量'}, inplace=True)
            df_jd = df_jd[df_jd['花费'] > 0]

        projection = {
            '日期': 1,
            '产品线': 1,
            '花费': 1,
            '全站投产比': 1,
            '全站交易额': 1,
            '全站订单行': 1,
            '全站订单成本': 1,
            '全站费比': 1,
            '核心位置展现量': 1,
            '核心位置点击量': 1,
            '店铺名称': 1,
        }
        df_jd_qzyx = self.download.data_to_df(
            db_name='京东数据3',
            table_name='推广数据_全站营销',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        if len(df_jd_qzyx) > 0:
            df_jd_qzyx = df_jd_qzyx.groupby(['日期', '店铺名称', '产品线', '花费'], as_index=False).agg(
                **{'全站投产比': ('全站投产比', np.max),
                   '成交金额': ('全站交易额', np.max),
                   '成交笔数': ('全站订单行', np.max),
                   '全站订单成本': ('全站订单成本', np.max),
                   '全站费比': ('全站费比', np.max),
                   '展现量': ('核心位置展现量', np.max),
                   '点击量': ('核心位置点击量', np.max),
                   }
            )
            df_jd_qzyx.rename(columns={'产品线': '营销场景'}, inplace=True)
            df_jd_qzyx = df_jd_qzyx[['日期', '店铺名称', '营销场景', '花费', '展现量', '点击量', '成交笔数', '成交金额']]
            df_jd_qzyx = df_jd_qzyx[df_jd_qzyx['花费'] > 0]

        _datas = [item for item in  [df_tm, df_tb, df_tb_qzt, df_tm_pxb, df_tm_living, df_jd, df_jd_qzyx] if len(item) > 0]  # 阻止空的 dataframe
        df = pd.concat(_datas, axis=0, ignore_index=True)
        df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
        df = df.groupby(
            ['日期', '店铺名称', '营销场景'],
            as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '展现量': ('展现量', np.sum),
                '点击量': ('点击量', np.sum),
                '加购量': ('加购量', np.sum),
                '成交笔数': ('成交笔数', np.sum),
                '成交金额': ('成交金额', np.sum)
            }
        )
        df.sort_values(['日期', '店铺名称', '花费'], ascending=[False, False, False], ignore_index=True, inplace=True)
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '花费': 'decimal(12,2)',
            '展现量': 'int',
            '点击量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
        }
        if not self.update_service:
            return
        min_date = df['日期'].min().strftime('%Y-%m-%d')
        max_date = df['日期'].max().strftime('%Y-%m-%d')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '店铺名称', '营销场景', '花费', '展现量', '点击量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '店铺名称', '营销场景', '花费', '展现量', '点击量'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    @try_except
    def aikucun_bd_spu(self, db_name='聚合数据', table_name='爱库存_商品spu榜单'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            'spi_id': 1,
            '商品名称': 1,
            '品牌名称': 1,
            '商品款号': 1,
            '一级类目名称': 1,
            '二级类目名称': 1,
            '三级类目名称': 1,
            '转发次数': 1,
            '转发爱豆人数': 1,
            '访客量': 1,
            '浏览量': 1,
            '下单gmv': 1,
            '成交gmv': 1,
            '供货额': 1,
            '供货价': 1,
            '销售爱豆人数_成交': 1,
            '支付人数_交易': 1,
            '支付人数_成交': 1,
            '销售量_成交': 1,
            '销售量_交易': 1,
            '订单数_成交': 1,
            '订单数_交易': 1,
            '成交率_交易': 1,
            '成交率_成交': 1,
            '可售库存数': 1,
            '售罄率': 1,
            '在架sku数': 1,
            '可售sku数': 1,
            'sku数_交易': 1,
            'sku数_成交': 1,
            '营销后供货额': 1,
            '营销后供货价': 1,
            '店铺名称': 1,
        }
        projection = {}
        df = self.download.data_to_df(
            db_name='爱库存2',
            table_name='商品spu榜单',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df.drop_duplicates(
            subset=[
                '日期',
                '店铺名称',
                'spu_id',
                '访客量',
                '浏览量',
                '下单gmv',
                '成交gmv',
            ], keep='last', inplace=True, ignore_index=True)
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            'spu_id': 'varchar(100)',
            '图片': 'varchar(255)',
            '序号': 'smallint',
            '商品名称': 'varchar(255)',
            '商品款号': 'varchar(255)',
            '一级类目名称': 'varchar(255)',
            '二级类目名称': 'varchar(255)',
            '三级类目名称': 'varchar(255)',
            '数据更新时间': 'timestamp',
            '更新时间': 'timestamp',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        # new_dict = {
        #     '日期': '',
        #     '店铺名称': '',
        #     '序号': '',
        #     '商品名称': '',
        #     'spu_id': '',
        #     '商品款号': '',
        #     '一级类目名称': '',
        #     '二级类目名称': '',
        #     '三级类目名称': '',
        #     '访客量': '',
        #     '浏览量': '',
        #     '下单gmv': '',
        #     '成交gmv': '',
        #     '支付人数_成交': '',
        # }
        # for dict_data in df.to_dict(orient='records'):
        #     new_dict.update(dict_data)
        #     m_engine.dict_to_mysql(
        #         db_name=db_name,
        #         table_name=table_name,
        #         dict_data=new_dict,
        #         icm_update=['日期', '店铺名称', 'spu_id', '商品款号'],
        #         unique_main_key=None,
        #         set_typ=set_typ,
        #     )
        #     company_engine.dict_to_mysql(
        #         db_name=db_name,
        #         table_name=table_name,
        #         dict_data=new_dict,
        #         icm_update=['日期', '店铺名称', 'spu_id', '商品款号'],
        #         unique_main_key=None,
        #         set_typ=set_typ,
        #     )
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    def deeplink(self, db_name='聚合数据', table_name='达摩盘_deeplink人群洞察'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {}
        df = self.download.data_to_df(
            db_name='达摩盘3',
            table_name='店铺deeplink人群洞察',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df.drop_duplicates(subset=['日期', '人群类型', '店铺名称', '人群规模', '广告投入金额'], keep='last', inplace=True, ignore_index=True)
        if not self.update_service:
            return
        set_typ = {
            '日期': 'date',
            '人群类型': 'varchar(100)',
            '店铺名称': 'varchar(100)',
            '人群规模': 'int',
            '人均成交价值': 'decimal(10, 4)',
            'datatype': 'varchar(100)',
            '人群总计': 'int',
            '广告触达占比': 'decimal(12, 4)',
            '广告投入金额': 'decimal(12, 2)',
            'touchcharge': 'decimal(12, 2)',
            '人群占比': 'decimal(12, 4)',
            '长周期roi': 'decimal(12, 4)',
            '支付买家数': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(13, 2)',
            '触达人数': 'int',
            '长周期成交价值': 'decimal(13, 2)',
            '达摩盘id': 'int',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '人群类型', '店铺名称', '人群规模', '广告投入金额'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            # icm_update=['日期', '人群类型', '店铺名称', '人群规模', '广告投入金额'],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ
        )
        return True

    # @try_except
    def dmp_crowd(self, db_name='聚合数据', table_name='达摩盘_人群报表'):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '人群id': 1,
            '人群规模': 1,
            '用户年龄': 1,
            '消费能力等级': 1,
            '用户性别': 1,
        }
        # projection = {}
        df_crowd = self.download.data_to_df(
            db_name='达摩盘3',
            table_name='我的人群属性',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        df_crowd.sort_values('日期', ascending=True, ignore_index=True, inplace=True)
        df_crowd.drop_duplicates(subset=['人群id',], keep='last', inplace=True, ignore_index=True)
        df_crowd.pop('日期')
        df_crowd = df_crowd.astype({'人群id': 'int64'}, errors='ignore')

        projection = {}
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df_dmp = self.download.data_to_df(
                        db_name='达摩盘3',
                        table_name=f'dmp人群报表_{year}',
                        start_date=start_date,
                        end_date=end_date,
                        projection=projection,
                    )
            __res.append(df_dmp)
        df_dmp = pd.concat(__res, ignore_index=True)
        df_dmp = df_dmp.astype({'人群id': 'int64'}, errors='ignore')
        df_dmp.sort_values('日期', ascending=True, ignore_index=True, inplace=True)
        df_dmp.drop_duplicates(subset=['日期', '人群id', '消耗_元'], keep='last', inplace=True, ignore_index=True)
        df = pd.merge(df_dmp, df_crowd, left_on=['人群id'], right_on=['人群id'], how='left')
        # 清除一些不必要的字符
        df['用户年龄'] = df['用户年龄'].apply(lambda x: '~'.join(re.findall(r'^(\d+).*-(\d+)岁$', str(x))[0]) if '岁' in str(x) else x)
        df['消费能力等级'] = df['消费能力等级'].apply(lambda x: f'L{''.join(re.findall(r'(\d)', str(x)))}' if '购买力' in str(x) else x)
        # df.to_csv('/Users/xigua/Downloads/test3.csv', index=False, header=True, encoding='utf-8_sig')
        # breakpoint()
        df.rename(columns={'消耗_元': '消耗'}, inplace=True)
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '人群id': 'bigint',
            '人群名称': 'varchar(255)',
            '营销渠道': 'varchar(100)',
            '计划基础信息': 'varchar(255)',
            '推广单元信息': 'varchar(255)',
            '消耗_元': 'decimal(10,2)',
            '展现人数': 'int',
            '展现量': 'int',
            '点击人数': 'int',
            '点击量': 'int',
            '店铺收藏人数': 'smallint',
            '店铺收藏量': 'smallint',
            '加购人数': 'smallint',
            '加购量': 'smallint',
            '宝贝收藏人数': 'smallint',
            '宝贝收藏量': 'smallint',
            '收藏加购量': 'smallint',
            '收藏加购人数': 'smallint',
            '拍下人数': 'smallint',
            '拍下订单量': 'smallint',
            '拍下订单金额_元': 'decimal(10,2)',
            '成交人数': 'smallint',
            '成交订单量': 'smallint',
            '成交订单金额_元': 'decimal(10,2)',
            '店铺首购人数': 'smallint',
            '店铺复购人数': 'smallint',
            '点击率': 'decimal(10,4)',
            'uv点击率': 'decimal(10, 4)',
            '收藏加购率': 'decimal(10, 4)',
            'uv收藏加购率': 'decimal(10, 4)',
            '点击转化率': 'decimal(10, 4)',
            'uv点击转化率': 'decimal(10, 4)',
            '投资回报率': 'decimal(10, 4)',
            '千次展现成本_元': 'decimal(10, 2)',
            '点击成本_元': 'decimal(10, 2)',
            'uv点击成本_元': 'decimal(10, 2)',
            '收藏加购成本_元': 'decimal(10, 2)',
            'uv收藏加购成本_元': 'decimal(10, 2)',
            '更新时间': 'timestamp',
            '人群规模': 'int',
            '用户年龄': 'varchar(100)',
            '消费能力等级': 'varchar(100)',
            '用户性别': 'varchar(100)',
        }
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    @try_except
    def ret_keyword(self, keyword, as_file=False):
        """ 推广关键词报表，关键词分类， """
        datas = [
            {
                '类别': '品牌词',
                '值': [
                    '万里马',
                    'wanlima',
                    'fion',
                    '菲安妮',
                    '迪桑娜',
                    'dissona',
                    'hr',
                    'vh',
                    'songmont',
                    'vanessahogan',
                    'dilaks',
                    'khdesign',
                    'peco',
                    'giimmii',
                    'cassile',
                    'grotto',
                    'why',
                    'roulis',
                    'lesschic',
                    'amazing song',
                    'mytaste',
                    'bagtree',
                    '红谷',
                    'hongu',
                ]
            },
            {
                '类别': '智选',
                '值': [
                    '智选',
                ]
            },
            {
                '类别': '智能',
                '值': [
                    '智能',
                ]
            },
            {
                '类别': '年份',
                '值': [
                    '20',
                ]
            },
            {
                '类别': '材质',
                '值': [
                    '皮',
                    '牛仔',
                    '丹宁',
                    '帆布',
                ]
            },
            {
                '类别': '季节',
                '值': [
                    '春',
                    '夏',
                    '秋',
                    '冬',
                ]
            },
            {
                '类别': '一键起量',
                '值': [
                    '一键起量',
                ]
            },
            {
                '类别': '款式',
                '值': [
                    '水桶',
                    '托特',
                    '腋下',
                    '小方',
                    '通用款',
                    '手拿',
                    '马鞍',
                    '链条',
                    '菜篮',
                    'hobo',
                    '波士顿',
                    '凯莉',
                    '饺子',
                    '盒子',
                    '牛角',
                    '公文',
                    '月牙',
                    '单肩',
                    '枕头',
                    '斜挎',
                    '手提',
                    '手拎',
                    '拎手',
                    '斜肩',
                    '棒球',
                    '饺包',
                    '保龄球',
                    '戴妃',
                    '半月',
                    '弯月',
                    '法棍',
                    '流浪',
                    '拎包',
                    '中式',
                    '手挽',
                    '皮带',
                    '眼镜',
                    '斜跨',
                    '律师',
                    '斜背',
                ]
            },
            {
                '类别': '品类词',
                '值': [
                    '老花',
                    '包包',
                    '通勤',
                    '轻奢',
                    '包',
                    '新款',
                    '小众',
                    '爆款',
                    '工作',
                    '精致',
                    '奢侈',
                    '袋',
                    '腰带',
                    '裤带',
                    '女士',
                    '复古',
                    '高级',
                    '容量',
                    '时尚',
                    '商务',
                ],
            },
        ]
        if as_file:
            with open(os.path.join(self.output, f'分类配置.json'), 'w') as f:
                json.dump(datas, f, ensure_ascii=False, sort_keys=False, indent=4)
            breakpoint()
        result = ''
        res = []
        is_continue = False
        for data in datas:
            for item in data['值']:
                if item == '20':
                    pattern = r'\d\d'
                    res = re.findall(f'{item}{pattern}', str(keyword), re.IGNORECASE)
                else:
                    res = re.findall(item, str(keyword), re.IGNORECASE)
                if res:
                    result = data['类别']
                    is_continue = True
                    break
            if is_continue:
                break
        return result

    @try_except
    def set_crowd(self, keyword, as_file=False):
        """ 推广人群报表，人群分类， """
        result_a = re.findall('_a$|_a_|_ai|^a_', str(keyword), re.IGNORECASE)
        result_i = re.findall('_i$|_i_|^i_', str(keyword), re.IGNORECASE)
        result_p = re.findall('_p$|_p_|_pl|^p_||^pl_', str(keyword), re.IGNORECASE)
        result_l = re.findall('_l$|_l_|^l_', str(keyword), re.IGNORECASE)

        datas = [
            {
                '类别': 'A',
                '值': result_a,
            },
            {
                '类别': 'I',
                '值': result_i,
            },
            {
                '类别': 'P',
                '值': result_p,
            },
            {
                '类别': 'L',
                '值': result_l,
            }
        ]

        is_res = False
        for data in datas:
            if data['值']:
                data['值'] = [item for item in data['值'] if item != '']
                if data['值']:
                    return data['类别']
        if not is_res:
            return ''

    @try_except
    def set_crowd2(self, keyword, as_file=False):
        """ 推广人群报表，人群分类， """
        datas = [
            {
                '类别': 'A',
                '值': [
                    '相似宝贝',
                    '相似店铺',
                    '类目',
                    '88VIP',
                    '拉新',
                    '潮流',
                    '会场',
                    '意向',
                    '>>',  # 系统推荐的搜索相关人群
                    '关键词：',  # 系统推荐的搜索相关人群
                    '关键词_',  # 自建的搜索相关人群
                    '扩展',
                    '敏感人群',
                    '尝鲜',
                    '小二推荐',
                    '竞争',
                    '资深',
                    '女王节',
                    '本行业',
                    '618',
                    '包包树',
                    '迪桑娜',
                    '菲安妮',
                    '卡思乐',
                    '场景词',
                    '竞对',
                    '精选',
                    '发现',
                    '行业mvp'
                    '特征继承',
                    '机会',
                    '推荐',
                    '智能定向',
                    'AI',
                ]
            },
            {
                '类别': 'I',
                '值': [
                    '行动',
                    '收加',
                    '收藏',
                    '加购',
                    '促首购',
                    '店铺优惠券',
                    '高转化',
                    '认知',
                    '喜欢我',  # 系统推荐宝贝/店铺访问相关人群
                    '未购买',
                    '种草',
                    '兴趣',
                    '本店',
                    '领券',
                ]
            },
            {
                '类别': 'P',
                '值': [
                    '万里马',
                    '购买',
                    '已购',
                    '促复购'
                    '店铺会员',
                    '店铺粉丝',
                    '转化',
                ]
            },
            {
                '类别': 'L',
                '值': [
                    'L人群',
                ]
            },
        ]
        if as_file:
            with open(os.path.join(self.output, f'分类配置_推广人群分类_函数内置规则.json'), 'w') as f:
                json.dump(datas, f, ensure_ascii=False, sort_keys=False, indent=4)
            breakpoint()
        result = ''
        res = []
        is_continue = False
        for data in datas:
            for item in data['值']:
                res = re.findall(item, str(keyword), re.IGNORECASE)
                if res:
                    result = data['类别']
                    is_continue = True
                    break
            if is_continue:
                break
        return result

    # @try_except
    def performance(self, db_name, table_name, bb_tg=True):

        tg= [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '天猫_主体报表'][0]
        syj = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '生意经_宝贝指标'][0]
        idbm = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '商品id编码表'][0]
        pic = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '商品id图片对照表'][0]
        cost = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '商品成本'][0]

        # 由于推广表之前根据场景、营销渠道等聚合的，这里不含这些字段所以要进一步聚合
        tg = tg.groupby(
            ['日期', '店铺名称', '商品id'],
            as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '成交金额': ('成交金额', np.sum),
                '直接成交金额': ('直接成交金额', np.sum),
            }
        )
        # 4.  生意经，推广表聚合
        if bb_tg is True:
            # 生意经合并推广表，完整的数据表，包含全店所有推广、销售数据
            df = pd.merge(syj, tg, how='left', left_on=['日期', '店铺名称', '宝贝id'], right_on=['日期', '店铺名称', '商品id'])
            df.drop(labels='商品id', axis=1, inplace=True)  # 因为生意经中的宝贝 id 列才是完整的
            df.rename(columns={'宝贝id': '商品id'}, inplace=True)
        else:
            # 推广表合并生意经 , 以推广数据为基准，销售数据不齐全
            df = pd.merge(tg, syj, how='left', left_on=['日期', '店铺名称', '商品id'], right_on=['日期', '店铺名称', '宝贝id'])
            df.drop(labels='宝贝id', axis=1, inplace=True)

        df['商品id'] = df['商品id'].astype('int64')
        df = df.groupby(
            ['日期', '店铺名称', '商品id'],
            as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '成交金额': ('成交金额', np.sum),
                '直接成交金额': ('直接成交金额', np.sum),
                '销售额': ('销售额', np.sum),
                '销售量': ('销售量', np.sum),
                '退款额_发货后': ('退款额_发货后', np.sum),
                '退货量_发货后': ('退货量_发货后', np.sum),
            }
        )
        # print(df.info())

        idbm['宝贝id'] = idbm['宝贝id'].astype('int64')
        # 1.  id 编码表合并图片表
        df_cb = pd.merge(idbm, pic, how='left', left_on='宝贝id', right_on='商品id')
        df_cb = df_cb[['宝贝id', '商家编码', '商品图片']]
        # 2.  df 合并商品成本表
        df_cb = pd.merge(df_cb, cost, how='left', left_on='商家编码', right_on='款号')
        df_cb = df_cb[['宝贝id', '商家编码', '商品图片', '成本价']]
        # print(df_cb.info())
        # 3.  合并 df
        df = pd.merge(df, df_cb, how='left', left_on='商品id', right_on='宝贝id')
        df.drop(labels='宝贝id', axis=1, inplace=True)

        # df.drop_duplicates(subset=['日期', '店铺名称', '商品id', '花费', '销售额'], keep='last', inplace=True, ignore_index=True)
        df.fillna(0, inplace=True)
        df['成本价'] = df['成本价'].astype('float64')
        df['销售额'] = df['销售额'].astype('float64')
        df['销售量'] = df['销售量'].astype('int64')
        df['商品成本'] = df.apply(lambda x: (x['成本价'] + x['销售额']/x['销售量'] * 0.11 + 6) * x['销售量'] if x['销售量'] > 0 else 0, axis=1)
        df['商品毛利'] = df.apply(lambda x: x['销售额'] - x['商品成本'], axis=1)
        df['毛利率'] = df.apply(lambda x: round((x['销售额'] - x['商品成本']) / x['销售额'], 4) if x['销售额'] > 0 else 0, axis=1)
        df['盈亏'] = df.apply(lambda x: x['商品毛利'] - x['花费'], axis=1)
        [df[col].apply(lambda x: '0' if str(x) == '' else x) for col in df.columns.tolist()]
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '商品id': 'bigint',
            '销售额': 'decimal(12,2)',
            '销售量': 'int',
            '退款额_发货后': 'decimal(12,2)',
            '退货量_发货后': 'int',
            '花费': 'decimal(12,2)',
            '成交金额': 'decimal(12,2)',
            '直接成交金额': 'decimal(12,2)',
            '商家编码': 'varchar(100)',
            '商品图片': 'varchar(255)',
            '成本价': 'decimal(10,2)',
            '商品成本': 'decimal(10,2)',
            '商品毛利': 'decimal(10,2)',
            '毛利率': 'decimal(12,4)',
            '盈亏': 'decimal(12,4)',
        }
        if not self.update_service:
            return
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    # @try_except
    def performance_concat(self, db_name, table_name, bb_tg=True):
        tg = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '天猫汇总表调用'][0]
        zb = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '天猫_超级直播'][0]
        pxb = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '天猫_品销宝账户报表'][0]
        zb = zb.groupby(['日期', '店铺名称', '推广渠道', '营销场景'], as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '展现量': ('展现量', np.sum),
                '观看次数': ('观看次数', np.sum),
                '加购量': ('加购量', np.sum),
                '成交笔数': ('成交笔数', np.sum),
                '成交金额': ('成交金额', np.sum),
                '直接成交笔数': ('直接成交笔数', np.sum),
                '直接成交金额': ('直接成交金额', np.sum),
            }
        )
        pxb = pxb.groupby(['日期', '店铺名称', '推广渠道', '营销场景'], as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '展现量': ('展现量', np.sum),
                '点击量': ('点击量', np.sum),
                '加购量': ('加购量', np.sum),
                '成交笔数': ('成交笔数', np.sum),
                '成交金额': ('成交金额', np.sum)
            }
        )

        zb.rename(columns={
            '观看次数': '点击量',
        }, inplace=True)
        zb.fillna(0, inplace=True)  # astype 之前要填充空值
        tg.fillna(0, inplace=True)
        zb = zb.astype({
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'float64',
            '直接成交笔数': 'int64',
            '直接成交金额': 'float64',
        }, errors='raise')
        tg = tg.astype({
            '商品id': str,
            '花费': 'float64',
            '展现量': 'int64',
            '点击量': 'int64',
            '加购量': 'int64',
            '成交笔数': 'int64',
            '成交金额': 'float64',
            '直接成交笔数': 'int64',
            '直接成交金额': 'float64',
            '自然流量曝光量': 'int64',
        }, errors='raise')
        # tg = tg.groupby(['日期', '推广渠道', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
        #     **{'加购量': ('加购量', np.max),
        #        '成交笔数': ('成交笔数', np.max),
        #        '成交金额': ('成交金额', np.max),
        #        '自然流量曝光量': ('自然流量曝光量', np.max),
        #        '直接成交笔数': ('直接成交笔数', np.max),
        #        '直接成交金额': ('直接成交金额', np.max)
        #        }
        # )
        df = pd.concat([tg, zb, pxb], axis=0, ignore_index=True)
        df.fillna(0, inplace=True)  # concat 之后要填充空值
        df = df.astype(
            {
                '商品id': str,
                '自然流量曝光量': 'int64',
        }
        )
        [df[col].apply(lambda x: '0' if str(x) == '' else x) for col in df.columns.tolist()]
        set_typ = {
            '日期': 'date',
            '店铺名称': 'varchar(100)',
            '推广渠道': 'varchar(100)',
            '营销场景': 'varchar(100)',
            '商品id': 'bigint',
            '花费': 'decimal(12,2)',
            '展现量': 'int',
            '点击量': 'int',
            '加购量': 'int',
            '成交笔数': 'int',
            '成交金额': 'decimal(12,2)',
            '直接成交笔数': 'int',
            '直接成交金额': 'decimal(12,2)',
            '自然流量曝光量': 'int',
        }
        if not self.update_service:
            return
        min_date = df['日期'].min()
        max_date = df['日期'].max()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True

    # @try_except
    def performance_jd(self, db_name, table_name, jd_tg=True, ):
        jdtg = [item['数据主体'] for item in self.pf_datas_jd if item['集合名称'] == '京东_京准通'][0]
        sku_sales = [item['数据主体'] for item in self.pf_datas_jd if item['集合名称'] == '京东_sku_商品明细'][0]
        cost = [item['数据主体'] for item in self.pf_datas if item['集合名称'] == '商品成本'][0]

        jdtg = jdtg.groupby(['日期', '跟单sku_id'],
                        as_index=False).agg(
            **{
                '花费': ('花费', np.sum)
            }
        )
        df = pd.merge(sku_sales, cost, how='left', left_on='货号', right_on='款号')
        df = df[['日期', '商品id', '货号', '成交单量', '成交金额', '成本价']]
        df['商品id'] = df['商品id'].astype(str)
        jdtg['跟单sku_id'] = jdtg['跟单sku_id'].astype(str)
        jdtg = jdtg.astype({'日期': 'datetime64[ns]'}, errors='raise')
        df = df.astype({'日期': 'datetime64[ns]'}, errors='raise')
        if jd_tg is True:
            # 完整的数据表，包含全店所有推广、销售数据
            df = pd.merge(df, jdtg, how='left', left_on=['日期', '商品id'], right_on=['日期', '跟单sku_id'])  # df 合并推广表
        else:
            df = pd.merge(jdtg, df, how='left', left_on=['日期', '跟单sku_id'], right_on=['日期', '商品id'])  # 推广表合并 df
        df = df[['日期', '跟单sku_id', '花费', '货号', '成交单量', '成交金额', '成本价']]
        df.fillna(0, inplace=True)
        df['成本价'] = df['成本价'].astype('float64')
        df['成交金额'] = df['成交金额'].astype('float64')
        df['花费'] = df['花费'].astype('float64')
        df['成交单量'] = df['成交单量'].astype('int64')
        df['商品成本'] = df.apply(
            lambda x: (x['成本价'] + x['成交金额'] / x['成交单量'] * 0.11 + 6) * x['成交单量'] if x['成交单量'] > 0 else 0,
            axis=1)
        df['商品毛利'] = df.apply(lambda x: x['成交金额'] - x['商品成本'], axis=1)
        df['毛利率'] = df.apply(
            lambda x: round((x['成交金额'] - x['商品成本']) / x['成交金额'], 4) if x['成交金额'] > 0 else 0, axis=1)
        df['盈亏'] = df.apply(lambda x: x['商品毛利'] - x['花费'], axis=1)
        [df[col].apply(lambda x: '0' if str(x) == '' else x) for col in df.columns.tolist()]
        set_typ = {
            '日期': 'date',
            '跟单sku_id': 'bigint',
            '花费': 'decimal(12,2)',
            '货号': 'varchar(100)',
            '成交单量': 'int',
            '成交金额': 'decimal(12,2)',
            '成本价': 'decimal(10,2)',
            '商品成本': 'decimal(10,2)',
            '商品毛利': 'decimal(10,2)',
            '毛利率': 'decimal(12,4)',
            '盈亏': 'decimal(12,4)',
        }
        if not self.update_service:
            return
        min_date = df['日期'].min().strftime("%Y-%m-%d")
        max_date = df['日期'].max().strftime("%Y-%m-%d")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{now} 正在更新: mysql ({host}:{port}) {db_name}/{table_name} -> {min_date}~{max_date}')
        m_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        company_engine.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            icm_update=[],  # 增量更新, 在聚合数据中使用，其他不要用
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename=None,  # 用来追踪处理进度
            reset_id=True,  # 是否重置自增列
            set_typ=set_typ,
        )
        return True


def get_day_of_month(num):
    """
    num: 获取n月以前的第一天和最后一天, num=0时, 返回当月第一天和最后一天
    """
    _today = datetime.date.today()
    months_ago = _today - relativedelta(months=num)  # n 月以前的今天
    _, _lastDay = calendar.monthrange(months_ago.year, months_ago.month)  # 返回月的第一天的星期和当月总天数
    _firstDay = datetime.date(months_ago.year, months_ago.month, day=1).strftime('%Y-%m-%d')
    _lastDay = datetime.date(months_ago.year, months_ago.month, day=_lastDay).strftime('%Y-%m-%d')

    return _firstDay, _lastDay


def date_table():
    """
    生成 pbix 使用的日期表
    """
    start_date = '2022-01-07'  # 日期表的起始日期
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

    # 重构 df，添加 1 列，从周五～下周四作为 1 周 汇总
    df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')  # 转换日期列
    grouped = df.groupby(pd.Grouper(key='日期', freq='7D'))
    __res = []
    num = 1
    for name, group in grouped:
        if num > 52:
            num = 1
        # print(f'Group: {name}')
        group['第n周_new'] = f'第{num}周'
        num += 1
        __res.append(group.copy())
        # print(group)
        # break
    df = pd.concat(__res, ignore_index=True)
    # df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
    df['weekname'] = df['日期'].dt.day_name()
    dict_dt = {
        'Monday': '星期一',
        'Tuesday': '星期二',
        'Wednesday': '星期三',
        'Thursday': '星期四',
        'Friday': '星期五',
        'Saturday': '星期六',
        'Sunday': '星期日',
    }
    df['星期'] = df['weekname'].apply(lambda x: dict_dt[x])
    df['索引'] = p
    df['月索引'] = mon
    df.sort_values('日期', ascending=False, ignore_index=True, inplace=True)
    df = df.reset_index(drop=True)
    df = df.reset_index(drop=False)
    df.rename(columns={'index': 'id'}, inplace=True)
    df['id'] = df['id'].apply(lambda x: x + 1)

    m = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
    )
    set_typ = {
        '日期': 'date',
        '年': 'varchar(50)',
        '月': 'varchar(50)',
        '日': 'int',
        '年月': 'varchar(50)',
        '月日': 'varchar(50)',
        '第n周': 'varchar(50)',
        '第n周_new': 'varchar(50)',
        '星期': 'varchar(50)',
        'weekname': 'varchar(50)',
        '索引': 'int',
        '月索引': 'int',
    }
    m.df_to_mysql(
        df=df,
        db_name='聚合数据',
        table_name='日期表',
        move_insert=True,  # 先删除，再插入
        df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
        drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
        count=None,
        filename=None,  # 用来追踪处理进度
        set_typ=set_typ,
    )


def query1(months=1, less_dict=[]):
    if months == 0:
        print(f'months 不建议为 0 ')
        return
    sdq = MysqlDatasQuery()  # 实例化数据处理类
    sdq.months = months  # 设置数据周期， 1 表示近 2 个月
    sdq.update_service = True  # 调试时加，true: 将数据写入 mysql 服务器

    sdq.tg_wxt(db_name='聚合数据', table_name='天猫_主体报表')
    sdq.syj(db_name='聚合数据', table_name='生意经_宝贝指标')
    sdq.idbm(db_name='聚合数据', table_name='商品id编码表')
    sdq.sp_picture(db_name='聚合数据', table_name='商品id图片对照表')
    sdq.sp_cost(db_name='聚合数据', table_name='商品成本')
    sdq.jdjzt(db_name='聚合数据', table_name='京东_京准通')
    sdq.jdqzyx(db_name='聚合数据', table_name='京东_京准通_全站营销')
    sdq.sku_sales(db_name='聚合数据', table_name='京东_sku_商品明细')
    sdq.spu_sales(db_name='聚合数据', table_name='京东_spu_商品明细')
    sdq.tg_cjzb(db_name='聚合数据', table_name='天猫_超级直播')
    sdq.pxb_zh(db_name='聚合数据', table_name='天猫_品销宝账户报表')
    sdq.zb_ccfx(db_name='聚合数据', table_name='生意参谋_直播场次分析')
    sdq.tg_by_day(db_name='聚合数据', table_name='多店推广场景_按日聚合')
    sdq.performance(bb_tg=True, db_name='聚合数据', table_name='_全店商品销售')  # _全店商品销售
    sdq.performance(bb_tg=False, db_name='聚合数据', table_name='_推广商品销售')  # _推广商品销售
    sdq.performance_jd(jd_tg=False, db_name='聚合数据', table_name='_京东_推广商品销售')  # _推广商品销售
    sdq.performance_concat(bb_tg=False, db_name='聚合数据', table_name='天猫_推广汇总')  # _推广商品销售


def query2(months=1, less_dict=[]):
    if months == 0:
        print(f'months 不建议为 0 ')
        return
    sdq = MysqlDatasQuery()  # 实例化数据处理类
    sdq.months = months  # 设置数据周期， 1 表示近 2 个月
    sdq.update_service = True  # 调试时加，true: 将数据写入 mysql 服务器
    sdq.dplyd(db_name='聚合数据', table_name='店铺流量来源构成')
    sdq.tg_rqbb(db_name='聚合数据', table_name='天猫_人群报表')
    sdq.tg_gjc(db_name='聚合数据', table_name='天猫_关键词报表')
    sdq.jd_gjc(db_name='聚合数据', table_name='京东_关键词报表')
    sdq.se_search(db_name='聚合数据', table_name='天猫店铺来源_手淘搜索')
    sdq.aikucun_bd_spu(db_name='聚合数据', table_name='爱库存_商品spu榜单')
    sdq.dmp_crowd(db_name='聚合数据', table_name='达摩盘_人群报表')
    sdq.deeplink(db_name='聚合数据', table_name='达摩盘_deeplink人群洞察')


def main(days=150, months=3):
    """
    days:    清理聚合数据的日期长度
    months:   生成聚合数据的长度
    """
    # 1. 更新日期表  更新货品年份基准表， 属性设置 3 - 货品年份基准
    date_table()
    p = products.Products()
    p.to_mysql()

    # 清理非聚合数据库
    db_list = [
        "京东数据3",
        "属性设置3",
        "推广数据2",
        "推广数据_淘宝店",
        "爱库存2",
        "生意参谋3",
        "生意经3",
        "达摩盘3",
        '人群画像2',
        '商品人群画像2',
        '市场数据3',
    ]
    # 使用 ThreadPoolExecutor 来并行运行
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for step in range(len(db_list)):
            future_to_function = {
                executor.submit(
                    optimize_data.op_data,
                    days=31,
                    is_mongo=False,
                    is_mysql=True,
                    db_name_lists=[db_list[step]],
                ),
            }
        # # 等待所有任务完成并获取执行结果
        # for future in concurrent.futures.as_completed(future_to_function):
        #     future.result()

    # 2. 数据聚合
    query_list = [query1, query2]
    # 使用 ThreadPoolExecutor 来并行运行
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for func_query in query_list:
            future_to_function = {
                executor.submit(
                    func_query,
                    months=months,
                    less_dict=[],
                ),
            }
    # query_(months=months)
    time.sleep(10)

    # 3. 清理聚合数据
    optimize_data.op_data(
        db_name_lists=['聚合数据'],
        days=days,  # 清理聚合数据的日期长度
        is_mongo=False,
        is_mysql=True,
    )


if __name__ == '__main__':
    main(
        days=150,  # 清理聚合数据的日期长度
        months=3  # 生成聚合数据的长度
    )

    # query_list = [query1, query2]
    # # 使用 ThreadPoolExecutor 来并行运行
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for func_query in query_list:
    #         future_to_function = {
    #             executor.submit(
    #                 func_query,
    #                 months=1,
    #                 less_dict=[],
    #             ),
    #         }

    # # 3. 清理聚合数据
    # optimize_data.op_data(
    #     db_name_lists=['聚合数据'],
    #     days=30,  # 清理聚合数据的日期长度
    #     is_mongo=False,
    #     is_mysql=True,
    # )
