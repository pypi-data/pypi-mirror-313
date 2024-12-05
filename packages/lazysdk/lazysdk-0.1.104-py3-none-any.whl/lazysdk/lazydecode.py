

def decode(
        string,
        decode_list: list = None
):
    if not decode_list:
        decode_list = [
            "UTF-8",
            "ISO-8859-1",
            "gb18030",
            "gb2312",
            "gbk",
            "latin-1"
        ]
    for each_decode in decode_list:
        try:
            return string.decode(each_decode)
        except UnicodeDecodeError:
            pass
    pass

