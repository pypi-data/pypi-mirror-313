# -*- coding: UTF-8 –*-
import os
import platform
import warnings
import getpass
import sys
import configparser
import datetime
import shutil
import time
import re
import socket
from mdbq.bdup import bdup
from mdbq.aggregation import query_data
from mdbq.aggregation import optimize_data
from mdbq.config import set_support
from mdbq.config import myconfig
from mdbq.mysql import mysql
from mdbq.clean import clean_upload
warnings.filterwarnings('ignore')


if platform.system() == 'Windows':
    # windows版本
    from mdbq.pbix import refresh_all
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

upload_path = os.path.join(D_PATH, '数据上传中心')  # 此目录位于下载文件夹，将统一上传百度云备份
source_path = os.path.join(Data_Path, '原始文件3')  # 此目录保存下载并清洗过的文件，作为数据库备份
if not os.path.exists(upload_path):  # 数据中心根目录
    os.makedirs(upload_path)
if not os.path.exists(Data_Path):  # 数据中心根目录
    os.makedirs(Data_Path)
if not os.path.exists(source_path):  # 原始文件
    os.makedirs(source_path)


class TbFiles:
    """
    用于在公司台式机中 定时同步pandas数据源文件到共享
    """
    def __init__(self):

        support_path = set_support.SetSupport(dirname='support').dirname

        self.my_conf = os.path.join(support_path, '.copysh_conf')
        self.path1 = os.path.join(support_path, 'tb_list.txt')
        self.path2 = os.path.join(support_path, 'cp_list.txt')
        self.d_path = None
        self.data_path = None
        self.share_path = None
        self.before_max_time = []
        self.sleep_minutes = 30
        self.tomorrow = datetime.date.today()

    def check_change(self):
        """ 检查 source_path 的所有文件修改日期, 函数返回最新修改日期 """
        source_path = os.path.join(self.data_path, 'pandas数据源')
        if not os.path.exists(source_path):
            return
        results = []
        for root, dirs, files in os.walk(source_path, topdown=False):
            for name in files:
                if '~$' in name or 'baiduyun' in name or name.startswith('.') or 'Icon' in name or 'xunlei' in name:
                    continue  # 排除这些文件的变动
                # stat_info = os.path.getmtime(os.path.join(root, name))
                _c = os.stat(os.path.join(root, name)).st_mtime  # 读取文件的元信息 >>>文件修改时间
                c_time = datetime.datetime.fromtimestamp(_c)  # 格式化修改时间
                results.append(c_time)
        return max(results).strftime('%Y%m%d%H%M%S')

    def check_conf(self):
        if not os.path.isfile(self.my_conf):
            self.set_conf()  # 添加配置文件
            print('因缺少配置文件, 已自动初始化')
        config = configparser.ConfigParser()  # 初始化configparser类
        try:
            config.read(self.my_conf, 'UTF-8')
            self.d_path = config.get('database', 'd_path')
            self.data_path = config.get('database', 'data_path')
            self.share_path = config.get('database', 'share_path')
            if self.d_path is None or self.data_path is None or self.share_path is None:
                self.set_conf()
                print('配置文件部分值不完整, 已自动初始化')
            if not os.path.exists(self.d_path) or not os.path.exists(self.data_path) or not os.path.exists(self.share_path):
                self.set_conf()
                print('配置文件异常(可能跨系统), 已自动初始化')
        except Exception as e:
            print(e)
            print('配置文件部分值缺失, 已自动初始化')
            self.set_conf()
        sys.path.append(self.share_path)

    def set_conf(self):
        if platform.system() == 'Windows':
            self.d_path = os.path.join('C:\\Users', getpass.getuser(), 'Downloads')
            self.data_path = os.path.join('C:\\同步空间', 'BaiduSyncdisk')
            self.share_path = os.path.join('\\\\192.168.1.198', '时尚事业部\\01.运营部\\天猫报表')  # 共享文件根目录
        elif platform.system() == 'Darwin':
            self.d_path = os.path.join('/Users', getpass.getuser(), 'Downloads')
            self.data_path = os.path.join('/Users', getpass.getuser(), '数据中心')
            self.share_path = os.path.join('/Volumes/时尚事业部/01.运营部/天猫报表')  # 共享文件根目录
        else:
            self.d_path = 'Downloads'
            self.data_path = os.path.join(getpass.getuser(), '数据中心')
            self.share_path = os.path.join('/Volumes/时尚事业部/01.运营部/天猫报表')  # 共享文件根目录

        if not os.path.exists(self.share_path):
            self.share_path = re.sub('时尚事业部', '时尚事业部-1', self.share_path)

        with open(self.my_conf, 'w+', encoding='utf-8') as f:
            f.write('[database]\n')
            f.write(f'# 配置文件\n')
            f.write('# 下载目录\n')
            f.write(f'd_path = {self.d_path}\n\n')
            f.write('# 数据中心目录\n')
            f.write(f'data_path = {self.data_path}\n\n')
            f.write('# 共享目录\n')
            f.write(f'share_path = {self.share_path}\n\n')
            f.write('# 公司台式机中，用于触发下载百度云文件，更新至本机数据库\n')
            f.write(f'ch_record = False\n\n')
        print('目录初始化!')

    def tb_file(self):

        self.check_conf()  # 检查配置文件

        now_max_time = self.check_change()
        if now_max_time in  self.before_max_time:
            return  # 不更新
        else:
            self.before_max_time = []  # 重置变量，以免越来越占内存
            self.before_max_time.append(now_max_time)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        res = self.check_upload_mysql()
        if not res:
            print(f'检测到源文件修改, 但今日已经同步过, 不再同步')
            return
        print(f'{now}pandas数据源文件修改, 触发同步 ({self.sleep_minutes}分钟后开始)')

        if not os.path.exists(self.data_path):
            print(f'{self.data_path}: 本地目录不存在或配置文件异常, 无法同步此目录')
            return None
        if not os.path.exists(self.share_path):
            print(f'{self.share_path}: 本机未连接共享或配置文件异常, 无法同步')
            return None

        time.sleep(self.sleep_minutes*60)  # 开始同步前休眠时间
        recent_time = 48  # 同步近N小时内更新过的文件，单位：小时
        tb_list = []
        pd_list = []
        try:
            with open(self.path1, 'r', encoding='utf-8') as f:
                content = f.readlines()
                content = [item.strip() for item in content if not item.strip().startswith('#')]
                tb_list = [item for item in content if item]

            with open(self.path2, 'r', encoding='utf-8') as f:
                content = f.readlines()
                content = [item.strip() for item in content if not item.strip().startswith('#')]
                pd_list = [item for item in content if item]
        except Exception as e:
            print(e)

        source_path = os.path.join(self.data_path, 'pandas数据源')  # \BaiduSyncdisk\pandas数据源
        target_path = os.path.join(self.share_path, 'pandas数据源')  # \01.运营部\天猫报表\pandas数据源

        if not os.path.exists(target_path):  # 检查共享主目录,创建目录
            os.makedirs(target_path, exist_ok=True)

        # 删除共享的副本
        file_list = os.listdir(self.share_path)
        for file_1 in file_list:
            if '副本_' in file_1 or 'con' in file_1:  # or '.DS' in file_1
                try:
                    os.remove(os.path.join(self.share_path, file_1))
                    print(f'移除: {os.path.join(self.share_path, file_1)}')
                except Exception as e:
                    print(e)
                    print(f'移除失败：{os.path.join(self.share_path, file_1)}')
        file_list2 = os.listdir(target_path)  # 删除乱七八糟的临时文件
        for file_1 in file_list2:
            if '.DS' in file_1 or 'con' in file_1:
                try:
                    os.remove(os.path.join(target_path, file_1))
                    print(f'移除: {os.path.join(target_path, file_1)}')
                except Exception as e:
                    print(e)

        # 删除 run_py的 副本
        del_p = os.path.join(self.data_path, '自动0备份', 'py', '数据更新', 'run_py')
        for file_1 in os.listdir(del_p):
            if '副本_' in file_1:
                try:
                    os.remove(os.path.join(del_p, file_1))
                    print(f'移除: {os.path.join(del_p, file_1)}')
                except Exception as e:
                    print(e)
                    print(f'移除失败：{os.path.join(del_p, file_1)}')

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now} 正在同步文件...')
        # 复制 run_py的文件到共享
        for file_1 in tb_list:
            s = os.path.join(del_p, file_1)
            t = os.path.join(self.share_path, file_1)
            try:
                shutil.copy2(s, t)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
                print(f'{now}复制: {s}')
            except Exception as e:
                print(e)
                s1 = os.path.join(del_p, f'副本_{file_1}')
                t1 = os.path.join(self.share_path, f'副本_{file_1}')
                shutil.copy2(s, s1)  # 创建副本
                shutil.copy2(s1, t1)  # 复制副本到共享
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
                print(f'{now}已创建副本 -->> {s1}')

        # 同步 pandas 文件到共享
        now_time = time.time()
        for filenames in pd_list:
            src = os.path.join(source_path, filenames)  # 原位置，可能是文件或文件夹
            dst = os.path.join(target_path, filenames)  # 目标位置，可能是文件或文件夹
            if os.path.isdir(src):  # 如果是文件夹
                for root, dirs, files in os.walk(src, topdown=False):
                    for name in files:
                        if '~$' in name or 'DS_Store' in name:
                            continue
                        if name.endswith('csv') or name.endswith('xlsx') or name.endswith('pbix') or name.endswith(
                                'xls'):
                            new_src = os.path.join(root, name)
                            # share_path = dst + '\\' + new_src.split(src)[1]  # 拼接目标路径
                            share_path = os.path.join(f'{dst}{new_src.split(src)[1]}')  # 拼接目标路径
                            ls_paths = os.path.dirname(os.path.abspath(share_path))  # 获取上级目录，用来创建
                            if not os.path.exists(ls_paths):  # 目录不存在则创建
                                os.makedirs(ls_paths, exist_ok=True)
                            c_stat = os.stat(new_src).st_mtime  # 读取文件的元信息 >>>文件修改时间
                            if now_time - c_stat < recent_time * 3600:  # 仅同步近期更新的文件
                                # res_name = os.path.basename(new_src)
                                try:
                                    shutil.copy2(new_src, share_path)
                                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
                                    print(f'{now}复制文件: {new_src}')
                                except Exception as e:
                                    print(e)
            elif os.path.isfile(src) and 'DS_Store' not in src:  # 如果是文件
                if src.endswith('csv') or src.endswith('xlsx') or src.endswith('pbix') or src.endswith('xls'):
                    c_stat = os.stat(src).st_mtime  # 读取文件的元信息 >>>文件修改时间
                    if now_time - c_stat < recent_time * 3600:
                        ls_paths = os.path.dirname(os.path.abspath(src))  # 获取上级目录，用来创建
                        if not os.path.exists(ls_paths):  # 目录不存在则创建
                            os.makedirs(ls_paths, exist_ok=True)
                        # new_name = os.path.basename(src)
                        try:
                            shutil.copy2(src, dst)
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
                            print(f'{now}复制文件: {src}')
                        except Exception as e:
                            print(e)
            else:
                print(f'{src} 所需同步的文件不存在，请检查：pd_list参数')

        # 刷新共享位置的指定文件/文件夹
        if platform.system() == 'Windows':
            excel_path = os.path.join(self.share_path, 'EXCEL报表')
            files = os.listdir(excel_path)
            files = [f'{excel_path}\\{item}' for item in files if item.endswith('.xlsx') or item.endswith('.xls')]
            r = refresh_all.RefreshAll()
            for file in files:
                if '~' in file or 'DS_Store' in file or 'baidu' in file or 'xunlei' in file:
                    continue
                if file.endswith('.xlsx') or file.endswith('.xls'):
                    r.refresh_excel(file=file)
                time.sleep(5)

            # 临时加的
            # excel_file = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新\\0-WLM_运营周报-1012输出.xlsx'
            dir_files = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新'
            files = os.listdir(dir_files)
            for file in files:
                if file.endswith('.xlsx') and file.startswith('0-WLM_运营周报') and '~' not in file and 'baidu' not in file:
                    excel_file = os.path.join(dir_files, file)
                    r.refresh_excel(file=excel_file)

        self.before_max_time = self.check_change()  # 重置值, 避免重复同步

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now} 同步完成！')

    def refresh_excel(self):
        # 刷新共享位置的指定文件/文件夹
        if platform.system() == 'Windows' and socket.gethostname() == 'company':
            excel_path = os.path.join(Share_Path, 'EXCEL报表')
            files = os.listdir(excel_path)
            files = [f'{excel_path}\\{item}' for item in files if item.endswith('.xlsx') or item.endswith('.xls')]
            r = refresh_all.RefreshAll()
            for file in files:
                if '~' in file or 'DS_Store' in file or 'baidu' in file or 'xunlei' in file:
                    continue
                if file.endswith('.xlsx') or file.endswith('.xls'):
                    r.refresh_excel(file=file)
                time.sleep(5)

            # 临时加的
            # excel_file = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新\\0-WLM_运营周报-1012输出.xlsx'
            dir_files = f'\\\\192.168.1.198\\时尚事业部\\01.运营部\\0-电商周报-每周五更新'
            files = os.listdir(dir_files)
            for file in files:
                if file.endswith('.xlsx') and file.startswith(
                        '0-WLM_运营周报') and '~' not in file and 'baidu' not in file:
                    excel_file = os.path.join(dir_files, file)
                    r.refresh_excel(file=excel_file)

    def check_upload_mysql(self):
        # 每天只更新一次
        today = datetime.date.today()
        if today == self.tomorrow:
            self.tomorrow = today + datetime.timedelta(days=1)
            return True
        else:
            return False


