import ctypes
import hashlib
import json
import math
import os
import random
import re
import socket
import struct
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor  # 线程次
from datetime import datetime, timedelta
from urllib.parse import urlparse

import execjs  # pip install PyExecJS
import memcache  # pip3 install python-memcached
import pymysql
import redis
import requests
from django.http import JsonResponse
from elasticsearch import Elasticsearch  # ES
from lxml import etree  # 解析提取的库
from pypinyin import pinyin, Style  # 汉字转拼音
# 腾讯云cos  pip install -U cos-python-sdk-v5
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

"""
    配置文件
        所有配置在这个地方读取 
        使用内存缓存机制 memcache
        没有读取到内存中的配置，这个包相当于不能用
    pip3 cache purge
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Fr1997v011==2.4.4

    pip3 install --upgrade Fr1997v011
    pip3 install redis
    pip3 install pymysql
    pip3 install elasticsearch
    pip3 install python-memcached
    pip3 install PyExecJS
    pip3 install -U cos-python-sdk-v5
    pip3 install pypinyin
    pip3 install django
    pip3 install lxml
    
    pip38 install --upgrade Fr1997v011
    pip38 install redis
    pip38 install pymysql
    pip38 install elasticsearch
    pip38 install python-memcached
    pip38 install PyExecJS
    pip38 install -U cos-python-sdk-v5
    pip38 install pypinyin
    pip38 install django
    pip38 install lxml
"""
false = False
true = True
null = None
undefined = "undefined"
F_keyword = 'keyword'


# 存储内存数据
def cache_set(key, data, save_time=None):
    mc = memcache.Client(['127.0.0.1:11211'], debug=True)
    if save_time:
        mc.set(key=key, val=data, time=save_time)
    else:
        mc.set(key=key, val=data)  # 永久存储


# 获取内存数据
def cache_get(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=True)
    return mc.get(key)


config_dict = cache_get("my_config_dict")
if not config_dict:
    sys.exit(0)


# 抖音加密参数破解
class ZhihuSign(object):
    local_48 = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
    local_55 = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE"
    h = {
        "zk": [1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157,
               1933479194, -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428,
               -2029270069, 2035090028, -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135,
               1321810770, 456816404, -1391643889, -229302305, 330002838, -788960546, 363569021, -1947871109],
        "zb": [20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93, 252,
               205, 90, 79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80, 189,
               71, 191, 97, 84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22, 255,
               94, 238, 151, 85, 77, 124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146, 162,
               62, 224, 218, 196, 229, 1, 192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117,
               228, 215, 203, 53, 239, 251, 127, 81, 11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122,
               145, 106, 118, 74, 190, 29, 16, 174, 5, 177, 129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68,
               207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244, 155, 51, 236, 200, 233, 58, 61, 47, 100, 137,
               185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105, 24, 212, 78, 173, 45, 0, 116, 226, 119,
               136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21, 130, 98, 241, 40, 154, 66, 184, 49,
               181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201, 164, 89, 216, 202, 220, 50,
               221, 152, 140, 33, 235, 214],
        "zm": [120, 50, 98, 101, 99, 98, 119, 100, 103, 107, 99, 119, 97, 99, 110, 111]
    }

    @staticmethod
    def pad(data_to_pad):
        padding_len = 16 - len(data_to_pad) % 16
        padding = chr(padding_len).encode() * padding_len
        return data_to_pad + padding

    @staticmethod
    def unpad(padded_data):
        padding_len = padded_data[-1]
        return padded_data[:-padding_len]

    @staticmethod
    def left_shift(x, y):
        x, y = ctypes.c_int32(x).value, y % 32
        return ctypes.c_int32(x << y).value

    @staticmethod
    def Unsigned_right_shift(x, y):
        x, y = ctypes.c_uint32(x).value, y % 32
        return ctypes.c_uint32(x >> y).value

    @classmethod
    def Q(cls, e, t):
        return cls.left_shift((4294967295 & e), t) | cls.Unsigned_right_shift(e, 32 - t)

    @classmethod
    def G(cls, e):
        t = list(struct.pack(">i", e))
        n = [cls.h['zb'][255 & t[0]], cls.h['zb'][255 & t[1]], cls.h['zb'][255 & t[2]], cls.h['zb'][255 & t[3]]]
        r = struct.unpack(">i", bytes(n))[0]
        return r ^ cls.Q(r, 2) ^ cls.Q(r, 10) ^ cls.Q(r, 18) ^ cls.Q(r, 24)

    @classmethod
    def g_r(cls, e):
        n = list(struct.unpack(">iiii", bytes(e)))
        [n.append(n[r] ^ cls.G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ cls.h['zk'][r])) for r in range(32)]
        return list(
            struct.pack(">i", n[35]) + struct.pack(">i", n[34]) + struct.pack(">i", n[33]) + struct.pack(">i", n[32]))

    @classmethod
    def re_g_r(cls, e):
        n = [0] * 32 + list(struct.unpack(">iiii", bytes(e)))[::-1]
        for r in range(31, -1, -1):
            n[r] = cls.G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ cls.h['zk'][r]) ^ n[r + 4]
        return list(
            struct.pack(">i", n[0]) + struct.pack(">i", n[1]) + struct.pack(">i", n[2]) + struct.pack(">i", n[3]))

    @classmethod
    def g_x(cls, e, t):
        n = []
        i = 0
        for _ in range(len(e), 0, -16):
            o = e[16 * i: 16 * (i + 1)]
            a = [o[c] ^ t[c] for c in range(16)]
            t = cls.g_r(a)
            n += t
            i += 1
        return n

    @classmethod
    def re_g_x(cls, e, t):
        n = []
        i = 0
        for _ in range(len(e), 0, -16):
            o = e[16 * i: 16 * (i + 1)]
            a = cls.re_g_r(o)
            t = [a[c] ^ t[c] for c in range(16)]
            n += t
            t = o
            i += 1
        return n

    @classmethod
    def b64encode(cls, md5_bytes: bytes, device: int = 0, seed: int = 63) -> str:
        local_50 = bytes([seed, device]) + md5_bytes  # 随机数  0 是环境检测通过
        local_50 = cls.pad(bytes(local_50))
        local_34 = local_50[:16]
        local_35 = [local_34[local_11] ^ cls.local_48[local_11] ^ 42 for local_11 in range(16)]
        local_36 = cls.g_r(local_35)
        local_38 = local_50[16:]
        local_39 = cls.g_x(local_38, local_36)
        local_53 = local_36 + local_39
        local_56 = 0
        local_57 = ""
        for local_13 in range(len(local_53) - 1, 0, -3):
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_53[local_13] ^ cls.Unsigned_right_shift(58, local_58) & 255
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 1] ^ cls.Unsigned_right_shift(58, local_58) & 255) << 8
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 2] ^ cls.Unsigned_right_shift(58, local_58) & 255) << 16
            local_57 = local_57 + cls.local_55[local_59 & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 6) & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 12) & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 18) & 63]
        return local_57

    @classmethod
    def b64decode(cls, x_zse_96: str) -> dict:
        local_56 = 0
        local_57 = []
        for local_13 in range(0, len(x_zse_96), 4):
            local_59 = (cls.local_55.index(x_zse_96[local_13 + 3]) << 18) + (
                    cls.local_55.index(x_zse_96[local_13 + 2]) << 12) + (
                               cls.local_55.index(x_zse_96[local_13 + 1]) << 6) + cls.local_55.index(
                x_zse_96[local_13])
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append((local_59 & 255) ^ cls.Unsigned_right_shift(58, local_58))
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append(((local_59 >> 8) & 255) ^ cls.Unsigned_right_shift(58, local_58))
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append(((local_59 >> 16) & 255) ^ cls.Unsigned_right_shift(58, local_58))
        local_36, local_39 = local_57[-16:][::-1], local_57[:-16][::-1]
        local_38 = cls.re_g_x(local_39, local_36)
        local_35 = cls.re_g_r(local_36)
        local_34 = [local_35[local_11] ^ cls.local_48[local_11] ^ 42 for local_11 in range(16)]
        local_50 = cls.unpad(bytes(local_34 + local_38))
        return {
            'seed': local_50[0],
            'device': local_50[1],
            'md5_bytes': local_50[2:]
        }


