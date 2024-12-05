#!/usr/bin/env python3
# coding = utf8
"""
    这个模块的作用非常简单
    就是将数据表显示的好看一点
"""

import json
import datetime
from rich.console import Console
console = Console()


def show_df(df):
    """
    更好的方式：
    利用prettytable对输出结果进行美化 https://www.cnblogs.com/shuchang/articles/11029456.html
    :param df:
    :return:
    """
    from prettytable import PrettyTable  # prettytable==3.8.0
    x = PrettyTable()
    # x.padding_width = 1  # One space between column edges and contents (default)
    x.add_column(
        fieldname='data_index',
        column=df.index
    )
    for col in df.columns.values:  # df.columns.values的意思是获取列的名称
        x.add_column(col, df[col])
    print(x)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


def show_dict(
        obj: dict,
        use_rich: bool = False
):
    """
    显示字典dict
    """
    if use_rich:
        console.print(obj)
    else:
        show_res = json.dumps(
            obj=obj,
            sort_keys=True,
            indent=4,
            cls=DateEncoder,
            ensure_ascii=False
        )
        print(show_res)

