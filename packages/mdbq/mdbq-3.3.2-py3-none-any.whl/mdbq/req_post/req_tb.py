# -*- coding: UTF-8 –*-
import os
import time
import datetime
import pandas as pd
import warnings
import requests
from mdbq.other import ua_sj
from mdbq.config import get_myconf
from mdbq.mysql import mysql
import json
import socket
import platform
import random

warnings.filterwarnings('ignore')


class RequestData:
    def __init__(self):
        self.date = datetime.date.today().strftime('%Y%m%d')
        self.url = None
        self.headers = None
        self.cookies = None
        self.datas = []
        self.path = None
        self.filename = None
        self.is_json_file = False
        self.df = pd.DataFrame()

    def qxg_hx_data(self):
        """ 抢先购 预热期核心指标 """
        date = datetime.date.today().strftime('%Y-%m-%d')
        url = (f'https://sycm.taobao.com/datawar/v4/activity/detail/kpi/coreIndex/live.json?'
               f'activityId=92072444'
               f'&status=1'
               f'&dateType=today'
               f'&dateRange={date}%7C{date}'
               f'&_=1729216673692'
               f'&token=0939158d0'
               )
        headers = {'User-Agent': ua_sj.get_ua()}
        cookies = {
            'session': 't=c198527347800dafa75165f084784668; thw=cn; cc_gray=1; 2210244713719_euacm_ac_c_uid_=713197610; 2210244713719_euacm_ac_rs_uid_=713197610; _portal_version_=new; xlly_s=1; _euacm_ac_l_uid_=2210244713719; _tb_token_=GzT2Grwtrep02E5awyhr; _samesite_flag_=true; 3PcFlag=1729299229095; cookie2=15f3dfc1aa68e07b05043bf7f8fb5565; sgcookie=E100r7l2QLYERk5SKLinmW40F%2BbdvBhfP7ZwSPi%2BjxeXI6Y%2B%2BraqfGzS%2BKX3ME%2FRfXZKeLBwECj63B245VuW%2FZBpg5X3Ydq2WK05z0QvsUxuyJQNNaVJTDy8WSQXRpKhFDHF; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie14=UoYcCoJCtZ6mUg%3D%3D&cookie21=UtASsssmfufd; csg=7d17ab64; _cc_=V32FPkk%2Fhw%3D%3D; cancelledSubSites=empty; skt=214c26d846e4ece2; cna=8+iAHxeojXcCAXjsc5Mt+BAV; v=0; XSRF-TOKEN=a4816e90-82aa-4743-b438-67e826b8ebbe; datawar_version=new; mtop_partitioned_detect=1; _m_h5_tk=c1140ed9be58a574cf0740ca0fad2f9c_1729340693031; _m_h5_tk_enc=2a93813f4e75d7928cc79cc6bc9db5d7; _euacm_ac_rs_sid_=67090549; JSESSIONID=3DBCB84C04569B30741EF0263731963E; tfstk=gbRSfuVwPHdqd3wyBX3VCcGDfR5IVHGN9y_pSeFzJ_CRvXKpc9FEE_WCOnI2ag8Pww1BSHZrr95ROMTMVJ8PY8-XJet_aL-eYzvDbFFyaYfUO_fh9coZ_fzkr6fKIj10GzfA-NE-TgF-MUjmccen_f8kyz7-7Ehwagr3NGjd9TBLkZIcSMQpvTeYHibhJuQd2qTAmie8ygBRHsQP-7Cd9HLxlwcOeP_IFgYSohIbYoEQeUSb9WdfkDj9PrNGyQ_5FGLJNLJkGlX5XUIb9cAVGNjA5In34MAXkQQHDjP5OEQBf_pjD7tBydxhW3hb2a9J5FWXtcFCoKKl3a9jJ-IJWgfRcB03tgpyJBWBwcUF2QxyGOA3VmSeQERRhhn4GHXBedCJOcGA4FVNfUSadr6gOZsZlqw3KbGMRi1XJjWceZb53qgb2pXRoZ_mlqw3KTQcPagjluph.; isg=BOrqXtnOebYXhfQ1b9KgdzAAO1aMW2618WeuUnSgRz1Qp45hXO-pxEuRN9O7V-ZN'}
        # cookies = {}
        path = '/Users/xigua/Downloads'
        filename = 'test'
        result = requests.get(
            url=url,
            headers=headers,
            cookies=cookies,
        )
        m_data = json.loads(result.text)
        # print(m_data)
        update_time = m_data['data']['updateTime']
        all_data = m_data['data']['data']
        timestamp = all_data['statDate']['value'] // 1000  # 毫秒转为秒，不然无法转换时间戳

        datas=[{
            '日期': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp))),
            '预热加购人数': all_data['preheatCartByrCnt']['value'],
            '加购转化率': all_data['cartRate']['value'],
            '预热加购件数': all_data['preheatCartItmCnt']['value'],
            '预热访客数': all_data['preheatUv']['value'],
            '收藏转化率': all_data['cltRate']['value'],
            '预热收藏次数': all_data['preheatCltItmCnt']['value'],
            '预热收藏人数': all_data['preheatCltByrCnt']['value'],
            '更新时间': update_time,
            '促销活动': '2024双11抢先购',
            '版块': '预热期核心指标',
        }]
        df = pd.DataFrame(datas)
        df = df.astype({
            '预热加购人数': int,
            '预热加购件数': int,
            '预热访客数': int,
            '预热收藏次数': int,
            '预热收藏人数': int,
            '促销活动': str,
            '版块': str,
        }, errors='raise')
        return '活动分析2', '2024双11抢先购预热期核心指标', df  # 注意这些是实际数据表名字

    def ys_ll_data(self):
        """ 活动预售页面 流量来源 """
        date = datetime.date.today().strftime('%Y%m%d')
        url = (f'https://sycm.taobao.com/datawar/v6/activity/detail/guide/chl/presale/online/v4.json?'
               f'dateRange={date}%7C{date}'
               f'&dateType=today'
               f'&pageSize=10'
               f'&page=1'
               f'&order=desc'
               f'&orderBy=frontPreheatUv'  # 必传参数
               f'&activityId=94040472'  # 关键，必传参数
               # f'&activityStatus=3'
               # f'&device=2'
               # f'&indexCode=frontPreheatUv%2CfrontPayByrCnt%2CfrontPayRate'
               # f'&_=1729079731795'
               # f'&token=7e94ba030'
               )
        headers = {
            # "referer": "https://dmp.taobao.com/index_new.html",
            'User-Agent': ua_sj.get_ua(),
        }
        cookies = {
            'session': 't=c198527347800dafa75165f084784668; thw=cn; cc_gray=1; 2210244713719_euacm_ac_c_uid_=713197610; 2210244713719_euacm_ac_rs_uid_=713197610; _portal_version_=new; xlly_s=1; _euacm_ac_l_uid_=2210244713719; _tb_token_=GzT2Grwtrep02E5awyhr; _samesite_flag_=true; 3PcFlag=1729299229095; cookie2=15f3dfc1aa68e07b05043bf7f8fb5565; sgcookie=E100r7l2QLYERk5SKLinmW40F%2BbdvBhfP7ZwSPi%2BjxeXI6Y%2B%2BraqfGzS%2BKX3ME%2FRfXZKeLBwECj63B245VuW%2FZBpg5X3Ydq2WK05z0QvsUxuyJQNNaVJTDy8WSQXRpKhFDHF; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie14=UoYcCoJCtZ6mUg%3D%3D&cookie21=UtASsssmfufd; csg=7d17ab64; _cc_=V32FPkk%2Fhw%3D%3D; cancelledSubSites=empty; skt=214c26d846e4ece2; cna=8+iAHxeojXcCAXjsc5Mt+BAV; v=0; XSRF-TOKEN=a4816e90-82aa-4743-b438-67e826b8ebbe; datawar_version=new; mtop_partitioned_detect=1; _m_h5_tk=c1140ed9be58a574cf0740ca0fad2f9c_1729340693031; _m_h5_tk_enc=2a93813f4e75d7928cc79cc6bc9db5d7; _euacm_ac_rs_sid_=67090549; JSESSIONID=3DBCB84C04569B30741EF0263731963E; tfstk=gbRSfuVwPHdqd3wyBX3VCcGDfR5IVHGN9y_pSeFzJ_CRvXKpc9FEE_WCOnI2ag8Pww1BSHZrr95ROMTMVJ8PY8-XJet_aL-eYzvDbFFyaYfUO_fh9coZ_fzkr6fKIj10GzfA-NE-TgF-MUjmccen_f8kyz7-7Ehwagr3NGjd9TBLkZIcSMQpvTeYHibhJuQd2qTAmie8ygBRHsQP-7Cd9HLxlwcOeP_IFgYSohIbYoEQeUSb9WdfkDj9PrNGyQ_5FGLJNLJkGlX5XUIb9cAVGNjA5In34MAXkQQHDjP5OEQBf_pjD7tBydxhW3hb2a9J5FWXtcFCoKKl3a9jJ-IJWgfRcB03tgpyJBWBwcUF2QxyGOA3VmSeQERRhhn4GHXBedCJOcGA4FVNfUSadr6gOZsZlqw3KbGMRi1XJjWceZb53qgb2pXRoZ_mlqw3KTQcPagjluph.; isg=BOrqXtnOebYXhfQ1b9KgdzAAO1aMW2618WeuUnSgRz1Qp45hXO-pxEuRN9O7V-ZN'}

        path = '/Users/xigua/Downloads'
        filename = 'test'

        result = requests.get(
            url=url,
            headers=headers,
            cookies=cookies,
        )
        m_data = json.loads(result.text)
        # print(m_data)
        update_time = m_data['data']['updateTime']
        # pt_data = data['data']['data'][0]  # 平台流量
        # gg_data = data['data']['data'][1]  # 广告流量
        datas = []
        for all_data in m_data['data']['data']:
            datas.append(
                {
                    'frontPayByrCnt': all_data['frontPayByrCnt']['value'],
                    '一级标识id': all_data['pageId']['value'],
                    '二级标识id': '',
                    '三级标识id': '',
                    '一级来源': all_data['pageName']['value'],
                    '二级来源': '',
                    '三级来源': '',
                    '活动商品访客数（定金期）': all_data['frontPreheatUv']['value'],
                    '定金支付买家数': all_data['frontPayByrCnt']['value'],
                    '定金支付转化率': all_data['frontPayRate']['value'],
                    '日期': all_data['statDateStr']['value'],
                    '更新时间': update_time,
                    '促销活动': '2024双11预售',
                    '版块': '流量来源',
                }
            )
            if 'children' not in all_data.keys():  # 这一句有点多余，因为一级来源必定细分有二级来源
                continue
            for children_data in all_data['children']:
                one_source_id = children_data['pPageId']['value']
                one_source_name = children_data['pPageName']['value']
                datas.append(
                    {
                        'frontPayByrCnt': children_data['frontPayByrCnt']['value'],
                        '一级标识id': children_data['pPageId']['value'],
                        '二级标识id': children_data['pageId']['value'],
                        '三级标识id': '',
                        '一级来源': children_data['pPageName']['value'],
                        '二级来源': children_data['pageName']['value'],
                        '三级来源': '',
                        '活动商品访客数（定金期）': children_data['frontPreheatUv']['value'],
                        '定金支付买家数': children_data['frontPayByrCnt']['value'],
                        '定金支付转化率': children_data['frontPayRate']['value'],
                        '日期': children_data['statDateStr']['value'],
                        '更新时间': update_time,
                        '促销活动': '2024双11预售',
                        '版块': '流量来源',
                    }
                )
                # print(children_data['children'])
                # print(children_data)
                if 'children' not in children_data.keys():  # 部分二级来源没有细分的三级来源，因为需要跳过 children 字段
                    continue
                for children_children_data in children_data['children']:
                    # print(children_children_data)
                    # print(one_source_name)
                    datas.append(
                        {
                            'frontPayByrCnt': children_children_data['frontPayByrCnt']['value'],
                            '一级标识id': one_source_id,
                            '二级标识id': children_children_data['pPageId']['value'],
                            '三级标识id': children_children_data['pageId']['value'],
                            '一级来源': one_source_name,
                            '二级来源': children_children_data['pPageName']['value'],
                            '三级来源': children_children_data['pageName']['value'],
                            '活动商品访客数（定金期）': children_children_data['frontPreheatUv']['value'],
                            '定金支付买家数': children_children_data['frontPayByrCnt']['value'],
                            '定金支付转化率': children_children_data['frontPayRate']['value'],
                            '日期': children_children_data['statDateStr']['value'],
                            '更新时间': update_time,
                            '促销活动': '2024双11预售',
                            '版块': '流量来源',
                        }
                    )
        for item in datas:
            if item['日期'] != '':
                item.update({'日期': f'{item['日期'][0:4]}-{item['日期'][4:6]}-{item['日期'][6:8]}'})
        if self.is_json_file:
            if self.path and self.filename:
                with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
                    json.dump(datas, f, ensure_ascii=False, sort_keys=True, indent=4)
            else:
                print(f'尚未指定 self.path/ self.filename')
        df = pd.DataFrame(datas)
        df.fillna('0', inplace=True)
        df = df.astype(
            {
                'frontPayByrCnt': int,
                '一级标识id': str,
                '二级标识id': str,
                '三级标识id': str,
                '一级来源': str,
                '二级来源': str,
                '三级来源': str,
                '活动商品访客数（定金期）': int,
                '定金支付买家数': int,
                '促销活动': str,
                '版块': str,
        }, errors='raise')
        return '活动分析2', '2024双11预售实时流量分析', df  # 注意这些是实际数据表名字

    def qxg_ll(self):
        flow_biz_types = {
            'classic': '非全站推广期',
            'qzt': '全站推广期',
        }
        page_types = {
            'item': '商品流量',
            'shop': '店铺流量',
            'live': '直播流量',
            'content': '内容流量',
        }
        for k_flow, v_flow in flow_biz_types.items():
            for k_page, v_page in page_types.items():
                if v_flow == '全站推广期' and v_page != '商品流量':
                    continue  # 只有商品流量才可以传 qzt值
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                print(f'{now} {v_flow} -> {v_page}: 正在获取数据...')
                date = datetime.date.today().strftime('%Y%m%d')
                url = (
                    f'https://sycm.taobao.com/flow/v5/live/shop/source/tree/v4.json?'
                   f'dateRange={date}%7C{date}'
                   f'&dateType=today'
                   f'&order=desc'
                   f'&orderBy=uv'
                   f'&flowBizType={k_flow}'  # classic: 非全站推广期，qzt: 全站推广期（只有商品流量才可以传 qzt值）
                   f'&pageType={k_page}'  # item：商品流量，shop: 店铺流量，live: 直播流量， content： 内容流量
                   f'&crowdType=all'
                   f'&activityId=92072444'
                   f'&indexCode=uv'
                   # f'&_=1729232086296'
                   # f'&token=2507b8098'
                )
                headers = {
                    # "referer": "https://dmp.taobao.com/index_new.html",
                    'User-Agent': ua_sj.get_ua(),
                }
                cookies = {
                    'session': 't=c198527347800dafa75165f084784668; thw=cn; cc_gray=1; 2210244713719_euacm_ac_c_uid_=713197610; 2210244713719_euacm_ac_rs_uid_=713197610; _portal_version_=new; xlly_s=1; _euacm_ac_l_uid_=2210244713719; _tb_token_=GzT2Grwtrep02E5awyhr; _samesite_flag_=true; 3PcFlag=1729299229095; cookie2=15f3dfc1aa68e07b05043bf7f8fb5565; sgcookie=E100r7l2QLYERk5SKLinmW40F%2BbdvBhfP7ZwSPi%2BjxeXI6Y%2B%2BraqfGzS%2BKX3ME%2FRfXZKeLBwECj63B245VuW%2FZBpg5X3Ydq2WK05z0QvsUxuyJQNNaVJTDy8WSQXRpKhFDHF; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie14=UoYcCoJCtZ6mUg%3D%3D&cookie21=UtASsssmfufd; csg=7d17ab64; _cc_=V32FPkk%2Fhw%3D%3D; cancelledSubSites=empty; skt=214c26d846e4ece2; cna=8+iAHxeojXcCAXjsc5Mt+BAV; v=0; XSRF-TOKEN=a4816e90-82aa-4743-b438-67e826b8ebbe; datawar_version=new; mtop_partitioned_detect=1; _m_h5_tk=c1140ed9be58a574cf0740ca0fad2f9c_1729340693031; _m_h5_tk_enc=2a93813f4e75d7928cc79cc6bc9db5d7; _euacm_ac_rs_sid_=67090549; JSESSIONID=3DBCB84C04569B30741EF0263731963E; tfstk=gbRSfuVwPHdqd3wyBX3VCcGDfR5IVHGN9y_pSeFzJ_CRvXKpc9FEE_WCOnI2ag8Pww1BSHZrr95ROMTMVJ8PY8-XJet_aL-eYzvDbFFyaYfUO_fh9coZ_fzkr6fKIj10GzfA-NE-TgF-MUjmccen_f8kyz7-7Ehwagr3NGjd9TBLkZIcSMQpvTeYHibhJuQd2qTAmie8ygBRHsQP-7Cd9HLxlwcOeP_IFgYSohIbYoEQeUSb9WdfkDj9PrNGyQ_5FGLJNLJkGlX5XUIb9cAVGNjA5In34MAXkQQHDjP5OEQBf_pjD7tBydxhW3hb2a9J5FWXtcFCoKKl3a9jJ-IJWgfRcB03tgpyJBWBwcUF2QxyGOA3VmSeQERRhhn4GHXBedCJOcGA4FVNfUSadr6gOZsZlqw3KbGMRi1XJjWceZb53qgb2pXRoZ_mlqw3KTQcPagjluph.; isg=BOrqXtnOebYXhfQ1b9KgdzAAO1aMW2618WeuUnSgRz1Qp45hXO-pxEuRN9O7V-ZN'}
                self.qxg_ll_data(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    flow_biz_type=v_flow,
                    page_type=v_page,
                )
                time.sleep(random.randint(5, 10))
        df = pd.concat(self.datas)
        df.fillna(0, inplace=True)
        df = df.astype(
            {
                '支付买家数': int,
                '详情页访客数': int,
                '来源等级': int,
                'showDetailChannel': int,
            }, errors='raise')
        # df.to_csv('/Users/xigua/Downloads/test.csv', index=False, header=True, encoding='utf-8_sig')
        return '活动分析2', '2024双11抢先购预热期流量来源', df  # 注意这些是实际数据表名字

    def qxg_ll_data(self, url, headers, cookies, flow_biz_type, page_type):
        """ 抢先购 流量来源 """
        result = requests.get(
            url=url,
            headers=headers,
            cookies=cookies,
        )
        json_datas = json.loads(result.text)
        update_time = json_datas['data']['updateTime']
        # print(update_time)
        datas = []
        json_datas = json_datas['data']['data']
        dict_data = {}
        if page_type == '直播流量' or page_type == '内容流量':
            for item in json_datas:
                datas.append(
                    {
                        '访客数': item['uv']['value'],
                        'pageId': item['pageId']['value'],
                        '0级来源': item['pageName']['value'],
                        'pPageId': item['pPageId']['value'],
                        '日期': update_time,
                        '更新时间': update_time,
                        '促销活动': '2024双11抢先购',
                        '版块': '流量来源',
                        '来源分类': flow_biz_type,
                        '流量类型': page_type,
                    })
            json_datas = json_datas[0]['children']

        for all_data in json_datas:
            # one_source_id = all_data['pageId']['value']
            one_source_name = all_data['pageName']['value']
            # print(all_data)
            for k_first, v_first in all_data.items():
                # print(k_first, v_first)

                if k_first == 'children':
                    continue
                for k_second, v_second in v_first.items():
                    if k_second != 'value':
                        dict_data.update({k_second: v_second})
            dict_data.update(
                {
                    'guideToShortVideoUv': all_data['guideToShortVideoUv']['value'],
                    'hiddenIndexgroup': all_data['hiddenIndexgroup']['value'],
                    '访客数': all_data['uv']['value'],
                    '访客数占比': all_data['uv']['ratio'],
                    '支付买家数': all_data['payByrCnt']['value'],
                    '详情页访客数': all_data['ipvUvRelate']['value'],
                    '支付转化率': all_data['payRate']['value'],
                    'orderByrCnt': all_data['orderByrCnt']['value'],
                    'showDesc': all_data['showDesc']['value'],
                    'showChannel': all_data['showChannel']['value'],
                    '来源等级': all_data['pageLevel']['value'],
                    'channelType': all_data['channelType']['value'],
                    'orderAmt': all_data['orderAmt']['value'],
                    'pageId': all_data['pageId']['value'],
                    'pPageId': all_data['pPageId']['value'],
                    'payAmt': all_data['payAmt']['value'],
                    '一级来源': all_data['pageName']['value'],
                    '二级来源': '',
                    '三级来源': '',
                    'showDetailChannel': all_data['showDetailChannel']['value'],
                    'pageDesc': all_data['pageDesc']['value'],
                    'payPct': all_data['payPct']['value'],
                    'pPageId': all_data['pPageId']['value'],
                    'crtRate': all_data['crtRate']['value'],
                    '日期': update_time,
                    '更新时间': update_time,
                    '促销活动': '2024双11抢先购',
                    '版块': '流量来源',
                    '来源分类': flow_biz_type,
                    '流量类型': page_type,
                }
            )
            datas.append(dict_data)

            if 'children' not in all_data.keys():  # 这一句有点多余，因为一级来源必定细分有二级来源
                continue

            for children_data in all_data['children']:
                # one_source_id = children_data['pPageId']['value']
                second_source_name = children_data['pageName']['value']
                for k_first, v_first in children_data.items():
                    # print(k_first, v_first)
                    dict_data = {}
                    if k_first == 'children':
                        continue
                    for k_second, v_second in v_first.items():
                        if k_second != 'value':
                            dict_data.update({k_second: v_second})
                dict_data.update(
                    {
                        'guideToShortVideoUv': children_data['guideToShortVideoUv']['value'],
                        'hiddenIndexgroup': children_data['hiddenIndexgroup']['value'],
                        '访客数': children_data['uv']['value'],
                        '访客数占比': children_data['uv']['ratio'],
                        '支付买家数': children_data['payByrCnt']['value'],
                        '详情页访客数': children_data['ipvUvRelate']['value'],
                        '支付转化率': children_data['payRate']['value'],
                        'orderByrCnt': children_data['orderByrCnt']['value'],
                        'showDesc': children_data['showDesc']['value'],
                        'showChannel': children_data['showChannel']['value'],
                        '来源等级': children_data['pageLevel']['value'],
                        'channelType': children_data['channelType']['value'],
                        'orderAmt': children_data['orderAmt']['value'],
                        'pageId': children_data['pageId']['value'],
                        'pPageId': children_data['pPageId']['value'],
                        'payAmt': children_data['payAmt']['value'],
                        '一级来源': one_source_name,
                        '二级来源': children_data['pageName']['value'],
                        '三级来源': '',
                        'showDetailChannel': children_data['showDetailChannel']['value'],
                        'pageDesc': children_data['pageDesc']['value'],
                        'payPct': children_data['payPct']['value'],
                        'pPageId': children_data['pPageId']['value'],
                        'crtRate': children_data['crtRate']['value'],
                        '日期': update_time,
                        '更新时间': update_time,
                        '促销活动': '2024双11抢先购',
                        '版块': '流量来源',
                        '来源分类': flow_biz_type,
                        '流量类型': page_type,
                    }
                )
                datas.append(dict_data)
                # print(children_data['children'])
                # print(children_data)
                if 'children' not in children_data.keys():  # 部分二级来源没有细分的三级来源，因为需要跳过 children 字段
                    continue
                for children_children_data in children_data['children']:
                    # print(children_children_data)
                    # print(one_source_name)
                    for k_first, v_first in children_data.items():
                        # print(k_first, v_first)
                        dict_data = {}
                        if k_first == 'children':
                            continue
                        for k_second, v_second in v_first.items():
                            if k_second != 'value':
                                dict_data.update({k_second: v_second})
                    dict_data.update(
                        {
                            'guideToShortVideoUv': children_children_data['guideToShortVideoUv']['value'],
                            'hiddenIndexgroup': children_children_data['hiddenIndexgroup']['value'],
                            '访客数': children_children_data['uv']['value'],
                            '访客数占比': children_children_data['uv']['ratio'],
                            '支付买家数': children_children_data['payByrCnt']['value'],
                            '详情页访客数': children_children_data['ipvUvRelate']['value'],
                            '支付转化率': children_children_data['payRate']['value'],
                            'orderByrCnt': children_children_data['orderByrCnt']['value'],
                            'showDesc': children_children_data['showDesc']['value'],
                            'showChannel': children_children_data['showChannel']['value'],
                            '来源等级': children_children_data['pageLevel']['value'],
                            'channelType': children_children_data['channelType']['value'],
                            'orderAmt': children_children_data['orderAmt']['value'],
                            'pageId': children_children_data['pageId']['value'],
                            'pPageId': children_children_data['pPageId']['value'],
                            'payAmt': children_children_data['payAmt']['value'],
                            '一级来源': one_source_name,
                            '二级来源': second_source_name,
                            '三级来源': children_children_data['pageName']['value'],
                            'showDetailChannel': children_children_data['showDetailChannel']['value'],
                            'pageDesc': children_children_data['pageDesc']['value'],
                            'payPct': children_children_data['payPct']['value'],
                            'pPageId': children_children_data['pPageId']['value'],
                            'crtRate': children_children_data['crtRate']['value'],
                            '日期': update_time,
                            '更新时间': update_time,
                            '促销活动': '2024双11抢先购',
                            '版块': '流量来源',
                            '来源分类': flow_biz_type,
                            '流量类型': page_type,
                        }
                    )
                    datas.append(dict_data)
        # for item in datas:
        #     if item['日期'] != '':
        #         item.update({'日期': f'{item['日期'][0:4]}-{item['日期'][4:6]}-{item['日期'][6:8]}'})
        df = pd.DataFrame(datas)
        self.datas.append(df)

    def hd_sp(self, date, url, headers, cookies, path, filename, pages=5):
        """ 活动预售页面 分商品效果 """

        self.date = date
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.path = path
        self.filename = filename
        for page in range(1, pages + 1):
            self.url = f'{self.url}&page={page}'
            result = requests.get(
                self.url,
                headers=self.headers,
                cookies=self.cookies,
            )
            m_data = json.loads(result.text)
            # print(m_data)
            # with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
            #     json.dump(m_data, f, ensure_ascii=False, sort_keys=True, indent=4)
            update_time = m_data['data']['updateTime']
            time_stamp = m_data['data']['timestamp']
            # pt_data = data['data']['data'][0]  # 平台流量
            # gg_data = data['data']['data'][1]  # 广告流量
            for all_data in m_data['data']['data']['data']:
                self.datas.append({
                    'activityItemDepUv': all_data['activityItemDepUv']['value'],
                    '商品链接': all_data['item']['detailUrl'],
                    '商品id': all_data['item']['itemId'],
                    '商品图片': all_data['item']['pictUrl'],
                    'startDate': all_data['item']['startDate'],
                    '商品标题': all_data['item']['title'],
                    '预售订单金额': all_data['presaleOrdAmt']['value'],
                    '定金支付件数': all_data['presalePayItemCnt']['value'],
                    '预售访客人数': all_data['presaleUv']['value'],
                    '定金支付金额': all_data['sumPayDepositAmt']['value'],
                    '定金支付买家数': all_data['sumPayDepositByrCnt']['value'],
                    '支付转化率': all_data['uvPayRate']['value'],
                    '日期': date,
                    '时间戳': time_stamp,
                    '更新时间': update_time,
                    '促销活动': '2024双11预售',
                    '类型': '分商品效果',
                })
            time.sleep(random.randint(5, 10))
        for item in self.datas:
            if item['日期'] != '':
                item.update({'日期': f'{item['日期'][0:4]}-{item['日期'][4:6]}-{item['日期'][6:8]}'})
        if self.is_json_file:
            with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
                json.dump(self.datas, f, ensure_ascii=False, sort_keys=True, indent=4)

    def request_jd(self, date, url, headers, cookies, path, filename):
        """ 京东 """
        self.date = date
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.path = path
        self.filename = filename
        result = requests.post(
            url,
            headers=headers,
            cookies=cookies,
        )
        print(result.text)