# 静态函数 【其它函数集合】
class ModeStatic:
    # 运行计算机判断 【通过判断计算机，方便链接内网，加快数据库访问速度，判断资源位置】
    @staticmethod
    def run_machine():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
        machine_cfg = {
            # win_gx8r9
            'd4:93:90:25:1b:60': {
                'type': 'win_gx8r9',
                'platform': 0
            },

            # win_gx8r9 (2)
            'd4:d8:53:ff:fc:52': {
                'type': 'win_gx8r9',
                'platform': 0
            },

            # 台式
            '38:87:d5:7a:07:5a': {
                'type': '3080',
                'platform': 0
            },

            # esc_tx 高阳的腾讯云
            '52:54:00:55:0b:d4': {
                'type': 'esc_tx',
                'platform': 0
            },

            # esc_jike_pachong1
            '52:54:00:03:18:2c': {
                'type': 'esc_jike_pachong1',
                'platform': 1
            },
        }

        if mac_address in machine_cfg:
            return machine_cfg[mac_address]
        else:
            return {'type': 'other', 'platform': 0}

    # 手机号判断
    @staticmethod
    def phone_num(num):
        num = str(num.strip())
        # 中国联通：130，131，132，155，156，185，186，145，176
        # 中国移动：134, 135 ,136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188
        # 中国电信：133,153,189
        pat_lt = re.compile(r'^1(3[0-2]|45|5[5-6]|8[5-6]|76)\d{8}$')
        pat_yd = re.compile(r'^1(3[4-9]|47|5[0-27-9]|8[2-47-8]|78)\d{8}$')
        pat_dx = re.compile(r'^1(33|53|89)\d{8}$')

        if pat_lt.match(num):
            return f"联通_{pat_lt.match(num).group()}"
        elif pat_yd.match(num):
            return f"移动_{pat_yd.match(num).group()}"
        elif pat_dx.match(num):
            return f"电信_{pat_dx.match(num).group()}"
        else:
            return 0

    # 文本截取手机号  --> dict
    @staticmethod
    def phone_text(text):
        # text 不需要去空白
        phone_dict = {}  # 号码 + 个数

        # 匹配出所有 以1开头 11位的数字
        pat = re.compile(r'1\d{10}')
        res = pat.findall(text)

        # 统计每个好吗 以及个数 判断是否是标准号码 以及 运营商
        for phone in res:
            if phone_dict.get(phone):
                phone_dict[phone] += 1
            else:
                phone_dict[phone] = 1
        return phone_dict

    # user_agent
    @staticmethod
    def get_user_agent(one=False):
        user_agents = config_dict['user_agents']
        if one:
            return random.choice(user_agents)
        else:
            return user_agents

    # Windows合法文件名 转为Windows合法文件名
    @staticmethod
    def title_path(title: str):
        lst = ['\r', '\n', '\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for key in lst:
            title = title.replace(key, '-')
        if len(title) > 60:
            title = title[:60]
        return title.strip()

    # md5
    @staticmethod
    def md5_base(text, salt=None):
        md5 = hashlib.md5()
        if salt:
            md5 = hashlib.md5(salt.encode('utf-8'))
        md5.update(text.encode('utf-8'))
        result = md5.hexdigest()
        return result

    # ua 详情
    @staticmethod
    def ua_info(ua_string):
        from user_agents import parse
        user_agent = parse(ua_string)

        if user_agent.is_pc:
            user_use = '电脑'
        elif user_agent.is_mobile:
            user_use = '手机'
        elif user_agent.is_tablet:
            user_use = '平板'
        else:
            user_use = '其他'

        return {
            'browser': user_agent.browser.family,  # 浏览器
            'user_use': user_use,
            'browser_sys': user_agent.os.family,  # 系统
            'browser_device_brand': user_agent.device.brand,  # '品牌'
            'browser_device_type': user_agent.device.model,  # 'iPhone'
            'browser_all': str(user_agent),  # "iPhone / iOS 5.1 / Mobile Safari 5.1"
        }

    # 图片转base64
    @staticmethod
    def img_md5(pic_path):
        import base64
        # 将本地图片转换为base64编码和md5值
        with open(pic_path, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
            my_md5 = hashlib.md5()
            img_data = base64.b64decode(image_base64)
            my_md5.update(img_data)
            myhash = my_md5.hexdigest()
        return image_base64, myhash

    # cookie解析
    @staticmethod
    def cookies_split(cookie_str: str) -> str:
        # 判断是否为字符串
        if not isinstance(cookie_str, str):
            raise TypeError("cookie_str must be str")

        # 拆分Set-Cookie字符串,避免错误地在expires字段的值中分割字符串。
        cookies_list = re.split(', (?=[a-zA-Z])', cookie_str)

        # 拆分每个Cookie字符串，只获取第一个分段（即key=value部分）
        cookies_list = [cookie.split(';')[0] for cookie in cookies_list]

        # 拼接所有的Cookie
        cookie_str = ";".join(cookies_list)

        return cookie_str

    # 增长率
    @staticmethod
    def add_rate(v_new, v_old):
        if v_new == 0 or v_old == 0:
            rate = 0
        else:
            rate = round((v_new - v_old) / v_old * 100, 2)
        return rate

    # 增长率
    @staticmethod
    def cookie_str_to_cookie_dict(cookie_str: str):
        cookie_blocks = [cookie_block.split("=")
                         for cookie_block in cookie_str.split(";") if cookie_block]
        return {cookie[0].strip(): cookie[1].strip() for cookie in cookie_blocks}

    # 综合表
    @staticmethod
    def ak_name(keyword):
        all_k_table = config_dict['keyword']['关键词综合表']
        base_table = 'all_keyword_v90'
        alias_name = 'other'
        first_py = mode_pro.chinese_to_pinyin(chinese=keyword, ret=3)
        for i in all_k_table:
            if first_py in all_k_table[i]:
                alias_name = i
        return f'{base_table}_{alias_name}'


# requests 封装
class HttpJike(object):

    def __init__(self):
        self.status_code = 500
        self.msg = 'ok'
        self.text = None
        self.json = None
        self.ret_url = None

    # cookie 分隔
    @staticmethod
    def cookie_format(cookie):
        cookie_dict = {}
        c = cookie.split(";")
        for i in c:
            cc = i.split('=')
            if len(cc) > 1:
                cookie_dict[str(cc[0]).strip()] = str(cc[1]).strip()
            else:
                cookie_dict[str(cc[0]).strip()] = ''
        return cookie_dict

    # ip代理 隧道代理
    @staticmethod
    def proxies_choose(p=1, httpx=0):
        # 注意:目前只有 1,2 两个可以使用  httpx特殊请求
        if p is None:
            p = random.randint(1, 2)

        proxy = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['proxy']
        port = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['port']
        acc = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['acc']
        pwd = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['pwd']

        proxies = {
            "http": f"http://{acc}:{pwd}@{proxy}:{port}/",
            "https": f"http://{acc}:{pwd}@{proxy}:{port}/"
        }
        if httpx == 1:
            proxies = {
                "http://": f"http://{acc}:{pwd}@{proxy}:{port}/",
                "https://": f"http://{acc}:{pwd}@{proxy}:{port}/"
            }
        return proxies

    # scrapy 代理选择 数据返回
    @classmethod
    def proxies_choose_dict(cls, p):
        # 注意:目前只有 1,2,3 两个可以使用
        proxies_dict = {
            'proxy': config_dict["proxy"]["tunnel"][f"proxy_{p}"]['proxy'],
            'port': config_dict["proxy"]["tunnel"][f"proxy_{p}"]['port'],
            'acc': config_dict["proxy"]["tunnel"][f"proxy_{p}"]['acc'],
            'pwd': config_dict["proxy"]["tunnel"][f"proxy_{p}"]['pwd']
        }
        return proxies_dict

    # 异步代理 的使用
    @staticmethod
    def aiohttp_proxy():
        ret = []
        ip_tunnel = config_dict['proxy']['tunnel']
        for i in ip_tunnel:
            ret.append({
                'proxy': f'http://{ip_tunnel[i]["proxy"]}:15818',
                'a': ip_tunnel[i]['acc'],
                'p': ip_tunnel[i]['pwd'],
            })
        return ret

    @staticmethod
    def get_headers(headers):
        if headers is None:
            return config_dict['base_headers']
        return headers

    @classmethod
    def get(cls, url, headers=None, proxies=None):
        req = cls()
        try:
            response = requests.get(
                url=url,
                headers=cls.get_headers(headers=headers),
                proxies=proxies
            )
            req.status_code = response.status_code
            req.ret_url = response.url
            req.text = response.text
            req.json = response.json()

            if response.status_code != 200:
                req.msg = '状态码错误'
        except Exception as e:
            req.msg = f'err {e}'
        return req

    @classmethod
    def post(cls, url, headers=None, data=None):
        req = cls()
        try:
            response = requests.post(
                url=url,
                headers=cls.get_headers(headers=headers),
                data=json.dumps(data),
            )
            req.status_code = response.status_code
            req.text = response.text
            req.json = response.json()

            if response.status_code != 200:
                req.msg = '状态码错误'
        except Exception as e:
            req.msg = f'err {e}'
        return req

    # 代理
    @classmethod
    def http_ip(cls, ip):
        proxies = {
            'https': ip,
            'http': ip
        }
        return proxies

    # 返回一个http代理
    @classmethod
    def http_proxy(cls):
        return random.choice(mode_pro.douchacha_ips_mysql()['request_ip'])

    @classmethod
    def params_link(cls, url, params):
        return f"{url}?" f"{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    @classmethod
    def base_headers(cls):
        try:
            return config_dict['base_headers']
        except:
            return {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'}


# 飞书
class Feishu:
    """
        组成：                             app_token        table_id        views
        https://bchje44bsl.feishu.cn/base/XXXXXXXXXXXXXXXX?table=XXXXXXXXX&view=XXXXXXXX
    """

    def __init__(self):
        # 飞书
        self.feishu_base_url = config_dict['feishu']['fs_base_url']
        self.feishu_bot_url = config_dict['feishu']['fs_bot_url']  # 飞书机器人
        self.feishu_token_url = config_dict['feishu']['fs_token_url']  # 飞书token
        self.feishu_app_url = config_dict['feishu']['fs_app_url']  # 飞书app

        # 翻页返回
        self.ret_data_all = []

    # 获取应用token token的过期时间为2小时
    def get_token(self, app_name):
        key = f'feishu_token_{app_name}_v3'
        tenant_access_token = cache_get(key)
        if not tenant_access_token:
            r = requests.post(self.feishu_token_url, data=config_dict['feishu']['apps'][app_name])
            tenant_access_token = r.json()["tenant_access_token"]
            cache_set(key, tenant_access_token, 1800)  # 缓存半小时
        return tenant_access_token

    # 基础请求头
    def base_headers(self, app_name):
        return {
            'Authorization': f"Bearer {self.get_token(app_name)}",
        }

    # 获取 app_token下 所有 table
    def get_all_table(self, app_name, app_token):
        url = f'{mode_feishu.feishu_app_url}{app_token}/tables'
        res = requests.get(url=url, headers=self.base_headers(app_name))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                items = data['items']
                return items
            else:
                print("内容获取失败")
        else:
            print("状态码 错误")

    # 创建 表 table
    def create_new_table(self, app_name, app_token, table_name):
        url = f"{mode_feishu.feishu_app_url}{app_token}/tables"
        data = {
            "table": {
                "name": table_name
            }
        }
        res = requests.post(url=url, headers=self.base_headers(app_name), data=json.dumps(data))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                return 1

    # 删除 表
    def del_table(self, app_name, app_token, table_id):
        url = f"{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}"
        res = requests.delete(url=url, headers=self.base_headers(app_name))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                return 1

    # 表 增加字段
    def create_table_fields_test(self, app_name, app_token, table_id, field_update):
        """
        table管理
            1：多行文本
            2：数字
                整数	"0"
                保留1位小数	"0.0"
                保留2位小数	"0.00"
                保留3位小数	"0.000"
                保留4位小数	"0.0000"
                千分位	"1,000"
                千分位（小数点）	"1,000.00"
                百分比	"%"
                百分比（小数点）	"0.00%"
                人民币	"¥"
                人民币（小数点）	"¥0.00"
                美元	"$"
                美元（小数点）	"$0.00"
            3：单选
            4：多选
            5：日期
                2021/01/30	"yyyy/MM/dd"
                2021/01/30 14:00	"yyyy/MM/dd HH:mm"
                2021-01-30	"yyyy-MM-dd"
                2021-01-30 14:00	"yyyy-MM-dd HH:mm"
                01-30	"MM-dd"
                01/30/2021	"MM/dd/yyyy"
                30/01/2021	"dd/MM/yyyy"
            7：复选框
            11：人员
            15：超链接
            17：附件
            18：关联
            20：公式
            21：双向关联
            1001：创建时间
            1002：最后更新时间
            1003：创建人
            1004：修改人
            1005：自动编号
            13：电话号码
            22：地理位置

            -- 示例
            field_update = [
                {"field_name": '普通文本', "type": 1},  # 添加普通文本
                {"field_name": '数字-整数', "type": 2, "property": {"formatter": "0"}},  # 添加数字 整形
                {"field_name": '数字-浮点', "type": 2, "property": {"formatter": "0.00"}},  # 添加数字 浮点数
                {"field_name": '日期', "type": 5},  # 日期
            ]
            mode_feishu.create_table_fields_test(fapp_name, fapp_token, 'tblJyCmlB0Ly6yvr', field_update)

        """
        url = f'{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/fields'
        for i in field_update:
            res = requests.post(url=url, headers=self.base_headers(app_name), data=json.dumps(i))
            if res.status_code == 200:
                ret_data = res.json()
                code = ret_data.get("code")
                msg = ret_data.get("msg")
                if code == 0 and msg == 'success':
                    print(app_token, "添加字段 成功")
                else:
                    print(app_token, "添加字段 添加失败")
            else:
                print(app_token, "添加字段 状态码错误")

            time.sleep(1)

    # 表 修改字段
    def update_table_field(self, app_name, app_token, table_id, field_id, field_dict):
        url = f"{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/fields/{field_id}"
        requests.put(url=url, headers=self.base_headers(app_name), data=json.dumps(field_dict))

    # 表 修改字段 批量
    def update_table_fields_test(self, app_name, app_token, table_id, field_update):
        """
            field_update = [
                # {"old_field_name": '多行文本', "field_name": '多行文本1', "type": 1},  # 添加普通文本
                {"old_field_name": '多行文本1', "field_name": '测试数据', "type": 2, "property": {"formatter": "0"}},  # 添加数字 整形
            ]
            mode_feishu.update_table_fields_test(app_name, app_token, 'tblJyCmlB0Ly6yvr', field_update)
        """
        # 获取table所有字段
        fields = self.get_table_fields(app_name, app_token, table_id)
        if fields:
            # 整理数据
            fields_dict = {}
            for f in fields:
                fields_dict[f['field_name']] = f['field_id']

            # 获取字段对应的 field_id 并更新
            for i in field_update:
                old_field_name = i['old_field_name']
                field_id = fields_dict.get(old_field_name)
                url = f"{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/fields/{field_id}"
                del i['old_field_name']
                res = requests.put(url=url, headers=self.base_headers(app_name), data=json.dumps(i))
                if res.status_code == 200:
                    ret_data = res.json()
                    code = ret_data.get("code")
                    msg = ret_data.get("msg")
                    if code == 0 and msg == 'success':
                        print(app_token, "修改字段 成功")
                    elif msg == 'DataNotChange':
                        print(app_token, "修改字段 无需修改")
                    else:
                        print(app_token, "修改字段 修改失败")
                else:
                    print(app_token, "修改字段 状态码错误")
                time.sleep(1)

    # 表 创建+修改字段
    def create_table_and_fields(self, app_name, app_token, table_name, dct=0, fields_create=None):
        """
            fields_create = [
            {"field_name": '普1', "type": 1},  # 添加普通文本
            {"field_name": '数字-整数', "type": 2, "property": {"formatter": "0"}},  # 添加数字 整形
            {"field_name": '日期', "type": 5},  # 日期
        ]
        mode_feishu.create_table_and_fields(fapp_name, fapp_token, 'sada', dct=1, fields_create=fields_create)
        """
        # 获取当前应用存在相同表
        all_table = self.get_all_table(app_name, app_token)
        for at in all_table:
            if at['name'] == table_name:
                if dct == 0:
                    print("存在相同表 不创建")
                    return
                else:
                    self.del_table(app_name, app_token, at['table_id'])
                    time.sleep(1)
        # 创建表
        self.create_new_table(app_name, app_token, table_name)

        # 获取字段
        all_table = self.get_all_table(app_name, app_token)
        for at in all_table:
            if at['name'] == table_name:
                table_id = at['table_id']
                fields = self.get_table_fields(app_name, app_token, table_id)
                if fields_create:
                    # 要对第一个字段进行修改
                    self.update_table_field(app_name, app_token, table_id, fields[0]['field_id'], fields_create[0])
                    if fields_create[1:]:
                        self.create_table_fields_test(app_name, app_token, table_id, fields_create[1:])

    # 获取 table 字段 【table有字段，视图没有】
    def get_table_fields(self, app_name, app_token, table_id):
        url = f'{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/fields'
        res = requests.get(url=url, headers=self.base_headers(app_name))
        print(res.text)
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                items = data['items']
                return items
            else:
                print("内容获取失败")
        else:
            print("状态码 错误")

    # 获取 table 视图
    def get_table_views(self, app_name, app_token, table_id):
        url = f'{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/views'
        res = requests.get(url=url, headers=self.base_headers(app_name))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                items = data['items']
                return items
            else:
                print("内容获取失败")
        else:
            print("状态码 错误")

    # 获取view数据
    def get_table_view_info(self, app_name, app_token, table_id, view_id, page_toke=None, ret_all=None):
        """
        每次最多返回500个
        :param app_token:
        :param table_id:
        :return:
        """
        if page_toke:
            url = f'{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/records?view_id={view_id}&page_token={page_toke}'
        else:
            url = f'{mode_feishu.feishu_app_url}{app_token}/tables/{table_id}/records?view_id={view_id}'
        ret_data = {
            'code': 0,
            'total': 0,
            'has_more': False,
            'page_token': "",
            'items': []
        }
        res = requests.get(url=url, headers=self.base_headers(app_name))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                page_token = data.get('page_token')
                has_more = data.get('has_more')
                total = data.get('total')
                items = data.get('items')
                if ret_all == 1:
                    if items:
                        self.ret_data_all += items
                    if has_more:
                        time.sleep(1)
                        print("请求下一页")
                        self.get_table_view_info(app_name, app_token, table_id, view_id, page_toke=page_token)
                else:
                    if items:
                        for index, it in enumerate(items):
                            id_id = it.get("id")
                            record_id = it.get("record_id")
                            fields = it.get("fields")
                            print(index, id_id, record_id, fields)

                    return {
                        'code': 1,
                        'total': total,
                        'has_more': has_more,
                        'page_token': page_token,
                        'items': items
                    }
            else:
                print("内容获取失败")
        else:
            print("状态码 错误")

    # 新增数据 需外部限制500条
    def add_more_view(self, app_name, app_token, table_id, add_data, ret=0):
        records = []
        for i in add_data:
            records.append({'fields': i})
        url = mode_feishu.fs_url(app_token, 'add_more', table_id=table_id)
        data = {
            "records": records
        }
        res = requests.post(url=url, headers=self.base_headers(app_name), data=json.dumps(data))
        if res.status_code == 200:
            data_data = res.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                if ret == 1:
                    return data
                return 1

    # 飞书 机器人推送
    def feishu_send_message(self, text, WEBHOOK_URL=''):
        if WEBHOOK_URL == '':
            WEBHOOK_URL = config_dict['feishu']['fs_url']

        data = {
            "timestamp": int(time.time()),
            "msg_type": "text",
            "content": {"text": text},
        }
        res = HttpJike.post(url=WEBHOOK_URL, data=data)
        if res.status_code == 200:
            print(res.json)

    # 飞书 应用token
    def feishu_get_token(self, app_id, app_secret):
        try:
            post_data = {"app_id": app_id,
                         "app_secret": app_secret}
            res = HttpJike.post(url=self.feishu_token_url, data=post_data)
            if res.status_code == 200:
                tenant_access_token = res.json["tenant_access_token"]
                return tenant_access_token
        except:
            pass

    # 飞书 批量新增
    def feishu_add_more_view(self, app_token, table_id, records, tenant_access_token):
        url = self.fs_url(app_token, 'add_more', table_id=table_id)
        headers = {
            'Authorization': f"Bearer {tenant_access_token}",
            'Content-Type': "application/json; charset=utf-8",
        }
        data = {
            "records": records
        }
        res = HttpJike.post(url=url, headers=headers, data=data)
        if res.status_code == 200:
            data_data = res.json
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                return 1

    # 飞书各种url统一
    def fs_url(self, app_token, mode="", **kwargs):
        base_url = f'{config_dict["feishu"]["fs_app_url"]}{app_token}/'
        if mode == 'add_more':
            table_id = kwargs['table_id']
            return f'{base_url}tables/{table_id}/records/batch_create'
        elif mode == 'tables':
            return f'{base_url}tables'


# 时间
class TimeJike:
    @staticmethod
    def zero_clock(day=0) -> int:
        """
        获取某一天的零点时间戳。

        :param day: 距离今天的天数（正数表示之前的日期，负数表示之后的日期）
        :return: 指定日期的零点时间戳（整数）
        """
        # 获取当前日期时间并去除时分秒，获取当天零点
        target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 计算目标日期零点
        target_date -= timedelta(days=day)

        # 转换为时间戳并返回
        return int(target_date.timestamp())

    @staticmethod
    def today_seconds() -> int:
        """
        获取现在是今天的第多少秒。

        :return: 当前时间距离今天零点的秒数。
        """
        # 获取当前时间
        now = datetime.now()

        # 获取今天零点的时间
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # 计算当前时间与今天零点之间的秒数差
        return int((now - midnight).total_seconds())

    @staticmethod
    def hours_start_time(hours=0) -> int:
        """
        获取指定小时的开始时间戳。

        :param hours: 与当前时间相差的小时数（正数表示过去的小时，负数表示未来的小时）
        :return: 指定小时的开始时间戳（整数）
        """
        # 获取当前时间，并将分钟、秒和微秒置零，得到本小时的开始时间
        current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

        # 计算目标小时的开始时间
        target_hour = current_hour - timedelta(hours=hours)

        # 转换为时间戳并返回
        return int(target_hour.timestamp())

    @staticmethod
    def week(t=None) -> str:
        """
        返回指定时间戳的星期几。

        :param t: 时间戳，默认值为当前时间。
        :return: 周几的中文名称（字符串）。
        """
        if t is None:
            t = int(time.time())

        # 将星期几的数字映射到中文名称
        weekday_map = {
            0: "周日",
            1: "周一",
            2: "周二",
            3: "周三",
            4: "周四",
            5: "周五",
            6: "周六",
        }

        # 获取指定时间戳的星期几
        weekday_number = datetime.fromtimestamp(t).weekday()

        # 返回对应的中文名称
        return weekday_map[weekday_number]

    @staticmethod
    def ymd(t=None) -> str:
        """
        将时间戳转换为日期字符串（格式：YYYYMMDD）。

        :param t: 时间戳，默认为当前时间。
        :return: 格式化的日期字符串。
        """
        if t is None:
            t = datetime.now()
        else:
            t = datetime.fromtimestamp(t)

        return t.strftime("%Y%m%d")

    @staticmethod
    def y_m_d(t=None) -> str:
        """
        将时间戳转换为日期字符串（格式：YYYY-MM-DD）。

        :param t: 时间戳，默认为当前时间。
        :return: 格式化的日期字符串。
        """
        # 使用当前时间作为默认值
        t = datetime.fromtimestamp(t) if t is not None else datetime.now()

        return t.strftime("%Y-%m-%d")

    @staticmethod
    def y_m_d__h_m_s(t=None) -> str:
        """
        将时间戳转换为日期和时间字符串（格式：YYYY-MM-DD HH:MM:SS）。

        :param t: 时间戳，默认为当前时间。
        :return: 格式化的日期和时间字符串。
        """
        # 使用当前时间作为默认值
        t = datetime.fromtimestamp(t) if t is not None else datetime.now()

        return t.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def hour(t=None) -> int:
        """
        获取指定时间戳的小时（24小时制）。

        :param t: 时间戳，默认为当前时间。
        :return: 小时（整数）。
        """
        t = datetime.fromtimestamp(t) if t is not None else datetime.now()
        return t.hour

    @staticmethod
    def minute(t=None) -> int:
        """
        获取指定时间戳的分钟。

        :param t: 时间戳，默认为当前时间。
        :return: 分钟（整数）。
        """
        t = datetime.fromtimestamp(t) if t is not None else datetime.now()
        return t.minute

    @staticmethod
    def hour_minute_seconds(t=None):
        """
        获取指定时间戳的时、分、秒（整数）。

        :param t: 时间戳，默认为当前时间。
        :return: (小时, 分钟, 秒)
        """
        t = datetime.fromtimestamp(t) if t is not None else datetime.now()
        return t.hour, t.minute, t.second


# 文本
class TextJike:
    # 清除字符串渣滓
    @staticmethod
    def word_change(xxx):
        """
        适用于mysql
        :param xxx:
        :return:
        """
        if xxx is not None:
            xxx = str(xxx)
            xxx = str(xxx).replace("'", " ")
            xxx = str(xxx).replace('"', ' ')
            xxx = str(xxx).replace('◕', ' ')
            xxx = str(xxx).replace('\\', ' ')
            xxx = str(xxx).replace('\n', ' ')
            xxx = str(xxx).replace('\r', ' ')
            xxx = str(xxx).replace('\t', ' ')
            xxx = str(xxx).replace('\f', ' ')
            xxx = str(xxx).replace('\v', ' ')
        return xxx

    # 字符串修改 --> 只要数字
    @staticmethod
    def only_number(xxx):
        try:
            if xxx:
                return int(re.sub('\D+', '', xxx))
        except:
            pass

    # 字符串修改 --> 全是数字
    @staticmethod
    def is_all_number(input_string):
        try:
            float(input_string)  # 尝试将字符串转换为浮点数
            return True  # 如果成功转换，说明字符串都是数字
        except ValueError:
            return False  # 如果转换失败，说明字符串包含非数字字符

    # 字符串修改 --> 去除数字
    @staticmethod
    def clear_number(xxx):
        try:
            if xxx:
                return int(re.sub('\d+', '', xxx))
        except:
            pass

    # 字符串修改 --> 去除html符号
    @staticmethod
    def clear_html(xxx):
        try:
            if xxx:
                return re.sub(pattern='<.+?>', repl='', string=xxx)
        except:
            pass

    # 字符串100万 --> 1000000
    @staticmethod
    def str_num_to_int(xxx):
        xxx = xxx.replace(' ', '')  # 去除空格
        if '万' in xxx:
            xxx_num = float(xxx[:-1])
            ret_xxx = xxx_num * 10000

        elif '亿' in xxx:
            xxx_num = float(xxx[:-1])
            ret_xxx = xxx_num * 100000000

        else:
            ret_xxx = xxx
        return ret_xxx

    # 分词处理
    @staticmethod
    def word_split_type2(word="拨片"):
        import jieba.posseg as pseg
        # 只会对单个词进行分析 如果存在两个分词以上 返回 NO
        word_types = []
        word_cls = pseg.cut(word)
        for word, flag in word_cls:
            if flag not in word_types:
                word_types.append(flag)
        return word_types

    # 去除标点
    @staticmethod
    def is_symbol_keyword(keyword):
        if re.compile(r'[^\w]').search(keyword):
            return 1
        return 0

    # 去除标点 忽略#号
    @staticmethod
    def is_symbol_keyword2(keyword):
        if re.compile(r'[^\w#]').search(keyword):
            return 1
        return 0


# 数据
class DataJike:
    # 列表_多个字典_排序  -----↓↓↓↓-----列表 字典 集合 -----↓↓↓↓-----
    @staticmethod
    def list_dicts_order(list_xxx, order_by, positive_or_negative=True):
        if list_xxx:
            return sorted(list_xxx, key=lambda x: x[order_by], reverse=positive_or_negative)

    # 列表 -> 变字典 自动计算 排序
    @staticmethod
    def dicts_order_auto(list_xxx, order_by=True):
        if list_xxx:
            ret_dict = {}
            for i in list_xxx:
                if i in ret_dict:
                    ret_dict[i] += 1
                else:
                    ret_dict[i] = 1
            lis = sorted(ret_dict.items(), key=lambda i: i[1], reverse=order_by)
            return lis

    # 两个列表操作 差集
    @staticmethod
    def diff(l1, l2):
        return list(set(l1).difference(set(l2)))

    # 平均分块
    @staticmethod
    def list_avg_split(list_data, each_num):
        all_list = []
        for i in range(0, len(list_data), each_num):
            all_list.append(list_data[i:i + each_num])
        return all_list

    # 字典合并
    @staticmethod
    def dict_marge(*dicts):
        result = {}
        for d in dicts:
            result.update(d)
        return result

    # 简单字典 返回最大键  {1: 82.0, 2: 18.0} --> max:1
    @staticmethod
    def dict_max(dict_data):
        result_max = max(dict_data, key=lambda x: dict_data[x])
        return result_max

    # 列表 平均值
    @staticmethod
    def list_avg(list_data):
        if len(list_data) < 1:
            return None
        else:
            return int(sum(list_data) / len(list_data))

    # 列表 去除指定元素
    @staticmethod
    def list_remove_by(list_old, removes=None):
        new_list = []
        if list_old and removes and type(removes) == list:
            removes = list(set(removes))  # 去重
            for i in list_old:
                if i not in removes:
                    new_list.append(i)
        return new_list

    # 列表 中位数
    @staticmethod
    def list_median(data):
        data = sorted(data)
        size = len(data)
        if size % 2 == 0:  # 判断列表长度为偶数
            median = (data[size // 2] + data[size // 2 - 1]) / 2
            data[0] = median
        if size % 2 == 1:  # 判断列表长度为奇数
            median = data[(size - 1) // 2]
            data[0] = median
        return data[0]

    # 文件 获取文件夹下所有文件信息
    @staticmethod
    def os_file_child_info(directory_path):
        all_file_info = []
        file_list = os.listdir(directory_path)

        # 遍历文件列表，获取每个文件的详细信息
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)

            # 获取文件信息
            file_info = os.stat(file_path)

            # 打印文件信息（示例，你可以根据需求选择性输出）
            all_file_info.append({
                'name': file_name,
                'size': file_info.st_size,
                'last_up': int(file_info.st_mtime),
                'created': int(file_info.st_ctime),
                'is_directory': os.path.isdir(file_path),
                'is_file': os.path.isfile(file_path),
            })
        return all_file_info

    # dict 多重数据结构提取web链接
    def dict_web_url(self, data):
        links = []

        if isinstance(data, dict):
            for value in data.values():
                links.extend(self.dict_web_url(value))
        elif isinstance(data, list):
            for item in data:
                links.extend(self.dict_web_url(item))
        elif isinstance(data, str):
            # 使用正则表达式查找所有链接
            found_links = re.findall(r'https?://\S+', data)
            links.extend(found_links)

        return links


# 采集
class SpiderJike:
    # >>>>----------------       spider_func         ----------------<<<<<
    # ai api2d 余额查询
    @staticmethod
    def ai_api2d_token_count():
        url = config_dict['ai']['api2d']['balance_url']
        token = config_dict['ai']['api2d']['token']['token1']
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
        res = HttpJike.get(url=url, headers=headers)
        if res.status_code == 200:
            data_data = res.json
            token_count = data_data['total_granted']
            return token_count

    # 获取 moonshot 余额
    @staticmethod
    def ai_moonshot_token_count():
        url = config_dict['ai']['moonshot']['balance_url']
        token = config_dict['ai']['moonshot']['token']['token1']
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
        res = HttpJike.get(url=url, headers=headers)
        if res.status_code == 200:
            data_data = res.json
            available_balance = data_data['data']['available_balance']
            return available_balance

    # 百度IP定位
    @staticmethod
    def api_baidu_ip(ip='60.12.139.18'):
        """
        http://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll //HTTP协议
        https://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll //HTTPS协议

        --参数
        ak    密钥   string    必填    E4jYvwZbl9slCjUALZpnl1xawvoIAlrP
        ip          string    可选
        sn    校验   string    可选
        coor  详细请求  string  可选
        -coor不出现、或为空：百度墨卡托坐标，即百度米制坐标
        -coor = bd09ll：百度经纬度坐标，在国测局坐标基础之上二次加密而来
        -coor = gcj02：国测局02坐标，在原始GPS坐标基础上，按照国家测绘行业统一要求，加密后的坐标
        """
        city = '北京'
        province = '北京'

        try:
            ak = 'E4jYvwZbl9slCjUALZpnl1xawvoIAlrP'
            url = f'http://api.map.baidu.com/location/ip?ak={ak}&ip={ip}&coor=bd09ll'
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)'
            }
            response = HttpJike.get(url=url, headers=headers)
            if response.status_code == 200:
                data_data = response.json
                content = data_data.get('content')
                status = data_data.get('status')
                if content is not None and status == 0:
                    address_detail = content.get('address_detail')
                    if address_detail is not None:
                        city_data = address_detail.get('city')
                        province_data = address_detail.get('province')

                        # 省会 城市 判断
                        if len(province_data) > 0:
                            province = province_data
                            if len(city_data) > 0:
                                city = city_data
                            else:
                                city = province
                        else:
                            pass
                        print(f'省会:{province},城市:{city}')
                        return data_data
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except:
            pass
        return [province, city]

    # 和风天气
    @staticmethod
    def api_qweather(location):
        key = 'fd9e6c4c11254fe19f2b4f46c3653397'
        url = f'https://geoapi.qweather.com/v2/city/lookup?&location={location}&key={key}'
        response = HttpJike.get(url=url)
        if response.status_code == 200:
            j = response.json
            id = j['location'][0]['id']

            # 二,根据城市id 获取城市天气
            url = f'https://devapi.qweather.com/v7/weather/now?location={id}&key={key}'
            headers = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
            }
            response = HttpJike.get(url=url)
            if response.status_code == 200:
                weather_now = response.json
                t_s = time.strftime("%X", time.localtime(time.time()))

                location = f'{location}'
                t_s = f'{t_s}'
                temp = f"{weather_now['now']['temp']}℃"  # 当前温度
                feelsLike = f"{weather_now['now']['feelsLike']}℃"  # 体感温度
                text_now = f"{weather_now['now']['text']}"  # 当前天气
                feng = f"{weather_now['now']['windDir']}{weather_now['now']['windScale']}级 {weather_now['now']['windSpeed']}公里/小时"  # 风
                humidity = f"{weather_now['now']['humidity']}%"  # 湿度
                precip = f"{weather_now['now']['precip']}毫米"  # 降水量值
                pressure = f"{weather_now['now']['pressure']}百帕"  # 大气压强
                vis = f"{weather_now['now']['vis']}公里"  # 能见度值
                cloud = f"{weather_now['now']['cloud']}%"  # 当前云量
                return {'location': location,
                        't_s': t_s,
                        'temp': temp,
                        'feelsLike': feelsLike,
                        'text_now': text_now,
                        'feng': feng,
                        'humidity': humidity,
                        'precip': precip,
                        'pressure': pressure,
                        'vis': vis,
                        'cloud': cloud,
                        }

    # 发送QQ邮件
    @staticmethod
    def send_email(title, text):
        """
        pip install PyEmail
        pip install email
        pip install smtplib
        """

        # 发送邮件配置
        import smtplib
        from email.mime.text import MIMEText
        # email 用于构建邮件内容
        from email.header import Header

        from_addr = '1079146598@qq.com'  # 发信方邮箱
        password = 'ouacnpxmtbavjecc'  # 收信方授权码
        to_addr = '3084447185@qq.com'  # 收信方邮箱
        # to_addr = '1048995287@qq.com'  # 王伟南

        smtp_server = 'smtp.qq.com'  # 发信服务器

        # ，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(text, 'plain', 'utf-8')  # 正文内容

        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(title)

        server = smtplib.SMTP_SSL(host=smtp_server)  # 开启发信服务
        server.connect(smtp_server, 465)  # 加密传输

        server.login(from_addr, password)  # 登录发信邮箱
        server.sendmail(from_addr, to_addr, msg.as_string())  # 发送邮件
        server.quit()  # 关闭服务器

    # fr1997 web 请求ip
    @staticmethod
    def api_fr1997_ip():
        url = 'https://dv.fr1997.cn/test_ip'
        res = HttpJike.get(url=url, proxies=HttpJike.proxies_choose(1))
        if res.status_code == 200:
            return res.json['test_ip']

    # 抖音视频数据解析
    @staticmethod
    def douyin_video_response(res_data, tp='django_video_info'):
        base_ret_data = {'aweme_type': 1, 'is_alive': 1}

        # 是否存在
        if '因作品权限或已被删除，无法观看，去看看其他作品吧' in str(res_data):
            base_ret_data['is_alive'] = 0
            return base_ret_data

        # 获取视频类型
        aweme_type = mode_douyin.douyin_video_type(res_data.get("aweme_type", 0))
        if aweme_type == 68:
            base_ret_data['aweme_type'] = aweme_type
            return base_ret_data

        like_num = res_data["statistics"]["digg_count"]
        forward_num = res_data["statistics"]["share_count"]
        comment_num = res_data["statistics"]["comment_count"]
        collect_count = res_data["statistics"]["collect_count"]

        # 播放时长
        try:
            release_time = round(int(res_data['video']['duration']) / 1000)  # 视频长度
        except:
            release_time = 0

        # 昵称
        nickname = res_data["author"]["nickname"]

        # 描述
        describe = res_data["author"]["signature"]

        # 标题
        desc = res_data["desc"]

        # 封面
        try:
            cover_img = res_data['video']['cover']['url_list'][0]
        except:
            cover_img = ''

        # 视频 vid
        try:
            v_id = res_data['video']['vid']
        except:
            v_id = res_data['video']['play_addr']['uri']

        # 视频创建时间比较特殊，如果没有创建时间，默认一个值
        create_time = res_data.get('create_time', config_dict['douyin']['douyin_video_create_time'])

        # sec_uid
        sec_uid = res_data['author']['sec_uid']

        # user_id
        user_id = res_data['author']['uid']

        # 视频下载地址
        try:
            download_addr_url_list = res_data['video']['download_addr']['url_list']
        except:
            download_addr_url_list = []

        # 视频下载地址 第二类型
        try:
            download_addr_url_list2 = res_data['video']['play_addr']['url_list']
        except:
            download_addr_url_list2 = []

        # mp3 url
        try:
            mp3_url_list = res_data['music']['play_url']['url_list']

            if '.mp3' in res_data['music']['play_url']['url_list'][0]:
                pass
            else:
                mp3_url_list = []
        except:
            mp3_url_list = []

        # author_head
        author_head = res_data['author']['avatar_thumb']['url_list'][0]
        base_ret_data['video_id'] = res_data["aweme_id"]
        base_ret_data['v_id'] = v_id
        base_ret_data['title'] = desc
        base_ret_data['video_cover'] = cover_img

        base_ret_data['play_num'] = 0
        base_ret_data['good_count'] = like_num
        base_ret_data['comment_count'] = comment_num
        base_ret_data['share_count'] = forward_num
        base_ret_data['collect_count'] = collect_count
        base_ret_data['user_id'] = user_id

        base_ret_data['update_time'] = int(time.time())
        base_ret_data['create_date'] = create_time
        base_ret_data['release_time'] = release_time
        base_ret_data['nickname'] = nickname
        base_ret_data['author_head'] = author_head
        base_ret_data['describe'] = describe

        base_ret_data['download_addr_url_list2'] = download_addr_url_list2
        base_ret_data['download_addr_url_list'] = download_addr_url_list
        base_ret_data['mp3_url_list'] = mp3_url_list

        if tp == 'django_video_info':
            return {
                "video_id": res_data["aweme_id"],
                "v_id": v_id,
                'video_description': desc,
                'video_cover': cover_img,

                'play_num': 0,  # 播放量
                'good_count': like_num,  # 点赞量
                'comment_count': comment_num,  # 评论量
                'share_count': forward_num,  # 分享数
                'collect_count': collect_count,  # 收藏数

                'update_time': int(time.time()),
                'create_date': create_time,
                'video_time_count': release_time,  # 视频时常
                'release_time': release_time,  # 视频时常
                'describe': describe,

                'nickname': nickname,
                'sec_uid': sec_uid,
                'user_id': user_id,
                'author_head': author_head,
            }
        elif tp == 'video_info':
            try:
                base_ret_data['follower_count'] = res_data['author']['follower_count']
            except:
                base_ret_data['follower_count'] = 0
            base_ret_data['sec_uid'] = res_data['author']['sec_uid']
            return base_ret_data
        elif tp == 'wav':
            # 获取音频
            bit_rate = res_data['video']['bit_rate'][-1]
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 改版 bit_rate中有很多链接，找到&cs=2为标准音频链接
            bit_rate = res_data['video']['bit_rate'][0]  # 保底一个
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 获取新的
            bit_rate = res_data['video']['bit_rate']
            for bt in bit_rate:
                wav_url_list = bt['play_addr']['url_list']
                if wav_url_list:
                    if '&cs=2' in wav_url_list[0]:
                        base_ret_data['wav_size'] = bt['bit_rate']
                        base_ret_data['wav_url'] = bt['play_addr']['url_list']

            return base_ret_data
        elif tp == 'wav_small':
            # 获取音频
            bit_rate = res_data['video']['bit_rate'][-1]
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']
            return base_ret_data
        else:
            return base_ret_data

    # 【api】 视频详情 2024-05-28
    @staticmethod
    def douyin_video_response2(res_data, tp='django_video_info'):
        base_ret_data = {'aweme_type': 1, 'is_alive': 1}

        # 是否存在
        if '因作品权限或已被删除，无法观看，去看看其他作品吧' in str(res_data):
            base_ret_data['is_alive'] = 0
            return base_ret_data

        # 获取视频类型
        aweme_type = mode_douyin.douyin_video_type(res_data.get('aweme_type', 0))
        if aweme_type == 68:
            base_ret_data['aweme_type'] = aweme_type
            return base_ret_data

        like_num = res_data["statistics"]["digg_count"]
        forward_num = res_data["statistics"]["share_count"]
        comment_num = res_data["statistics"]["comment_count"]
        collect_count = res_data["statistics"]["collect_count"]

        # 播放时长
        try:
            release_time = round(int(res_data['duration']) / 1000)  # 视频长度
        except:
            release_time = 0

        # 昵称
        nickname = res_data["author"]["nickname"]

        # 描述
        describe = res_data["author"]["signature"]

        # sec_uid
        sec_uid = res_data['author']['sec_uid']

        # user_id
        user_id = res_data['author']['uid']

        # 标题
        desc = res_data["desc"]

        # 封面
        try:
            cover_img = res_data['video']['cover']['url_list'][0]
        except:
            cover_img = ''

        # 视频 vid
        try:
            v_id = res_data['video']['vid']
        except:
            v_id = res_data['video']['play_addr']['uri']

        # 视频下载地址
        try:
            download_addr_url_list = res_data['video']['download_addr']['url_list']
        except:
            download_addr_url_list = []

        # 视频下载地址 第二类型
        try:
            download_addr_url_list2 = res_data['video']['play_addr']['url_list']
        except:
            download_addr_url_list2 = []

        # mp3 url
        try:
            mp3_url_list = res_data['music']['play_url']['url_list']

            if '.mp3' in res_data['music']['play_url']['url_list'][0]:
                pass
            else:
                mp3_url_list = []
        except:
            mp3_url_list = []

        # 增加视频分类
        """
            [
                {'tag_id': 2013, 'tag_name': '体育', 'level': 1},
                {'tag_id': 2013004, 'tag_name': '球类项目', 'level': 2},
                {'tag_id': 2013004001, 'tag_name': '足球', 'level': 3}
            ]
            为视频分类，tag1 tag2 tag3 
        """
        video_tag = res_data.get('video_tag', [])
        tag1, tag2, tag3, tag1_id, tag2_id, tag3_id = mode_douyin.douyin_tag_info(video_tag)

        # 视频创建时间比较特殊，如果没有创建时间，默认一个值
        create_time = res_data.get('create_time', config_dict['douyin']['douyin_video_create_time'])

        # author_head
        author_head = res_data['author']['avatar_thumb']['url_list'][0]
        base_ret_data['video_id'] = res_data["aweme_id"]
        base_ret_data['v_id'] = v_id
        base_ret_data['title'] = desc
        base_ret_data['video_cover'] = cover_img

        base_ret_data['play_num'] = 0
        base_ret_data['good_count'] = like_num
        base_ret_data['comment_count'] = comment_num
        base_ret_data['share_count'] = forward_num
        base_ret_data['collect_count'] = collect_count
        base_ret_data['user_id'] = user_id

        base_ret_data['update_time'] = int(time.time())
        base_ret_data['create_date'] = create_time
        base_ret_data['release_time'] = release_time
        base_ret_data['nickname'] = nickname
        base_ret_data['author_head'] = author_head
        base_ret_data['describe'] = describe

        base_ret_data['download_addr_url_list2'] = download_addr_url_list2
        base_ret_data['download_addr_url_list'] = download_addr_url_list
        base_ret_data['mp3_url_list'] = mp3_url_list

        if tp == 'django_video_info':
            return {
                "video_id": res_data["aweme_id"],
                "v_id": v_id,
                'video_description': desc,
                'video_cover': cover_img,

                'play_num': 0,  # 播放量
                'good_count': like_num,  # 点赞量
                'comment_count': comment_num,  # 评论量
                'share_count': forward_num,  # 分享数
                'collect_count': collect_count,  # 收藏数

                'update_time': int(time.time()),
                'create_date': create_time,
                'video_time_count': release_time,  # 视频时常
                'release_time': release_time,  # 视频时常
                'describe': describe,

                'nickname': nickname,
                'sec_uid': sec_uid,
                'user_id': user_id,
                'author_head': author_head,
            }
        elif tp == 'video_info':
            try:
                base_ret_data['follower_count'] = res_data['author']['follower_count']
            except:
                base_ret_data['follower_count'] = 0
            base_ret_data['sec_uid'] = res_data['author']['sec_uid']
            base_ret_data['tag1'] = tag1
            base_ret_data['tag2'] = tag2
            base_ret_data['tag3'] = tag3

            base_ret_data['tag1_id'] = tag1_id
            base_ret_data['tag2_id'] = tag2_id
            base_ret_data['tag3_id'] = tag3_id
            return base_ret_data
        elif tp == 'wav':
            # 获取音频
            bit_rate = res_data['video']['bit_rate'][-1]
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 改版 bit_rate中有很多链接，找到&cs=2为标准音频链接
            bit_rate = res_data['video']['bit_rate'][0]  # 保底一个
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 获取新的
            bit_rate = res_data['video']['bit_rate']
            for bt in bit_rate:
                wav_url_list = bt['play_addr']['url_list']
                if wav_url_list:
                    if '&cs=2' in wav_url_list[0]:
                        base_ret_data['wav_size'] = bt['bit_rate']
                        base_ret_data['wav_url'] = bt['play_addr']['url_list']

            return base_ret_data
        elif tp == 'wav_small':
            # 获取音频
            bit_rate = res_data['video']['bit_rate'][-1]
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']
            return base_ret_data
        else:
            return base_ret_data


# 抖音
class DouyinJike:
    # 抖音视频分类
    def douyin_video_type(self, aweme_type):
        ret_aweme_type = 0  # 默认视频
        try:
            if aweme_type == 68 or aweme_type == '68':  # 图文笔记
                return 68
            else:
                return 0
        except:
            pass
        return ret_aweme_type

    # 抖音视频id短链
    def short_url(self, url):
        return HttpJike.get(url=url).ret_url

    # 抖音 链接 -> video_id
    def get_video_id(self, video_url, tp=1):
        # 最终 https://www.douy...in.com/video/7218785833724185917
        if '://v.douyin' in video_url:
            pat = re.compile(r'https://v.douyin.com/[-_a-zA-Z0-9]{5,10}/')
            res = pat.findall(video_url)
            if res:
                v_url = self.get_video_id(self.short_url(res[0]))
                return v_url
        if 'www.douyin.com' in video_url and 'modal_id' in video_url:
            url1 = video_url.split('modal_id=')
            if url1:
                url2 = url1[-1]
                video_ids = []
                for i in url2:
                    if i in '1234567890':
                        video_ids.append(i)
                    else:
                        break
                video_id = ''.join(video_ids)
                return video_id
        if '.douyin.com/video' in video_url:
            video_idstr1 = video_url.split('/')
            if len(video_url) >= 5:
                video_idstr2 = video_idstr1[4]
                # 去除末尾杂项
                video_ids = []
                for i in video_idstr2:
                    if i in '1234567890':
                        video_ids.append(i)
                    else:
                        break
                video_id = ''.join(video_ids)
                return video_id
        if '/www.douyin.com/user/' in video_url and 'modal_id' in video_url:  # 其他
            video_idstr1 = video_url.split('modal_id=')[-1]
            video_ids = []
            for i in video_idstr1:
                if i in '1234567890':
                    video_ids.append(i)
                else:
                    break
            video_id = ''.join(video_ids)
            return video_id
        if 'www.iesdouyin.com/share/video/' in video_url:
            video_id = video_url.split('www.iesdouyin.com/share/video/')[-1].split('/?')[0]
            return video_id

        # 强制识别 可能出现问题(强制识别 视频id为19位数字)
        pat = re.compile(r'\d{19}')
        res = pat.findall(video_url)
        if res:
            return res[0]

    # 抖音 链接 -> sec_uid
    def get_douyin_sec_uid(self, user_url, tp=1):  # https://v.douyin.com/i3TDetD
        try:
            if 'www.douyin.com' in user_url and 'MS4' in user_url:
                sec_uid = user_url.split('https://www.douyin.com/user/')[-1].split('?')[0]
                return sec_uid

            if '://v.douyin.com':
                url_pattern = r'https://v\.douyin\.com/\w+/'
                matches = re.findall(url_pattern, user_url)
                if matches:
                    user_url = matches[0]
                res = HttpJike.get(url=user_url).ret_url
                sec_uid = res.split('https://www.iesdouyin.com/share/user/')[-1].split('?')[0]
                return sec_uid
        except:
            pass

    # 抖音搜索 20231025 数据解析
    @staticmethod
    def douyin_search_data_20231025(keyword, data_data, res_page):
        status_code = data_data.get('status_code')
        data = data_data.get('data')
        if status_code == 0 and data:
            data_list = []
            for index, v in enumerate(data):
                aweme_info = v['aweme_info']
                aweme_type = mode_douyin.douyin_video_type(aweme_info.get('aweme_type', 0))

                # 如何判断选集？ mixId？
                mixId = None
                mixInfo = aweme_info.get('mix_info')
                if mixInfo:
                    mixId = mixInfo.get('mix_id')

                # 播放时长
                try:
                    release_time = round(int(aweme_info['video']['duration']) / 1000)  # 视频长度
                except:
                    release_time = 0

                author = aweme_info['author']

                # 用户的介绍
                signature = author.get('signature', '')

                # unique_id
                unique_id = author.get('unique_id', '')
                if len(unique_id) == 0:
                    unique_id = author.get('short_id', '')
                data_dict = {
                    F_keyword: keyword,
                    'aweme_type': aweme_type,
                    'mixId': mixId,
                    'index': index,
                    'desc': aweme_info['desc'],
                    'aweme_id': aweme_info['aweme_id'],
                    'sec_uid': author['sec_uid'],
                    'user_id': author['uid'],
                    'unique_id': unique_id,
                    'enterprise_verify_reason': author.get('enterprise_verify_reason', ''),
                    'nickname': author['nickname'],
                    'followers_count': author['follower_count'],

                    'createTime': aweme_info['create_time'],
                    'like_count': aweme_info['statistics']['digg_count'],  # 电赞
                    'comment_num': aweme_info['statistics']['comment_count'],  # 评论
                    'share_count': aweme_info['statistics']['share_count'],  # 转发
                    'collect_count': aweme_info['statistics']['collect_count'],  # 收藏

                    'search_time': int(time.time()),
                    'source': 'app_dj_videopc',

                    'cover': aweme_info['video']['cover']['url_list'][0],  # 封面
                    'author_head': author['avatar_thumb']['url_list'][0],
                    'author_type': '其他',

                    # 至关重要的vid
                    'v_id': aweme_info['video']['play_addr']['uri'],
                    'p': res_page,  # 页数

                    # 视频时长
                    'release_time': release_time,

                    # 介绍
                    'signature': signature,
                }

                data_list.append(data_dict)
            return {'code': 200, 'msg': 'ok', 'data_list': data_list}
        else:
            return {'code': 500, 'msg': '没有数据'}

    # 缓存es 抖音关键词搜索视频
    @staticmethod
    def douyin_keyword_info_save(sava_data, source):
        sava_es_data = []
        for v in sava_data:
            keyword = v[F_keyword]
            index = v['index']
            aweme_id = v['aweme_id']
            desc = v['desc']
            sec_uid = v['sec_uid']
            nickname = v['nickname']
            createTime = v.get('createTime')
            like_count = v.get('like_count')
            mixId = v.get('mixId')
            v_id = v.get('v_id')
            sava_es_data.append({"index": {"_id": f"{keyword}__{index}"}})
            data_dict = {
                'aweme_id': aweme_id,
                'mixId': mixId,
                'index': index,  # 从1开始
                'desc': desc,
                'sec_uid': sec_uid,
                'nickname': nickname,
                F_keyword: keyword,
                'createTime': createTime,
                'like_count': like_count,
                'search_time': int(time.time()),
                'source': source,

                # 至关重要的vid
                'v_id': v_id,
            }
            sava_es_data.append(data_dict)
        return sava_es_data, 'douyin_search_keyword_data'

    # 【api】 用户详情
    def api_douyin_user(self, sec_uid):
        device_id = ''.join(random.choice("0123456789") for _ in range(16))
        url = f"https://www.douyin.com/aweme/v1/web/user/profile/other/?sec_user_id={sec_uid}&device_id={device_id}&aid=1128"
        url = mode_pro.get_xbogus_new_gbk(url, config_dict['base_ua'])
        response = HttpJike.get(url=url, headers=self.ttwid_headers(), proxies=HttpJike.proxies_choose())
        if response.status_code == 200:
            data_data = response.json
            user_detail = data_data.get('user')

            data_json = self.analysis_douyin_user(user_detail)  # 数据获取
            return data_json

    # 【api】 视频详情 2024-05-28
    def api_douyin_video(self, video_id, use_proxies=1, res_tp='video_info', proxies_dcc=0):
        headers = {
            "user-agent": config_dict['base_ua'],
        }
        url = f'https://aweme.snssdk.com/aweme/v1/multi/aweme/detail/?aweme_ids=[{video_id}]'
        try:
            if use_proxies:
                response = HttpJike.get(url=url, headers=headers, proxies=HttpJike.proxies_choose())
            else:
                if proxies_dcc == 1:
                    all_p = mode_pro.douchacha_ips_mysql()['request_ip']
                    response = HttpJike.get(url=url, headers=headers, proxies=random.choice(all_p))
                else:
                    response = HttpJike.get(url=url, headers=headers)
            if response.status_code == 200:
                data_data = response.json
                aweme_details = data_data['aweme_details']
                if aweme_details:
                    video_detail = aweme_details[0]
                    data_json = mode_spider.douyin_video_response2(video_detail, tp=res_tp)  # 数据获取
                    return data_json
                else:
                    return {'aweme_type': 1, 'is_alive': 0, 'err': '没有数据'}

        except Exception as E:
            return {'aweme_type': 1, 'is_alive': 0, 'err': E}

    # 【api】 抖音合集列表
    def api_douyin_mix_list(self, cursor=0, limit=6, use_proxies=1):
        headers = self.ttwid_headers()
        url = f'https://www.douyin.com/aweme/v1/web/mix/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAqfJDRsNO2778Ye6WecYtOl1qISyLAwUoG2rgsZFqzS9ZAKpN7tMuqr7O6P2Acwos&req_from=channel_pc_web&cursor={cursor}&count={limit}&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=2048&screen_height=1280&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=32&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50'
        url = mode_pro.get_xbogus_new_gbk(url, config_dict['base_ua'])
        try:
            if use_proxies:
                response = HttpJike.get(url=url, headers=headers, proxies=HttpJike.proxies_choose())
            else:
                response = HttpJike.get(url=url, headers=headers)
            if response.status_code == 200:
                data_data = response.json
                print(data_data)
                return data_data
        except Exception as E:
            pass

    # 【api】 抖音合集详情
    def api_douyin_mix_page(self, mix_id):
        url = f'https://www.douyin.com/aweme/v1/web/mix/aweme/?device_platform=webapp&aid=6383&channel=channel_pc_web&mix_id={mix_id}&cursor=0&count=20&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=2048&screen_height=1280&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=32&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50'
        url = mode_pro.get_xbogus_new_gbk(url, config_dict['base_ua'])
        response = requests.get(
            url=url,
            headers=self.ttwid_headers(),
        )
        print(response.status_code)
        print(response.json())

    # 【api】 用户主页视频列表 amemv版本
    def user_video_list_mv(self, sec_uid, max_cursor='0', timeout=30):
        ret_data = {
            'list': []
        }
        headers = {
            'authority': 'www.douyin.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.douyin.com',
            "user-agent": config_dict['base_ua'],
        }
        params = {
            "sec_uid": sec_uid,
            'aid': '1128',
            "count": 21,
            "max_cursor": max_cursor,  # 需要 max_cursor 跳转到下一页
        }
        try:
            response = requests.get(f'https://www.amemv.com/web/api/v2/aweme/post/', params=params,
                                    headers=headers, proxies=HttpJike.proxies_choose(), timeout=timeout)
            if response.status_code == 200:
                data_data = response.json()
                max_cursor = data_data.get('max_cursor')
                has_more = data_data.get('has_more')
                ret_data['max_cursor'] = max_cursor
                ret_data['has_more'] = has_more
                status_code = data_data.get('status_code')
                if status_code == 0:
                    aweme_list = data_data["aweme_list"]
                    for v in aweme_list:
                        aweme_id = v['aweme_id']
                        author_info = v.get('author', {})
                        nickname = author_info.get('nickname', '')
                        uid = author_info.get('uid', '')
                        sec_uid = author_info.get('sec_uid', '')

                        statistics = v.get('statistics', {})
                        digg_count = statistics.get('digg_count', 0)
                        share_count = statistics.get('share_count', 0)
                        # comment_count = statistics.get('comment_count', 0)  # 没有
                        # collect_count = statistics.get('collect_count', 0)  # 没有
                        # create_time = statistics.get('create_time', 0)  # 没有

                        video_info = v.get('video', {})
                        release_time = round(int(video_info.get('duration', 0)) / 1000)
                        vid = video_info.get('vid', '')

                        ret_data['list'].append({
                            'aweme_id': aweme_id,
                            'aweme_type': mode_douyin.douyin_video_type(v.get('aweme_type', 0)),
                            'title': v['desc'],
                            'digg_count': digg_count,
                            'share_count': share_count,

                            'nickname': nickname,
                            'sec_uid': sec_uid,
                            'uid': uid,

                            'release_time': release_time,
                            'vid': vid,
                        })
        except:
            pass

        return ret_data

    # api 抖音用户 来之于django
    def api_douyin_user_info(self, sec_uid):
        url = "http://pythonapi.yinliu.club/douyin_users_info/"
        data = {
            'token': config_dict['token']['django'],
            'user_ids': sec_uid,
        }
        res = requests.post(url=url, data=data)
        return res.json()

    # 【数据解析】 用户主页列表
    def analysis_douyin_video_list(self, aweme_list):
        save_data = []
        for v in aweme_list:
            author = v['author']

            # 链接，
            sec_uid = author['sec_uid']

            # 链接，
            aweme_id = v['aweme_id']

            # 类型
            aweme_type = mode_douyin.douyin_video_type(v.get('aweme_type', 0))

            # 点赞数
            digg_count = v['statistics']['digg_count']

            # 评论数
            comment_count = v['statistics']['comment_count']

            # 评论数
            collect_count = v['statistics']['collect_count']

            # 评论数
            share_count = v['statistics']['share_count']

            release_time = round(int(v['duration']) / 1000)  # 视频长度

            # 标题
            desc = mode_text.word_change(v['desc'])
            if len(str(desc)) < 0:
                desc = ''

            # 发布时间。
            create_time = v['create_time']
            create_time_str = time.strftime("%Y-%m-%d %X", time.localtime(create_time))  # 2021-04-12 14:36:20
            save_data.append({
                'sec_uid': sec_uid,
                'aweme_id': aweme_id,
                'aweme_type': aweme_type,
                'title': desc,

                'digg_count': digg_count,
                'comment_count': comment_count,
                'collect_count': collect_count,
                'share_count': share_count,
                'release_time': release_time,
                'create_time': create_time,
                'create_time_str': create_time_str,
            })
        return save_data

    # 【数据解析】 用户详情
    def analysis_douyin_user(self, res_data):
        aweme_count = res_data['aweme_count']
        follower_count = res_data['follower_count']
        nickname = res_data['nickname']
        unique_id = res_data.get('unique_id', '')
        if len(unique_id) == 0:
            unique_id = res_data.get('short_id', '')
        user_id = res_data['uid']
        total_favorited = res_data['total_favorited']
        author_head = res_data['avatar_168x168']['url_list'][0]
        introduction = mode_text.word_change(res_data['signature'])
        # 用户类型 1=个人  2=黄V  3=蓝V  4=注销  5=未知
        user_type = 5
        organization = ''
        custom_verify = res_data['custom_verify']
        enterprise_verify_reason = res_data.get('enterprise_verify_reason', '')
        if len(custom_verify) > 0:
            user_type = 2
            organization = custom_verify
        if len(enterprise_verify_reason) > 0:
            user_type = 3
            organization = enterprise_verify_reason

        return {
            'nickname': nickname,
            'unique_id': unique_id,
            'user_id': user_id,
            'introduction': introduction,
            'video_count': aweme_count,
            'follower_count': follower_count,
            'good_count': total_favorited,
            'user_type': user_type,
            'organization': organization,
            'author_head': author_head,
            'user_update_date': int(time.time()),
        }

    # 【数据解析】 视频详情
    def douyin_video_response(self, res_data, tp='django_video_info'):
        base_ret_data = {'aweme_type': 1, 'is_alive': 1}

        # 是否存在
        if '因作品权限或已被删除，无法观看，去看看其他作品吧' in str(res_data):
            base_ret_data['is_alive'] = 0
            return base_ret_data

        # 获取视频类型
        aweme_type = mode_douyin.douyin_video_type(res_data.get('aweme_type', 0))
        if aweme_type == 68:
            base_ret_data['aweme_type'] = 68
            return base_ret_data

        like_num = res_data["statistics"]["digg_count"]
        forward_num = res_data["statistics"]["share_count"]
        comment_num = res_data["statistics"]["comment_count"]
        collect_count = res_data["statistics"]["collect_count"]

        # 播放时长
        try:
            release_time = round(int(res_data['video']['duration']) / 1000)  # 视频长度
        except:
            release_time = 0

        # 昵称
        nickname = res_data["author"]["nickname"]

        # 描述
        describe = res_data["author"]["signature"]

        # 标题
        desc = res_data["desc"]

        # 封面
        try:
            cover_img = res_data['video']['cover']['url_list'][0]
        except:
            cover_img = ''

        # 视频 vid
        try:
            v_id = res_data['video']['vid']
        except:
            v_id = res_data['video']['play_addr']['uri']

        # 视频创建时间比较特殊，如果没有创建时间，默认一个值
        create_time = res_data.get('create_time', config_dict['douyin']['douyin_video_create_time'])

        # sec_uid
        sec_uid = res_data['author']['sec_uid']

        # user_id
        user_id = res_data['author']['uid']

        # author_head
        author_head = res_data['author']['avatar_thumb']['url_list'][0]
        base_ret_data['video_id'] = res_data["aweme_id"]
        base_ret_data['v_id'] = v_id
        base_ret_data['title'] = desc
        base_ret_data['video_cover'] = cover_img

        base_ret_data['play_num'] = 0
        base_ret_data['good_count'] = like_num
        base_ret_data['comment_count'] = comment_num
        base_ret_data['share_count'] = forward_num
        base_ret_data['collect_count'] = collect_count

        base_ret_data['update_time'] = int(time.time())
        base_ret_data['create_date'] = create_time
        base_ret_data['release_time'] = release_time
        base_ret_data['nickname'] = nickname
        base_ret_data['describe'] = describe

        if tp == 'django_video_info':
            return {
                "video_id": res_data["aweme_id"],
                "v_id": v_id,
                'video_description': desc,
                'video_cover': cover_img,

                'play_num': 0,  # 播放量
                'good_count': like_num,  # 点赞量
                'comment_count': comment_num,  # 评论量
                'share_count': forward_num,  # 分享数
                'collect_count': collect_count,  # 收藏数

                'update_time': int(time.time()),
                'create_date': create_time,
                'video_time_count': release_time,  # 视频时常
                'release_time': release_time,  # 视频时常
                'describe': describe,

                'nickname': nickname,
                'sec_uid': sec_uid,
                'user_id': user_id,
                'author_head': author_head,
            }
        elif tp == 'video_info':
            base_ret_data['follower_count'] = res_data['author']['follower_count']
            base_ret_data['sec_uid'] = res_data['author']['sec_uid']
            return base_ret_data
        elif tp == 'wav':
            # 获取音频
            bit_rate = res_data['video']['bit_rate'][-1]
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 改版 bit_rate中有很多链接，找到&cs=2为标准音频链接
            bit_rate = res_data['video']['bit_rate'][0]  # 保底一个
            base_ret_data['sec_uid'] = sec_uid
            base_ret_data['wav_size'] = bit_rate['bit_rate']
            base_ret_data['wav_url'] = bit_rate['play_addr']['url_list']

            # 获取新的
            bit_rate = res_data['video']['bit_rate']
            for bt in bit_rate:
                wav_url_list = bt['play_addr']['url_list']
                if wav_url_list:
                    if '&cs=2' in wav_url_list[0]:
                        base_ret_data['wav_size'] = bt['bit_rate']
                        base_ret_data['wav_url'] = bt['play_addr']['url_list']
            return base_ret_data
        else:
            return base_ret_data

    # 获取ttwid
    @staticmethod
    def get_ttwid_20240111():
        result = None
        try:
            json = {"region": "cn", "aid": 1768, "needFid": False, "service": "www.ixigua.com",
                    "migrate_info": {"ticket": "", "source": "node"}, "cbUrlProtocol": "https", "union": True}
            r = requests.post("https://ttwid.bytedance.com/ttwid/union/register/", json=json,
                              proxies=HttpJike.proxies_choose())
            cookie = r.headers['Set-Cookie']
            match = re.search("ttwid=([^;]+)", cookie)
            if match:
                result = match.group(1)
            else:
                result = ""
        except:
            print("err ttwid_cookie获取失败")
        if result:
            return result

    # 千川指数
    def qianchuan_index_req(self, cookie_use, word):
        cookies = []
        all_cookie = mode_pro.qianchuan_index_cookie()  # 具有缓存性
        for cookie in all_cookie:
            if cookie['id_id'] in cookie_use:
                cookies.append(cookie)

        cookie = random.choice(cookies)
        acc = cookie['id_id']

        t0 = mode_time.zero_clock()
        t30 = t0 - 86400 * 30
        data = {"word": word, "start_datetime": t30, "end_datetime": t0}

        try:
            response = requests.post(
                f'https://ad.oceanengine.com/platform/api/v1/search_ad/search_trend_v2/?aadvid={cookie["aadvid"]}',
                # 监控
                headers=cookie['headers'],
                cookies=cookie['cookies'],
                data=json.dumps(data)
            )
            if response.status_code == 200:
                data_data = response.json()
                code = data_data.get('code')
                data = data_data.get('data')
                if code == 0 and data:
                    return {'code': 200, 'msg': 'ok', 'data': mode_pro.keyword_day_index_get(data=data), 'acc': acc}
                else:
                    return {'code': 500, 'msg': f'err 1', 'acc': acc}
            else:
                return {'code': 500, 'msg': f'err:{response.status_code}', 'acc': acc}
        except Exception as E:
            return {'code': 500, 'msg': 'err 2', 'acc': acc}

    # 千川指数
    def qianchuan_index_data_do(self, day_index, _id):
        # 日均值
        day_index_new = [i['v'] for i in day_index]
        day_index_new.sort()
        day_index_new = day_index_new[1:][:-1]
        index_avg = mode_data.list_avg(day_index_new)
        if index_avg is None:
            index_avg = 0

        # 计算中位数
        if day_index:
            day_index_new = [i['v'] for i in day_index]
            median = mode_data.list_median(day_index_new)
        else:
            median = 0

        return {
            'is_open': 1,
            F_keyword: _id,
            'day_index': day_index,  # 日指数
            'median': median,  # 中位数
            'index_avg': index_avg,  # 平均数
        }

    # 千川指数 批量存储
    def qianchuan_index_save(self, save_data):
        should_keyword = []
        keyword_index_doc = []
        keyword_index_sign_doc = []
        if save_data:
            for i in save_data:
                _id = i[F_keyword]
                should_keyword.append(_id)
            is_in, is_in_data, shoulds_not = mode_pro.es_in_or_notins(config_dict['db_name']['table11'], should_keyword)
            for i in save_data:
                _id = i[F_keyword]
                keyword_index_doc.append({"index": {"_id": f"{_id}"}})
                keyword_index_doc.append({
                    'is_open': i['is_open'],
                    F_keyword: _id,  # 平均指数
                    'day_index': i['day_index'],  # 日指数
                    'median': i['median'],  # 中位数
                    'index_avg': i['index_avg'],  # 平均数
                    'create_time': int(time.time()),
                    'update_time': int(time.time()),
                })

                # 同步到关键词表
                if _id in is_in_data:
                    keyword_pinyin = mode_pro.chinese_to_pinyin(chinese=_id, ret=3)
                    keyword_index_sign_doc.append(
                        {'update': {'_index': f"dso_douyin_keyword_{keyword_pinyin}", '_id': _id}})
                    keyword_index_sign_doc.append({'doc': {
                        'index_avg_new': i['index_avg'],
                        'median_new': i.get('median', 0),
                        'update_index_time': int(time.time()),
                    }})
        mode_pro.es_create_update(doc=keyword_index_doc, index='douyin_keyword_index')
        mode_pro.es_create_update_noIndex(doc=keyword_index_sign_doc)

    # 视频分类
    @staticmethod
    def douyin_tag_info(video_tag):
        tag1 = ""
        tag1_id = ""
        tag2 = ""
        tag2_id = ""
        tag3 = ""
        tag3_id = ""
        try:
            for tg in video_tag:
                tag_id = tg['tag_id']
                tag_name = tg['tag_name']
                level = tg['level']

                if level == 1:
                    tag1 = tag_name
                    tag1_id = tag_id
                elif level == 2:
                    tag2 = tag_name
                    tag2_id = tag_id
                elif level == 3:
                    tag3 = tag_name
                    tag3_id = tag_id
        except:
            pass
        return tag1, tag2, tag3, tag1_id, tag2_id, tag3_id

    # 抖音批量视频详情请求url
    @staticmethod
    def douyin_video_batch_url(aweme_ids):
        url_start = 'https://aweme.snssdk.com/aweme/v1/multi/aweme/detail/?aweme_ids=['
        for v in aweme_ids:
            url_start += f'{v},'
        if aweme_ids:
            url_start = url_start[:-1]
        return url_start + ']'

    # mix
    @staticmethod
    def mix_str(mixId):
        if mixId is None:
            video_category = 2
            video_mixid = ''
        else:
            video_category = 1
            video_mixid = mixId
        return video_mixid, video_category

    # 视频分类
    @staticmethod
    def douyin_tag_info_html(video_tag):
        tag1 = ""
        tag1_id = ""
        tag2 = ""
        tag2_id = ""
        tag3 = ""
        tag3_id = ""
        try:
            for tg in video_tag:
                tag_id = tg['tagId']
                tag_name = tg['tagName']
                level = tg['level']

                if level == 1:
                    tag1 = tag_name
                    tag1_id = tag_id
                elif level == 2:
                    tag2 = tag_name
                    tag2_id = tag_id
                elif level == 3:
                    tag3 = tag_name
                    tag3_id = tag_id
        except:
            pass
        return tag1, tag2, tag3, tag1_id, tag2_id, tag3_id

    def ttwid_headers(self):
        cookies = mode_pro.ttwid_cookie_tt(get_cache=1)
        return {
            "authority": "www.douyin.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept": "application/json, text/plain, */*",
            "user-agent": config_dict['base_ua'],
            "referer": "https://www.douy" + "in.com/user/MS4wLjABAAAAM5BxLLRhN2jrzttuOUI3LEmFClP8t6dp0bf67Oi3deE",
            "accept-language": "zh-CN,zh;q=0.9",
            'cookie': f'msToken={mode_pro.get_douyin_token(107)};odin_tt=;passport_csrf_token=1;{random.choice(cookies)}'
        }

    # 抖音视频 笔记 html版本 错误->【None】
    def api_douyin_html(self, video_id, use_proxies=1, is_ocr=0):
        headers = self.ttwid_headers()
        try:
            url = f'https://www.douyin.com/note/{video_id}'
            if use_proxies:
                response = HttpJike.get(url=url, headers=headers, proxies=HttpJike.proxies_choose())
            else:
                response = HttpJike.get(url=url, headers=headers)
            if response.status_code == 200:
                return self.res_html_data(response, is_ocr=is_ocr)
        except Exception as e:
            print(e)

    # 数据解析 抖音作品详情 html版本
    def res_html_data(self, response, is_ocr=0):
        base_ret_data = {'aweme_type': 1, 'is_alive': 1}
        is_alive = 1
        pattern = r'self\.__pace_f\.push\(\[1,"\d:\[\S+?({[\s\S]*?)\]\\n"\]\)</script>'
        render_data: str = re.findall(pattern, response.text)[-1]
        if render_data:
            render_data = render_data.replace(
                '\\"', '"').replace('\\\\', '\\')
            data_data_each = json.loads(render_data)

            # 失效的视频判断
            if data_data_each['statusCode'] == -404:
                if is_ocr:
                    base_ret_data['is_alive'] = 0
                    return base_ret_data
                return {'code': 501}

            detail = data_data_each['aweme']['detail']
            # 备用字段
            base_ret_data['desc'] = detail["desc"]
            base_ret_data['aweme_id'] = detail['awemeId']
            base_ret_data['like_count'] = detail["stats"]["diggCount"]
            base_ret_data['forward_num'] = detail["stats"]["shareCount"]
            base_ret_data['sce_uid'] = detail["authorInfo"]["secUid"]
            base_ret_data['cover_img'] = detail['video']['coverUrlList'][0]

            base_ret_data['title'] = detail["desc"]
            base_ret_data['aweme_type'] = mode_douyin.douyin_video_type(detail.get('awemeType', 0))
            base_ret_data['video_id'] = detail['awemeId']

            base_ret_data['play_num'] = 0
            base_ret_data['good_count'] = detail["stats"]["diggCount"]
            base_ret_data['comment_count'] = detail["stats"]["commentCount"]
            base_ret_data['share_count'] = detail["stats"]["shareCount"]
            base_ret_data['collect_count'] = detail["stats"]["collectCount"]

            base_ret_data['nickname'] = detail["authorInfo"]["nickname"]
            base_ret_data['sec_uid'] = detail["authorInfo"]["secUid"]
            base_ret_data['follower_count'] = detail["authorInfo"]["followerCount"]
            base_ret_data['total_favorited'] = detail["authorInfo"]["totalFavorited"]
            base_ret_data['uid'] = detail["authorInfo"]["uid"]
            base_ret_data['author_head'] = detail['authorInfo']['avatarThumb']['urlList'][0]
            base_ret_data['video_cover'] = detail['video']['coverUrlList'][0]
            base_ret_data['user_id'] = detail['authorInfo']['uid']
            base_ret_data['describe'] = ''

            base_ret_data['update_time'] = int(time.time())

            try:
                base_ret_data['v_id'] = detail['video']['uri']
                if base_ret_data['aweme_type'] == 68:
                    base_ret_data['v_id'] = ''
            except:
                base_ret_data['v_id'] = ''

            try:
                base_ret_data['create_time'] = detail.get('createTime',
                                                          config_dict['douyin']['douyin_video_create_time'])
            except:
                base_ret_data['create_time'] = config_dict['douyin']['douyin_video_create_time']
            base_ret_data['create_date'] = base_ret_data['create_time']

            try:
                base_ret_data['release_time'] = round(int(detail['video']['duration']) / 1000)  # 视频长度
            except:
                base_ret_data['release_time'] = 0

            # 视频下载地址 第二类型
            try:
                download_addr_url_list2 = detail['video']['playAddr']
                download_addr_url = []
                for i in download_addr_url_list2:
                    each_src = i['src']
                    if 'https:' not in each_src:
                        each_src = f'https:{each_src}'
                    download_addr_url.append(each_src)
                base_ret_data['download_addr_url_list2'] = download_addr_url
            except Exception as E:
                base_ret_data['download_addr_url_list2'] = []

            # 获取tag
            tag1, tag2, tag3, tag1_id, tag2_id, tag3_id = self.douyin_tag_info_html(detail['videoTag'])
            base_ret_data['tag_info'] = {
                'tag1': tag1,
                'tag2': tag2,
                'tag3': tag3,
                'tag1_id': tag1_id,
                'tag2_id': tag2_id,
                'tag3_id': tag3_id,
            }

        if is_ocr:
            if base_ret_data['aweme_type'] == 0:
                base_ret_data['aweme_type'] = 1
            return base_ret_data
        return {'code': 200, 'is_alive': is_alive, 'date': base_ret_data}

    @staticmethod
    def is_hot_note(like_count, follower_count):
        """
        any 2024-10-22
            增加低粉爆款（笔记），低粉爆款的笔记取数逻辑为：
            1. 点赞数>=10000的视频
            2. 点赞数/粉丝数>=10
        """
        is_hot = 0
        try:
            if like_count >= 10000 and follower_count > 0:
                if like_count / follower_count >= 10:
                    is_hot = 1
        except:
            pass
        return is_hot


# 小红书
class XhsJike:
    cookie_table = 'cd_xiaohongshu_cookie'

    def xhs_web_note_into(self, text, note_id):
        def ret_json(code=200, msg=None, data=None):
            return {'code': code, 'msg': msg, 'data': data}

        if '当前内容无法展示' in text:
            return ret_json(500, '内容不见了')

        text = text.split('window.__INITIAL_STATE__=')[-1]
        text = text.split('</script>')[0]
        data_json = json.loads(json.dumps(eval(text)))

        errorCode = data_json['note']['serverRequestInfo']['errorCode']
        if errorCode == -510000:
            return ret_json(500, '内容不见了')

        note_info = data_json['note']['noteDetailMap'][note_id]['note']
        aweme_type = note_info.get('type')
        if aweme_type is None:
            return ret_json(500, '类型 错误')

        # 关于视频链接
        dld_video_url = ''
        duration = 0
        try:
            find_dld_video_url = 0
            dld_video_url = None
            stream = note_info['video']['media']['stream']
            for m in stream:
                if stream[m] and find_dld_video_url == 0:
                    # 有？无法转译
                    dld_video_url = stream[m][0]['backupUrls'][-1]

            duration = note_info['video']['capa']['duration']
        except:
            pass

        # 获取封面
        try:
            note_cover = note_info['imageList'][0]['urlDefault']
        except:
            note_cover = ''

        # 全部封面
        note_cover_list = []
        try:
            res_note_cover = note_info['imageList']
            for nc in res_note_cover:
                note_cover_list.append(nc['urlDefault'])
        except:
            note_cover = []

        # 话题
        topic = []
        try:
            tagList = note_info['tagList']
            for ti in tagList:
                topic.append(ti['name'])
        except:
            pass

        interactInfo = note_info['interactInfo']
        like_count = interactInfo['likedCount']
        collect_count = interactInfo['collectedCount']
        share_count = interactInfo['shareCount']
        comment_count = interactInfo['commentCount']

        return ret_json(200, 'ok', {
            'aweme_type': aweme_type,
            'note_id': note_id,
            'create_date': int(note_info['time'] / 1000),
            'title': mode_text.word_change(note_info['title']),
            'desc': mode_text.word_change(note_info['desc']),
            'location': note_info.get('ipLocation', ''),
            'duration': duration,
            'dld_video_url': dld_video_url,
            'note_cover': note_cover,
            'note_cover_list': note_cover_list,
            'topic': topic,

            'nickname': mode_text.word_change(note_info['user']['nickname']),
            'user_id': note_info['user']['userId'],
            'avatar': note_info['user']['avatar'],

            'like_count': like_count,
            'collect_count': collect_count,
            'share_count': share_count,
            'comment_count': comment_count,
        })

    def xhs_web_video_main_data(self, data_json, note_id):
        def ret_json(code=200, msg=None, data=None):
            return {'code': code, 'msg': msg, 'data': data}

        try:
            note_info = data_json['note']['noteDetailMap'][note_id]['note']

            aweme_type = note_info.get('type')
            if aweme_type is None or aweme_type != 'video':
                return ret_json(200, '请输入视频作品')

            # 关于视频链接
            find_dld_video_url = 0
            dld_video_url = None
            stream = note_info['video']['media']['stream']
            for m in stream:
                if stream[m] and find_dld_video_url == 0:
                    try:
                        # 有？无法转译
                        dld_video_url = stream[m][0]['backupUrls'][-1]
                    except:
                        pass

            if not dld_video_url:
                return ret_json(200, '未找到url')

            # 获取封面
            try:
                note_cover = note_info['imageList'][0]['urlDefault']
            except:
                note_cover = ''

            note_cover_list = []
            try:
                note_cover = note_info['imageList']
                for nc in note_cover:
                    note_cover_list.append(nc['urlDefault'])
            except:
                note_cover = ''

            return ret_json(200, 'ok', {
                'note_id': note_id,
                'aweme_type': 1,
                'create_date': int(note_info['time'] / 1000),
                'title': mode_text.word_change(note_info['title']),
                'desc': mode_text.word_change(note_info['desc']),
                'location': note_info.get('ipLocation', ''),
                'duration': note_info['video']['capa']['duration'],
                'dld_video_url': dld_video_url,
                'note_cover': note_cover,
                'note_cover_list': note_cover_list,

                'nickname': mode_text.word_change(note_info['user']['nickname']),
                'user_id': note_info['user']['userId'],
                'avatar': note_info['user']['avatar'],
            })
        except Exception as e:
            return ret_json(500, e)

    def xhs_video_id_pc(self, url):
        note_id = None
        if '://www.xiaohongshu.com/discovery' in url:
            note_id = url.split('://www.xiaohongshu.com/discovery/item/')[-1].split('?')[0]

        if '://www.xiaohongshu.com/explore/' in url:
            note_id = url.split('://www.xiaohongshu.com/explore/')[-1].split('?')[0]
        return note_id

    def xhs_app_url_302(self, url):
        pattern = r'://xhslink\.com(/?[A-Za-z0-9]+/[A-Za-z0-9]{6,12})|://xhslink\.com/([A-Za-z0-9]{6})'
        match = re.search(pattern, url)

        if match:
            if match.group(1):
                app_url = f'http://xhslink.com{match.group(1)}'
            else:
                app_url = f'http://xhslink.com/{match.group(2)}'
            return requests.get(app_url, headers=config_dict['base_headers']).url
        else:
            return None

    def xhs_cookie(self, cookie_status=1, use_status=1):
        """
            ret
            {
                '65ee99ca000000000d025711': {
                    'user_id': '65ee99ca000000000d025711',
                    'nickname': 'Sp2',
                    'cookie': 'a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043;gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy;gid.sign=PSF1M3U6EBC/Jv6eGddPbmsWzLI=;webId=ba57f42593b9e55840a289fa0b755374;web_session=040069b49ada82640747c5e8ba344bd27cba68;acw_tc=007e1ba81f48bb265761f2ca4e2ca2b6e56437254e85e2c0b78814337ee9525e',
                    'cookie_dict': {
                        'a1': '187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043',
                        'gid': 'yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy',
                        'gid.sign': 'PSF1M3U6EBC/Jv6eGddPbmsWzLI',
                        'webId': 'ba57f42593b9e55840a289fa0b755374',
                        'web_session': '040069b49ada82640747c5e8ba344bd27cba68',
                        'acw_tc': '007e1ba81f48bb265761f2ca4e2ca2b6e56437254e85e2c0b78814337ee9525e'
                    }
                }
            }
        """
        cache_key = f'xhs_cookie_v1'
        all_cookie = cache_get(cache_key)
        if not all_cookie:
            all_cookie = {}
            sql = f'SELECT user_id,nickname,cookie FROM {self.cookie_table} where use_status = {cookie_status} and cookie_status = {cookie_status}'
            all_data = mode_pro.mysql_db(method='s', table=self.cookie_table, sql=sql)
            if all_data:
                for i in all_data:
                    user_id = i[0]
                    nickname = i[1]
                    cookie = i[2]
                    cookie_dict = mode_pros.cookie_str_to_cookie_dict(cookie)
                    all_cookie[user_id] = {'user_id': user_id, 'nickname': nickname,
                                           'cookie': cookie, 'cookie_dict': cookie_dict}
            if not all_cookie:
                print("-- cookie 耗尽了！！！！！")
                sql = f'SELECT user_id,nickname,cookie FROM {self.cookie_table} where use_status = {cookie_status} and cookie_status = {cookie_status}'
                all_data = mode_pro.mysql_db(method='s', table=self.cookie_table, sql=sql)
                if all_data:
                    for i in all_data:
                        user_id = i[0]
                        nickname = i[1]
                        cookie = i[2]
                        cookie_dict = mode_pros.cookie_str_to_cookie_dict(cookie)
                        all_cookie[user_id] = {'user_id': user_id, 'nickname': nickname,
                                               'cookie': cookie, 'cookie_dict': cookie_dict}

            print(f"-- 当前可用cookie:{len(all_cookie.keys())}")
            cache_set(cache_key, all_cookie, 60)
        return all_cookie

    def xhs_video_main(self, req_url, proxies=None, user_cookie=0, user_cookie_str=''):
        def ret_json(code=200, msg=None, data=None):
            return {'code': code, 'msg': msg, 'data': data}

        # app端要特殊处理
        if 'xhslink' in req_url:
            req_url = self.xhs_app_url_302(req_url)
            if req_url is None:
                return ret_json(500, '未找到该视频 XHS009')

        # 获取小红书xsec_token
        matches = re.findall(r'xsec_token=([^&]+)', req_url)
        xsec_token = matches[0] if matches else ''

        # 获取id
        note_id = self.xhs_video_id_pc(req_url)
        if note_id is None:
            return ret_json(500, '未找到该视频 XHS008')

        xhs_url = f'https://www.xiaohongshu.com/explore/{note_id}'
        headers = config_dict['base_headers']
        if user_cookie == 1:
            cookies = self.xhs_cookie()
            a1 = None
            web_session = None
            for c in cookies:
                a1 = cookies[c]['cookie_dict']['a1']
                web_session = cookies[c]['cookie_dict']['web_session']
            headers['cookie'] = f"a1={a1}; web_session={web_session};"
            if user_cookie_str:
                headers['cookie'] = user_cookie_str
        else:
            xhs_url = f'https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed'

        if proxies:
            response = requests.get(xhs_url, headers=headers, proxies=proxies)
        else:
            response = requests.get(xhs_url, headers=headers)

        ret_data = self.xhs_web_note_into(response.text, note_id)
        return ret_data

    def get_xsec_tokens(self):
        cache_key = 'xsec_tokens_loc'
        data_list = cache_get(cache_key)
        if data_list:
            return data_list
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
            }
            data = {
                'token': '6auY6Ziz5piv5LiW55WM5LiK5pyA5Y6J5a6z55qE54is6Jmr5bel56iL5biI'
            }
            res = requests.post('http://42.193.7.147:7666/api/xhs/xsec_tokens', headers=headers, data=data)
            data_list = res.json()['data_list']
        except:
            data_list = ['ABEYLLyVLWG08-G_kO1QjaRUbpEaR29Qp3x4FDuVu426Q=',
                         'ABvV_W-E_VoxQSWCz1XendH268Med-HREFf7yno5IHCGo=',
                         'ABtBwHcu7rrk2ZOH0uuALyQI9oodA7sxPQyLRTfPhG5og=',
                         'ABDqV1xAR3SEoDdoB40_yD09avHnKGui_9VILZWXg3KWU=',
                         'ABuVs-3eDbtBfMHKwjHNr_hSMspIejizaqy51WQ9PoZEs=',
                         'ABsyzeuCaB5MPqaxXLX4KN89uhUiR-mLFAScprAu8x3bU=',
                         'ABe4gWUH7BK_r6Kgr8MkH2KPgMhKsPelpyE5dYYaIDoyg=',
                         'ABB7yHf8D8NW7IKk8dannxhwtSt3Xe2pWBw8UA6X14nzY=',
                         'ABho-zF_Jgw0LOiTT7J_5Y41slfUKZqL7QSu6xNHP-074=',
                         'ABiKahsJveydyvyBLdalMttlsQkENKAi9rbj6jIUPEdYc=',
                         'ABwMlOi53Bwe0jUAImDKByPaN2LFoGTn9zUb1URi8rYOY=',
                         'ABVbNcwQ0f1BWXtmtonOugs6o3g9T79LKtjcWwjDwQJBI=',
                         'ABm2t24JDR3esni55egnOcYn_gbldE9YdTCbUqnnmHQcU=',
                         'ABgOqOeYao7rUrNtI7XReJiykIDAYpSb6l9yF7_GOdJrs=',
                         'ABDhb0tLEyG-h7GadFcad3JT0PE-GGAWd6Hr1I3BDmu00=',
                         'ABlOZqc5waGwnbRWh4_-8FAzXlvBK-hNdFSXaDbyO80b0=',
                         'ABrtj6WWKntX-NsHZYowrMD3nyFjTgyOUz8RBe5TWJCyY=',
                         'ABoq-5CYRk-V0DY3iMSrHu-W7SFDhxh_Z_82f9j3KkC-k=',
                         'ABmNO7UiQrtbj3C254ulqkv6sM2uebgGtK0SySVNpvVbU=',
                         'ABzAhu8qQ1S24JcioVxkWeNRgv03FoSO83klaJRMeiDoI=',
                         'AB7F7OTfM7z8Wy4FYWzkdUpmMHMs0zUJVPb5GZKRhZatA=',
                         'ABLoiHV-amiurHpzoLHH6U6Y3SUXuil-syWnCzN-TkbuQ=',
                         'ABho-zF_Jgw0LOiTT7J_5Y4-JeR1W4mkWkwfh_MstqHc4=',
                         'ABEe6GwZ6YvsATZpGFwBMaKyikgFVqRRQ06dr4j4TLtgY=',
                         'ABUUOADRu6dI8NlNWT9_SMJwLK5SEn67LB320ru9tj7O4=']
        cache_set(cache_key, data_list, 600)
        return data_list

    # 聚光
    def h(self, keyword, js_path):
        # 聚光
        def js_e():
            e = ""
            for t in range(16):
                e += "abcdef0123456789"[math.floor(16 * random.random())]
            return e

        sign = self.js_go(keyword, js_path)
        headers = {
            'authority': 'ad.xiaohongshu.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/tools/keywordTool',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^110^\\^, ^\\^Not',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '^\\^Windows^\\^',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
            'x-b3-traceid': js_e(),
            'x-s': sign['X-s'],
            'x-t': str(sign['X-t'])
        }
        return headers

    # 聚光
    def js_go(slef, keyword, js_path='/www/wwwroot/gy_pyhton_project/all_project/xiaohongshu/keyword/j2.js'):
        if js_path == 'loc':
            js_path = 'C://Users/30844\Documents\project_all\python_project\mofan\gy_pyhton_project/all_project/xiaohongshu/keyword/j2.js'
        with open(js_path, 'r', encoding='utf-8-sig') as w:
            s = w.readline()
            js_code = ''
            while s:
                js_code = js_code + s
                s = w.readline()

        ctx1 = execjs.compile(js_code)
        return ctx1.call('sign', '/api/leona/rtb/tool/keyword/search', "{keyword: " + f'{keyword}' + "}")

    # 聚光 小红书关键词
    @classmethod
    def target_word(cls, target_word):
        if '/' in str(target_word):
            return None
        return target_word

    # 聚光 小红书关键词
    @classmethod
    def mounth_search_index(cls, monthpv):
        if monthpv <= 0:
            monthpv = 0
        return monthpv

    # 聚光 小红书关键词
    @classmethod
    def competition(cls, completionLevel):
        if completionLevel == '高':
            return 3
        elif completionLevel == '中':
            return 2
        elif completionLevel == '低':
            return 1
        else:
            return 0

    # 聚光 小红书关键词
    @classmethod
    def suggested_bid(cls, suggestedBid):
        return float(suggestedBid)

    # 聚光 小红书关键词
    @classmethod
    def recommend_reason(cls, recommendReason):
        if recommendReason:
            return ','.join(recommendReason)
        else:
            return ''

    # 去除标点
    @classmethod
    def is_symbol_keyword(cls, keyword):
        if re.compile(r'[^\w]').search(keyword):
            return 1
        return 0

    # 聚光
    @staticmethod
    def bad_word():
        cache_key = 'xhs_bad_keyword'
        bad_keyword = cache_get(cache_key)
        if not bad_keyword:
            sql = 'SELECT good_word,all_word FROM `cd_xhs_repeat_keyword` where good_word is not null'
            all_data = mode_pro.mysql_db(method='s', table='cd_xhs_repeat_keyword', sql=sql)
            bad_keyword = ['没家']
            for i in all_data:
                good_word = i[0]
                all_word = i[1]
                good_word_list = good_word.split(',')
                all_word_list = all_word.split(',')
                for j in all_word_list:
                    if j not in good_word_list:
                        bad_keyword.append(j)
            cache_set(cache_key, bad_keyword, 5 * 60)

        return bad_keyword


# django
class DjangoJike:
    # 配置
    @staticmethod
    def django_config():
        sc = 'status_code'  # 返回码
        msg = 'message'  # 返回消息

        return {
            "status_codes": {
                "code_200": {sc: 200, msg: '成功-200'},
                "code_400": {sc: 400, msg: '错误-400'},
                "code_500": {sc: 500, msg: '错误-500'},
                "code_xxx": {sc: 555, msg: '错误-xxx'},
                "code_token": {sc: 556, msg: '错误-token'},
                "code_method": {sc: 557, msg: '错误-method'},
            },
            "save_logs": 0,
            "save_logs_post": [
                '/',
                '/web/love/index',
                '/web/love/photo',
                '/test/test',
                '/test/logs',
            ],
            "save_logs_get": [
                '/',
                '/web/love/index',
                '/web/love/photo',
                '/test/test',
                '/test/logs',
            ],
        }

    # 存储日志
    @staticmethod
    def django_save_log(request, code=200):
        meta = request.META
        method = request.method
        form_data = request.POST
        user_ip = meta.get('HTTP_X_FORWARDED_FOR', '127.0.0.2')  # django版本不一样，参数不一样
        user_ua = meta.get('HTTP_USER_AGENT', '')
        user_path_info = meta.get('PATH_INFO', '')

        values = meta.items()
        info = []
        for k, v in values:
            info.append(f'{k}:{v}')

        # 排除一些请求
        for no_save in ['/static/', '/favicon.ico']:
            if no_save in user_path_info:
                return 0

        create_time = int(time.time())
        create_time_str = time.strftime("%Y-%m-%d %X", time.localtime(create_time))  # 2021-04-12 14:36:20
        save_table = config_dict['mysql_table']['fr1997']['django_logs']['name']
        mode_pro.mysql_db(method="ins", table=save_table, save_data={
            'code': code,
            'method': method,
            'form_data': form_data,
            'user_ua': user_ua,
            'user_ip': user_ip,
            'info': str(info),
            'user_path_info': user_path_info,
            'create_time': create_time,
            'create_time_str': create_time_str,
        }, conn_tp=5)
        return {
            'info': info,
            'user_ua': user_ua,
            'user_ip': user_ip,
            'user_path_info': user_path_info,
        }

    # 装饰器 请求限制
    def django_res_limit(self, func):
        """
            get 不验证token   post  需要验证
        """

        def wrapper(request):
            method = request.method
            form_data = request.POST
            url_path = str(request.path)
            # 存储日志(存储的是请求，不是结果)
            if method == 'GET' and url_path in self.django_config()['save_logs_get']:
                self.django_save_log(request)  # 存储django日志
            elif method == 'POST' and url_path in self.django_config()['save_logs_post']:
                self.django_save_log(request)  # 存储django日志

            # POST 要验证token
            try:
                if method == 'GET':
                    return func(request)
                elif method == 'POST':
                    token = form_data.get('token', '')  # 验证参数
                    if token == config_dict['token']['django'] or url_path in config_dict['django']['no_token_check']:
                        return func(request)
                    else:
                        django_code = "code_token"
                else:
                    django_code = "code_method"
            except Exception as E:
                print(E)
                django_code = "code_xxx"
            from django.http import JsonResponse  # 2.返回json对象
            ret = self.django_return(code=django_code)
            return JsonResponse(ret)

        return wrapper

    # django 返回配置
    def django_return(self, **kwargs):
        sc = 'status_code'  # 返回码
        msg = 'message'  # 返回消息
        code = kwargs.get('code')
        status_codes = self.django_config()['status_codes']
        return {
            sc: status_codes[code][sc],
            msg: status_codes[code][msg],
        }

    # 获取请求的ip 【1=正式】 【2=测试】
    def user_ip(self, request):
        if request.META.get('REMOTE_ADDR', None) == '1.14.10.13':
            return 1
        else:
            return 2


# mode
class ModeFunc:
    def __init__(self):
        self.path = mode_pros.run_machine()['platform']

    # >>>>----------------       数据库 redis数据库        ----------------<<<<<
    def db_redis(self, RedisDb=0, db=0):
        redis_cfg = 'redis_loc'
        if RedisDb == 0:
            redis_cfg = 'redis_loc'
        elif RedisDb == 10:
            redis_cfg = 'redis_spider1'
        elif RedisDb == 11:  # 内网
            redis_cfg = 'redis_spider1'
        elif RedisDb == 3:
            redis_cfg = 'redis_spider3'

        if self.path == 1:
            redis_host = '127.0.0.1'
        else:
            redis_host = config_dict['redis'][redis_cfg]['host']
        redis_port = config_dict['redis'][redis_cfg]['port']
        redis_pwd = config_dict['redis'][redis_cfg]['pwd']
        return redis.StrictRedis(host=redis_host, port=int(redis_port), password=redis_pwd, db=db)

    # Redis 表记录
    @staticmethod
    def redis_task(task_name):
        """
            tp:选用哪个数据库
            type:存储类型
                kv=键值对   start_：前缀
        """
        redis_task = {
            'douyin_user_cloud': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_cloud', 'ttl': 6000
            },  # 抖音用户云词 几万
            'douyin_user_krm': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_krm', 'ttl': 6000
            },  # 抖音krm
            'douyin_user_ranks': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_ranks', 'ttl': 6000
            }  # 抖音krm
        }
        return redis_task[task_name]

    # >>>>----------------       数据库 mysql数据库         ----------------<<<<<
    @staticmethod
    def db_mysql(path=None):
        config_mysql = config_dict["mysql"]
        if path == 1:
            db_cfg = "mysql_jike_in"
        elif path == 2:
            db_cfg = "mysql_jike_test"
        elif path == 3:
            db_cfg = "mysql_loc"
        elif path == 5:
            db_cfg = "mysql_my_tx"
        else:
            db_cfg = "mysql_jike_out"

        # 寻找特定的数据库配置
        if path in config_mysql:
            db_cfg = path

        mysql_host = config_mysql[db_cfg]['host']
        mysql_user = config_mysql[db_cfg]['user']
        mysql_passwd = config_mysql[db_cfg]['pwd']
        mysql_db = config_mysql[db_cfg]['db']
        mysql_port = int(config_mysql[db_cfg]['port'])
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=int(mysql_port))
        return conn

    # db Mysql 操作 20230719新
    def mysql_db(self, method, table, conn_tp=None, **kwargs):
        """
        method
            - s -- select
            - up --date_more_byid
            - ins -- insert
            - iss -- insert_all
            - tc -- create_table 创建表
            - te -- table_exist 查询 表是否存在
            - sql -- 执行sql -> commit()
        :param method: 方法
        :param table: 表明
        :param conn_tp: 链接
        :return:
        """
        if conn_tp is None:
            conn_tp = 0

        sql = kwargs.get('sql', '')
        save_data = kwargs.get('save_data')

        # mysql链接 【自动】0=内网 1=外网
        conn = self.db_mysql(path=conn_tp)

        # 通用sql 查看表是否存在
        sql_table_exist = f"SELECT * FROM information_schema.tables WHERE table_name = '{table}'"

        # 数据库操作
        try:
            with conn.cursor() as cursor:
                if method == 'insert' or method == 'ins':
                    save_data = kwargs['save_data']
                    columns = ', '.join(save_data.keys())
                    placeholders = ', '.join(['%s'] * len(save_data))
                    params = tuple(save_data.values())
                    sql = f"INSERT ignore INTO {table} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, params)
                    conn.commit()
                elif method == 'insert_all' or method == 'iss':
                    fields = list(save_data[0].keys())
                    placeholders = ', '.join(f'%({i})s' for i in fields)
                    fields_str = ','.join(fields)
                    sql_inserts = f"INSERT ignore INTO {table} ({fields_str}) values({placeholders})"
                    n = cursor.executemany(sql_inserts, save_data)
                    conn.commit()
                    return n
                elif method == 'insert_creat_all' or method == 'isc':
                    pass
                    # # 根据索引插入或更新 没有索引最后 没有更新默认
                    # key = kwargs.get('key')
                    # if key in None:
                    #
                    # update_key = []
                    #
                    # fields = list(save_data[0].keys())
                    # placeholders = ', '.join(f'%({i})s' for i in fields)
                    # fields_str = ','.join(fields)
                    # sql_inserts = f"INSERT INTO {table} ({fields_str}) values({placeholders}) on DUPLICATE {key} update"
                    # return sql_inserts
                    # # n = cursor.executemany(sql_inserts, save_data)
                    # # conn.commit()
                    # # return n
                elif method == 'table_exist' or method == 'te':
                    # 查询 表是否存在
                    return cursor.execute(sql_table_exist)
                elif method == 'create_table' or method == 'tc':  # 创建一个表
                    table_exist = cursor.execute(sql_table_exist)
                    if table_exist:
                        del_and_create = kwargs.get('del_and_create', 0)
                        if del_and_create:
                            print('表已经存在 删除并创建')
                            self.mysql_db(method='dt', table=table, conn_tp=conn_tp)
                        else:
                            print('表已经存在')
                            return '表已经存在'
                    """
                        TINYINT = [-128,127]
                        SMALLINT = [-32768,32767]
                    """
                    fields_sql = []
                    field_cfg = kwargs['field_cfg']
                    for f in field_cfg['fields']:
                        name = f[0]
                        field_type = f[1]
                        length = f[2]
                        default = f[3]
                        comment = f[4]

                        if field_type == 'VARCHAR':
                            fields_sql.append(f"{name} {field_type}({length}) DEFAULT '{default}' COMMENT '{comment}'")
                        elif field_type == 'INT' or field_type == 'TINYINT' or field_type == 'SMALLINT':
                            fields_sql.append(f"{name} {field_type}({length}) DEFAULT {default} COMMENT '{comment}'")
                        elif field_type == 'TEXT':  # 新增条件处理 TEXT 类型
                            fields_sql.append(f"{name} {field_type} DEFAULT '{default}' COMMENT '{comment}'")
                        elif field_type == 'JSON':
                            fields_sql.append(f"{name} {field_type} DEFAULT NULL COMMENT '{comment}'")
                    if fields_sql:
                        this_time = time.strftime("%Y-%m-%d %X", time.localtime(int(time.time())))
                        table_notes = f'{this_time} 【高阳】创建此表'  # 表备注
                        sql_create_base = f"CREATE TABLE {table} ({field_cfg['id']} INT AUTO_INCREMENT PRIMARY KEY,{','.join(fields_sql)}) COMMENT='{table_notes}'"
                        cursor.execute(sql_create_base)

                        # 增加唯一索引
                        field_index = field_cfg['field_index']
                        if field_index:
                            if len(field_index) == 1:
                                sql_index = f"ALTER TABLE {table} ADD UNIQUE INDEX field_index ({field_index[0]});"
                            else:
                                sql_index = f"ALTER TABLE {table} ADD CONSTRAINT field_index UNIQUE ({','.join(field_index)});"
                            cursor.execute(sql_index)
                        print(f"创建{table}成功")
                        return f"创建{table}成功"
                elif method == 'field_add':
                    # 查看一个表所有字段
                    sql_columns = f"SHOW COLUMNS FROM {table};"
                    cursor.execute(sql_columns)
                    columns = cursor.fetchall()
                    columns_list = [i[0] for i in columns]
                    field_change = kwargs.get('field_change')  # ['user', 'VARCHAR', 50, '', '用户名称']
                    field_name = field_change[0]
                    if field_name in columns_list:
                        print(f"{field_name}字段已经存在")
                        return

                    # 增加字段
                    field_type = field_change[1]
                    length = field_change[2]
                    default = field_change[3]
                    comment = field_change[4]
                    if field_type == 'VARCHAR':
                        query = f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type}({length}) COMMENT '{comment}'"
                    elif field_type == 'INT' or field_type == 'TINYINT' or field_type == 'SMALLINT':
                        query = f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type}({length}) DEFAULT {default} COMMENT '{comment}'"
                    elif field_type == 'TEXT':  # 新增条件处理 TEXT 类型
                        query = f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type} COMMENT '{comment}'"
                    elif field_type == 'JSON':
                        query = f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type} DEFAULT NULL COMMENT '{comment}'"
                    cursor.execute(query)
                    print(f"字段{field_name}增加成功")
                elif method == 'field_del':
                    sql_columns = f"SHOW COLUMNS FROM {table};"
                    cursor.execute(sql_columns)
                    columns = cursor.fetchall()
                    columns_list = [i[0] for i in columns]
                    field_del = kwargs.get('field_del')  # ['user', 'VARCHAR', 50, '', '用户名称']
                    if field_del not in columns_list:
                        print(f"{field_del}字段不存在")
                        return

                    query = f"ALTER TABLE {table} DROP COLUMN {field_del}"
                    cursor.execute(query)
                    print(f"字段{field_del}删除成功")
                elif method == 'field_up':
                    sql_columns = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"

                    cursor.execute(sql_columns)
                    columns = cursor.fetchall()
                    field_old = kwargs.get('field_old')
                    field_dict = {i[3]: i for i in columns}
                    if field_old not in field_dict:
                        print(f"{field_old} 老字段不存在")
                        return

                    change_name = kwargs.get('change_name')
                    if change_name is None:
                        change_name = field_old

                    change_type = kwargs.get('change_type')
                    if change_type is None:
                        change_type = field_dict[field_old][15]

                    change_comment = kwargs.get('change_comment')
                    if change_comment is None:
                        change_comment = field_dict[field_old][-3]

                    query = f"ALTER TABLE {table} CHANGE COLUMN {field_old} {change_name} {change_type} COMMENT '{change_comment}'"
                    cursor.execute(query)
                    print(f"字段{field_old}修改名字成功")
                elif method == 'sql':
                    cursor.execute(sql)
                    conn.commit()
                elif method == 'update_more_byid' or method == 'up':  # 更新 根据id进行批量更新
                    if save_data:
                        fields = list(save_data[0].keys())
                        update_fields = [f'{i}=%s' for i in fields[:-1]]
                        sql_update = f"UPDATE {table} SET {','.join(update_fields)} WHERE {fields[-1]} = %s"
                        tuple_data_list = [tuple(data.values()) for data in save_data]
                        cursor.executemany(sql_update, tuple_data_list)
                        conn.commit()
                elif method == 'select' or method == 's':
                    cursor.execute(sql)
                    return cursor.fetchall()
                elif method == 'del_table' or method == 'dt':
                    sql_del = f'DROP TABLE {table}'
                    cursor.execute(sql_del)
                    conn.commit()
                elif method == 'in':
                    field = kwargs.get('field')
                    by_id = kwargs.get('by_id')
                    id_list = kwargs.get('id_list')
                    if not id_list or not field or not by_id:
                        return ()
                    format_strings = ','.join(['%s'] * len(id_list))
                    sql_in = f"SELECT {field} FROM {table} WHERE {by_id} IN ({format_strings})"
                    cursor.execute(sql_in, id_list)
                    return cursor.fetchall()
                else:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"数据库链接错误:{e}")
        finally:
            conn.close()

    # >>>>----------------       数据库 es数据库        ----------------<<<<<
    def db_es(self):
        if self.path == 1:
            es_cfg = 'es_jike_in'
        else:
            es_cfg = 'es_jike_out'
        es_ip = config_dict['es'][es_cfg]['ip']
        es_user = config_dict['es'][es_cfg]['user']
        es_pwb = config_dict['es'][es_cfg]['pwd']
        es_port = config_dict['es'][es_cfg]['port']
        es = Elasticsearch([f'{es_ip}:{es_port}'], http_auth=(es_user, es_pwb))
        return es

    # ES 查询
    def es_search_new_20231215(self, table, query, _source, size=1, sort_info=None, is_ret_num=1, ret_num=0, **kwargs):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
            "_source": _source,
        }

        # 排序
        if sort_info and sort_info != 0:
            body['sort'] = sort_info
        else:
            body['sort'] = {
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }

        es = self.db_es()
        response = es.search(
            index=table,
            body=body
        )
        _shards = response.get('_shards')
        if _shards:
            successful = _shards.get('successful')
            if successful > 0:
                value = response.get('hits')['total']['value']
                hits_list = response.get('hits')['hits']
                print(f'总个数:{value} 取出:{len(hits_list)}')
                if ret_num == 0:
                    return hits_list
                else:
                    return [hits_list, value]

    # ES 查询 适配es8 【jike_api py3.8.5✅】 【py3.6 目前不支持】
    def es_search(self, table, query, _source=None, size=1, sort_info=None, is_ret_num=1, ret_num=0):
        """
        优化后的 Elasticsearch 查询函数。

        :param table: 索引名称
        :param query: 查询条件
        :param _source: 返回字段的筛选列表，默认为 None，表示返回所有字段
        :param size: 返回结果的数量，默认为 1
        :param sort_info: 排序信息，默认为 None
        :param is_ret_num: 是否返回总条数，默认为 1（True）
        :param ret_num: 返回结果模式，0 为只返回数据，1 为返回数据和总数
        :param kwargs: 其他可选参数
        :return: 返回的结果集或结果集和总数
        """
        # 构建参数字典
        params = {
            "index": table,
            "query": query,
            "track_total_hits": is_ret_num == 1,  # 是否追踪总匹配数
            "size": size
        }

        # 处理 _source 参数：如果提供，则使用它；否则返回所有字段
        if _source is not None:
            params["_source"] = _source

        # 排序处理
        if sort_info:
            params['sort'] = sort_info
        else:
            # 默认排序：随机排序
            params['sort'] = [{
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }]

        # 获取 ES 客户端
        es = self.db_es()

        # 执行搜索请求
        response = es.search(**params)

        # 处理响应
        _shards = response.get('_shards', {})
        successful = _shards.get('successful', 0)
        if successful > 0:
            value = response.get('hits', {}).get('total', {}).get('value', 0)
            hits_list = response.get('hits', {}).get('hits', [])
            print(f'总个数:{value} 取出:{len(hits_list)}')
            if ret_num == 0:
                return hits_list
            else:
                return [hits_list, value]
        else:
            print("ES查询失败或无结果")
            return [] if ret_num == 0 else [[], 0]

    # ES 查询 单条
    def es_search_one(self, table, _id, is_print=1):
        body = {
            "track_total_hits": True,
            "query": {
                "match": {"_id": _id}
            }
        }
        es = self.db_es()
        response = es.search(
            index=table,
            body=body
        )
        hits_list = response.get('hits')['hits']
        if is_print:
            value = response.get('hits')['total']['value']
            hits_list = response.get('hits')['hits']
            print(f'总个数:{value} 取出:{len(hits_list)}')
        return hits_list

    # ES 查询 纯es
    def es_search_es(self, table, query):

        es = self.db_es()
        response = es.search(
            index=table,
            body=query
        )
        return response

    # ES 数量
    def es_count(self, table):
        try:
            body = {
                "size": 1,
                "track_total_hits": True
            }
            es = self.db_es()
            response = es.search(
                index=table,
                body=body
            )
            count = response.get('hits')['total']['value']
            return count
        except:
            return -1

    # ES 数量
    def es_count_with_query(self, table, query):
        try:
            body = {
                "query": query,
                "size": 1,
                "track_total_hits": True
            }
            es = self.db_es()
            response = es.search(
                index=table,
                body=body
            )
            count = response.get('hits')['total']['value']
            return count
        except:
            return -1

    # ES 合并查询
    def es_search_merge(self, queries, table):
        es = self.db_es()

        def process_query(query):
            result = es.search(index=table, body=query)
            return result

        # 创建线程池
        pool = ThreadPoolExecutor(max_workers=5)  # 根据需求设置最大工作线程数

        # 提交查询任务到线程池
        futures = [pool.submit(process_query, query) for query in queries]

        # 获取查询结果
        results = [future.result() for future in futures]

        return results

    # ES 查询 分页
    def es_search_page(self, table, query, sort, size=1, offset=0, is_ret_num=1, is_print=0, **kwargs):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
            "from": offset,
            "sort": sort,
        }

        _source = kwargs.get("_source")
        if _source is not None:
            body['_source'] = _source

        # 排序方式
        es = self.db_es()
        response = es.search(
            index=table,
            body=body
        )
        _shards = response.get('_shards')
        if _shards:
            successful = _shards.get('successful')
            if successful > 0:
                hits_list = response.get('hits')['hits']
                if is_print:
                    value = response.get('hits')['total']['value']
                    hits_list = response.get('hits')['hits']
                    print(f'总个数:{value} 取出:{len(hits_list)}')
                return hits_list

    # ES 查询 多表合并查询
    def es_search_alias(self, table, query, size=1, sort_info=None, is_ret_num=1, is_print=0, ret_num=0,
                        **kwargs):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
        }

        _source = kwargs.get("_source")
        if _source is not None:
            body['_source'] = _source

        # 根据规则排序
        if sort_info:
            body['sort'] = sort_info
        else:
            body['sort'] = {
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }

        es = self.db_es()
        response = es.search(
            index=table,
            body=body
        )

        hits = response['hits']
        db_total = hits['total']['value']
        hits_list = hits['hits']
        print(f'总个数:{db_total} 取出:{len(hits_list)}')

        if ret_num == 0:
            return hits_list
        else:
            return [hits_list, db_total]

    # ES 更新
    def es_create_update(self, doc, index, split_num=0):
        es = self.db_es()
        if doc:
            if split_num:
                each_item = mode_data.list_avg_split(doc, split_num * 2)
                for it_doc in each_item:
                    time.sleep(1)
                    es.bulk(body=it_doc, index=index)
            else:
                es.bulk(body=doc, index=index)

    # ES 更新 (自动判断内外网)
    def es_create_update_noIndex(self, doc, split_num=0):
        es = self.db_es()
        if doc:
            if split_num:
                each_item = mode_data.list_avg_split(doc, split_num * 2)
                for it_doc in each_item:
                    time.sleep(1)
                    es.bulk(body=it_doc)
            else:
                es.bulk(body=doc)

    # ES 更新 分表
    def es_create_update_alias(self, doc):
        es = self.db_es()
        if doc:
            es.bulk(body=doc)

    # ES 删除
    def es_del(self, query, index):
        es = self.db_es()
        es.delete_by_query(index=index, body=query, doc_type='_doc')

    # ES 多id查询
    def es_in_or_notin(self, table, shoulds, query=None):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.db_es()
        if shoulds:
            if query is None:
                query = {
                    "bool": {
                        "must": [
                            {"terms": {"_id": shoulds}}
                        ],
                        # "must_not": {"match": {"update_time_1": 0}}
                    }
                }
            response = es.search(
                index=table,
                body={
                    "query": query,
                    "size": 1500,  # 返回数量
                    "track_total_hits": 'true',  # 显示总量有多少条
                }
            )
            if response:
                _shards = response.get('_shards')
                if _shards:
                    successful = _shards.get('successful')
                    if successful == 1:
                        # 数据集
                        hits_list = response.get('hits')['hits']
                        print('本次取出符合条件的总数:', len(hits_list))

                        for index_x, i in enumerate(hits_list):
                            _s = i['_source']
                            _id = i['_id']
                            is_in.append(_id)
                            is_in_data[f'{_id}'] = _s

        shoulds_not = [i for i in shoulds if str(i) not in is_in]
        return is_in, is_in_data, shoulds_not

    # ES 多id查询
    def es_in_or_notin_20231215(self, table, shoulds, _source, split_num=200):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        shoulds_not = []
        es = self.db_es()

        each_item = mode_data.list_avg_split(shoulds, split_num)
        for it_shoulds in each_item:
            time.sleep(1)
            if it_shoulds:
                query = {
                    "bool": {
                        "must": [
                            {"terms": {"_id": it_shoulds}}
                        ],
                    }
                }
                body = {
                    "query": query,
                    "size": split_num,
                    "_source": _source,
                    "track_total_hits": 'true',
                }
                response = es.search(index=table, body=body)
                if response:
                    _shards = response.get('_shards')
                    if _shards:
                        successful = _shards.get('successful')
                        if successful > 0:
                            # 数据集
                            hits_list = response.get('hits')['hits']
                            print('本次取出符合条件的总数:', len(hits_list))

                            for index_x, i in enumerate(hits_list):
                                _s = i['_source']
                                _id = i['_id']
                                is_in.append(_id)
                                is_in_data[f'{_id}'] = _s

            it_shoulds_not = [i for i in it_shoulds if str(i) not in is_in]
            shoulds_not += it_shoulds_not
        return is_in, is_in_data, shoulds_not

    # ES 多id查询(多表)
    def es_in_or_notins(self, table, shoulds, query=None, is_print=0, is_index=0):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.db_es()
        if shoulds:
            if query is None:
                query = {
                    "bool": {
                        "must": [
                            {"terms": {"_id": shoulds}}
                        ],
                        # "must_not": {"match": {"update_time_1": 0}}
                    }
                }
            response = es.search(
                index=table,
                body={
                    "query": query,
                    "size": 1500,  # 返回数量
                    "track_total_hits": 'true',  # 显示总量有多少条
                }
            )
            if response:
                _shards = response.get('_shards')
                if _shards:
                    successful = _shards.get('successful')
                    if successful > 0:
                        # 数据集
                        hits_list = response.get('hits')['hits']
                        if is_print:
                            print('本次取出符合条件的总数:', len(hits_list))

                        for index_x, i in enumerate(hits_list):
                            _s = i['_source']
                            _id = i['_id']
                            is_in.append(_id)
                            if is_index == 1:
                                _s['_index'] = i['_index']
                            is_in_data[f'{_id}'] = _s

        shoulds_not = [i for i in shoulds if str(i) not in is_in]
        return is_in, is_in_data, shoulds_not

    # 分词 老版本
    @staticmethod
    def word_split_old(txt, num=100, clear_myself="???"):
        import jieba

        try:
            num = int(num)
        except:
            num = 100

        # 文本过滤 [去空格 去数字]
        txt = str(txt).replace('\n', '').replace('\r', '').replace('\\', '')
        txt = str(txt).replace(' ', '')
        txt = str(txt).replace("'", " ").replace('"', ' ').replace('◕', ' ').replace(':', ' ').replace('：', ' ')
        words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
        counts = {}  # 通过键值对的形式存储词语及其出现的次数

        # 单个词语不计算在内
        for word in words:
            if word != clear_myself:
                if len(word) == 1:
                    continue
                else:
                    counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

        # 根据词语出现的次数进行从大到小排序
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        if num > len(items):
            num = len(items)

        # 分级选择
        data_list = []
        for i in range(num):
            data_dict = {}
            word, count = items[i]
            data_dict['word'] = word
            data_dict['count'] = count
            if count >= 100:
                data_dict['category'] = '100'
            elif count >= 50:
                data_dict['category'] = '50'
            elif count >= 10:
                data_dict['category'] = '10'
            elif count >= 7:
                data_dict['category'] = '7'
            elif count >= 4:
                data_dict['category'] = '4'
            else:
                data_dict['category'] = '1'
            data_list.append(data_dict)
            # print("{0:<5}{1:>5}".format(word, count))
        return data_list

    # 汉字 => 拼音
    def chinese_to_pinyin(self, chinese="你好", ret=1):
        """
            ret = 1  -->  [['ni3'], ['hao3']]
            ret = 2  -->  nh
            ret = 3  -->  n

            英文的全部转换为小写

            更多复杂判断 都在这里写
                符号开头的返回 ”other“
                数字开头的返回 ”number“
        """
        try:
            chinese = chinese.lower()
            if chinese:
                # 将中文转换为拼音，设置输出格式为带声调的拼音
                pinyin_list = pinyin(chinese, style=Style.TONE3)

                # 提取每个拼音的第一个字母
                first_letters = [p[0][0] for p in pinyin_list]

                # 将字母列表连接成字符串
                first_letters_string = ''.join(first_letters)
                if ret == 2:
                    return first_letters_string
                elif ret == 3:
                    first_word = first_letters_string[:1]
                    if first_word in config_dict['numbers'] or first_word in config_dict['numbers_str']:  # 数字开头
                        return "number"
                    elif first_word == ' ':
                        return "empty"
                    elif first_word not in config_dict['low_word']:  # 符号开头
                        return "other"
                    else:
                        return first_letters_string[:1]
                else:
                    return pinyin_list
            else:
                return "empty"
        except:
            return "other"

    # 关键词日数据 快速查询
    def keyword_day_index_select(self, keyword_list):
        # 获取今日时间戳 获取12个小时时间戳
        order_time = int(time.time()) - 600
        t0 = mode_time.zero_clock()
        if order_time < t0:
            order_time = t0 + 1
        if order_time < 1694491630:  # Bug修改
            order_time = 1694491630

        query1 = {
            "bool": {
                "filter": [
                    {
                        "terms": {
                            F_keyword: keyword_list
                        }
                    },
                    {
                        "range": {"update_time": {"gte": order_time}}
                    }
                ]
            }
        }
        is_in = []
        is_in_data = {}
        ret_hits_list = self.es_search_alias(table='douyin_keyword_index', query=query1, size=1000)
        if ret_hits_list:
            for index_x, i in enumerate(ret_hits_list):
                _s = i['_source']
                _id = i['_id']
                is_in.append(_id)
                is_in_data[f'{_id}'] = _s
        should_not = [i for i in keyword_list if str(i) not in is_in]
        return is_in, is_in_data, should_not

    # 巨量广告cookie
    def qianchuan_index_cookie(self):

        # 缓存到内存
        data_list = cache_get('jike_qianchuan_ad_cookie')
        if not data_list:
            data_list = []
            sql = f"SELECT * FROM `cd_task` WHERE id IN (17,27,33,38);"
            ret = self.mysql_db(method='s', table='cd_task', sql=sql)
            for i in ret:
                data_dict = {}
                json_data = eval(i[7])
                csrftoken = json_data['csrftoken']
                sid_tt = json_data['sid_tt']
                aadvid = json_data['aadvid']
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Origin': 'https://ad.ocean' + 'engine.com',
                    'Referer': f'https://ad.ocean' + f'engine.com/bp/material/traffic_analysis.html?aadvid={aadvid}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    'X-CSRFToken': csrftoken,
                }
                cookies = {'csrftoken': csrftoken, 'sid_tt': sid_tt}
                data_dict['headers'] = headers
                data_dict['cookies'] = cookies
                data_dict['aadvid'] = aadvid
                data_dict['sid_tt'] = sid_tt
                data_dict['csrftoken'] = csrftoken
                data_dict['id_id'] = i[0]
                data_list.append(data_dict)
            cache_set('jike_qianchuan_ad_cookie', data_list, 200)
        return data_list

    # 关键词日数据 数据分析
    @staticmethod
    def keyword_day_index_get(data):
        """
        原：[{'date': '2024-04-14', 'pv': 39078}, {'date': '2024-04-15', 'pv': 20346},
        变：[{'t': 1691164800, 'v': 2595}, {'t': 1691251200, 'v': 2292}, {'t': 1691337600, 'v': 2048}, {'t': 1691424000, 'v': 1965}, {'t': 1691510400, 'v': 2095}, {'t': 1691596800, 'v': 2503}, {'t': 1691683200, 'v': 2177}, {'t': 1691769600, 'v': 2166}, {'t': 1691856000, 'v': 1997}, {'t': 1691942400, 'v': 2025}, {'t': 1692028800, 'v': 2030}, {'t': 1692115200, 'v': 2159}, {'t': 1692201600, 'v': 2648}, {'t': 1692288000, 'v': 2107}, {'t': 1692374400, 'v': 2392}, {'t': 1692460800, 'v': 2378}, {'t': 1692547200, 'v': 2173}, {'t': 1692633600, 'v': 2093}, {'t': 1692720000, 'v': 2020}, {'t': 1692806400, 'v': 1969}, {'t': 1692892800, 'v': 2244}, {'t': 1692979200, 'v': 2924}, {'t': 1693065600, 'v': 2697}, {'t': 1693152000, 'v': 2454}, {'t': 1693238400, 'v': 2431}, {'t': 1693324800, 'v': 2221}, {'t': 1693411200, 'v': 2254}, {'t': 1693497600, 'v': 1748}, {'t': 1693584000, 'v': 2087}, {'t': 1693670400, 'v': 1912}]
        """
        day_index = []
        keyword_pv_trend = data.get('keyword_pv_trend')
        if keyword_pv_trend:
            for i in keyword_pv_trend:
                t = i['date']
                v = i['pv']
                timestamp1 = int(time.mktime(time.strptime(t, '%Y-%m-%d')))
                day_index.append({'t': timestamp1, 'v': v})
        return day_index

    # ip 信息
    def get_user_ip(self, ip):
        url = f'http://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true'
        Default_return = {
            'ip': ip,
            'country': '',
            'province': '',
            'city': '',
            'isp': '',
            'city_id': '',
            'create_time': int(time.time()),
            'addr': '',
        }

        if ip == '101.35.29.36':
            return Default_return

        if ip.split('.')[0] == '127':
            return Default_return

        if ip.split('.')[0] == '192' and ip.split('.')[1] == '168':
            return Default_return

        # 请求
        try:
            res = HttpJike.post(url=url)
            if res.status_code == 200:
                data_data = res.json()
                country = data_data.get('country')
                city = data_data.get('city')
                city_id = data_data.get('cityCode')
                province = data_data.get('pro')
                addr = data_data.get('addr')

                isp = '其他'
                for k in ['电信', '移动', '联通']:
                    if k in addr:
                        isp = k
                        break

                self.mysql_db(method="insert", table='member_ips', save_data={
                    'ip': ip,
                    'country': country,
                    'province': province,
                    'city': city,
                    'isp': isp,
                    'city_id': str(city_id),
                    'create_time': int(time.time()),
                    'addr': addr,
                }, conn_tp=5)
                return {
                    'ip': ip,
                    'country': country,
                    'province': province,
                    'city': city,
                    'isp': isp,
                    'city_id': str(city_id),
                    'create_time': int(time.time()),
                    'addr': addr,
                }
        except:
            pass
        return Default_return

    # 抖查查 代理(缓存到mysql中的ip)
    def douchacha_ips_mysql(self, num=1):
        ips = cache_get('dcc_ip_v1')
        dcc_proxies = {
            'ip': [],
            'aiohttp_ip': [],
            'request_ip': [],
        }
        for ip in ips:
            dcc_proxies['ip'].append(ip)
            dcc_proxies['aiohttp_ip'].append(f"http://{ip}")
            dcc_proxies['request_ip'].append(HttpJike.http_ip(ip))
        return dcc_proxies

    # 获取js文件的绝对路径
    def get_js_base_path(self, js_name):
        base_path = f'gy_pyhton_project/all_project/old/js/{js_name}.js'
        if self.path == 1:
            return f'/www/wwwroot/{base_path}'
        else:
            # return f'E:\Fr1997_D\doc\project\python/{base_path}'
            return f'C://Users/30844\Documents\project_all\python_project\mofan/{base_path}'

    # 抖音xb
    def get_xbogus_new(self, url, ua, mstoken=''):
        # 获取js文件绝对路径
        js_path = self.get_js_base_path(js_name='dy_x_bogus_v2')

        # 重编url
        url_p = urlparse(url)
        params_dict = dict()
        for i in url_p.query.split("&"):
            key, values = i.split('=')[0], i.split('=')[-1]
            if key not in ["msToken", "X-Bogus"]:
                params_dict[key] = values
        param_str = "&".join([f"{i}={params_dict[i]}" for i in params_dict])
        url = f"{url_p.scheme}://{url_p.netloc}{url_p.path}?{param_str}"
        url_para = url.split('?')[1] + '&msToken='

        with open(js_path, 'r', encoding='UTF-8') as file:
            result = file.read()
            context = execjs.compile(result)

            # 提前对参数进行处理
            md5_url = mode_pros.md5_base(url_para)

            str1 = bytes.fromhex(md5_url)
            hash_object = hashlib.md5(str1)
            md5her = hash_object.hexdigest()
            res = context.call("get_xbogus", url_para, ua, md5her)
            result_url = f'{url}&msToken={mstoken}&X-Bogus={res}'
            return result_url

    # 抖音xb
    def get_xbogus_new_gbk(self, url, ua, mstoken=''):
        # 获取js文件绝对路径
        js_path = self.get_js_base_path(js_name='dy_x_bogus_v2')

        # 重编url
        url_p = urlparse(url)
        params_dict = dict()
        for i in url_p.query.split("&"):
            key, values = i.split('=')[0], i.split('=')[-1]
            if key not in ["msToken", "X-Bogus"]:
                params_dict[key] = values
        param_str = "&".join([f"{i}={params_dict[i]}" for i in params_dict])
        url = f"{url_p.scheme}://{url_p.netloc}{url_p.path}?{param_str}"
        url_para = url.split('?')[1] + '&msToken='

        with open(js_path, 'r', encoding='gbk') as file:
            result = file.read()
            context = execjs.compile(result)

            # 提前对参数进行处理
            md5_url = mode_pros.md5_base(url_para)

            str1 = bytes.fromhex(md5_url)
            hash_object = hashlib.md5(str1)
            md5her = hash_object.hexdigest()
            res = context.call("get_xbogus", url_para, ua, md5her)
            result_url = f'{url}&msToken={mstoken}&X-Bogus={res}'
            return result_url

    # 抖音xb
    def get_xbogus_news_gbk(self, urls, ua, mstoken=''):
        ret_sign_urls = []

        # 获取js文件绝对路径
        js_path = self.get_js_base_path(js_name='dy_x_bogus_v2')

        # 重编url
        url_paras = []
        for url in urls:
            url_p = urlparse(url)
            params_dict = dict()
            for i in url_p.query.split("&"):
                key, values = i.split('=')[0], i.split('=')[-1]
                if key not in ["msToken", "X-Bogus"]:
                    params_dict[key] = values
            param_str = "&".join([f"{i}={params_dict[i]}" for i in params_dict])
            url = f"{url_p.scheme}://{url_p.netloc}{url_p.path}?{param_str}"
            url_para = url.split('?')[1] + '&msToken='
            md5_url =  mode_pros.md5_base(url_para)
            str1 = bytes.fromhex(md5_url)
            hash_object = hashlib.md5(str1)
            md5her = hash_object.hexdigest()
            url_paras.append([url_para, md5her])

        with open(js_path, 'r', encoding='gbk') as file:
            result = file.read()
            context = execjs.compile(result)
            res = context.call("get_xboguss", ua, url_paras)
            for url, xb in zip(urls, res):
                sign_url = f'{url}&msToken={mstoken}&X-Bogus={xb}'
                ret_sign_urls.append(sign_url)
        return ret_sign_urls

    # 抖音 msToken生成方式
    @staticmethod
    def get_douyin_token(string_len=16):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(string_len):
            random_str += base_str[random.randint(0, length)]
        return random_str

    # 抖音cookie ttwid版本 db数据库
    def ttwid_cookie_tt(self, num=200, get_cache=0):
        table = 'cd_cookie_douyin'
        if self.path == 1:  # 服务器运行强制默认缓存数据
            get_cache = 1

        cookie_tt = []
        if get_cache == 1:
            cookie_tt = cache_get('jike_ttwid_cookies')
        else:
            sql = f'SELECT douyin_cookie_ttwid FROM {table} where douyin_cookie_ttwid is not null order by rand() limit {num}'
            all_cookie = mode_pro.mysql_db(method='s', table=table, sql=sql)
            for i in all_cookie:
                cookie_tt.append(i[0])
        return cookie_tt

    # 查看某个文件夹所有文件
    @staticmethod
    def get_all_file(directory_path):
        fs = []
        try:
            # 使用 os.listdir 获取目录中的所有文件和子目录
            files = os.listdir(directory_path)

            # 输出所有文件和子目录的名称
            for file in files:
                fs.append(file)

        except Exception as e:
            print(f"Error listing files in directory: {e}")
        return fs

    # 获取知乎cookie
    def get_zhihu_cookie(self):
        cookies = cache_get('jike_zhihu_cookies')
        if not cookies:
            cookies = []
            sql = f"SELECT * FROM cd_zhihu_cookie where id > 0"
            all_cookie = self.mysql_db(method='s', table='cd_zhihu_cookie', sql=sql)
            for each in all_cookie:
                cookie = each[1]
                cookies.append(cookie)
            cache_set('jike_zhihu_cookies', cookies, 50)
        return cookies

    # 知乎加密 python版本
    def x_zse_96_b64encode(self, md5_bytes: bytes):
        h = {
            "zk": [1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157,
                   1933479194, -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428,
                   -2029270069, 2035090028, -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135,
                   1321810770, 456816404, -1391643889, -229302305, 330002838, -788960546, 363569021, -1947871109],
            "zb": [20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93,
                   252,
                   205, 90, 79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80,
                   189,
                   71, 191, 97, 84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22,
                   255,
                   94, 238, 151, 85, 77, 124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146,
                   162,
                   62, 224, 218, 196, 229, 1, 192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117,
                   228, 215, 203, 53, 239, 251, 127, 81, 11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122,
                   145, 106, 118, 74, 190, 29, 16, 174, 5, 177, 129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68,
                   207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244, 155, 51, 236, 200, 233, 58, 61, 47, 100, 137,
                   185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105, 24, 212, 78, 173, 45, 0, 116, 226,
                   119,
                   136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21, 130, 98, 241, 40, 154, 66, 184,
                   49,
                   181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201, 164, 89, 216, 202, 220, 50,
                   221, 152, 140, 33, 235, 214],
            "zm": [120, 50, 98, 101, 99, 98, 119, 100, 103, 107, 99, 119, 97, 99, 110, 111]
        }

        def left_shift(x, y):
            x, y = ctypes.c_int32(x).value, y % 32
            return ctypes.c_int32(x << y).value

        def Unsigned_right_shift(x, y):
            x, y = ctypes.c_uint32(x).value, y % 32
            return ctypes.c_uint32(x >> y).value

        def Q(e, t):
            return left_shift((4294967295 & e), t) | Unsigned_right_shift(e, 32 - t)

        def G(e):
            t = list(struct.pack(">i", e))
            n = [h['zb'][255 & t[0]], h['zb'][255 & t[1]], h['zb'][255 & t[2]], h['zb'][255 & t[3]]]
            r = struct.unpack(">i", bytes(n))[0]
            return r ^ Q(r, 2) ^ Q(r, 10) ^ Q(r, 18) ^ Q(r, 24)

        def g_r(e):
            n = list(struct.unpack(">iiii", bytes(e)))
            [n.append(n[r] ^ G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ h['zk'][r])) for r in range(32)]
            return list(
                struct.pack(">i", n[35]) + struct.pack(">i", n[34]) + struct.pack(">i", n[33]) + struct.pack(">i",
                                                                                                             n[32]))

        def g_x(e, t):
            n = []
            i = 0
            for _ in range(len(e), 0, -16):
                o = e[16 * i: 16 * (i + 1)]
                a = [o[c] ^ t[c] for c in range(16)]
                t = g_r(a)
                n += t
                i += 1
            return n

        local_48 = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
        local_50 = bytes([63, 0]) + md5_bytes  # 随机数  0 是环境检测通过
        local_50 = ZhihuSign.pad(bytes(local_50))
        local_34 = local_50[:16]
        local_35 = [local_34[local_11] ^ local_48[local_11] ^ 42 for local_11 in range(16)]
        local_36 = g_r(local_35)
        local_38 = local_50[16:]
        local_39 = g_x(local_38, local_36)
        local_53 = local_36 + local_39
        local_55 = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE"
        local_56 = 0
        local_57 = ""
        for local_13 in range(len(local_53) - 1, 0, -3):
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_53[local_13] ^ Unsigned_right_shift(58, local_58) & 255
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 1] ^ Unsigned_right_shift(58, local_58) & 255) << 8
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 2] ^ Unsigned_right_shift(58, local_58) & 255) << 16
            local_57 = local_57 + local_55[local_59 & 63]
            local_57 = local_57 + local_55[Unsigned_right_shift(local_59, 6) & 63]
            local_57 = local_57 + local_55[Unsigned_right_shift(local_59, 12) & 63]
            local_57 = local_57 + local_55[Unsigned_right_shift(local_59, 18) & 63]
        return '2.0_' + local_57

    # 巨量广告数据
    def qianchuan_ad_keyword_hot(self, industry_id="19060101", city=None, cookie=None, search_type='hot_search_words',
                                 business_words_num=500, offset=0, limit=0):
        ret_data = []
        ret_err = 0

        if cookie is None:
            all_cookie = mode_pro.qianchuan_index_cookie()
            cookie = random.choice(all_cookie)
        headers = cookie['headers']
        cookies = cookie['cookies']
        aadvid = cookie['aadvid']
        day0 = mode_time.zero_clock(0)
        day2 = mode_time.zero_clock(2)
        day7 = mode_time.zero_clock(7)

        city_change = {
            "北京-北京": "北京",
            "天津-天津": "天津",
            "台湾-台湾": "台湾",
            "香港-香港": "香港",
            "澳门-澳门": "澳门",
            "重庆-重庆": "重庆",
            "上海-上海": "上海",
        }

        # 热搜词=hot_search_words，商机词=business_words，飙升词=up_words
        if search_type == 'hot_search_words':
            stat_time_type = 7
            metric_type = 1
            filed1 = 'search_rank_pv_filter'
            metrics = ["search_rank_query_pv", "search_rank_pv_filter"]
            orderBy = 'search_rank_query_pv'
            startTime = day7 * 1000
        elif search_type == 'business_words':
            stat_time_type = 7
            metric_type = 2
            filed1 = 'search_rank_cost_filter'
            metrics = ["search_rank_cost", "search_rank_cost_filter"]
            orderBy = 'search_rank_cost'
            startTime = day7 * 1000
        else:
            stat_time_type = 2
            metric_type = 3
            filed1 = 'search_rank_surging_filter'
            metrics = ["search_rank_surging_pv", "search_rank_surging_rate", "search_rank_surging_filter"]
            orderBy = 'search_rank_surging_pv'
            startTime = day2 * 1000

        # 请求参数
        filters = [{"field": "stat_time_type", "operator": 7, "type": 3, "values": [f"{stat_time_type}"]},
                   {"field": "metric_type", "operator": 7, "type": 1, "values": [f"{metric_type}"]},
                   {"field": "industry_id", "operator": 7, "type": 3, "values": industry_id},
                   {"field": filed1, "operator": 1, "type": 3, "values": ["1"]}]
        city = eval(city)
        for index_ct, ct in enumerate(city):
            if ct in city_change:
                city[index_ct] = city_change[ct]
        filters.append({"field": "region", "operator": 7, "type": 2, "values": city})

        data = {
            "dataTopic": "ad_query_traffic_data",
            "dimensions": ["query"],
            "endTime": day0 * 1000,
            "filters": filters,
            "metrics": metrics,
            "orderBy": [{"field": orderBy, "type": 1}], "page": {"limit": limit, "offset": offset},
            "platform": 1,
            "startTime": startTime,
            "extraInfo": {"refer_origin": "ad.oceane" + "ngine.com/statistics_pages/tool_apps/flow_analysis/search",
                          "refer_code": "ad_platform_search_traffic_analysis"}
        }
        response = requests.post(
            f'https://ad.oceanengine.com/nbs/api/statistics/customize_report/data?aadvid={aadvid}',  # 分类热词
            headers=headers, cookies=cookies, data=json.dumps(data))
        if response.status_code == 200:
            data_data = response.json()
            code = data_data.get('code')
            msg = data_data.get('msg')
            if code == 0 and msg == '':
                ret_err = 1
                data_main = data_data.get('data')
                if data_main:
                    rows = data_main.get('rows')
                    rank = 1

                    if search_type == 'hot_search_words':
                        for r in rows:
                            ret_data.append({
                                F_keyword: r['dimensions']['query'],
                                'search_day7_value': r['metrics']['search_rank_query_pv'],
                                'search_day7_rank': rank
                            })
                            rank += 1
                    elif search_type == 'business_words':
                        for r in rows:
                            ret_data.append({
                                F_keyword: r['dimensions']['query'],
                                'search_rank_cost': r['metrics']['search_rank_cost'],
                                'search_rank': rank
                            })
                            rank += 1
                    else:
                        for r in rows:
                            ret_data.append({
                                F_keyword: r['dimensions']['query'],
                                'search_value': r['metrics']['search_rank_surging_pv'],
                                'search_value_rate': r['metrics']['search_rank_surging_rate'],
                                'search_rank': rank
                            })
                            rank += 1

        return ret_err, ret_data

    def api_chat_gpt(self, content):
        url = config_dict['ai']['api2d']['chat_url']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config_dict['ai']['api2d']['token']['token1']}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": content}]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except:
            pass

    # 巨量广告cookie
    def wechat_search_keyword_cookie(self):
        data_list = []
        sql = f"SELECT * FROM `cd_task` WHERE id IN (43);"
        ret = self.mysql_db(method='s', table='cd_task', sql=sql)
        for i in ret:
            data_dict = {}
            json_data = eval(i[7])
            gdt_token = json_data['gdt_token']
            g_tk = json_data['g_tk']
            owner = json_data['owner']
            mp_tk = json_data['mp_tk']
            campaign_id = json_data['campaign_id']
            data_dict['gdt_token'] = gdt_token
            data_dict['g_tk'] = g_tk
            data_dict['owner'] = owner
            data_dict['mp_tk'] = mp_tk
            data_dict['campaign_id'] = campaign_id

            data_list.append(data_dict)
        return data_list

    # 本地地址
    @classmethod
    def loc_ip(cls):
        hostname = socket.gethostname()
        ip_list = []
        # 获取IP地址信息
        addr_infos = socket.getaddrinfo(hostname, None)
        for addr in addr_infos:
            ip_list.append(addr[4][0])
        return ip_list

    # 公网ip
    @classmethod
    def public_ip(cls):
        return requests.get(r'https://jsonip.com').json()

    # 错误推送
    def err_log(self, func, p=4, err_times=3, sleep=30, err_msg="err!!!", save_mysql=0):
        """
        import inspect
        func_info = inspect.getframeinfo(inspect.currentframe())
        mode_pro.err_log(func_info, p=5, err_msg="这个错误啊!!!", err_times=1, sleep=10, save_mysql=1)

            如果函数发生错误，需要发送推送信息
                规则：
                    1.两次推送的间要有休眠时间 sleep
                    2.推送包含 错误等级p 错误信息 错误位置
                    3.要有错误阈值err_times，错误n次后再推送

            p等级 0-5 越小越紧急
            - 0  服务器挂了
            - 1  高度重视
            - 2  中等错误
            - 3  小错误
            - 4  日常错误
            - 5  except 抛出

            err_times 错误次数 1-100000次
        """

        func_name = func.function
        func_filename = func.filename
        func_lineno = func.lineno

        # 错误唯一标志
        v = 'v11132sd'
        key = f"err_log_{v}_{mode_pros.md5_base(f'{func_name}_{func_filename}_{func_lineno}')}"
        key_send = f"err_send_{v}_{mode_pros.md5_base(f'{func_name}_{func_filename}_{func_lineno}')}"

        def send(this_err_count):
            mode_feishu.feishu_send_message(f"""err {p}
        错误信息：{err_msg}
        错误次数：{this_err_count}
        错误函数：{func_name}
        错误位置：{func_filename}
        错误行数：{func_lineno}""")

        err_cache = cache_get(key)
        if err_cache:
            err_count = err_cache['err_count'] + 1
            cache_set(key, {'err_count': err_cache['err_count'] + 1})
        else:
            err_count = 1
            cache_set(key, {'err_count': err_count})

        if err_count >= err_times:
            err_send_cache = cache_get(key_send)
            if not err_send_cache:
                send(err_count)
                cache_set(key_send, 1, sleep)

                # 存储mysql
                mode_pro.mysql_db(method='iss', table='cd_err_log_python', save_data=[{
                    'p': p,
                    'err_msg': err_msg,
                    'err_count': err_count,
                    'func_name': func_name,
                    'func_filename': func_filename,
                    'func_lineno': func_lineno,
                    'create_time': int(time.time()),
                }])


