# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 8:50
# 文件名称： network_utils.py
# 项目描述： 网络工具模块，提供发送 HTTP 请求并返回响应的功能，包括同步和异步版本。
# 开发工具： PyCharm
import time
import httpx
import asyncio
from httpx import Limits
from parsel import Selector
from fake_useragent import UserAgent
from xiaoqiangclub.config.log_config import log
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from typing import (Any, Optional, Union, Dict, Tuple, List, Literal)

VALID_REQUEST_METHODS = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'}


def get_random_ua(system_type: Union[str, List[str]] = None,
                  browser_type: Union[str, List[str]] = None,
                  platform_type: Union[str, List[str]] = None,
                  min_version: float = 0.0) -> str:
    """
    生成随机用户代理（UA）字符串，支持指定系统、浏览器、平台类型及最小版本。
    参数支持单个字符串或字符串列表类型。

    :param system_type: 系统类型（如 "windows", "macos", "linux", "android", "ios"），支持单个字符串或字符串列表。
    :param browser_type: 浏览器类型（如 "chrome", "edge", "firefox", "safari"），支持单个字符串或字符串列表。
    :param platform_type: 平台类型（如 "pc", "mobile", "tablet"），支持单个字符串或字符串列表。
    :param min_version: 最低版本，默认为 0.0。
    :return: 随机生成的用户代理（UA）字符串。
    """

    # 将所有输入的字符串或列表中的字符串转为小写
    if isinstance(system_type, str):
        system_type = [system_type.lower()]
    elif isinstance(system_type, list):
        system_type = [s.lower() for s in system_type]

    if isinstance(browser_type, str):
        browser_type = [browser_type.lower()]
    elif isinstance(browser_type, list):
        browser_type = [b.lower() for b in browser_type]

    if isinstance(platform_type, str):
        platform_type = [platform_type.lower()]
    elif isinstance(platform_type, list):
        platform_type = [p.lower() for p in platform_type]

    # 创建 UserAgent 实例
    ua = UserAgent(
        browsers=browser_type if browser_type else ["chrome", "edge", "firefox", "safari"],
        os=system_type if system_type else ["windows", "macos", "linux", "android", "ios"],
        platforms=platform_type if platform_type else ["pc", "mobile", "tablet"],
        min_version=min_version
    )
    return ua.random


def format_method(method: Optional[str], data: Optional[dict], json: Optional[Union[dict, str]]) -> str:
    """格式化请求方法为大写，并验证是否合法。"""
    if method is None:
        # 根据 data 和 json 判断请求方法
        if isinstance(data, dict) or isinstance(json, (dict, str)):
            return 'POST'
        return 'GET'
    method_upper = method.upper()
    if method_upper not in VALID_REQUEST_METHODS:
        raise ValueError(f"无效的请求方法: {method}. 允许的方法包括: {', '.join(VALID_REQUEST_METHODS)}")
    return method_upper


def handle_error(e: Exception, attempt: int, retries: int, raise_on_failure: bool, logger: Any) -> None:
    """处理错误的通用函数。

    :param e: 异常对象
    :param attempt: 当前尝试次数
    :param retries: 最大重试次数
    :param raise_on_failure: 是否在失败时抛出异常
    :param logger: 日志记录器
    """
    if attempt == retries:
        if raise_on_failure:
            raise
        if retries > 0:
            logger.error(f"请求错误: {type(e).__name__}: {e}, 已达到最大重试次数 {retries} 次",
                         exc_info=not raise_on_failure)
        else:
            logger.error(f"请求错误: {type(e).__name__}: {e}", exc_info=not raise_on_failure)
    else:
        logger.error(f"请求错误: {type(e).__name__}: {e}, 进行第 {attempt + 1}/{retries} 次重试:...")


