# -*- coding: UTF-8 –*-
import platform
import getpass
import configparser
import os
from urllib import parse
from mdbq.config import set_support
"""
文件被 copysh.py / all-datas.py  调用, update_config 函数
更新完成后修改 conf 中值为 True
"""


class UpdateConf:
    """
    读取配置文件信息
    """
    def __init__(self):
        self.path = set_support.SetSupport(dirname='support').dirname
        self.section = 'database'  # 默认 文件头标记
        self.filename = None
        self.conf_file = None
        self.config = None

    def read_txt(self, filename, option=None):
        self.filename = filename
        self.conf_file = os.path.join(self.path, self.filename)
        if not os.path.exists(self.conf_file):
            print(f'缺少配置文件: {self.conf_file}')
            return
        with open(self.conf_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            content = [item.strip() for item in content if not item.strip().startswith('#') and not item.strip().startswith('[')]
            pbix_list = [item for item in content if item]
        return pbix_list  # ['推广数据.pbix', '市场数据新.pbix']

    def read_conf(self, filename, option=None):
        self.filename = filename
        self.conf_file = os.path.join(self.path, self.filename)
        if not os.path.exists(self.conf_file):
            print(f'缺少配置文件: {self.conf_file}')
            return
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file, 'UTF-8')
        if not option:
            results = []
            for option in self.config.options(self.section):
                results.append({option: self.config.get(self.section, option)})
            return results
        else:
            if option not in self.config.options(self.section):
                print(f'不存在的配置项: {option}，文件: {self.conf_file}')
            else:
                return self.config.get(self.section, option)

    def update_config(self, filename, option, new_value):
        """
        更新配置文件
        copysh.py / all-datas.py 调用
        """
        self.filename = filename
        self.conf_file = os.path.join(self.path, self.filename)
        with open(self.conf_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        config = configparser.ConfigParser(allow_no_value=True)  # 读取配置（不包括注释和空白行）
        config.read_string(''.join(line for line in lines if not line.strip().startswith('#') and line.strip()))
        in_section = False  # 标记是否在当前section内

        with open(self.conf_file, 'w', encoding='utf-8') as file:  # 写入更新后的配置文件
            for line in lines:
                if line.strip().startswith('[') and line.strip().endswith(']'):  # 检查是否是section的开始
                    section_name = line.strip()[1:-1]
                    if section_name == self.section:
                        in_section = True
                    file.write(line)
                    continue
                if in_section and '=' in line:  # 如果在section内，检查是否是配置项
                    option_name, _, _ = line.strip().partition('=')
                    if option_name.strip() == option:
                        file.write(f"{option} = {new_value}\n")  # 更新配置项
                        continue
                file.write(line)  # 如果不是配置项或不在section内，则保留原样（包括注释和空白行）

            if not config.has_option(self.section, option):  # 如果配置项没有在当前section中找到，则添加它
                for i, line in enumerate(lines):  # 假设我们要在section的末尾添加配置项
                    if line.strip().startswith(f'[{self.section}]'):
                        file.write(f"{option} = {new_value}\n")  # 写入配置项到section之后
                        break
                else:
                    # 如果section不存在，则在文件末尾添加新的section和配置项
                    file.write(f"\n[{self.section}]\n{option} = {new_value}\n")


def main():
    pass


if __name__ == '__main__':
    w = UpdateConf()
    # w.update_config(filename='.copysh_conf', option='ch_record', new_value='false')
    res = w.read_txt(filename='tb_list.txt')
    print(res)
