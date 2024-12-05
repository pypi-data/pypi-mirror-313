import random
import uuid
import time
import datetime
import os

uuid_node = random.randint(100000000, 999999999)  # 避免泄密设备信息


# def random_mac_uuid():
#     """
#     uuid1
#     由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，
#     但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。
#     这里使用随机数代替
#     """
#     return str(uuid.uuid1(node=uuid_node))  # 替换原来的MAC地址为随机数


# def timestamp_uuid():
#     """
#     使用纳秒级别时间戳+uuid作为id
#     """
#     return f'{time.time_ns()}_{random_mac_uuid()}'


def make_id():
    """
    基于毫秒级时间和随机字符串拼接生成id，默认生成长度为50
    """
    return MakeId()


class MakeId:
    def __init__(self):
        utcnow = datetime.datetime.utcnow()  # UTC时间
        utcnow_str = utcnow.strftime('%Y%m%d%H%M%S%f')  # 时间格式为：[4位年，2位月，2位日，2位时，2位分，2位秒，6位毫秒]
        urandom_hex = os.urandom(15).hex()  # 算出来的字符长度是输入长度的2倍
        self.utcnow = utcnow
        self.utcnow_str = utcnow_str
        self.urandom_hex = urandom_hex
        self.id = f"{utcnow_str}{urandom_hex}"
        self.random_uuid = str(uuid.uuid1(node=uuid_node))
        self.mac_uuid = str(uuid.uuid1())
