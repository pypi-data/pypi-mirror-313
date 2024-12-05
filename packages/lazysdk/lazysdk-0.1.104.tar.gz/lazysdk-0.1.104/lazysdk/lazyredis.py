#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import showlog
import redis
import time
import envx

default_db = 0  # 默认数据库
default_env_file_name = 'local.redis.env'  # 默认链接信息文件
"""
统一定义：
数据库层为db
集合层叫name
下一层hash的叫key,value

全局默认解码(decode_responses=True)

redis的基本用法可以参考：https://www.runoob.com/redis

python的redis用法可以参考：https://www.runoob.com/w3cnote/python-redis-intro.html

返回：
    {
        "code": 0,
        "msg": "ok",
        "data": <返回的数据>/None
    }
    
    code=0为正常，code!=0为异常，msg参数为原因
    
    code=1为未知错误
"""


class Basics:
    def __init__(
            self,
            con_info: dict = None,  # 连结信息，如果设置，将优先使用
            db: int = None,  # 需要连接的数据库，以数字为序号的，从0开始
            host=None,  # 连接的域名
            port=None,  # 连接的端口
            password=None,  # 连接的密码,
            max_connections=None,
            decode_responses=True
    ):
        # 初始化所有参数
        if con_info is not None:
            self.con_db = con_info.get('db', 0)
            self.host = con_info.get('host', 'localhost')
            self.port = con_info.get('port', 6379)
            self.pwd = con_info.get('password')
            self.max_connections = con_info.get('max_connections')
            self.decode_responses = con_info.get('decode_responses', True)
        else:
            if db is None:
                self.con_db = 0
            else:
                self.con_db = db
            self.host = host
            self.port = port
            self.pwd = password
            self.max_connections = max_connections
            self.decode_responses = decode_responses
        self.pool = self.make_connect_pool()
        self.conn = self.connect()

    def make_connect_pool(
            self
    ):
        # 使用连接池连接，节省每次连接用的时间
        pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.pwd,
            db=self.con_db,
            max_connections=self.max_connections,
            decode_responses=self.decode_responses
        )
        return pool

    def connect(
            self
    ):
        # 从连接池中拿出一个连接
        connection = redis.Redis(
            connection_pool=self.pool
        )
        return connection

    def delete_key(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        删除 db中的一个key
        data: 存在key且删除成功为1，不存在key/删除失败为0
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.delete(key)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def get_db_key_list(
            self,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 db中键列表
        若有key，则返回key列表；若无key，则返回空列表
        """
        while True:
            try:
                inner_keys = list(self.conn.keys())
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": inner_keys
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_get_values_count(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        获取 list 的 元素数量
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.llen(key)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_read_key_values(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 列表的 键的所有值列表
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.lrange(name=key, start=0, end=-1)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_read_first_value(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 列表的 第一个元素
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.lindex(key, 0)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_read_last_value(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        获取 列表的 最后一个元素
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.lindex(key, -1)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_add_l(
            self,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        在list左侧添加值，作为队列使用时一般不用此方法，一般在右侧入队列，在左侧出队列
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.lpush(key, value)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_add_r(
            self,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        在list右侧添加值，作为队列使用时，一般使用此方法从右侧入队列
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.rpush(key, value)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_pop_l(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        从左侧出队列，作为队列时，经常使用此方法
        """
        while True:
            try:
                key_type = self.conn.type(key)
                if key_type == 'list':
                    return {
                        "code": 0,
                        "msg": "ok",
                        "data": self.conn.lpop(key)
                    }
                else:
                    return {
                        "code": 2,
                        "msg": f'key type is not list, type is {key_type}',
                        "data": None
                    }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def list_pop_r(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        从右侧侧出队列
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.rpop(key)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def set_save(
            self,
            name,
            value,
            ex=None,
            px=None,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 设置键值，ex过期时间（秒），px过期时间（毫秒）
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.set(
                        name=name,
                        value=value,
                        ex=ex,
                        px=px,
                        nx=False,
                        xx=False
                    )
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def set_get(
            self,
            name,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 获取键值
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.get(name)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def count_add(
            self,
            name,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Incr 命令将 key 中储存的数字值增一。
        如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作。
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.incr(name=name)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def count_reduce(
            self,
            name,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Decr 命令将 key 中储存的数字值减一。
        如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 DECR 操作。
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.decr(name=name)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def count_read(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 键 计数 获取值
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.get(key)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    # -------------------- hash --------------------

    def hash_set(
            self,
            name,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hset 命令用于为哈希表中的字段赋值 。
        如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。
        如果字段已经存在于哈希表中，旧值将被覆盖。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.hset(
                        name=name,
                        key=key,
                        value=value
                    )
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def hash_delete(
            self,
            name,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hdel 命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.hdel(
                        name,
                        key
                    )
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def hash_keys(
            self,
            name,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hkeys 命令用于获取哈希表中的所有域（field）。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.hkeys(name=name)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def hash_get(
            self,
            name,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hget 命令用于返回哈希表中指定字段的值。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.hget(name=name, key=key)
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def hash_get_many(
            self,
            name,
            key_list: list,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hmget 命令用于返回哈希表中，一个或多个给定字段的值。
        如果指定的字段不存在于哈希表，那么返回一个 nil 值。
        """
        while True:
            try:
                return {
                    "code": 0,
                    "msg": "ok",
                    "data": self.conn.hmget(
                        name=name,
                        keys=key_list
                    )
                }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }

    def hash_get_all(
            self,
            name,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        Redis Hgetall 命令用于返回哈希表中，所有的字段和值。
        在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，所以返回值的长度是哈希表大小的两倍。
        """
        while True:
            try:
                key_type = self.conn.type(name=name)
                if key_type is None:
                    return {
                        "code": 1,
                        "msg": "type is None",
                        "data": None
                    }
                elif 'hash' not in key_type:
                    return {
                        "code": 1,
                        "msg": "type is not hash",
                        "data": None
                    }
                else:
                    return {
                        "code": 0,
                        "msg": "ok",
                        "data": self.conn.hgetall(name=name)
                    }
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return {
                        "code": 1,
                        "msg": e,
                        "data": None
                    }


def make_con_info(
        env_file_name: str = default_env_file_name
):
    """
    制作连接信息
    :param env_file_name: 环境文件名，默认为

    """
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    if inner_env is None or len(inner_env) == 0:
        showlog.warning('[%s]文件不存在或文件填写错误！' % env_file_name)
        exit()
    else:
        max_connections = inner_env.get('max_connections')
        if max_connections is not None:
            try:
                max_connections = int(max_connections)
            except:
                showlog.warning('max_connections必须是数字！')
        else:
            max_connections = None
        con_info = {
            "host": inner_env.get('host', 'localhost'),
            "port": int(inner_env.get('port', '6379')),
            "password": inner_env.get('password'),
            "max_connections": max_connections,
            "decode_responses": inner_env.get('decode_responses', True)
        }
        return con_info


def get_db_key_list(
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        auto_reconnect: bool = True,  # 自动重连
        reconnect_delay: int = 1  # 重连延时，单位为秒
):
    """
    获取 当前数据库的所有键列表
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.get_db_key_list(
        auto_reconnect=auto_reconnect,
        reconnect_delay=reconnect_delay
    )


def delete_key(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        auto_reconnect: bool = True,  # 自动重连
        reconnect_delay: int = 1  # 重连延时，单位为秒
):
    """
    删除 key
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.delete_key(
        key=key,
        auto_reconnect=auto_reconnect,
        reconnect_delay=reconnect_delay
    )


def list_add_r(
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_add_r(
        key=key,
        value=value
    )


def list_pop_l(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_pop_l(
        key=key
    )


def list_read_key_values(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_read_key_values(
        key=key
    )


def list_read_first_value(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 获取列表的第一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_read_first_value(
        key=key
    )


def list_read_last_value(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 获取列表的最后一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_read_last_value(
        key=key
    )


def count_set(
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 设定值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.set_save(
        name=key,
        value=value
    )


def count_add(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 增加1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_add(
        name=key
    )


def count_reduce(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 减少1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_reduce(
        name=key
    )


def count_read(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 获取值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_read(
        key=key
    )


def list_get_values_count(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 获取列表元素数量
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_get_values_count(
        key=key
    )


# -------------------- hash --------------------


def hash_set(
        name,
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    设置hash值

    :param name: 数据库层的键
    :param key: Hash的键
    :param value: Hash的值
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_set(
        name=name,
        key=key,
        value=value,
    )


def hash_delete(
        name,
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    删除hash的一个键

    :param name: 数据库层的键
    :param key: Hash的键
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_delete(
        name=name,
        key=key
    )


def hash_keys(
        name,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    获取hash所有键

    :param name: 数据库层的键
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_keys(
        name=name
    )


def hash_get(
        name,
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    获取hash的某个键的值，一次只获取一个键的值

    :param name: 数据库层的键
    :param key: Hash的键
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get(
        name=name,
        key=key
    )


def hash_get_many(
        name,
        key_list: list,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    获取hash的某个键的值，一次只获取多个键的值

    :param name: 数据库层的键
    :param key_list: Hash的键列表
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get_many(
        name=name,
        key_list=key_list
    )


def hash_get_all(
        name,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        auto_reconnect: bool = True,  # 自动重连
) -> dict:
    """
    获取hash的所有键的值

    :param name: 数据库层的键
    :param db: 数据库序号
    :param con_info: 连接信息
    :param env_file_name: 环境文件名
    :param auto_reconnect: 是否自动重连，默认为True
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get_all(
        name=name,
        auto_reconnect=auto_reconnect
    )
