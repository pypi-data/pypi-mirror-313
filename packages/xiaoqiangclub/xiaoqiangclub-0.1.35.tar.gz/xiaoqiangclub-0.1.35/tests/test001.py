import httpx
import time
from typing import Dict, Union
import asyncio


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

        async with httpx.AsyncClient(proxies="127.0.0.1:10808", timeout=timeout) as client:
            response = await client.get(test_url)

        response_time = time.time() - start_time

        if response.status_code == 200:
            return {
                "status": "success",
                "response_time": f"{response_time:.2f}s",
                "data":  response.json()
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


# 示例使用
if __name__ == "__main__":
    # 同步测试
    proxy_ip = "127.0.0.1:10808"  # 替换为你的代理 IP
    # proxy_ip = "192.168.1.111:7891"  # 替换为你的代理 IP
    test_url = "https://httpbin.org/ip"
    print("同步测试结果:")
    print(test_proxy(proxy_ip, test_url, timeout=20))

    # 异步测试
    async def main():
        print("\n异步测试结果:")
        print(await test_proxy_async(proxy_ip, timeout=20))

    asyncio.run(main())