# cos
class Cos:

    def __init__(self, **kwargs):
        # 选择服务器
        server_select = kwargs.get("server_select", 'jike')
        if server_select == 'personal':
            self.secret_id = config_dict['cos']['gaoyang']['secret_id']
            self.secret_key = config_dict['cos']['gaoyang']['secret_key']
        else:
            self.secret_id = config_dict['cos']['secret_id']
            self.secret_key = config_dict['cos']['secret_key']
        self.region = config_dict['cos']['region']
        self.scheme = config_dict['cos']['scheme']
        self.config = CosConfig(Region=self.region,
                                SecretId=self.secret_id,
                                SecretKey=self.secret_key,
                                Scheme=self.scheme)
        self.client = CosS3Client(self.config)

    # 创建存储桶
    def create_bucket(self, bucket_name):
        response = self.client.create_bucket(
            Bucket=bucket_name
        )

    # 查看文件是否纯在
    def file_exist(self, Bucket, path, file):
        try:
            response = self.client.head_object(
                Bucket=Bucket,
                Key=f'{path}{file}',  # video/qq.png
            )
            return response
        except:
            return False

    # 上传文件
    def upload_file(self, Bucket, loc_path, path, file):
        try:
            response = self.client.upload_file(
                Bucket=Bucket,
                LocalFilePath=loc_path,  # 本地文件的路径 'qq.png'
                Key=f'{path}{file}',  # 上传到桶之后的文件名  'video/qq.png'
                PartSize=1,  # 上传分成几部分
                MAXThread=10,  # 支持最多的线程数
                EnableMD5=False  # 是否支持MD5
            )
            return response
        except:
            return False

    # 获取链接
    def get_url(self, Bucket, path, file):
        try:
            download_url = self.client.get_presigned_url(
                Bucket=Bucket,
                Key=f'{path}{file}',  # video/qq.png
                Method='GET',
            )
            return download_url
        except Exception as E:
            print('Fr包err cnd获取路径失败', E)


