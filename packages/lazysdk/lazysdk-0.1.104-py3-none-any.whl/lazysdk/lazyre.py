import re


def find_between(
        text: str,
        left: str,
        right: str,
        until_line_end: bool = False  # 是否匹配到行尾
):
    """
    找两个之间
    """
    if until_line_end:
        return re.findall(pattern=f'{left}(.*?){right}$', string=text, flags=re.S)
    else:
        return re.findall(pattern=f'{left}(.*?){right}', string=text, flags=re.S)


def find_all(
        text: str,
        left: str,
        right: str,
        until_line_end: bool = False  # 是否匹配到行尾
):
    """
    找一个之后所有
    """
    if until_line_end:
        return re.findall(pattern=f'{left}(.*){right}$', string=text, flags=re.S)
    else:
        return re.findall(pattern=f'{left}(.*){right}', string=text, flags=re.S)


def find_chs(
        text: str
):
    """
    提取中文，目前不能去掉括号
    """
    return re.sub(pattern="[A-Za-z0-9\!\%\[\]\,\。\ \']", repl="", string=text)
