#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from ua_parser import user_agent_parser
from user_agents import parse
ua_match_ignore_values = ['Other', None]


def dict_values_match(
        dict_a: dict,
        dict_b: dict,
        ignore_values: list = None  # 忽略值，例如：['Other', None]
):
    """
    统计字典的value匹配量
    """
    dict_keys = list()
    dict_keys.extend(dict_a.keys())
    dict_keys.extend(dict_b.keys())
    dict_keys = set(dict_keys)
    count_all = 0  # 有效比对元素总数
    count_match = 0  # 对比结果匹配数
    for user_agent_key in dict_keys:
        each_value_a = dict_a.get(user_agent_key)
        each_value_b = dict_b.get(user_agent_key)
        if each_value_a == each_value_b:
            if ignore_values is not None and each_value_a in ignore_values:
                continue
            else:
                count_all += 1
                count_match += 1
        else:
            count_all += 1
    return {'count_all': count_all, 'count_match': count_match}


def ua_similarity(
        ua_a: str,
        ua_b: str,
        user_agent_match: bool = False,
        os_match: bool = True,
        device_match: bool = True
):
    """
    ua相似性算法，返回一个0-1之间的数，0为完全不匹配，1为完全匹配
    通过对user_agent、os、device中的元素进行比对，按照比对的成功个数/比对的总个数作为匹配率

    ua_match_ignore_values为无效或者无法失败的值的情况，不作为比对依据

    ua格式化后的格式为:
        {
            'user_agent': {
                'family': 'Other',
                'major': None,
                'minor': None,
                'patch': None
            },
            'os': {
                'family': 'Other',
                'major': None,
                'minor': None,
                'patch': None,
                'patch_minor': None
            },
            'device': {
                'family': 'Other',
                'brand': None,
                'model': None
            },
            'string': 'ua_string'
        }
    """
    if ua_a == ua_b:
        return 1
    else:
        ua_a_parser = user_agent_parser.Parse(ua_a)
        ua_b_parser = user_agent_parser.Parse(ua_b)

        match_res = list()
        if user_agent_match is True:
            user_agent_match_res = dict_values_match(
                dict_a=ua_a_parser.get('user_agent'),
                dict_b=ua_b_parser.get('user_agent'),
                ignore_values=ua_match_ignore_values
            )
            match_res.append(user_agent_match_res)
        else:
            pass
        if os_match is True:
            os_match_res = dict_values_match(
                dict_a=ua_a_parser.get('os'),
                dict_b=ua_b_parser.get('os'),
                ignore_values=ua_match_ignore_values
            )
            match_res.append(os_match_res)
        else:
            pass
        if device_match is True:
            device_match_res = dict_values_match(
                dict_a=ua_a_parser.get('device'),
                dict_b=ua_b_parser.get('device'),
                ignore_values=ua_match_ignore_values
            )
            match_res.append(device_match_res)
        else:
            pass

        # 计算匹配度
        count_all = 0  # 有效比对元素总数
        count_match = 0  # 对比结果匹配数
        for each_match_res in match_res:
            count_all += each_match_res.get('count_all')
            count_match += each_match_res.get('count_match')
        if count_all == 0:
            return 0
        else:
            return count_match/count_all


def ua_match(
        ua1: str,
        ua2: str,
        match_os: bool = True,
        match_device: bool = True
):
    """
    按照os和device匹配信息，匹配成功返回True，匹配失败返回False
    """
    user_agent1 = parse(ua1)
    user_agent2 = parse(ua2)
    user_agent1_os = user_agent1.os
    user_agent1_device = user_agent1.device
    user_agent2_os = user_agent2.os
    user_agent2_device = user_agent2.device
    if match_os and match_device:
        user_agent1_str = str(user_agent1_os) + str(user_agent1_device)
        user_agent2_str = str(user_agent2_os) + str(user_agent2_device)
    elif match_os and not match_device:
        user_agent1_str = str(user_agent1_os)
        user_agent2_str = str(user_agent2_os)
    elif not match_os and match_device:
        user_agent1_str = str(user_agent1_device)
        user_agent2_str = str(user_agent2_device)
    else:
        return False
    if user_agent1_str == user_agent2_str:
        return True
    else:
        return False
