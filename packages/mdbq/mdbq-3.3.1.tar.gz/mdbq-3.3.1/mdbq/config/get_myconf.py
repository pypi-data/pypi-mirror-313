# -*- coding: UTF-8 –*-
import platform
import getpass
import socket
import configparser
import os
import sys
from posixpath import dirname
from urllib import parse
from mdbq.config import set_support


class MyConf:
    """
    读取配置文件信息
    """
    def __init__(self, path='support'):
        self.top_path = os.path.realpath(os.path.dirname(sys.argv[0]))  # 程序运行目录, 打包时使用
        self.conf_file = os.path.join(self.top_path, path, '.my_conf')
        self.config = None

    def get_myconf(self, options: list):
        if not os.path.exists(self.conf_file):
            print(f'尚未配置: 缺少 .my_conf 文件 {self.conf_file}')
            return
        if not options:
            print(f'传入的参数为空: {options}')
            return
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file, 'UTF-8')
        results = []
        for option in options:
            try:
                results.append(self.config.get('database', option))
            except configparser.NoOptionError:
                results.append('')
        return results


def select_config_values(target_service, database, path=None):
    """
    target_service: 指向: home_lx, aliyun
    database: 指向: mongodb, mysql
    """
    if not path:
        path = set_support.SetSupport(dirname='support').dirname

    m = MyConf(path=path)
    options = []
    if target_service == 'home_lx':  # 1. 家里笔记本
        if database == 'mongodb':
            if socket.gethostname() == 'xigua_lx':
                # 本机自身运行使用 127.0.0.1
                options = ['username_db_lx_nw', 'password_db_lx_nw', 'host_bd',  'port_db_lx_nw',]
            elif socket.gethostname() == 'xigua1' or socket.gethostname() == 'MacBook-Pro':
                # 内网地址：正在运行的是 家里笔记本或者台式机，或者 macbook pro
                options = ['username_db_lx_nw', 'password_db_lx_nw', 'host_db_lx_nw',  'port_db_lx_nw',]
            else:
                options = ['username_db_lx', 'password_db_lx', 'host_db_lx', 'port_db_lx']

        elif database == 'mysql':
            if socket.gethostname() == 'xigua_lx':
                # 本机自身运行使用 127.0.0.1
                options = ['username_mysql_lx_nw', 'password_mysql_lx_nw', 'host_bd',  'port_mysql_lx_nw',]
            elif socket.gethostname() == 'xigua1' or socket.gethostname() == 'MacBookPro':
                # 内网地址：正在运行的是 家里笔记本或者台式机，或者 macb    ook pro
                options = ['username_mysql_lx_nw', 'password_mysql_lx_nw', 'host_mysql_lx_nw',  'port_mysql_lx_nw',]
            else:
                options = ['username_mysql_lx', 'password_mysql_lx', 'host_mysql_lx', 'port_mysql_lx']

    elif target_service == 'home_xigua1':
        if database == 'mongodb':
            print('未配置')
        elif database == 'mysql':
            if socket.gethostname() == 'xigua_lx':
                # 本机自身运行使用 127.0.0.1
                options = ['username_mysql_xigua1_nw', 'password_mysql_xigua1_nw', 'host_mysql_xigua1_nw',  'port_mysql_xigua1_nw',]
            elif socket.gethostname() == 'xigua1' or socket.gethostname() == 'macbook pro':
                # 内网地址：正在运行的是 家里笔记本或者台式机，或者 macb    ook pro
                options = ['username_mysql_xigua1_nw', 'password_mysql_xigua1_nw', 'host_bd',  'port_mysql_xigua1_nw',]
            else:
                print('未配置')
                options = ['', '', '', '']

    elif target_service == 'aliyun':  # 2. 阿里云服务器
        if database == 'mongodb':
            if socket.gethostname() == 'xigua-cloud':
                # 阿里云自身运行使用 127.0.0.1
                options = ['username_db_aliyun', 'password_db_aliyun', 'host_bd', 'port_db_aliyun', ]
            else:
                options = ['username_db_aliyun', 'password_db_aliyun', 'host_db_aliyun', 'port_db_aliyun', ]
        elif database == 'mysql':
            if socket.gethostname() == 'xigua-cloud':
                # 阿里云自身运行使用 127.0.0.1
                options = ['username_mysql_aliyun', 'password_mysql_aliyun', 'host_bd', 'port_mysql_aliyun', ]
            else:
                options = ['username_mysql_aliyun', 'password_mysql_aliyun', 'host_mysql_aliyun', 'port_mysql_aliyun', ]

    elif target_service == 'company':  # 3. 公司台式机
        if database == 'mongodb':
            options = ['username_db_company_nw', 'password_db_company_nw', 'host_db_company_nw', 'port_db_company_nw', ]
        elif database == 'mysql':
            options = ['username_mysql_company_nw', 'password_mysql_company_nw', 'host_mysql_company_nw', 'port_mysql_company_nw', ]

    elif target_service == 'nas':  # 4. 群晖
        if database == 'mysql':
            options = ['username_mysql_nas_nw', 'password_mysql_nas_nw', 'host_mysql_nas_nw', 'port_mysql_nas_nw', ]

    value = m.get_myconf(options=options)
    if not value:
        return '', '', '', 0
    if database == 'mongodb':  # mongodb 特殊字符要转码, mysql 不需要转
        username = parse.quote_plus(str(value[0]).strip())  # 对可能存在的特殊字符进行编码
        password = parse.quote_plus(str(value[1]).strip())  # 如果密码含有 @、/ 字符，一定要进行编码
    else:
        username = str(value[0]).strip()
        password = str(value[1]).strip()
    host = str(value[2]).strip()
    port = int(value[3])
    return username, password, host, port


def main():
    pass


if __name__ == '__main__':
    # main()
    r, d, s, g = select_config_values(target_service='home_lx', database='mysql')
    print(r, d, s, g, type(r), type(d), type(s), type(g))
    print(f'本机: {platform.system()} // {socket.gethostname()}')
