#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import copy
from collections import OrderedDict
from urllib import parse


def dict_list_ranker_x(dict_list, rank_by_list):
    """
    对dict组成的list按照某个元素重新排序
    可对多个元素排序,目前支持2个
    rank_by_list：[['a','asc']]
    :return:
    """
    ranker_res_list = list()
    for each_dict in dict_list:
        each_rank_by_value_1 = each_dict.get(rank_by_list[0][0])
        each_rank_by_value_2 = each_dict.get(rank_by_list[1][0])
        if len(ranker_res_list) == 0:
            ranker_res_list.append(each_dict)
        else:
            pos_num = 0
            for each_ranker_res in ranker_res_list:
                each_ranker_res_rank_by_value_1 = each_ranker_res.get(rank_by_list[0][0])
                each_ranker_res_rank_by_value_2 = each_ranker_res.get(rank_by_list[1][0])
                if rank_by_list[0][1].lower() == 'asc' and rank_by_list[1][1].lower() == 'desc':
                    if each_rank_by_value_1 > each_ranker_res_rank_by_value_1:
                        pos_num += 1
                    elif each_rank_by_value_1 == each_ranker_res_rank_by_value_1:
                        if each_rank_by_value_2 < each_ranker_res_rank_by_value_2:
                            pos_num += 1
                        else:
                            pass
                    elif each_rank_by_value_1 < each_ranker_res_rank_by_value_1:
                        pass
            ranker_res_list.insert(pos_num, each_dict)
    return ranker_res_list


def dict_list_ranker(dict_list, rank_by_list):
    """
    对dict组成的list按照某个元素重新排序
    可对多个元素排序,目前支持1个
    rank_by_list：[['a','asc']]
    :return:
    """
    ranker_res_list = list()
    for each_dict in dict_list:
        each_rank_by_value_1 = each_dict.get(rank_by_list[0][0])
        if len(ranker_res_list) == 0:  # 如果结果列表为空，放入初始值
            ranker_res_list.append(each_dict)
        else:
            pos_num = 0
            for each_ranker_res in ranker_res_list:
                each_ranker_res_rank_by_value_1 = each_ranker_res.get(rank_by_list[0][0])
                if each_rank_by_value_1 > each_ranker_res_rank_by_value_1:
                    pos_num += 1
                else:
                    pass
            ranker_res_list.insert(pos_num, each_dict)
    if rank_by_list[0][1].lower() == 'asc':
        return ranker_res_list
    else:
        ranker_res_list.reverse()
        return ranker_res_list


def dict_list_group(list_in, by):
    """
    将dict组成的list按照某个key的值分组，分组后组成新的dict嵌套list
    :param list_in:
    :param by:
    :return:
    """
    if not list_in:
        return
    else:
        by_list = list()
        for each_dict in list_in:
            by_value = each_dict.get(by)
            by_list.append(by_value)
        by_set = set(by_list)
        group_dict = dict()
        for each_by in by_set:
            group_dict[each_by] = list()
        for each_dict in list_in:
            by_value = each_dict.get(by)
            group_dict[by_value].extend([each_dict])
        return group_dict


def dict_key_f(in_dict):
    """
    将以驼峰方式命名的dict转换为下划线方式
    """
    out_dict = dict()
    for key, value in in_dict.items():
        # key_split = list(key)
        # print(key, key_split)
        key_split_new = list()
        for index, temp_key in enumerate(key):
            if temp_key.isupper() is True:
                if index == 0:
                    key_split_new.append(temp_key.lower())
                else:
                    key_split_new.append('_')
                    key_split_new.append(temp_key.lower())
            else:
                key_split_new.append(temp_key)
        key_new = ''.join(key_split_new)
        # print(key_new, key_split_new)
        out_dict[key_new] = value
    return out_dict


def list_dict_key_f(in_list):
    """
    将以驼峰方式命名的list嵌套dict转换为下划线方式
    """
    out_list = list()
    for each_dict in in_list:
        out_dict = dict_key_f(each_dict)
        out_list.append(out_dict)
    return out_list


