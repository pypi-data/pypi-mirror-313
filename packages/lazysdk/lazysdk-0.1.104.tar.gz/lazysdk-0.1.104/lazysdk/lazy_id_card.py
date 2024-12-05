from . import lazytime
import re


def clean_id_card(
        id_card
):
    """
    清洗身份证号码，只保留数字和X，不会改变字符串长度
    """
    # 定义正则表达式，匹配数字和字母X
    pattern = re.compile(r'[0-9Xx]+')

    # 使用正则表达式匹配身份证号码中的数字和字母X
    matches = pattern.findall(id_card)

    # 将匹配结果拼接成身份证号码
    cleaned_id_card = ''.join(matches)

    return cleaned_id_card.upper()


def validate_id_card(
        id_card
):
    """
    校验身份证号码，正确输出True，错误输出False
    """
    # 去除干扰字符，只保留身份证号码中的数字和字母X
    id_card = clean_id_card(id_card=id_card)

    # 身份证号码必须为18位
    if len(id_card) != 18:
        return False

    # 校验前17位是否都是数字
    if not id_card[:-1].isdigit():
        return False

    # 校验最后一位是否是数字或者字母X
    if not (id_card[-1].isdigit() or id_card[-1] == 'X'):
        return False

    # 加权因子
    weight_factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码对应值
    validate_values = '10X98765432'
    # 计算校验位
    sum_value = sum(int(id_card[i]) * weight_factors[i] for i in range(17))
    validate_index = sum_value % 11
    validate_code = validate_values[validate_index]

    # 校验最后一位
    return id_card[-1] == validate_code


def id_card_info(
        id_card: str
):
    """
    在身份证号码中，第17位是性别位，用于表示持证人的性别。性别位的奇偶性规则如下：

    奇数表示男性（例如，1、3、5、7、9）
    偶数表示女性（例如，0、2、4、6、8）

    通过身份证号码的性别位，我们可以快速判断持证人的性别。
    """
    id_card = clean_id_card(id_card=id_card)
    if validate_id_card(id_card=id_card):
        ana_id_info = dict()
        ana_id_info['id_str'] = id_card

        year_now = lazytime.get_year()
        ana_id_info['year_now'] = year_now

        year = id_card[6:10]
        month = id_card[10:12]
        day = id_card[12:14]
        ana_id_info['year'] = year
        ana_id_info['month'] = month
        ana_id_info['day'] = day

        age = year_now - eval(year)
        ana_id_info['age'] = age

        gender_num = id_card[16]
        s = eval(gender_num)
        if s % 2 == 0:
            gender_str = "女"
        else:
            gender_str = "男"
        ana_id_info['gender_num'] = gender_num
        ana_id_info['gender_str'] = gender_str
        ana_id_info['msg'] = 'success'
        ana_id_info['code'] = 0
        return ana_id_info
    else:
        return {
            'code': -1,
            'msg': '身份证号码错误'
        }