class RetJson:

    @classmethod
    def data_list(cls, data):
        if data is None:
            return []
        return data

    @classmethod
    def data_dict(cls, data):
        if data is None:
            return {}
        return data

    @classmethod
    def ret_json(cls, code, msg, data_list, data_dict, code_remark=None):
        data_list = cls.data_list(data_list)
        data_dict = cls.data_dict(data_dict)
        if code_remark:
            return JsonResponse({
                'code': code,
                'msg': msg,
                'code_remark': code_remark,
                'data_list': data_list,
                'data_dict': data_dict
            })
        return JsonResponse({
            'code': code,
            'msg': msg,
            'data_list': data_list,
            'data_dict': data_dict
        })

    @classmethod
    def code200(cls, msg='ok', data_list=None, data_dict=None):
        return cls.ret_json(200, msg, data_list, data_dict)

    @classmethod
    def code201(cls, msg='ok', data_list=None, data_dict=None):
        return cls.ret_json(201, msg, data_list, data_dict, 201)

    @classmethod
    def code202(cls, msg='ok', data_list=None, data_dict=None):
        return cls.ret_json(202, msg, data_list, data_dict, 202)

    @classmethod
    def code400(cls, msg='err', data_list=None, data_dict=None):
        return cls.ret_json(400, msg, data_list, data_dict)

    @classmethod
    def code404(cls, msg='err', data_list=None, data_dict=None):
        return cls.ret_json(404, msg, data_list, data_dict, 404)

    @classmethod
    def code500(cls, msg='err', data_list=None, data_dict=None):
        return cls.ret_json(500, msg, data_list, data_dict)

    @classmethod
    def code501(cls, msg='err', data_list=None, data_dict=None):
        return cls.ret_json(501, msg, data_list, data_dict, 501)

    @classmethod
    def code502(cls, msg='err', data_list=None, data_dict=None):
        return cls.ret_json(502, msg, data_list, data_dict, 502)


