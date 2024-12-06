# -*- coding: UTF-8 –*-
import os
import time
import pandas as pd
import warnings
import datetime
from dateutil.relativedelta import relativedelta
from mdbq.config import get_myconf
from mdbq.mysql import mysql
from mdbq.mysql import s_query

""" 这是一个临时文件， 用来修改原始文件中大量 csv 文件中的场景名字（万相台报表） """
warnings.filterwarnings('ignore')


def id_account_rpt(id_rpt):
    """
    id_rpt: 传入原二级场景id/原二级场景名字 ，返回其他键值
    只可以旧推新，不可以新推旧
    例如： 粉丝快 -> 人群推广， 精准人群推广 -> 人群推广
    但不可以：人群推广 对应着旧的多个值，会发生问题
    """
    if '="' in str(id_rpt):
        id_rpt = str(id_rpt).replace('="', '')
        id_rpt = str(id_rpt).replace('"', '')
    _id_account_rpt = [
        {
            '原二级场景id': '436',
            '原二级场景名字': '全站推广',
            '场景id': '436',
            '场景名字': '全站推广',
        },
        {
            '原二级场景id': '407',
            '原二级场景名字': '粉丝快',
            '场景id': '372',
            '场景名字': '人群推广',
        },
        {
            '原二级场景id': '114',
            '原二级场景名字': '货品加速',
            '场景id': '376',
            '场景名字': '货品运营',
        },
        {
            '原二级场景id': '372',
            '原二级场景名字': '精准人群推广',
            '场景id': '372',
            '场景名字': '人群推广',
        },
        {
            '原二级场景id': '371',
            '原二级场景名字': '关键词推广',
            '场景id': '371',
            '场景名字': '关键词推广',
        },
        {
            '原二级场景id': '361',
            '原二级场景名字': '全店智投',
            '场景id': '361',
            '场景名字': '全店智投',
        },
        {
            '原二级场景id': '183',
            '原二级场景名字': '超级短视频',
            '场景id': '183',
            '场景名字': '超级短视频',
        },
        {
            '原二级场景id': '154',
            '原二级场景名字': '活动加速',
            '场景id': '154',
            '场景名字': '活动加速',
        },
        {
            '原二级场景id': '133',
            '原二级场景名字': '会员快',
            '场景id': '372',
            '场景名字': '人群推广',
        },
        {
            '原二级场景id': '108',
            '原二级场景名字': '超级直播',
            '场景id': '108',
            '场景名字': '超级直播',
        },
        {
            '原二级场景id': '105',
            '原二级场景名字': '上新快',
            '场景id': '105',
            '场景名字': '上新快',
        },
        {
            '原二级场景id': '78',
            '原二级场景名字': '拉新快',
            '场景id': '372',
            '场景名字': '人群推广',
        },
    ]

    for data in _id_account_rpt:
        if id_rpt == data['原二级场景id'] or id_rpt == data['原二级场景名字']:
            return data


class ReCheckMysql:
    def __init__(self, target_service):
        username, password, host, port = get_myconf.select_config_values(target_service=target_service,
                                                                         database='mysql')
        self.download = s_query.QueryDatas(username=username, password=password, host=host, port=port)
        self.months = 1  # 读取近 num 个月的数据, 0 表示读取当月的数据

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    def recheck_cols(self, db_name, table_name, service_name='company'):
        start_date, end_date = self.months_data(num=self.months)
        df = self.download.data_to_df(
            db_name=db_name,
            table_name=table_name,
            start_date=start_date,
            end_date=end_date,
            projection={},
        )
        # df.to_csv('/Users/xigua/Downloads/test_before.csv', index=False, header=True, encoding='utf-8_sig')
        # 调用 self.id_account_rpt 函数，根据场景id 修改对应的场景名字，如果没有匹配则不修改
        df['场景名字'] = df.apply(lambda x: id_account_rpt(x['场景id']) if id_account_rpt(x['场景id']) else x['场景名字'], axis=1)
        # df.to_csv('/Users/xigua/Downloads/test.csv', index=False, header=True, encoding='utf-8_sig')

        username, password, host, port = get_myconf.select_config_values(
            target_service=service_name,
            database='mysql',
        )
        m = mysql.MysqlUpload(
            username=username,
            password=password,
            host=host,
            port=port,
        )
        m.df_to_mysql(
            df=df,
            db_name=db_name,
            table_name=table_name,
            move_insert=True,  # 先删除，再插入
            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
            count=None,
            filename='',  # 用来追踪处理进度
        )


def recheck_csv():
    path = '/Users/xigua/数据中心/原始文件2/推广报表34324234'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if '~' in name or 'baidu' in name or 'Ds_' in name or 'xunlei' in name:
                continue
            if name.endswith('.csv'):
                df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                if '场景ID' not in df.columns.tolist():
                    continue
                if '原二级场景名字' in df.columns.tolist() and '原二级场景ID' in df.columns.tolist():
                    df['原二级场景ID'].replace(to_replace='="', value='', regex=True, inplace=True)
                    df['原二级场景ID'].replace(to_replace='"', value='', regex=True, inplace=True)
                if '场景名字' in df.columns.tolist() and '场景ID' in df.columns.tolist():
                    df['场景ID'].replace(to_replace='="', value='', regex=True, inplace=True)
                    df['场景ID'].replace(to_replace='"', value='', regex=True, inplace=True)
                if '场景名字' in df.columns.tolist() and '场景ID' in df.columns.tolist() and '原二级场景名字' not in df.columns.tolist():
                    df.rename(columns={
                        '场景名字': '原二级场景名字',
                        '场景ID': '原二级场景ID',
                    }, inplace=True)
                    # 根据 id 修正 场景名字
                    df['原二级场景名字'] = df.apply(
                        lambda x: id_account_rpt(x['原二级场景ID'])['原二级场景名字'] if id_account_rpt(x['原二级场景ID']) else x['原二级场景名字'], axis=1)
                    # 根据原场景id获取新场景名字
                    df['场景名字'] = df.apply(
                        lambda x: id_account_rpt(x['原二级场景ID'])['场景名字'] if id_account_rpt(x['原二级场景ID']) else '', axis=1)
                    # 根据原场景id获取新场景id
                    df['场景ID'] = df.apply(
                        lambda x: id_account_rpt(x['原二级场景ID'])['场景id'] if id_account_rpt(x['原二级场景ID']) else '', axis=1)
                print(name)
                df.to_csv(os.path.join(root, name), index=False, header=True, encoding='utf-8_sig')


if __name__ == '__main__':
    # r = ReCheckMysql(target_service='company')
    # r.months = 100
    # r.recheck_cols(
    #     db_name='推广数据2',
    #     table_name='营销场景报表',
    #     service_name='company',
    # )

    recheck_csv()
