# -*- coding: UTF-8 –*-
import platform
import getpass

"""
专门用来设置 support 文件夹路径
support 文件夹包含很多配置类文件，是程序必不可少的依赖
"""
class SetSupport:
    def __init__(self, dirname):
        self.dirname = dirname
        if platform.system() == 'Windows':
            self.dirname = f'C:\\同步空间\\BaiduSyncdisk\\自动0备份\\py\\数据更新\\support'
        elif platform.system() == 'Darwin':
            self.dirname = f'/Users/{getpass.getuser()}/数据中心/自动0备份/py/数据更新/support'
        else:
            self.dirname = '数据中心/数据更新/support'  # 没有用可以删


if __name__ == '__main__':
    s = SetSupport(dirname='support').dirname
    print(s)