def dict_value_parse(dict_in):
    # 对字典的值进行解码
    dict_out = dict()
    for key, value in dict_in.items():
        if isinstance(value, str):
            dict_out[key] = parse.unquote(value)
        else:
            dict_out[key] = value
    return dict_out


def list_dict_value_parse(list_in):
    # 在dict上面封装一层list，解码
    list_out = list()
    for each_list_in in list_in:
        dict_out = dict_value_parse(dict_in=each_list_in)
        list_out.append(dict_out)
    return list_out


def dict_tiler(dict_in, connector_str='-'):
    """
    字典展开器
    只展开一层
    将嵌套了一层的dict铺展开，键值之间用"-"连接
    针对纯dict形式
    :param dict_in: 输入一个待处理的dict
    :param connector_str: 输入连接符
    :return: 输出处理好的dict
    """
    dict_f = dict()
    if dict_in is None:
        return
    elif len(dict_in) == 0:
        return
    else:
        for key in dict_in:
            value = dict_in.get(key)
            if isinstance(value, dict):  # 如果某个key的值是dict，则展开这组
                for each_value_key in value:
                    dict_f['%s%s%s' % (key, connector_str, each_value_key)] = value.get(each_value_key)
            else:
                dict_f[key] = value
        return dict_f


def list_dict_tiler(list_in, connector_str='-'):
    list_out = list()
    for each in list_in:
        dict_f = dict_tiler(dict_in=each, connector_str=connector_str)
        list_out.append(dict_f)
    return list_out


def list_same_order_dict(
        list_data: list = None,
        na_value=None,
        keys_sort: list = None
) -> list:
    """
    list重排格式化，将单层dict组成的list按照全部key的顺序排序并补充缺失值
    :param list_data: 原始list
    :param na_value: 缺失值的默认值
    :param keys_sort: 指定顺序,按照指定列的顺序先排，不包含的向后排
    :return list_data_f: 处理后的结果

    test data:
        [
            {'a': 1},
            {'b': 2},
            {'b': 2, 'a': 1},
            {'c': 21}
        ]
    """
    keys = list()  # 存储所有的key
    for each_dict in list_data:
        # 遍历list中的每个dict
        each_keys = list(each_dict.keys())  # 提取当前dict的所有key
        for each_key in each_keys:
            # 遍历，得到全量唯一的key
            if each_key in keys:
                continue
            else:
                keys.append(each_key)
    keys.sort()  # 先按照升序排序一次
    if keys_sort:
        keys_new = copy.deepcopy(keys_sort)  # 先直接拷贝一下排序表
        for each_key in keys:
            # 遍历生成的key列表
            if each_key in keys_new:
                # 如果遍历的key已存在，将跳过
                continue
            else:
                # 如果遍历的key不已存在，则追加
                keys_new.append(each_key)
    else:
        keys_new = copy.deepcopy(keys)
    list_data_f = list()  # 存储处理后的数据
    for each_dict in list_data:
        each_dict_order = OrderedDict()  # 有序字典
        for each_key in keys_new:
            each_dict_order[each_key] = each_dict.get(each_key, na_value)
        list_data_f.append(each_dict_order)
    return list_data_f


def list_dict_filter(
        list_in: list,
        filter_key,
        filter_value
):
    """
    从[{},{}]中按照某个key-value条件筛选出符合条件的记录
    """
    list_out = list(filter(lambda x: x[filter_key] == filter_value, list_in))
    return list_out


def key_max_value(
        list_in: list,
        key
):
    """
    求list嵌套的dict中某个key的最大值
    """
    max_value = None
    for each in list_in:
        key_value = each.get(key)
        if key_value:
            if max_value is None or key_value > max_value:
                max_value = copy.deepcopy(key_value)
            else:
                continue
        else:
            continue
    return max_value


def key_min_value(
        list_in: list,
        key
):
    """
    求list嵌套的dict中某个key的最小值
    """
    min_value = None
    for each in list_in:
        key_value = each.get(key)
        if key_value:
            if min_value is None or key_value < min_value:
                min_value = copy.deepcopy(key_value)
            else:
                continue
        else:
            continue
    return min_value
