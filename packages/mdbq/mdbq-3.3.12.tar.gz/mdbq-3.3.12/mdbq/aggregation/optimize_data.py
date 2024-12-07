# -*- coding: UTF-8 –*-
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.config import myconfig
import socket
import subprocess
import psutil
import time
import platform
"""
对指定数据库所有冗余数据进行清理
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
    print(f'找不到主机：')



def restart_mongodb():
    """
    检查服务, 并重启, 只能操作本机
    """

    def get_pid(program_name):
        # macos 系统中，使用psutil.process_iter()遍历系统中所有运行的进程
        for process in psutil.process_iter(['name', 'pid']):
            if process.info['name'] == program_name:
                return process.info['pid']
        return None

    if platform.system() == 'Windows':
        print(f'即将重启 mongodb 服务')
        time.sleep(60)
        stop_command = f'net stop MongoDB'
        subprocess.call(stop_command, shell=True)  # 停止MongoDB服务

        time.sleep(30)
        start_command = f'net start MongoDB'
        subprocess.call(start_command, shell=True)  # 启动MongoDB服务
        time.sleep(30)

    elif platform.system() == 'Darwin':
        print(f'即将重启 mongodb 服务')
        time.sleep(60)
        result = get_pid('mongod')  # 获取进程号
        if result:  # 有 pid, 重启服务
            command = f'kill {result}'
            subprocess.call(command, shell=True)
            time.sleep(10)
            command = f'mongod --config /usr/local/mongodb/mongod.conf'
            subprocess.call(command, shell=True)
            # print('已重启服务')
        else:  # 没有启动, 则启动服务
            command = f'mongod --config /usr/local/mongodb/mongod.conf'
            subprocess.call(command, shell=True)

    elif platform.system() == 'Linux':
        print(f'即将重启 mongodb 服务')
        time.sleep(60)
        command = f'service mongod restart'
        subprocess.call(command, shell=True)


def op_data(db_name_lists, days: int = 63, is_mongo=True, is_mysql=True):
    # Mysql
    if is_mysql:
        s = mysql.OptimizeDatas(username=username, password=password, host=host, port=port)
        s.db_name_lists = db_name_lists
        s.days = days
        s.optimize_list()


if __name__ == '__main__':
    op_data(db_name_lists=['聚合数据'], days=10, is_mongo=True, is_mysql=True)
