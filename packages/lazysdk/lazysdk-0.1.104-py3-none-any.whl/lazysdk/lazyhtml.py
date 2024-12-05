from collections import OrderedDict


def make_thead(head_list: list):
    """
    制作表头，输入表头列表，输出生成的行代码列表
    """
    thead_list = list()
    for each_head in head_list:
        head_line = f'<th>{each_head}</th>'
        thead_list.append(head_line)
    return thead_list


def make_tbody(body_list: list):
    """
    制作表格主题，即表格的数据部分
    """
    tbody_list = list()
    for each_body in body_list:
        body_line = f'<td>{each_body}</td>'
        tbody_list.append(body_line)
    return tbody_list


def make_tb(
        data: list,
        border: int = 0,
        beautiful: bool = False,
        charset: str = "UTF-8",
        col_name_dict: OrderedDict = None
) -> str:
    """
    输入数据为list(dict())，输出生成的html表格代码
    border=2--> 边框宽度为2,是指外面灰色边框
    """
    key_list = list()
    for each_data in data:
        key_list.extend(list(each_data.keys()))
    key_list = list(set(key_list))
    if col_name_dict:
        key_list_new = list()
        for each_key in key_list:
            each_value = col_name_dict.get(each_key)
            if each_value:
                key_list_new.append(each_value)
            else:
                key_list_new.append(each_key)
        thead_list = make_thead(head_list=key_list_new)
    else:
        thead_list = make_thead(head_list=key_list)
    html_head = f"<tr>{''.join(thead_list)}</tr>"

    html_body = ''
    for each_data in data:
        body_list = list()
        for each_key in key_list:
            body_list.append(each_data.get(each_key))
        body_list = make_tbody(body_list=body_list)  # 这里每行数据都要生成一次
        html_body += f"<tr>{''.join(body_list)}</tr>\n"

    table_others = ''
    if border:
        table_others += f' border={border}'

    html_table = f"""<meta http-equiv="Content-Type" content="text/html;charset={charset}"/>\n<table{table_others}>\n{html_head}\n{html_body}</table>"""

    if beautiful:
        # 美化输出
        from lxml import html
        from lxml.html import builder as E
        # 创建一个lxml的Element对象
        root = html.fromstring(html_table)

        # 设置HTML的缩进和换行
        E.PRETTY_PRINT = True

        # 漂亮地打印HTML
        html_table = html.tostring(root, pretty_print=True)

    return html_table


def get_text(content: str):
    """
    从html中提取文本
    """
    import html2text
    return html2text.html2text(content)
