import urllib.parse as urlparse


def get_url_params(
        url: str
):
    """
    获取url的params参数，返回dict形式
    """
    params_str = urlparse.urlsplit(url).query
    if params_str:
        params_str_split = params_str.split('&')
        params_dict = dict()
        for each in params_str_split:
            each_split = each.split('=', maxsplit=1)
            params_dict[each_split[0]] = each_split[1]
        return params_dict
    else:
        return


def url_info(
        url: str
):
    url_info_dict = dict()
    url_info_dict['url'] = url
    if url:
        urlparse_obj = urlparse.urlsplit(url)
        url_info_dict['host'] = urlparse_obj.hostname  # 域名
        url_info_dict['path'] = urlparse_obj.path  # 路径
        url_info_dict['scheme'] = urlparse_obj.scheme  # 协议
        url_info_dict['params'] = get_url_params(url)
    else:
        pass
    return url_info_dict


def url_quote(url):
    """
    url编码
    """
    return urlparse.quote(url)


def url_unquote(url):
    """
    url解码
    """
    return urlparse.unquote(url)


def domain_split(url):
    """
    对输入的url分析域名，拆分域名
    domain_1: 顶级域名
    domain_2: 二级域名
    """
    import urllib
    if 'http' in url:
        netloc = urllib.parse.urlparse(url).netloc
    else:
        netloc = url
    netloc_split = netloc.split('.')
    domain_dict = dict()
    for _ in range(len(netloc_split)):
        domain_dict[f'domain_{_+1}'] = '.'.join(netloc_split[-_ - 1:])
    return domain_dict