# myself 高阳本人信息
class MyGy:

    def __init__(self, **kwargs):
        self.fr1997_config_dict = cache_get("fr1997_config_dict")

    # 获取信息
    def get_myself_info(self):
        return self.fr1997_config_dict

    # 获取出生年龄等信息
    def get_age_info(self):
        name = self.fr1997_config_dict['name']
        return name


# 字段的统一
class J_Field:
    __keyword__ = F_keyword


class AllKeyword:
    table = config_dict['db_name']['table12']

    df_wx_index = 1
    df_wx_competition = 1

    df_xhs_index = 0
    df_xhs_competition = 1
    df_xhs_company_count = 0

    def __init__(self):
        pass

    # 综合指数
    @staticmethod
    def all_index(dy_index, wx_index, xhs_index):
        """
        计算逻辑：
        1. 用关键词在（每个平台中的搜索指数/三个平台中的搜索指数总和）计算出三个平台的比例
        2. 抖音搜索指数 * 1中计算出的抖音的比例 + 微信搜索指数 * 1中计算出的微信的比例 + 小红书搜索指数 * 1中计算出的小红书的比例

        :param dy_index: 抖音指数
        :param wx_index: 微信指数
        :param xhs_index: 小红书指数
        :return: 综合指数
        """
        # 计算总搜索指数
        index_all = dy_index + wx_index + xhs_index

        # 避免除以零的情况
        if index_all == 0:
            return 0

        # 计算各个平台的比例
        dy_ratio = dy_index / index_all
        wx_ratio = wx_index / index_all
        xhs_ratio = xhs_index / index_all
        keyword_all_index = (dy_index * dy_ratio) + (wx_index * wx_ratio) + (xhs_index * xhs_ratio)
        return round(keyword_all_index, 2)

    # 综合备注
    @staticmethod
    def all_record(dy_record, xhs_record):
        """
        1. 抖音关键词备注和小红书关键词的推荐理由。
        2. 同一个关键词在抖音和小红书平台都有备注和推荐理由，取合集后去重，比如在抖音和小红书中均为蓝海词，备注则显示一次蓝海词
        3. 筛选条件也为抖音和小红书备注和推荐理由合集去重

        :return:
        """
        record_info = config_dict['keyword']['record_info']
        dy_record_list = dy_record.split(',')
        xhs_record_list = xhs_record.split(',')
        for i in xhs_record_list:
            if i in record_info:
                record_str = record_info[i]['record_type']
                if record_str not in dy_record_list:
                    dy_record_list.append(record_str)
        return ','.join(dy_record_list)

    # 综合竞争度
    @staticmethod
    def all_competition(dy, wx, xhs):
        return round((dy + wx + (xhs + 1)) / 3, 2)

    # 综合竞价
    @staticmethod
    def all_company_count(dy, wx):
        return round((dy + wx) / 2, 2)

    # 指数处理
    @staticmethod
    def index_30(index):
        index30 = round(index / 30, 2)
        return index30


