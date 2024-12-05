#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   fetch.py
# @Time    :   2021/04/09 15:59:10
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :   None

# here put the import lib
import time
import requests
import urllib3
from curl_cffi import requests as ja3_requests

# 禁用安全请求警告
urllib3.disable_warnings()


def format_proxies(proxies=None, http2=False):
    """

    :param proxies:
    :param http2:
    :return:
    """
    # 格式化代理
    if isinstance(proxies, dict):
        _proxies = proxies

    elif isinstance(proxies, str):
        if http2:
            _proxies = {
                "http://": "",
                "https://": "",
            }
        else:
            _proxies = {
                "http": "",
                "https": "",
            }
        for k in _proxies.keys():
            _proxies[k] = proxies if proxies.startswith(
                'http') else f'http://{proxies}'
    else:
        _proxies = None
    return _proxies


def http_fetch(url, method='GET', data=None, headers=None, proxies=None, ja3_enable=False, http2=False, impersonate="safari15_3", **kwargs):
    """
    :param url: 要请求的url
    :param method: 请求参数 支持 get/post
    :param data: post请求时的请求body
    :param headers: 请求头
    :param proxies: 代理， 支持使用封装的类型 或者使用固定url, 固定的url格式为  1.2.3.4:8080
    :param ja3_enable: ja3指纹绕过
    :param http2: 是否使用http2
    :return: 请求结果
    """
    _method = method.upper()
    if _method not in ('GET', 'POST'):
        return int(time.time()), f'暂不支持 {method} 请求方法', None

    # 格式化请求头
    if not isinstance(headers, dict):
        kwargs['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
    else:
        kwargs['headers'] = headers
    kwargs['proxies'] = format_proxies(proxies, http2=http2)
    if 'verify' not in kwargs:
        kwargs['verify'] = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (6.05, 8.05)
    try:
        if http2 or ja3_enable:
            # elif ja3_enable:
            if _method == 'GET':
                _response = ja3_requests.get(
                    url, impersonate=impersonate, **kwargs)
            else:
                _response = ja3_requests.post(
                    url, data=data, impersonate=impersonate, **kwargs)
        else:
            if _method == 'GET':
                _response = requests.get(url, **kwargs)
            else:
                _response = requests.post(url, data=data, **kwargs)
    except Exception as e:
        return int(time.time()), repr(e), None
    else:
        return int(time.time()), _response.status_code, _response
