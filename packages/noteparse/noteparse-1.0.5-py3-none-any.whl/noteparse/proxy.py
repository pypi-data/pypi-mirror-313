# -*- coding: UTF-8 -*-
'''
@File    ：proxy_pool.py
@Author  ：VerSion/08398
@Date    ：2023/12/05 10:18 
@Corp    ：Uniview
'''

import time
from selenium import webdriver
import requests
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy,ProxyType
from datetime import datetime
_user_key = 'NP4342851E'
_proxy_instance = None
_driver_instance = None



def get_new_ip(ip_count=1):
    headers = {'User-Agent': UserAgent().random}
    url = f'http://15397190355.user.xiecaiyun.com/api/proxies?action=getJSON&key=NP5399BC3F&count=1&word=&rand=false&norepeat=false&detail=true&ltime=&idshow=true'
    # url = f'http://imdlxin.user.xiecaiyun.com/api/proxies?action=getJSON&key=NP0D3CB941&count=&word=&rand=false&norepeat=false&detail=true&ltime=&idshow=true'
    r = requests.get(url,headers=headers)
    r.close()
    if r.status_code != 200:
        raise Exception('代理接口请求失败')
    if not r.json()['success']:
        raise Exception('获取代理失败：' + r.json()['message'])
    proxy_list = r.json()['result']
    if len(proxy_list) == 0:
        raise Exception('暂无可用代理')
    return proxy_list




def get_singleton(new_flag=False):
    global _proxy_instance
    if new_flag or _proxy_instance is None or int(time.time()) > _proxy_instance['ltime']:
        _proxy_instance = get_new_ip(1)[0]
        # proxy = "http://"+proxy_list[0]['ip'].__str__()+":"+proxy_list[0]['port'].__str__()

    return _proxy_instance

# ip不可用时更新代理ip
def reflash_singleton():
    global _proxy_instance
    _proxy_instance = get_new_ip(1)[0]
    print("代理ip异常,更新ip",datetime.now())

    return _proxy_instance

def get_new_driver():
    user = '15397190355'
    pwd = '147258'
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-gpu')
    proxy_list = get_new_ip()
    proxyIp = "http://"+proxy_list[0]['ip'].__str__()+":"+proxy_list[0]['port'].__str__()
    # proxyIp = "http://"+str(proxy_list[0])
    # proxyIp = f"http://{user}:{pwd}@{str(proxy_list[0]['ip'])}:{str(proxy_list[0]['port'])}"
    print('----daili',proxyIp)

    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = f"http://{user}:{pwd}@{str(proxy_list[0]['ip'])}:{str(proxy_list[0]['port'])}"
    # proxy.ssl_proxy = f"https://{user}:{pwd}@{str(proxy_list[0]['ip'])}:{str(proxy_list[0]['port'])}"
    option.add_argument('--proxy-server=%s' % proxyIp)

    wireOption = {
        'proxy':{
            'http':f"http://{user}:{pwd}@{str(proxy_list[0]['ip'])}:{str(proxy_list[0]['port'])}",
            'https': f"http://{user}:{pwd}@{str(proxy_list[0]['ip'])}:{str(proxy_list[0]['port'])}",
            'ssl_verify': False
            
        }
    }
    # 放弃样式\图像\子帧
    # option.page_load_strategy='eager'
    # driver = wirewebdriver.Chrome(options=option,seleniumwire_options=wireOption)
    driver = webdriver.Chrome(options=option)
    return driver

def get_daily_ip():
    url = f'http://imdlxin.user.xiecaiyun.com/api/proxies?action=getJSON&key=NP0D3CB941&count=&word=&rand=false&norepeat=false&detail=true&ltime=&idshow=true'
    headers = {'User-Agent': UserAgent().random}

    r = requests.get(url,headers=headers)
    r.close()
    if r.status_code != 200:
        raise Exception('代理接口请求失败')
    if not r.json()['success']:
        raise Exception('获取代理失败：' + r.json()['message'])
    proxy_list = r.json()['result']
    if len(proxy_list) == 0:
        raise Exception('暂无可用代理')
    return proxy_list[0]