def hd_sp_data(service_databases=[], db_name=None, table_name=None, pages=5):
    """ 2024双11预售 分商品效果 """
    date = datetime.date.today().strftime('%Y%m%d')
    url = (
        f'https://sycm.taobao.com/datawar/v7/presaleActivity/itemCoreIndex/getItemListLive.json?'
        f'activityId=94040472'
        f'&itemType=0'  # 必传， 查看全部商品 0， 活动商品 1 ， 跨店满减商品 2 ，官方立减 3（无数据）
        f'&device=1'
        f'&dateRange={date}%7C{date}'
        f'&dateType=today'
        f'&pageSize=10'  # 必传
        # f'&page=1'   # 必传
        # f'&order=desc'
        # f'&orderBy=presaleOrdAmt'
        # f'&indexCode=presaleOrdAmt%2CsumPayDepositByrCnt%2CpresalePayItemCnt'
        # f'&_=1729133575797'
           )
    headers = {
        # "referer": "https://dmp.taobao.com/index_new.html",
        'User-Agent': ua_sj.get_ua(),
    }
    cookies = {
        'session': 't=c198527347800dafa75165f084784668; thw=cn; cc_gray=1; 2210244713719_euacm_ac_c_uid_=713197610; 2210244713719_euacm_ac_rs_uid_=713197610; _portal_version_=new; xlly_s=1; _euacm_ac_l_uid_=2210244713719; _tb_token_=GzT2Grwtrep02E5awyhr; _samesite_flag_=true; 3PcFlag=1729299229095; cookie2=15f3dfc1aa68e07b05043bf7f8fb5565; sgcookie=E100r7l2QLYERk5SKLinmW40F%2BbdvBhfP7ZwSPi%2BjxeXI6Y%2B%2BraqfGzS%2BKX3ME%2FRfXZKeLBwECj63B245VuW%2FZBpg5X3Ydq2WK05z0QvsUxuyJQNNaVJTDy8WSQXRpKhFDHF; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie14=UoYcCoJCtZ6mUg%3D%3D&cookie21=UtASsssmfufd; csg=7d17ab64; _cc_=V32FPkk%2Fhw%3D%3D; cancelledSubSites=empty; skt=214c26d846e4ece2; cna=8+iAHxeojXcCAXjsc5Mt+BAV; v=0; XSRF-TOKEN=a4816e90-82aa-4743-b438-67e826b8ebbe; datawar_version=new; mtop_partitioned_detect=1; _m_h5_tk=c1140ed9be58a574cf0740ca0fad2f9c_1729340693031; _m_h5_tk_enc=2a93813f4e75d7928cc79cc6bc9db5d7; _euacm_ac_rs_sid_=67090549; JSESSIONID=3DBCB84C04569B30741EF0263731963E; tfstk=gbRSfuVwPHdqd3wyBX3VCcGDfR5IVHGN9y_pSeFzJ_CRvXKpc9FEE_WCOnI2ag8Pww1BSHZrr95ROMTMVJ8PY8-XJet_aL-eYzvDbFFyaYfUO_fh9coZ_fzkr6fKIj10GzfA-NE-TgF-MUjmccen_f8kyz7-7Ehwagr3NGjd9TBLkZIcSMQpvTeYHibhJuQd2qTAmie8ygBRHsQP-7Cd9HLxlwcOeP_IFgYSohIbYoEQeUSb9WdfkDj9PrNGyQ_5FGLJNLJkGlX5XUIb9cAVGNjA5In34MAXkQQHDjP5OEQBf_pjD7tBydxhW3hb2a9J5FWXtcFCoKKl3a9jJ-IJWgfRcB03tgpyJBWBwcUF2QxyGOA3VmSeQERRhhn4GHXBedCJOcGA4FVNfUSadr6gOZsZlqw3KbGMRi1XJjWceZb53qgb2pXRoZ_mlqw3KTQcPagjluph.; isg=BOrqXtnOebYXhfQ1b9KgdzAAO1aMW2618WeuUnSgRz1Qp45hXO-pxEuRN9O7V-ZN'}

    path = '/Users/xigua/Downloads'
    filename = 'test'
    r = RequestData()
    r.is_json_file = False
    r.hd_sp(
        date=date,
        url=url,
        headers=headers,
        cookies=cookies,
        path=path,
        filename=filename,
        pages = pages,
    )
    # print(r.datas)
    df = pd.DataFrame(r.datas)
    df.to_csv(os.path.join(path, 'test.csv'), index=False, header=True, encoding='utf-8_sig')


