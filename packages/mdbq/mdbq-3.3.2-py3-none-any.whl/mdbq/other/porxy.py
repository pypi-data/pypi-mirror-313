import requests
import kdl
import warnings
import os
import requests
import datetime
import re
import time
import socket
warnings.filterwarnings('ignore')
"""
需要传入 订单的 secret_id 和 secret_key
"""


class MyProxy(object):

    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.cookie_path = 'cookies'
        if not os.path.exists(self.cookie_path):
            os.mkdir(self.cookie_path)

    def get_proxy(self):
        """
        从代理网站获取代理ip， 默认参数是文件位置，不需要修改
        """
        secret_id = self.secret_id
        secret_key = self.secret_key
        cookie_path = self.cookie_path
        headers = {
            "User-Agent": 'Mozilla/5.0'
        }
        auth = kdl.Auth(secret_id=secret_id, secret_key=secret_key)
        client = kdl.Client(auth)

        def ip_address():
            try:
                _response = requests.get("https://api.ipify.org/?format=json")
                _ip = _response.json()["ip"]
            except:
                _ip = ''
            return str(_ip)

        myip_path = f'{cookie_path}/本机ip_{socket.gethostname()}.txt'  # 将本机地址保存本地, 下次直接使用, 避免获取失败
        if os.path.exists(myip_path):
            file_timestamp = os.path.getmtime(myip_path)
            file_date = datetime.datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d')
            today_date = datetime.datetime.today().strftime('%Y-%m-%d')
            if file_date == today_date:
                with open(myip_path) as m:
                    my_ip = m.read().strip()
            else:
                my_ip = ip_address()
                with open(f'{cookie_path}/本机ip_{socket.gethostname()}.txt', 'w') as f:
                    f.write(my_ip)
        else:
            my_ip = ip_address()
            with open(f'{cookie_path}/本机ip_{socket.gethostname()}.txt', 'w') as f:
                f.write(my_ip)
        try:
            ip_whitelist = client.get_ip_whitelist()  # 检查ip白名单, 如果这句报错，就直接设置白名单
            if my_ip not in ip_whitelist:
                ip_whitelist.append(my_ip)
                client.set_ip_whitelist(ip_whitelist)  # 添加本机到白名单
        except Exception as e:
            print(e)
            client.set_ip_whitelist(my_ip)  # 设置本机到白名单，会清空其他ip

        if not os.path.isfile(f'{cookie_path}/secret_token_{socket.gethostname()}.txt'):  # 如果本地没有密钥令牌则创建
            secret_token = client.get_secret_token()
            with open(f'{cookie_path}/secret_token_{socket.gethostname()}.txt', 'w') as f:
                f.write(secret_token)
        else:
            with open(f'{cookie_path}/secret_token_{socket.gethostname()}.txt', 'r') as f:
                secret_token = f.read()
        data = f'secret_id={secret_id}&secret_token={secret_token}'  # 检查密钥令牌的有效时长
        token_expire = requests.post(
            'https://dev.kdlapi.com/api/check_secret_token',
            data, headers=headers).json()['data']['expire']
        if token_expire < 300:  # token_expire 密钥令牌距离过期的剩余时长（单位：秒），不足5分钟则重新创建令牌
            secret_token = client.get_secret_token()
            with open(f'{cookie_path}/secret_token_{socket.gethostname()}.txt', 'w') as f:
                f.write(secret_token)
        # api地址
        proxy_url = (f'https://dev.kdlapi.com/api/getdps/?'
                     f'secret_id={secret_id}'
                     f'&signature={secret_token}'
                     f'&num=1&pt=1&format=text&sep=1&f_loc=1&f_citycode=1&area=440100')
        # expire_time = client.get_order_expire_time()  # 账户有效期
        _proxy = requests.get(proxy_url, headers=headers).text  # 通过api地址获取代理ip
        ip_times = client.get_dps_valid_time(proxy=_proxy).values()  # ip有效时间
        for t in ip_times:
            if str(t) != '0':
                ip_times = t
        balance = client.get_ip_balance(sign_type='hmacsha1')  # 可用ip余额
        d_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_proxy = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', _proxy)[0]
        city_proxy = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+,([\u4e00-\u9fa5]+),', _proxy)[0]
        ip_port = ip_proxy.split(':')
        content = (f'{d_time} 中转IP：{ip_port[0]}, '
                   f'端口：{ip_port[1]}, '
                   f'出口地址：{city_proxy}, '
                   f'ip时长：{ip_times}秒, '
                   f'可用ip余额：{balance}, '
                   )
        # print(content)
        with open(f'{cookie_path}/代理ip地址.txt', 'a', encoding='utf-8') as f:
            f.write(content)
        return ip_proxy


if __name__ == '__main__':
    cookie_path = 'cookies'
