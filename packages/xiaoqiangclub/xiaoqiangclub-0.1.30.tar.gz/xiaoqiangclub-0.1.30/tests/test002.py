import random
from urllib.parse import urlparse, urlunparse, urljoin

# 旧版和新版hao6v网站链接
HAO6V_OLD_URLS = ["https://www.hao6v.me", "https://www.6v520.com", "https://www.6v520.net", "https://www.hao6v.tv"]
HAO6V_NEW_URLS = ["https://www.xb6v.com", "https://www.66s6.net", "https://www.66s6.cc",
                  "https://www.66ss.org", "https://www.i6v.tv/"]


def get_hao6v_random_url(url: str, is_new_url: bool = None):
    """
    获取hao6v的随机完整URL，自动从HAO6V_OLD_URLS或HAO6V_NEW_URLS中随机选一个同类的前缀进行替换，并返回是否是新版URL。
    如果URL是相对路径，拼接成完整URL。

    :param url: 用户提供的URL
    :param is_new_url: 如果提供了该参数，则会强制使用新版URL或旧版URL（True表示新版，False表示旧版）
    :return: 新的URL和一个布尔值，表示是否是新版URL
    """

    # 解析用户传入的URL
    parsed_url = urlparse(url)

    # 如果是相对路径，拼接成完整URL
    def get_random_url(is_new: bool):
        """根据is_new_url返回一个随机的URL前缀"""
        return random.choice(HAO6V_NEW_URLS if is_new else HAO6V_OLD_URLS)

    # 处理相对路径
    if not parsed_url.scheme:  # 没有协议部分，说明是相对路径
        is_new = is_new_url if is_new_url is not None else parsed_url.netloc in [urlparse(new_url).netloc for new_url in
                                                                                 HAO6V_NEW_URLS]
        new_url = get_random_url(is_new)
        return urljoin(new_url, url), is_new

    # 对于完整URL，直接替换域名
    is_new = is_new_url if is_new_url is not None else parsed_url.netloc in [urlparse(new_url).netloc for new_url in
                                                                             HAO6V_NEW_URLS]
    new_url = get_random_url(is_new)
    new_parsed_url = parsed_url._replace(netloc=urlparse(new_url).netloc)
    return urlunparse(new_parsed_url), is_new


# 示例使用
url1 = "https://www.xb6v.com/"
url2 = "/some/path?query=123#anchor"
new_url1, is_new1 = get_hao6v_random_url(url1)
new_url2, is_new2 = get_hao6v_random_url(url2, is_new_url=False)

print(f"新URL1: {new_url1}, 是否新版: {is_new1}")
print(f"新URL2: {new_url2}, 是否新版: {is_new2}")
