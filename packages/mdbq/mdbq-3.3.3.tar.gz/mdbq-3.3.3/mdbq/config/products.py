# -*- coding: UTF-8 –*-
import json
import os
import platform
import getpass
import socket
import pandas as pd
from mdbq.mysql import mysql
from mdbq.config import myconfig
from numpy.ma.core import product

""" 
天猫货品年份基准对照
用于聚合数据，通过此数据表进一步可确定商品上架年月
"""
username, password, host, port, service_database = None, None, None, None, None,
if socket.gethostname() in ['xigua_lx', 'xigua1', 'MacBookPro']:
    conf = myconfig.main()
    data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = data['username'], data['password'], data['host'], data['port']
    service_database = {'xigua_lx': 'mysql'}
elif socket.gethostname() in ['company', 'Mac2.local']:
    conf = myconfig.main()
    data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = data['username'], data['password'], data['host'], data['port']
    service_database = {'company': 'mysql'}
if not username:
    print(f'找不到主机1：')


class Products:
    def __init__(self):
        self.datas = []

    def update_my_datas(self):
        my_datas = [
            {
                '平台': '天猫', '商品id': '848929365673', '上市年份': '2024年11月'
            },
            {
                '平台': '天猫', '商品id': '840499705810', '上市年份': '2024年10月'
            },
            {
                '平台': '天猫', '商品id': '830789689032', '上市年份': '2024年9月'
            },
            {
                '平台': '天猫', '商品id': '822020840000', '上市年份': '2024年8月'
            },
            {
                '平台': '天猫', '商品id': '811000000000', '上市年份': '2024年7月'
            },
            {
                '平台': '天猫', '商品id': '800000000000', '上市年份': '2024年6月'
            },
            {
                '平台': '天猫', '商品id': '791359643000', '上市年份': '2024年5月'
            },
            {
                '平台': '天猫', '商品id': '778971448000', '上市年份': '2024年4月'
            },
            {
                '平台': '天猫', '商品id': '770576016820', '上市年份': '2024年3月'
            },
            {
                '平台': '天猫', '商品id': '766115058400', '上市年份': '2024年2月'
            },
            {
                '平台': '天猫', '商品id': '759478591187', '上市年份': '2024年1月'
            },
            {
                '平台': '天猫', '商品id': '752770183000', '上市年份': '2023年12月'
            },
            {
                '平台': '天猫', '商品id': '745123890000', '上市年份': '2023年11月'
            },
            {
                '平台': '天猫', '商品id': '741000000000', '上市年份': '2023年10月'
            },
            {
                '平台': '天猫', '商品id': '736841920000', '上市年份': '2023年9月'
            },
            {
                '平台': '天猫', '商品id': '730800000000', '上市年份': '2023年8月'
            },
            {
                '平台': '天猫', '商品id': '726939636835', '上市年份': '2023年7月'
            },
            {
                '平台': '天猫', '商品id': '721366048631', '上市年份': '2023年6月'
            },
            {
                '平台': '天猫', '商品id': '716130443004', '上市年份': '2023年5月'
            },
            {
                '平台': '天猫', '商品id': '709824308589', '上市年份': '2023年4月'
            },
            {
                '平台': '天猫', '商品id': '705440027804', '上市年份': '2023年3月'
            },
            {
                '平台': '天猫', '商品id': '701096067973', '上市年份': '2023年2月'
            },
            {
                '平台': '天猫', '商品id': '696017000000', '上市年份': '2023年1月'
            },
            {
                '平台': '天猫', '商品id': '666510000000', '上市年份': '2022年货品'
            },
            {
                '平台': '天猫', '商品id': '636010000000', '上市年份': '2021年货品'
            },
            {
                '平台': '天猫', '商品id': '610485872286', '上市年份': '2020年货品'
            },
            {
                '平台': '天猫', '商品id': '585066000000', '上市年份': '2019年货品'
            },
            {
                '平台': '天猫', '商品id': '563237000000', '上市年份': '2018年货品'
            },
            {
                '平台': '天猫', '商品id': '100', '上市年份': '历史悠久'
            },
        ]
        self.datas += my_datas


    def to_mysql(self):
        self.update_my_datas()
        df = pd.DataFrame(self.datas)
        m_engine = mysql.MysqlUpload(
            username=username,
            password=password,
            host=host,
            port=port,
        )
        for dict_data in df.to_dict(orient='records'):
            m_engine.dict_to_mysql(
                db_name='属性设置3',
                table_name='货品年份基准',
                dict_data=dict_data,
                # icm_update=['日期', '店铺名称', '宝贝id'],  # 唯一组合键
                unique_main_key=['商品id'],
                set_typ={
                    '商品id': 'bigint',
                    '平台': 'varchar(100)',
                    '上市年份': 'varchar(100)',
                },
            )

    def market_date(self, product_id: int):
        try:
            product_id = int(product_id)
        except:
            return
        self.update_my_datas()
        market_date = [item['上市年份'] for item in self.datas if product_id > int(item['商品id'])]
        if market_date:
            return market_date[0]  # 返回上市年份


def main():
    pass


if __name__ == '__main__':
    product_id = '696017020186'
    p = Products()
    year = p.market_date(product_id=product_id)
    print(f'{product_id}:  {year}')