def company_run(service_databases=[]):
    # if platform.system() != 'Windows':
    #     return
    # if socket.gethostname() != 'company':
    #     return
    while True:
        r = RequestData()
        r.is_json_file = False

        my_data_list = [
            # r.ys_ll_data(),  # 双 11预售实时流量分析
            # r.qxg_hx_data(),  # 抢先购 预热期核心指标
            r.qxg_ll()  # 抢先购 流量来源
        ]

        results = []
        for my_data in my_data_list:
            db_name, table_name, df = my_data
            if len(df) == 0:
                print(f'{db_name} -> {table_name} has no data')
                continue
            # print(df)
            results.append([db_name, table_name, df])

        if not service_databases:
            return
        for dt in service_databases:
            for service_name, database in dt.items():
                username, password, host, port = get_myconf.select_config_values(
                    target_service=service_name,
                    database=database,
                )
                m = mysql.MysqlUpload(
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                )
                for result in results:
                    db_name, table_name, df = result
                    m.df_to_mysql(
                        df=df,
                        db_name=db_name,
                        table_name=table_name,
                        move_insert=False,  # 先删除，再插入
                        df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                        drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                        count=None,
                        filename=None,  # 用来追踪处理进度
                    )
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                    print(f'{now} {db_name} -> {table_name}: 已入库')

        time.sleep(random.randint(1500, 2000))


if __name__ == '__main__':
    company_run(service_databases=[{'company': 'mysql'}])