def op_data(days: int =100):

    # 清理数据库， 除了 聚合数据
    if socket.gethostname() == 'company':  # 公司台式机自身运行
        # 清理所有非聚合数据的库
        optimize_data.op_data(
            db_name_lists=[
                '京东数据2',
                '属性设置3',
                '推广数据2',
                '推广数据_淘宝店',
                '爱库存2',
                '生意参谋3',
                '生意经3',
                # '聚合数据',
                '达摩盘3',
            ],
            days=days,
        )

        # 数据聚合
        query_data.data_aggregation(service_databases=[{'company': 'mysql'}], months=3,)
        time.sleep(60)

        # 清理聚合数据
        optimize_data.op_data(db_name_lists=['聚合数据'], days=3650, )


def main():
    # if platform.system() != 'Windows':
    #     print(f'只可以在 windows 运行')
    #     return
    t = TbFiles()
    while True:
        system = platform.system()  # 本机系统
        host_name = socket.gethostname()  # 本机名
        conf = myconfig.main()
        data = conf[system][host_name]
        is_download = data['is_download']  # 读取配置, 如果是 Ture 则执行更新

        if is_download:
            bd_remoto_path = f'windows2/{str(datetime.date.today().strftime("%Y-%m"))}/{str(datetime.date.today())}'
            b = bdup.BaiDu()
            # 1. 从百度云下载文件
            b.download_dir(local_path=upload_path, remote_path=bd_remoto_path)

            clean_upload.main(
                is_mysql=True,  # 调试时加，False: 不进行后续的聚合数据及清理
                is_company=True,  # 公司电脑不需要移动文件到原始文件
            )

            #
            # # 3. 数据清理和聚合
            # op_data(days=100)

            if socket.gethostname() == 'company':
                # 此处不可以使用 data 更新，要使用具体键值，否则数据有覆盖
                conf['Windows']['company'].update(
                    {
                        'is_download': False  # 更新完成，下次需 all-datas.py 修改或者手动修改
                    }
                )
                # print(conf)
                myconfig.write_back(datas=conf)  # 写回文件生效
            elif socket.gethostname() == 'xigua1':
                conf['Windows']['xigua1'].update(
                    {
                        'is_download': False  # 更新完成，下次需 all-datas.py 修改或者手动修改
                    }
                )
                # print(conf)
                myconfig.write_back(datas=conf)  # 写回文件生效
            elif socket.gethostname() == 'xigua_lx':
                conf['Windows']['xigua_lx'].update(
                    {
                        'is_download': False  # 更新完成，下次需 all-datas.py 修改或者手动修改
                    }
                )
                # print(conf)
                myconfig.write_back(datas=conf)  # 写回文件生效
            elif socket.gethostname() == 'Mac2.local':
                conf['Darwin']['Mac2.local'].update(
                    {
                        'is_download': False  # 更新完成，下次需 all-datas.py 修改或者手动修改
                    }
                )
                # print(conf)
                myconfig.write_back(datas=conf)  # 写回文件生效
            elif socket.gethostname() == 'MacBookPro':
                conf['Darwin']['MacBookPro'].update(
                    {
                        'is_download': False  # 更新完成，下次需 all-datas.py 修改或者手动修改
                    }
                )
                # print(conf)
                myconfig.write_back(datas=conf)  # 写回文件生效

            if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
                t.refresh_excel()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
            print(f'{now}数据完成！')

        # t.sleep_minutes = 5  # 同步前休眠时间
        # if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
        #     t.tb_file()
        time.sleep(600)  # 检测间隔


if __name__ == '__main__':
    main()
