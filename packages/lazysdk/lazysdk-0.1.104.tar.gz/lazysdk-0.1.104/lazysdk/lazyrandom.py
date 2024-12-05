#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import string
import random


def random_str(
        str_length: int = 8,
        ascii_lowercase: bool = True,  # 小写字母
        ascii_uppercase: bool = True,  # 大写字母
        numbers: bool = True,  # 0-9的数字
        repeat: bool = True
):
    """
    按照规则生成某个长度的随机字符串
    :param str_length: 要生成的字符串长度
    :param ascii_lowercase: 包含小写字母
    :param ascii_uppercase: 包含大写字母
    :param numbers: 包含0-9的数字
    :param repeat: 是否重复，默认为True，False不重复采样，True可重复采样
    """
    random_sample = ""
    if ascii_lowercase is True:
        random_sample += string.ascii_lowercase
    if ascii_uppercase is True:
        random_sample += string.ascii_uppercase
    if numbers is True:
        random_sample += string.digits
    if repeat:
        # 可重复采样
        value = ''
        for _ in range(str_length):
            value += random.sample(
                random_sample,
                1
            )[0]
    else:
        # 不重复采样
        value = ''.join(
            random.sample(
                random_sample,
                str_length
            )
        )
    return value