class MysqlJike:
    """
        conn_tp 0外网(自动) 1内网(自动) 2测试 3本地 5腾讯
        mysql 方法
            常用：select，insert，update，delete，create，commit
            其他：alter, drop, grant, revoke, start, transaction, rollback, show, describe, use, explain, lock, unlock
    """

    def __init__(self, **kwargs):
        self.conn_tp = kwargs.get('conn_tp', 0)

    # def select(self, sql):
    #     return self.do_select(method='select', sql=sql)

    def select(self, **kwargs):
        print(kwargs)
        sql = "SELECT id,hightitle FROM `cd_shool_list` WHERE id > 0 LIMIT 10"

    def do_select(self, method, sql):
        conn = ModeFunc().db_mysql(path=self.conn_tp)
        try:
            with conn.cursor() as cursor:
                if method == 'select':
                    cursor.execute(sql)
                    return cursor.fetchall()
                else:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"数据库链接错误:{e}")
        finally:
            conn.close()


class WeiXinAuto:

    def __init__(self, **kwargs):
        host = kwargs.get('host', '')
        wx_port = kwargs.get('wx_port', 30001)
        self.base_url = f'http://{host}:{wx_port}/'
        self.headers = {"content-type": "application/json"}

        # 本人 wxid_ebbhdhy9megw22
        self.user_info_v1 = {
            'wxid_cb9xe21jsshf22': {
                'name': '高阳小号',
                'wxid_id': 'wxid_cb9xe21jsshf22',
                'wxid': 'Fr1996forever2',
            },
        }
        self.ai_chat_keyword = ['懒阳阳', '懒洋洋', '懒羊羊', 'lly']

    @staticmethod
    def ret_json(code=200, msg=None, data=None):
        return {'code': code, 'msg': msg, 'data': data}

    def req(self, method='post', url=None, from_data=None):
        # res = requests.post(url=url, headers=self.headers, json={"wxid": wxid, "msg": msg})
        res = requests.post(url=url, headers=self.headers, json=from_data)
        if res.status_code == 200:
            return self.ret_json(200, 'ok', res.json())
        return self.ret_json(500, '错误')

    # 个人 个人信息详情
    def get_self_login_info(self):
        url = f"{self.base_url}GetSelfLoginInfo"
        res_data = self.req(url=url)
        return res_data


