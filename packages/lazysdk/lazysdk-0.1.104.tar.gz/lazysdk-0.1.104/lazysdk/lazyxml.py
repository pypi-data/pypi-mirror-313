from xml.etree import ElementTree
import re


def xml2dict(xml_str: str):
    """
    XML代码转dict
    在格式化之前，先抽取出xml标签内的内容，防止有干扰
    参考：https://docs.python.org/zh-cn/3.8/library/xml.etree.elementtree.html
    https://blog.csdn.net/qdPython/article/details/115520713
    :param xml_str:
    :return:
    """
    res_dict = dict()
    xml_str_res = re.findall(r'<xml>(.*?)</xml>', xml_str, re.S)
    if xml_str_res:
        xml_str_process = f"<xml>{xml_str_res[0]}</xml>"
        root = ElementTree.fromstring(xml_str_process)
        for child in root:
            # print(child.tag, child.attrib, child.text)
            res_dict[child.tag] = child.text
        return res_dict
    else:
        return res_dict
