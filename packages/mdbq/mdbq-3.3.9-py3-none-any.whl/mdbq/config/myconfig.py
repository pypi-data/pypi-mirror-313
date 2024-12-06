# -*- coding: UTF-8 –*-
import os
import json
from mdbq.config import set_support



def main():
    support_path = set_support.SetSupport(dirname='support').dirname
    file = os.path.join(support_path, 'my_config.txt')
    if not os.path.isfile(file):
        print(f'缺少配置文件，无法读取配置文件： {file}')
        return
    with open(file, 'r', encoding='utf-8') as f:
        config_datas = json.load(f)
        return config_datas


def write_back(datas):
    """ 将数据写回本地 """
    support_path = set_support.SetSupport(dirname='support').dirname
    file = os.path.join(support_path, 'my_config.txt')
    with open(file, 'w+', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, sort_keys=False, indent=4)



if __name__ == '__main__':
    d = main()
    print(d)
