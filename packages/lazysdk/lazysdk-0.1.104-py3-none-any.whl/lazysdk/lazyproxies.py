#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""


def make_proxies(
        port,
        host='localhost',
        protocol='http'
):
    """
    这里设置本地开启代理的时候需要将脚本开到对应端口的代理上，否则无法使用代理
    """
    proxy_meta = f"{protocol}://{host}:{port}"
    proxies = {
        "http": proxy_meta,
        "https": proxy_meta
    }
    return proxies
