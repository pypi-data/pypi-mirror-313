#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import json

import requests


def get_public_ip() -> str:
    """
    获取当前网络公网ip地址
    备用地址：http://www.3322.org/dyndns/getip
    """
    import requests
    import json
    origin_ip = ''
    try:
        request_url = "http://httpbin.org/ip"
        response = requests.get(url=request_url)
        origin_ip = json.loads(response.text).get("origin")
    finally:
        return origin_ip


def get_local_ip() -> str:
    """
    获取内网ip地址
    """
    import socket
    ip = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def get_ip() -> dict:
    """
    获取当前网络ip地址（含有公网ip和内网ip）
    """
    origin_ip = get_public_ip()  # 获取公网ip
    local_ip = get_local_ip()  # 获取内网ip
    return {'origin_ip': origin_ip, 'local_ip': local_ip}


def get_ip_addr(ip: str):
    """
    查询ip归属地
    """
    api_url = f'http://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true'
    response = requests.get(api_url)
    response_text = response.text.replace("\\", "-")
    addr = json.loads(response_text)['addr']
    return addr
