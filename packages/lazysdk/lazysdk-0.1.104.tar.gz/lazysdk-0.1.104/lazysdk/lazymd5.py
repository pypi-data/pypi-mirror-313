#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import requests
import hashlib


def md5_file(
        file_path: str = None,
        file_url: str = None
):
    """
    计算文件的md5
    :param file_path: 本地文件路径
    :param file_url: 网络文件地址
    """
    # 文件名不影响md5
    d5 = hashlib.md5()
    if file_path:
        with open(r'%s' % file_path, 'rb') as f:
            while True:
                data = f.read(2048)
                if not data:
                    break
                d5.update(data)  # update添加时会进行计算
        return d5.hexdigest()
    elif file_url:
        resp = requests.get(file_url)
        d5.update(resp.content)  # update添加时会进行计算
        return d5.hexdigest()
    else:
        return


def md5_str(
        content,
        encoding='UTF-8'
):
    d5 = hashlib.md5()
    d5.update(content.encode(encoding=encoding))  # update添加时会进行计算
    return d5.hexdigest()