def __extract_kwargs(kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    处理 kwargs 参数，返回两个字典：http_client_params 和 request_params。
    :param kwargs: **kwargs 参数
    :return: httpx.Client的参数, client.request的参数
    """

    # 定义默认值
    http_client_default_params = {
        "auth": None,
        "cookies": None,
        "verify": True,
        "cert": None,
        "http1": True,
        "http2": False,
        "proxy": None,
        "proxies": None,
        "mounts": None,
        "timeout": 5.0,
        "limits": Limits(max_connections=100, max_keepalive_connections=20),
        "max_redirects": 20,
        "event_hooks": None,
        "base_url": "",
        "transport": None,
        "app": None,
        "trust_env": True,
    }

    # 从 kwargs 中提取 http_client 参数
    http_client_params = {key: kwargs.pop(key) for key in list(kwargs) if key in http_client_default_params}

    return http_client_params, kwargs


def get_response(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.Client] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        random_ua: Union[bool, dict] = False,
        retries: int = 0,
        retry_delay: float = 1,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    发送 HTTP 请求并返回响应。

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param headers: 请求头
    :param random_ua: 是否使用随机UA，当 headers 中未指定 User-Agent 时生效。
                   - True: 使用随机 UA。
                   - False: 不使用随机 UA。
                   - dict: 使用指定的 UA 配置，字典格式支持 `system_type`, `browser_type`, `platform_type`, `min_version` 键。
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                            UTF-8：最常用的编码格式，支持所有字符，包括中文。
                            GBK：常用于简体中文编码，特别是在某些旧版系统中。
                            GB2312：较早的简体中文编码，但支持的字符集较少。
                            ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                            ISO-8859-2：中欧语言的编码，也不支持中文。
                            Shift_JIS：日文编码，适用于日文内容。
                            Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    json = kwargs.pop('json', None)  # 兼容json参数
    method = format_method(method, data, json)
    retries = retries if retries and retries > 0 else 0  # 防止负数和None

    default_encoding = default_encoding or 'utf-8'  # 默认编码
    http_client_params, request_params = __extract_kwargs(kwargs)
    client = session if session else httpx.Client(default_encoding=default_encoding, **http_client_params)

    # 随机UA
    if random_ua:
        if not headers or not headers.get('User-Agent'):
            headers = headers or {}
            headers['User-Agent'] = get_random_ua()

    # 判断 random_ua 的类型并根据需要生成随机 UA
    if random_ua and (not headers or not headers.get('User-Agent')):
        headers = headers or {}

        # 如果 random_ua 是字典，使用字典中的配置生成 UA
        if isinstance(random_ua, dict):
            system_type = random_ua.get('system_type')
            browser_type = random_ua.get('browser_type')
            platform_type = random_ua.get('platform_type')
            min_version = random_ua.get('min_version', 0.0)
            headers['User-Agent'] = get_random_ua(
                system_type=system_type,
                browser_type=browser_type,
                platform_type=platform_type,
                min_version=min_version
            )
        else:  # 如果 random_ua 是 True，生成一个随机的 UA
            headers['User-Agent'] = get_random_ua()

    for attempt in range(retries + 1):
        log.debug(f"发送异步请求，请求方法：{method} 请求URL：{url} 请求头：{headers}...")

        try:
            response = client.request(method, url, data=data, json=json, headers=headers, **request_params)
            response.raise_for_status()

            if return_json:
                return response.json()
            if return_parsel_selector:
                return Selector(text=response.text)
            return response
        except httpx.HTTPStatusError as e:
            handle_error(e, attempt, retries, raise_on_failure, log)
        except Exception as e:
            handle_error(e, attempt, retries, raise_on_failure, log)
        # 等待一段时间再重试
        time.sleep(retry_delay)

    if session is None:  # 不使用自定义session时，需要关闭
        client.close()
    return None


async def __get_response_async(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        data: Optional[dict] = None,
        retries: int = 0,
        retry_delay: float = 1,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        random_ua: Union[bool, dict] = False,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    异步发送 HTTP 请求

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param random_ua: 是否使用随机UA，当 headers 中未指定 User-Agent 时生效。
                       - True: 使用随机 UA。
                       - False: 不使用随机 UA。
                       - dict: 使用指定的 UA 配置，字典格式支持 `system_type`, `browser_type`, `platform_type`, `min_version` 键。
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                    UTF-8：最常用的编码格式，支持所有字符，包括中文。
                    GBK：常用于简体中文编码，特别是在某些旧版系统中。
                    GB2312：较早的简体中文编码，但支持的字符集较少。
                    ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                    ISO-8859-2：中欧语言的编码，也不支持中文。
                    Shift_JIS：日文编码，适用于日文内容。
                    Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    json = kwargs.pop('json', None)
    method = format_method(method, data, json)
    retries = retries if retries and retries > 0 else 0  # 防止负数和None

    # 判断 random_ua 的类型
    if isinstance(random_ua, bool):
        if random_ua:  # 如果是 True，生成随机 User-Agent
            if 'headers' not in kwargs or not kwargs['headers'].get('User-Agent'):
                headers = kwargs.get('headers', {})
                headers['User-Agent'] = get_random_ua()
                kwargs['headers'] = headers

    elif isinstance(random_ua, dict):  # 如果是字典类型
        # 从字典中提取配置并生成 User-Agent
        system_type = random_ua.get('system_type')
        browser_type = random_ua.get('browser_type')
        platform_type = random_ua.get('platform_type')
        min_version = random_ua.get('min_version', 0.0)

        if 'headers' not in kwargs or not kwargs['headers'].get('User-Agent'):
            headers = kwargs.get('headers', {})
            headers['User-Agent'] = get_random_ua(
                system_type=system_type,
                browser_type=browser_type,
                platform_type=platform_type,
                min_version=min_version
            )
            kwargs['headers'] = headers

    default_encoding = default_encoding or 'utf-8'  # 默认编码
    http_client_params, request_params = __extract_kwargs(kwargs)

    async_client = session if session else httpx.AsyncClient(default_encoding=default_encoding, **http_client_params)

    for attempt in range(retries + 1):
        try:
            log.debug(f"发送异步请求，请求方法：{method} 请求URL：{url} 请求头：{kwargs.get('headers'), '无'}...")
            response = await async_client.request(method, url, data=data, json=json, **request_params)
            response.raise_for_status()

            if return_json:
                return response.json()
            if return_parsel_selector:
                return Selector(text=response.text)
            return response
        except httpx.HTTPStatusError as e:
            handle_error(e, attempt, retries, raise_on_failure, log)
        except Exception as e:
            handle_error(e, attempt, retries, raise_on_failure, log)
        # 等待一段时间再重试
        await asyncio.sleep(retry_delay)

    if session is None:  # 不使用自定义session时，需要关闭
        await async_client.aclose()

    return None


async def get_response_async(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        data: Optional[dict] = None,
        retries: int = 0,
        retry_delay: float = 1,
        sem: asyncio.Semaphore = None,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        random_ua: Union[bool, dict] = False,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    异步发送 HTTP 请求并返回响应。

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param sem: asyncio.Semaphore对象，用于控制并发请求的数量，默认为 None，不控制并发数量
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param random_ua: 是否使用随机UA，当 headers 中未指定 User-Agent 时生效。
                   - True: 使用随机 UA。
                   - False: 不使用随机 UA。
                   - dict: 使用指定的 UA 配置，字典格式支持 `system_type`, `browser_type`, `platform_type`, `min_version` 键。
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                    UTF-8：最常用的编码格式，支持所有字符，包括中文。
                    GBK：常用于简体中文编码，特别是在某些旧版系统中。
                    GB2312：较早的简体中文编码，但支持的字符集较少。
                    ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                    ISO-8859-2：中欧语言的编码，也不支持中文。
                    Shift_JIS：日文编码，适用于日文内容。
                    Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    if sem:
        async with sem:  # 限制并发请求
            return await __get_response_async(url=url, method=method, session=session, data=data, retries=retries,
                                              retry_delay=retry_delay, raise_on_failure=raise_on_failure,
                                              return_json=return_json, return_parsel_selector=return_parsel_selector,
                                              random_ua=random_ua, default_encoding=default_encoding, **kwargs)
    else:
        return await __get_response_async(url=url, method=method, session=session, data=data, retries=retries,
                                          retry_delay=retry_delay, raise_on_failure=raise_on_failure,
                                          return_json=return_json, return_parsel_selector=return_parsel_selector,
                                          random_ua=random_ua, default_encoding=default_encoding, **kwargs)


def get_response_with_js(url: str, headless: bool = True,
                         wait_until: Literal['domcontentloaded', 'load', 'networkidle'] = 'networkidle',
                         return_parsel_selector: bool = False,
                         timeout: int = 30000) -> Optional[str]:
    """
    获取页面内容并加载所有的JS，模拟用户行为，防止反爬虫（同步版本）。
    支持通过参数传递设置 User-Agent、浏览器视口大小、超时时间，并选择页面加载的状态。
    服务器上需要安装：
    playwright install chromium
    playwright install-deps

    :param url: 目标网页的URL
    :param headless: 是否启用无头模式，默认为True，启用无头模式，不显示浏览器界面
    :param wait_until: 页面加载的等待状态，支持以下选项：
        - 'domcontentloaded'：等待文档内容加载完成（即 DOM 加载完成），不包含样式、图像等资源的加载。
        - 'load'：等待页面的完全加载，包括所有资源（样式、图像等）加载完成，可能存在异步AJAX 无法加载完成的情况。
        - 'networkidle'：等待网络空闲，即没有网络请求在进行（通常是页面的所有资源加载完成时）。
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param timeout: 页面加载超时时间（毫秒），默认30000毫秒（30秒）
    :return: 网页内容的字符串
    """
    with sync_playwright() as p:
        # 启动 Chromium 浏览器（无头模式）
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # 设置随机 User-Agent，防止反爬虫识别
        user_agent = get_random_ua(system_type='windows')

        # 设置请求头，包括 User-Agent
        page.set_extra_http_headers({
            "User-Agent": user_agent
        })

        # 设置浏览器分辨率，模拟常见的屏幕大小
        page.set_viewport_size({"width": 2560, "height": 1440})

        # 访问目标页面，并设置超时时间
        try:
            log.debug(f"正在使用playwright访问 URL: {url}")
            page.goto(url, timeout=timeout)  # 设置超时
            # 等待页面加载完成，确保所有的JS和资源都加载完毕
            page.wait_for_load_state(wait_until, timeout=timeout)  # 等待直到页面加载到指定状态
            log.debug(f"页面 {url} 加载完成")
        except Exception as e:
            log.error(f"页面加载超时或发生错误: {e}")
            browser.close()
            return None

        # 获取页面内容
        content = page.content()

        # 关闭浏览器
        browser.close()

        if return_parsel_selector:
            return Selector(content)

        return content


async def get_response_with_js_async(url: str, headless: bool = True,
                                     wait_until: Literal[
                                         'domcontentloaded', 'load', 'networkidle'] = 'networkidle',
                                     return_parsel_selector: bool = False,
                                     timeout: int = 30000) -> Optional[str]:
    """
    获取页面内容并加载所有的JS，模拟用户行为，防止反爬虫（异步版本）。
    支持通过参数传递设置 User-Agent、浏览器视口大小、超时时间，并选择页面加载的状态。
    服务器上需要安装：
    playwright install chromium
    playwright install-deps

    :param url: 目标网页的URL
    :param headless: 是否开启无头模式，默认为True
    :param wait_until: 页面加载的等待状态，支持以下选项：
        - 'domcontentloaded'：等待文档内容加载完成（即 DOM 加载完成），不包含样式、图像等资源的加载。
        - 'load'：等待页面的完全加载，包括所有资源（样式、图像等）加载完成，可能存在异步AJAX 无法加载完成的情况。
        - 'networkidle'：等待网络空闲，即没有网络请求在进行（通常是页面的所有资源加载完成时）。
    :param return_parsel_selector: 是否返回解析后的Selector对象，默认为False
    :param timeout: 页面加载超时时间（毫秒），默认30000毫秒（30秒）
    :return: 网页内容的字符串
    """
    async with async_playwright() as p:
        # 启动 Chromium 浏览器（无头模式）
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()

        # 设置随机 User-Agent，防止反爬虫识别
        user_agent = get_random_ua(system_type='windows')

        # 设置请求头，包括 User-Agent
        await page.set_extra_http_headers({
            "User-Agent": user_agent
        })

        # 设置浏览器分辨率，模拟常见的屏幕大小
        await page.set_viewport_size({"width": 2560, "height": 1440})

        # 访问目标页面，并设置超时时间
        try:
            log.debug(f"正在使用playwright访问: {url}")
            await page.goto(url, timeout=timeout)  # 设置超时
            # 等待页面加载完成，确保所有的JS和资源都加载完毕
            await page.wait_for_load_state(wait_until, timeout=timeout)  # 等待直到页面加载到指定状态
            log.debug(f"页面 {url} 加载完成")
        except Exception as e:
            log.error(f"页面加载超时或发生错误: {e}")
            await browser.close()
            return None

        # 获取页面内容
        content = await page.content()

        # 关闭浏览器
        await browser.close()

        if return_parsel_selector:
            return Selector(content)

        return content


def test_proxy(proxy: str, test_url: str = "http://ip-api.com/json/", timeout: int = 20) -> Dict[
    str, Union[str, float, dict]]:
    """
    测试代理是否有效并获取相关信息（同步版本）。

    :param proxy: 代理地址（支持 http 和 socks5 格式）。
    :param test_url: 测试用的 URL，默认使用 IP-API，还可以使用"https://httpbin.org/ip"等测试网站。
    :param timeout: 超时时间（单位：秒），默认为 20 秒。
    :return: 包含代理状态和响应数据的字典。
    """
    # 判断代理协议并规范化
    if not proxy.startswith(("http://", "https://", "socks5://")):
        proxy = f"http://{proxy}"

    try:
        start_time = time.time()

        with httpx.Client(proxies=proxy, timeout=timeout) as client:
            response = client.get(test_url)

        response_time = time.time() - start_time

        if response.status_code == 200:
            return {
                "status": "success",
                "response_time": f"{response_time:.2f}s",
                "data": response.json()
            }
        else:
            return {
                "status": "failed",
                "response_time": response_time,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "failed",
            "response_time": "N/A",
            "error": str(e)
        }


async def test_proxy_async(proxy: str, test_url: str = "http://ip-api.com/json/", timeout: int = 10) -> Dict[
    str, Union[str, float, dict]]:
    """
    测试代理是否有效并获取相关信息（异步版本）。

    :param proxy: 代理地址（支持 http 和 socks5 格式）。
    :param test_url: 测试用的 URL，默认使用 IP-API，还可以使用"https://httpbin.org/ip"等测试网站。
    :param timeout: 超时时间（单位：秒）。
    :return: 包含代理状态和响应数据的字典。
    """
    # 判断代理协议并规范化
    if not proxy.startswith(("http://", "https://", "socks5://")):
        proxy = f"http://{proxy}"

    try:
        start_time = time.time()

        async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:
            response = await client.get(test_url)

        response_time = time.time() - start_time

        if response.status_code == 200:
            return {
                "status": "success",
                "response_time": f"{response_time:.2f}s",
                "data": response.json()
            }
        else:
            return {
                "status": "failed",
                "response_time": "N/A",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "failed",
            "response_time": "N/A",
            "error": str(e)
        }
