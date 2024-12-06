# -*- coding:utf-8 -*-
import datetime
import getpass
import json
import os
import pathlib
import platform
import re
import time
import warnings
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from mdbq.config import set_support
from selenium.webdriver.common.keys import Keys
from mdbq.other import ua_sj
from mdbq.mysql import mysql
from mdbq.config import myconfig
import socket

warnings.filterwarnings('ignore')


if platform.system() == 'Windows':
    # windows版本
    Data_Path = r'C:\同步空间\BaiduSyncdisk'
    D_PATH = str(pathlib.Path(f'C:\\Users\\{getpass.getuser()}\\Downloads'))
    Share_Path = str(pathlib.Path(r'\\192.168.1.198\时尚事业部\01.运营部\天猫报表'))  # 共享文件根目录
    Source_Path = str(pathlib.Path(Data_Path, '原始文件2'))
elif platform.system() == 'Linux':
    Data_Path = '数据中心'
    D_PATH = 'Downloads'
    if not os.path.exists(D_PATH):
        os.makedirs(D_PATH)
    Share_Path = ''  # linux 通常是远程服务器，不需要访问共享
    Source_Path = str(pathlib.Path(Data_Path, '原始文件2'))
else:
    Data_Path = f'/Users/{getpass.getuser()}/数据中心'  # 使用Mac独立网络时
    # Data_Path = '/Volumes'  # 直接使用共享连接台式机时的配置， 后面接 + 自动0备份/***
    D_PATH = str(pathlib.Path(f'/Users/{getpass.getuser()}/Downloads'))
    Share_Path = str(pathlib.Path('/Volumes/时尚事业部/01.运营部/天猫报表'))  # 共享文件根目录
    Source_Path = str(pathlib.Path(Data_Path, '原始文件2'))
upload_path = os.path.join(D_PATH, '数据上传中心', '爱库存')  # 此目录位于下载文件夹

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


def get_cookie_aikucun():
    """
    """
    _url = 'https://gray-merc.aikucun.com/index.html'
    cookie_path = os.path.join(set_support.SetSupport(dirname='support').dirname, 'cookies')
    filename_aikucun = 'cookie_aikucun.json'
    print(_url)

    option = webdriver.ChromeOptions()  # 浏览器启动选项
    option.headless = True  # False指定为无界面模式
    # 调整chrome启动配置
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    # if platform.system() == 'Windows':
    #     service = Service(os.path.join(f'C:\\Users\\{getpass.getuser()}\\chromedriver.exe'))
    # else:
    #     service = Service('/usr/local/bin/chromedriver')
    if platform.system() == 'Windows':
        # 设置Chrome的路径
        chrome_path = os.path.join(f'C:\\Users\\{getpass.getuser()}', 'chrome\\chrome_win64\\chrome.exe')
        chromedriver_path = os.path.join(f'C:\\Users\\{getpass.getuser()}', 'chrome\\chromedriver.exe')
        # os.environ["webdriver.chrome.driver"] = chrome_path
        option.binary_location = chrome_path  # windows 设置此参数有效
        service = Service(chromedriver_path)
        # service = Service(str(pathlib.Path(f'C:\\Users\\{getpass.getuser()}\\chromedriver.exe')))  # 旧路径
    else:
        # 设置Chrome的路径
        chrome_path = '/usr/local/chrome/Google Chrome for Testing.app'
        chromedriver_path = '/usr/local/chrome/chromedriver'
        os.environ["webdriver.chrome.driver"] = chrome_path

        service = Service(chromedriver_path)
    _driver = webdriver.Chrome(service=service, options=option)  # 创建Chrome驱动程序实例

    # 登录
    _driver.get(_url)
    time.sleep(0.1)
    _driver.maximize_window()  # 窗口最大化 方便后续加载数据
    print(f'请登录并切换到百宝箱，再保存 cookies: \n https://treasurebox.aikucun.com/dashboard/commodity/ranking/merchant?LS=true&shopId=1814114991487782914&from=menu&v=0.1936043279838604')
    wait = WebDriverWait(_driver, timeout=15)
    input_box = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//input[@placeholder="请输入用户名"]')))  #
    input_box.send_keys('广东万里马实业股份有限公司')
    input_box = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//input[@placeholder="请输入密码"]')))  #
    input_box.send_keys('wlm123$$$')
    time.sleep(0.1)
    elements = _driver.find_elements(
        By.XPATH, '//button[@class="merchant_login_btn" and contains(text(), "登录")]')
    _driver.execute_script("arguments[0].click();", elements[0])
    for i in range(100):
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@class="user-info nav-user-slider"]')))
            _driver.get(' https://treasurebox.aikucun.com/dashboard/commodity/ranking/merchant?LS=true&shopId=1814114991487782914&from=menu&v=0.1936043279838604')
            time.sleep(3)
            break
        except:
            time.sleep(5)

    d_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{d_time} 登录成功，正在获取cookie...')
    time.sleep(0.1)

    # 将cookies保存为json格式
    cookies_list = _driver.get_cookies()
    new_cookies_list = []
    for cookie in cookies_list:
        # 该字段有问题所以删除就可以
        if 'HWWAFSESTIME' in cookie:
            continue
        else:
            new_cookies_list.append(cookie)
    json_file = os.path.join(cookie_path, filename_aikucun)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(new_cookies_list, f, ensure_ascii=False, sort_keys=True, indent=4)
    print(f'cookie已保存: {json_file}')

    # _file = os.path.join(cookie_path, filename_aikucun)
    # with open(_file, 'w') as f:
    #     # 将cookies保存为json格式
    #     cookies_list = _driver.get_cookies()
    #     # for cookie in cookies_list:
    #     #     # 该字段有问题所以删除就可以
    #     #     if 'expiry' in cookie:
    #     #         del cookie['expiry']
    #     #     # if 'domain' in cookie:
    #     #     #     cookie['domain'] = '.taobao.com'
    #     cookies_list = json.dumps(cookies_list)
    #     f.write(cookies_list)
    #     print(f'cookie已保存: {_file}')
    _driver.quit()


