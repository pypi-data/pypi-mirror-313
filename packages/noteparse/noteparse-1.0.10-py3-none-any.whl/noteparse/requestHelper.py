import noteparse.proxyHelper as proxyHelper
import requests,time,re
from datetime import datetime
import json
import urllib3
from urllib.parse import urlencode
import ssl
import traceback
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context


_proxy_user = '15397190355'
_proxy_pass = '147258'

daily_proxy_user = 'imdlxin'
daily_proxy_pass = 'imdlxin'

originHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        
    }

def request_get(url,headers=originHeader):
    try:
        proxy_info = proxyHelper.get_singleton()
        proxies = {
            'http': f'http://{_proxy_user}:{_proxy_pass}@{str(proxy_info["ip"])}:{str(proxy_info["port"])}',
            'https': f'http://{_proxy_user}:{_proxy_pass}@{str(proxy_info["ip"])}:{str(proxy_info["port"])}'
        }
       
        response = requests.get(url=url,verify=False,proxies=proxies,timeout=30,headers=headers)
        return response
    except Exception as request_err:
        print(datetime.now(),'get请求失败,2s后重试',url,request_err)
        if 'Unable to connect to proxy' in str(request_err):
            proxyHelper.reflash_singleton()
        time.sleep(2)
        return request_get(url)
        # else:
        #     return None

def request_post_urlencode(url,param,headers=originHeader):
    try:
        proxy_info = proxyHelper.get_singleton()
        proxies = {
            'http': f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}',
            'https': f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}'
        }
        response = requests.post(url=url,data=param,headers=headers,verify=False,proxies=proxies,timeout=30)
        return response
    except Exception as request_err:
        print('post请求失败',url,param,request_err)
        traceback.print_exc()
        if 'Remote end closed connection without response' in str(request_err) or 'timed out' in str(request_err) or 'Unable to connect to proxy' in str(request_err):
            proxyHelper.reflash_singleton()
        time.sleep(5)
        return request_post_urlencode(url,param)
    
def request_post_json(url,param,headers=originHeader):
    try:
        headers['Content-Type'] = 'application/json;charset=UTF-8'
        proxy_info = proxyHelper.get_singleton()
        proxies = {
            'http': f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}',
            'https': f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}'
        }
        response = requests.post(url=url,data=json.dumps(param),headers=headers,verify=False,proxies=proxies,timeout=30)
        return response
    except Exception as request_err:
        print('post请求失败',url,param,request_err)
        if 'Remote end closed connection without response' in str(request_err) or 'timed out' in str(request_err) or 'Unable to connect to proxy' in str(request_err):
            proxyHelper.reflash_singleton()
        time.sleep(5)
        return request_post_json(url,param)


ctx = ssl.create_default_context()
# ctx.set_ciphers('AES128-SHA')
ctx.set_ciphers('AES128-SHA')

# daily_proxy = proxy.get_daily_ip()
# proxy_url = f'http://{daily_proxy_user}:{daily_proxy_pass}@{daily_proxy["ip"]}:{str(daily_proxy["port"])}'

timeout = urllib3.Timeout(connect=30,read=30)
# httpInston = urllib3.ProxyManager(proxy_url,ssl_context=ctx)
httpInston = None

def refreshHttp():
    print(datetime.now(),'刷新代理IP')
    global httpInston
    proxy_info = proxyHelper.get_singleton()
    # # 设置代理信息，这里以HTTP代理为例，如果是HTTPS代理，则将'http'改为'https'
    proxy_url = f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}'
    # daily_proxy = proxy.get_daily_ip()
    # proxy_url = f'http://{daily_proxy_user}:{daily_proxy_pass}@{daily_proxy["ip"]}:{str(daily_proxy["port"])}'

    httpInston = urllib3.ProxyManager(proxy_url,ssl_context=ctx)

# 自定义加密套件的post请求
def request_urllib3_get(url):
    global httpInston
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    # proxy_info = proxy.get_singleton()
    # # 设置代理信息，这里以HTTP代理为例，如果是HTTPS代理，则将'http'改为'https'
    # proxy_url = f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}'

    # 使用 urllib.parse.urlencode 编码表单数据
    # encoded_params = urlencode(param)

    # 创建一个带有自定义 SSL 上下文的 HTTP 连接池
    # http = urllib3.PoolManager(ssl_context=ctx)
    # 创建一个 SSL 上下文

    # proxy_info = proxy.get_singleton()
    # 设置代理信息，这里以HTTP代理为例，如果是HTTPS代理，则将'http'改为'https'
    # proxy_url = f'http://{_proxy_user}:{_proxy_pass}@{proxy_info["ip"]}:{str(proxy_info["port"])}'
    if httpInston:
        try:
            # 发送 POST 请求
            response = httpInston.request(
                'GET',
                url,
                headers=header,
                timeout=timeout
            )
            # 打印响应内容
            result = response.data.decode('utf-8')
            return result
        except Exception as e:
            print(datetime.now(),'请求发送失败,刷新代理5S后重试',e)
            refreshHttp()
            time.sleep(5)
            return request_urllib3_get(url)
    else:
        refreshHttp()
        return request_urllib3_get(url)
    

# 自定义加密套件的post请求
def request_urllib3_post(url,param):
    global httpInston
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    if httpInston:
        try:
            # 发送 POST 请求
            response = httpInston.request(
                'POST',
                url,
                headers=header,
                timeout=timeout,
                body=param,
                
            )
            # 打印响应内容
            result = response.data.decode('utf-8')
            return result
        except Exception as e:
            print(datetime.now(),'请求发送失败,刷新代理5S后重试',e)
            refreshHttp()
            time.sleep(5)
            return request_urllib3_get(url)
    else:
        refreshHttp()
        return request_urllib3_get(url)

# def request_urllib3_post(url,param):
    