class KIL:
    """
        列表记录90天数据
        详情记录全部

        增加字段 keyword_index_list

        如何定义初始值 -> 241120*654
        如何定义增加值 -> 241120*654;1_5
        如何定义减少值 -> 241120*654;1_5;2_-5
    """

    field_kil = 'keyword_index_list'

    # 时间变量
    today = time.strftime("%Y%m%d", time.localtime(int(time.time())))
    today_int = int(time.mktime(time.strptime(today, '%Y%m%d')))

    # 记录转列表
    def kil_list(self, keyword_index_list):
        base_value = 0
        base_time_int = 0
        ret_kil_info = []
        data_list = keyword_index_list.split(';')

        # 每天只有一个数据
        time_str_set = []
        for i in data_list:
            # 初始值
            if '*' in i:
                base_time = int(i.split('*')[0])  # 初始时间
                base_value = int(i.split('*')[1])  # 初始值
                each_index = base_value
                time_int = int(time.mktime(time.strptime(str(base_time), '%Y%m%d')))
                base_time_int = time_int
                time_str = base_time
            # 减法操作
            elif '-' in i:
                each_day = int(i.split('_')[0])
                time_int = base_time_int + 86400 * each_day
                time_str = time.strftime("%Y%m%d", time.localtime(time_int))
                each_index = base_value - int(i.split('_')[-1].split('-')[1])  # 用初始值减去 '-' 后的值
            # 加法操作
            else:
                each_day = int(i.split('_')[0])
                time_int = base_time_int + 86400 * each_day
                time_str = time.strftime("%Y%m%d", time.localtime(time_int))
                each_index = base_value + int(i.split('_')[-1])  # 默认加法，取第6位及后续数字

            if str(time_str) not in time_str_set:
                ret_kil_info.append({
                    'time_str': time_str,
                    'time_int': time_int,
                    'value': each_index,  # 计算后的数值
                })
                time_str_set.append(str(time_str))

        return ret_kil_info

    # 增加新记录 限制天数 一天内重复更新要刷新
    def kul_add(self, kil_list_info, new_m):
        index9 = kil_list_info[-1]

        # 存在更新 不存在插入
        if self.today == index9['time_str']:
            kil_list_info[-1]['value'] = new_m
        else:
            kil_list_info.append({'time_str': self.today, 'time_int': self.today_int, 'value': new_m})

        return kil_list_info[-720:]

    # 记录列表转文本
    def kil_str(self, data_list):
        # 初始化结果字符串和基准值
        result = []
        base_value = None
        base_time_int = None

        for idx, entry in enumerate(data_list):
            value = entry['value']  # 提取数值
            time_int = entry['time_int']  # 提取数值

            if idx == 0:
                # 第一个元素作为初始值，格式为 time*value
                result.append(f"{entry['time_str']}*{value}")
                base_value = value
                base_time_int = time_int
            else:
                # 后续元素比较 value 和 base_value 的差异
                time_part = int((time_int - base_time_int) / 86400)
                diff = value - base_value
                if diff >= 0:
                    result.append(f"{time_part}_{diff}")  # 增加情况
                elif diff < 0:
                    result.append(f"{time_part}_{diff}")  # 减少情况

        return ";".join(result)  # 使用下划线连接结果