def get_driver():
    global _driver_instance
    global _proxy_instance

    if _driver_instance is None:
        print('---创建driver')
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')
        proxyInfo = get_singleton()
        proxyIp = "http://"+proxyInfo['ip'].__str__()+":"+proxyInfo['port'].__str__()
        print('--daili--:',f'--proxy-server={proxyIp}')
        option.add_argument(f'--proxy-server={proxyIp}')
        # 放弃样式\图像\子帧
        # prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
        # option.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=option)
        option.add_experimental_option("detach", True)
        # driver.set_page_load_timeout(20)
        # driver.set_script_timeout(20)
        _driver_instance = driver
        return driver
    elif int(time.time()) > _proxy_instance['ltime']:
        print('---更换driver新IP')
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')
        proxyInfo = get_singleton()
        proxyIp = "http://"+proxyInfo['ip'].__str__()+":"+proxyInfo['port'].__str__()
        print('--daili--:',proxyIp)
        option.add_argument(f'--proxy-server={proxyIp}')
        driver = webdriver.Chrome(options=option)
        # driver.set_page_load_timeout(20)
        # driver.set_script_timeout(20)
        _driver_instance = driver
        return driver
    else:
        return _driver_instance

# 通过标题和地址查询省份
def getProvinceIdByName(address,bidUnit,title):
    for province in provinceList:
        if address !=None and province['dicValue'] in address:
            return province['provinceCode']
        elif title != None and province['dicValue'] in title:
            return province['provinceCode']
        elif bidUnit != None and province['dicValue'] in bidUnit:
            return province['provinceCode']
    return ''

provinceList = [
    {
        'dicValue': '总部',
        'dicCode': '10',
        'provinceCode': '110000'
    },
    {
        'dicValue': '北京',
        'dicCode': '11',
        'provinceCode': '110000'
    },
    {
        'dicValue': '天津',
        'dicCode': '12',
        'provinceCode': '120000'
    },
    {
        'dicValue': '河北',
        'dicCode': '13',
        'provinceCode': '130000'
    },
    {
        'dicValue': '山西',
        'dicCode': '14',
        'provinceCode': '140000'
    },
    {
        'dicValue': '内蒙古',
        'dicCode': '15',
        'provinceCode': '150000'
    },
    {
        'dicValue': '辽宁',
        'dicCode': '21',
        'provinceCode': '210000'
    },
    {
        'dicValue': '吉林',
        'dicCode': '22',
        'provinceCode': '220000'
    },
    {
        'dicValue': '黑龙江',
        'dicCode': '23',
        'provinceCode': '230000'
    },
    {
        'dicValue': '上海',
        'dicCode': '31',
        'provinceCode': '310000'
    },
    {
        'dicValue': '江苏',
        'dicCode': '32',
        'provinceCode': '320000'
    },
    {
        'dicValue': '浙江',
        'dicCode': '33',
        'provinceCode': '330000'
    },
    {
        'dicValue': '安徽',
        'dicCode': '34',
        'provinceCode': '340000'
    },
    {
        'dicValue': '福建',
        'dicCode': '35',
        'provinceCode': '350000'
    },
    {
        'dicValue': '江西',
        'dicCode': '36',
        'provinceCode': '360000'
    },
    {
        'dicValue': '山东',
        'dicCode': '37',
        'provinceCode': '370000'
    },
    {
        'dicValue': '河南',
        'dicCode': '41',
        'provinceCode': '410000'
    },
    {
        'dicValue': '湖北',
        'dicCode': '42',
        'provinceCode': '420000'
    },
    {
        'dicValue': '湖南',
        'dicCode': '43',
        'provinceCode': '430000'
    },
    {
        'dicValue': '广东',
        'dicCode': '44',
        'provinceCode': '440000'
    },
    {
        'dicValue': '广西',
        'dicCode': '45',
        'provinceCode': '450000'
    },
    {
        'dicValue': '海南',
        'dicCode': '46',
        'provinceCode': '460000'
    },
    {
        'dicValue': '重庆',
        'dicCode': '50',
        'provinceCode': '500000'
    },
    {
        'dicValue': '四川',
        'dicCode': '51',
        'provinceCode': '510000'
    },
    {
        'dicValue': '贵州',
        'dicCode': '52',
        'provinceCode': '520000'
    },
    {
        'dicValue': '云南',
        'dicCode': '53',
        'provinceCode': '530000'
    },
    {
        'dicValue': '西藏',
        'dicCode': '54',
        'provinceCode': '540000'
    },
    {
        'dicValue': '陕西',
        'dicCode': '61',
        'provinceCode': '610000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
    {
        'dicValue': '青海',
        'dicCode': '63',
        'provinceCode': '630000'
    },
    {
        'dicValue': '宁夏',
        'dicCode': '64',
        'provinceCode': '640000'
    },
    {
        'dicValue': '新疆',
        'dicCode': '65',
        'provinceCode': '650000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
    {
        'dicValue': '甘肃',
        'dicCode': '62',
        'provinceCode': '620000'
    },
       
]