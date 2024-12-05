#!/usr/bin/env python3
# coding = utf8
from Crypto.Cipher import AES


def aes_decode(
        data,
        key
):
    """
    AES解密
    :param data:  要解密的数据
    :param key:  密钥（16.32）一般16的倍数
    :return:  处理好的数据
    """
    cryptor = AES.new(key, AES.MODE_CBC, key)
    plain_text = cryptor.decrypt(data)
    return plain_text.rstrip(b'\0')