class AikuCun:
    def __init__(self):
        # self.url = 'https://gray-merc.aikucun.com/index.html'
        self.sp_url = 'https://treasurebox.aikucun.com/dashboard/commodity/ranking/merchant?LS=true&shopId=1814114991487782914&from=menu&v=0.1936043279838604'
        self.cookie_path = os.path.join(set_support.SetSupport(dirname='support').dirname, 'cookies')

    def login(self, shop_name='aikucun', headless=False):
        option = webdriver.ChromeOptions()
        if headless:
            option.add_argument("--headless")  # 设置无界面模式
        # 调整chrome启动配置
        option.add_argument("--disable-gpu")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止日志输出，减少控制台干扰
        option.add_experimental_option("useAutomationExtension", False)
        option.add_argument('--ignore-ssl-error')  # 忽略ssl错误
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出所有窗口
            "browser.download.manager. showAlertOnComplete": False,  # 下载完成后不显示下载完成提示框
            "profile.default_content_setting_values.automatic_downloads": 1,  # 允许自动下载多个文件
        }

        option.add_experimental_option('perfLoggingPrefs', {
            'enableNetwork': True,
            'enablePage': False,
        })
        option.set_capability("goog:loggingPrefs", {
            'browser': 'ALL',
            'performance': 'ALL',
        })
        option.set_capability("goog:perfLoggingPrefs", {
            'enableNetwork': True,
            'enablePage': False,
            'enableTimeline': False
        })

        option.add_experimental_option('prefs', prefs)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实验性参数, 左上角小字

        # 修改默认下载文件夹路径
        option.add_experimental_option("prefs", {"download.default_directory": f'{upload_path}'})

        # # 通过excludeSwitches参数禁用默认的启动路径
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])

        if platform.system() == 'Windows':
            # 设置 chrome 和 chromedriver 启动路径
            chrome_path = os.path.join(f'C:\\Users\\{getpass.getuser()}', 'chrome\\chrome_win64\\chrome.exe')
            chromedriver_path = os.path.join(f'C:\\Users\\{getpass.getuser()}', 'chrome\\chromedriver.exe')
            # os.environ["webdriver.chrome.driver"] = chrome_path
            option.binary_location = chrome_path  # windows 设置此参数有效
            service = Service(chromedriver_path)
            # service = Service(str(pathlib.Path(f'C:\\Users\\{getpass.getuser()}\\chromedriver.exe')))  # 旧路径
        elif platform.system() == 'Darwin':
            chrome_path = '/usr/local/chrome/Google Chrome for Testing.app'
            chromedriver_path = '/usr/local/chrome/chromedriver'
            os.environ["webdriver.chrome.driver"] = chrome_path
            # option.binary_location = chrome_path  # Macos 设置此参数报错
            service = Service(chromedriver_path)
        else:
            chrome_path = '/usr/local/chrome/Google Chrome for Testing.app'
            chromedriver_path = '/usr/local/chrome/chromedriver'
            os.environ["webdriver.chrome.driver"] = chrome_path
            # option.binary_location = chrome_path  # macos 设置此参数报错
            service = Service(chromedriver_path)
        _driver = webdriver.Chrome(options=option, service=service)  # 创建Chrome驱动程序实例
        _driver.maximize_window()  # 窗口最大化 方便后续加载数据

        # 登录
        _driver.get(self.sp_url)
        _driver.delete_all_cookies()  # 首先清除浏览器打开已有的cookies
        name_lists = os.listdir(self.cookie_path)  # cookie 放在主目录下的 cookies 文件夹
        for name in name_lists:
            if shop_name in name and name.endswith('.json') and '~' not in name and '.DS' not in name:
                with open(os.path.join(self.cookie_path, name), 'r') as f:
                    cookies_list = json.load(f)  # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                    for cookie in cookies_list:
                        _driver.add_cookie(cookie)  # 添加cookies信息
        _driver.refresh()
        time.sleep(3)
        return _driver

    def get_data(self, shop_name='aikucun', date_num=1, headless=True):
        """
        date_num: 获取最近 N 天数据，0表示今天
        所有数据都是逐日下载
        """

        _driver = self.login(shop_name=shop_name, headless=headless)

        _driver.get(self.sp_url)
        time.sleep(3)
        # breakpoint()

        today = datetime.date.today()
        for date_s in range(date_num):
            new_date = today - datetime.timedelta(days=date_s)  # 会用作文件名
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} 正在下载爱库存文件 {date_s+1}/{date_num}: {new_date}')
            str_date = str(new_date)[2:]
            wait = WebDriverWait(_driver, timeout=15)  #
            elements = _driver.find_elements(
                By.XPATH, '//input[@placeholder="开始日期"]')
            # _driver.execute_script("arguments[0].click();", elements[0])  # 点击

            input_box = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@placeholder="开始日期"]')))  #

            # from selenium.webdriver.common.keys import Keys
            for i in range(8):
                input_box.send_keys(Keys.BACKSPACE)
            input_box.send_keys(str_date)
            time.sleep(1)
            input_box = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@placeholder="结束日期"]')))  # 文件名输入框

            for i in range(8):
                input_box.send_keys(Keys.BACKSPACE)
            input_box.send_keys(str_date)
            time.sleep(2)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button/span[contains(text(), "查询")]')))
            elements = _driver.find_elements(
                By.XPATH, '//button/span[contains(text(), "查询")]')
            _driver.execute_script("arguments[0].click();", elements[0])  # 点击
            time.sleep(5)
            wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 '//button[@class="el-button el-button--primary el-button--small is-plain"]/span[contains(text(), "下载数据")]')))

            elements = _driver.find_elements(
                By.XPATH,
                '//div[@class="ak-page-list__table-empty" and contains(text(), "暂无数据")]')
            if elements:
                print(f'cookies 可能已过期，无法下载')
                _driver.quit()
                return

            elements = _driver.find_elements(
                By.XPATH,
                '//button[@class="el-button el-button--primary el-button--small is-plain"]/span[contains(text(), "下载数据")]')
            _driver.execute_script("arguments[0].click();", elements[0])  # 点击
            time.sleep(5)
            self.clean_data(date=new_date)  # 每下载一个文件，需要立即清洗数据
        _driver.quit()

    def clean_data(self, date):
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
        for root, dirs, files in os.walk(upload_path, topdown=False):
            for name in files:
                if '~$' in name or 'DS_Store' in name:
                    continue
                if name.endswith('csv'):
                    pattern = re.findall('[\u4e00-\u9fff]+', name)
                    if pattern:
                        continue
                    pattern = re.findall('^[0-9a-zA-Z_]{5,}-[0-9a-zA-Z_]+-[0-9a-zA-Z_]+-[0-9a-zA-Z_]+', name)
                    if not pattern:
                        continue
                    df = pd.read_csv(os.path.join(root, name), encoding='gb2312', header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'数据长度为 0 : {name}')
                        os.remove(os.path.join(root, name))
                        continue
                    df.insert(loc=0, column='日期', value=date)  # df中插入新列
                    df.insert(loc=1, column='店铺名称', value='爱库存平台')  # df中插入新列
                    df.rename(columns={'spuId': 'spu_id'}, inplace=True)
                    # df['数据更新时间'] = pd.to_datetime(df['数据更新时间'], format='%Y-%m-%d %H:%M:%S', errors='ignore')
                    # df['数据更新时间'] = df['数据更新时间'].apply(lambda x: re.sub('  ', ' ', str(x)) if x else x)
                    # print(df['数据更新时间'])
                    # breakpoint()
                    new_dict = {
                        '日期': '',
                        '店铺名称': '',
                        '序号': '',
                        '商品名称': '',
                        'spu_id': '',
                        '商品款号': '',
                        '一级类目名称': '',
                        '二级类目名称': '',
                        '三级类目名称': '',
                        '访客量': '',
                        '浏览量': '',
                        '下单gmv': '',
                        '成交gmv': '',
                        '支付人数_成交': '',
                    }
                    _results = []
                    for dict_data in df.to_dict(orient='records'):
                        new_dict.update(dict_data)
                        new_dict.update({'更新时间': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                        _results.append(new_dict)
                    if _results:
                        m_engine.insert_many_dict(
                            db_name='爱库存2',
                            table_name='商品spu榜单',
                            dict_data_list=_results,
                            icm_update=['日期', '店铺名称', 'spu_id', '商品款号'],
                            unique_main_key=None,
                            set_typ=set_typ,
                        )
                        company_engine.insert_many_dict(
                            db_name='爱库存2',
                            table_name='商品spu榜单',
                            dict_data_list=_results,
                            icm_update=['日期', '店铺名称', 'spu_id', '商品款号'],
                            unique_main_key=None,
                            set_typ=set_typ,
                        )

                    new_name = f'爱库存_商品榜单_spu_{date}_{date}.csv'
                    df.to_csv(os.path.join(root, new_name), encoding='utf-8_sig', index=False)
                    os.remove(os.path.join(root, name))


def akucun(headless=True, date_num=10):
    akc = AikuCun()
    akc.get_data(shop_name='aikucun', date_num=date_num, headless=headless)  # 获取最近 N 天数据，0表示今天


class AikuCunNew:

    def __init__(self, shop_name,):
        self.shop_name = shop_name
        self.today = datetime.date.today()
        self.headers = {'User-Agent': ua_sj.get_ua()}
        self.cookie_path = os.path.join(set_support.SetSupport(dirname='support').dirname, 'cookies')
        self.cookies = {}
        self.get_cookies()  # 更新 self.cookies 的值
        self.support_path = set_support.SetSupport(dirname='support').dirname
        self.start_date = (self.today - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        self.end_date = (self.today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def akc(self):
        """
        """
        start_date = self.start_date
        end_date = self.end_date
        url = 'https://treasurebox.aikucun.com/api/web/merchant/treasure/commodity/list/down?'
        self.headers.update({'Referer': 'https://treasurebox.aikucun.com/dashboard/commodity/ranking/merchant?LS=true&shopId=1814114991487782914&from=menu&v=0.1936043279838604'})
        now = datetime.datetime.now()
        timestamp_ms = round(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)
        data = {
            'time': timestamp_ms,
            'sign': '2DA6A7580C859B374AE830CAD78BB84B'
        }
        res = requests.post(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params=data
        )
        print(res.text)



    def get_cookies(self):
        files = os.listdir(self.cookie_path)
        for file in files:
            if self.shop_name in file and '~' not in file:
                with open(os.path.join(self.cookie_path, file), 'r') as f:
                    cookies_data = json.load(f)
                break
        for data in cookies_data:
            self.cookies.update({data['name']: data['value']})


if __name__ == '__main__':
    get_cookie_aikucun()  # 登录并获取 cookies
    akucun(date_num=5, headless=True)  # 下载数据

    # a = AikuCunNew(shop_name='aikucun')
    # a.akc()
