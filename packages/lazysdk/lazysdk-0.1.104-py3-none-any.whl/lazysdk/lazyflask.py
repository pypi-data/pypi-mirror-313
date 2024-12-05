#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import json


def make_json_callback_return(
        data=None,
        callback: str = None
):
    from flask import jsonify
    """
    判断包装返回，用以兼容ajax的jsonp请求，以实现支持前端跨域
    """
    if callback is None:
        # 无callback参数，正常返回json
        return jsonify(data)
    else:
        # 有callback参数，拼接字符串返回
        if type(data) == 'json':
            return '%s(%s)' % (callback, json.dumps(data))
        else:
            return '%s(%s)' % (callback, data)