mode_feishu = Feishu()  # 飞书app api
mode_time = TimeJike()  # ✅时间处理
mode_text = TextJike()  # 文本处理
mode_data = DataJike()  # 数据处理
mode_spider = SpiderJike()  # 数据请求
mode_django = DjangoJike()  # django配置
mode_douyin = DouyinJike()  # douyin配置
mode_wx = WeiXinAuto()  # douyin配置
mode_xhs = XhsJike()  # douyin配置
mode_pros = ModeStatic()  # 其它函数
mode_cos = Cos()  # cos
mode_fr_cos = Cos(server_select='personal')  # cos 高阳
mode_myself = MyGy()
mode_mysql = MysqlJike()

mode_pro = ModeFunc()  # main
JFD = J_Field()

# kil = KIL()
# db_data_v1 = {
#     'keyword': '阿里巴巴',
#     'mounth_search_index': 4557369,
#     # 'keyword_index_list': '20241118*4557399;1_5;2_-5'
# }
#
# new_m = 455587
#
# # 存储初始值
# if 'keyword_index_list' not in db_data_v1:
#     db_data_v1[kil.field_kil] = kil.kil_str([{'time_str': kil.today, 'time_int': kil.today_int, 'value': new_m}])
# else:
#     # 存在 解析数据
#     kil_list_info = kil.kil_list(db_data_v1['keyword_index_list'])
#
#     # 加入初始值
#     kil_list_info_new = kil.kul_add(kil_list_info, new_m)
#     print(kil_list_info_new)
#
#     # # 逆过程
#     # kkk = [{'time_str': '20241121', 'time_int': 1732118400, 'value': 4557399},
#     #        {'time_str': '20241122', 'time_int': 1732204800, 'value': 4557404},
#     #        {'time_str': '20241123', 'time_int': 1732291200, 'value': 4557394}]
#     db_data_v1[kil.field_kil] = kil.kil_str(kil_list_info_new)
# print(db_data_v1)
