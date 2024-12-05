import json
import decimal
import datetime


class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        super(LazyEncoder, self).default(obj)


def json2str(
        data: json,
        ensure_ascii: bool = False
):
    """
    在将json数据反序列化为str时，会遇到一些格式无法转换
    这里使用识别类型转换转为str
    目前支持类型：
    decimal --> str
    datetime.datetime --> str(%Y-%m-%d %H:%M:%S)
    datetime.date --> str(%Y-%m-%d)
    """
    return json.dumps(
        data,
        cls=LazyEncoder,
        ensure_ascii=ensure_ascii
    )
