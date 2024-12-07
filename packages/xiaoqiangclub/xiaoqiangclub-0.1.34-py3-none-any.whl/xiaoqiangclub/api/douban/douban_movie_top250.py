# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/14 18:00
# 文件名称： douban_movie_top250.py
# 项目描述： 爬取豆瓣电影top250，爬取容易被封IP，需要加很长的延迟
# 开发工具： PyCharm
import os.path
import time
import httpx
from typing import List, Dict, Optional
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.data.file import write_file, read_file
from xiaoqiangclub.utils.network_utils import get_response
from xiaoqiangclub.utils.decorators import is_valid_return, retry


@retry(max_retries=5, delay=5, valid_check=is_valid_return)
def get_detail_url(session: httpx.Client, start: int) -> Optional[List[str]]:
    """
    获取详情页链接
    :param start: 起始页码：250的倍数，从0开始，每页有25条数据
    :return: 电影的详情页链接
    """
    log.info(f'从 {start} 开始提取详情页链接...')

    headers = {
        "referer": "https://movie.douban.com/top250?start=100",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    url = f"https://movie.douban.com/top250?start={start}"

    selector = get_response(url, session=session, headers=headers, return_parsel_selector=True)
    if not selector:
        return None

    return selector.xpath(r'//ol[@class="grid_view"]/li//div[@class="hd"]/a/@href').getall()


@retry(max_retries=2, delay=2, valid_check=is_valid_return)
def get_detail_url_data(detail_url: str, session: httpx.Client, get_all_data: bool = False) -> Optional[Dict[str, str]]:
    """
    获取电影详情页数据。

    :param detail_url: 豆瓣影视详情页面链接
    :param get_all_data: 是否获取所有信息
    :return: 电影详情字典
    """
    log.info(f'提取详情页 {detail_url} 的数据...')
    selector = get_response(url=detail_url, session=session, return_parsel_selector=True,
                            random_ua={'platform_type': 'pc'},
                            retry_delay=2, follow_redirects=True)

    if not selector:
        return None

    movie_info = {
        'detail_url': detail_url,
        'title': selector.css('span[property="v:itemreviewed"]::text').get(),
        '又名': [tag.strip() for tag in (selector.xpath(
            '//span[contains(text(), "又名:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get() or '').split(
            '/')],
        '导演': [tag.strip() for tag in selector.css('span:contains("导演") + span.attrs a::text').getall()],
        '主演': [tag.strip() for tag in selector.css('span:contains("主演") + span.attrs a::text').getall()],
        '上映日期': selector.css('span[property="v:initialReleaseDate"]::text').getall(),
        '集数': selector.xpath(
            '//span[contains(text(), "集数:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
        '片长': selector.css('span[property="v:runtime"]::text').get() or selector.xpath(
            '//span[contains(text(), "单集片长:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
    }

    # 获取所有详细数据
    if get_all_data:
        # 制片国家/地区
        country = selector.xpath(
            '//span[contains(text(), "制片国家/地区:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get()
        country = country.split('/') if country else None
        country = [c.strip() for c in country if c.strip()] if country else None

        # 语言
        language = selector.xpath(
            '//span[contains(text(), "语言:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get()

        language = language.split('/') if language else None
        language = [l.strip() for l in language if l.strip()] if language else None

        movie_info.update({
            '海报': selector.css('#mainpic img::attr(src)').get(),
            '评分': selector.css('.ll.rating_num::text').get(),
            '产地': country,
            '编剧': [tag.strip() for tag in selector.css('span:contains("编剧") + span.attrs a::text').getall()],
            '类型': [tag.strip() for tag in selector.css('span[property="v:genre"]::text').getall()],
            '语言': language,
            'imdb': selector.xpath(
                '//span[contains(text(), "IMDb:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
        })

    return {k: v.strip() if isinstance(v, str) else v for k, v in movie_info.items() if v}


def douban_movie_top250(save_path: str, detail_urls_file: str = None) -> Optional[List[Dict]]:
    """
    爬取豆瓣电影top250
    https://movie.douban.com/top250
    :param save_path: 数据保存路径
    :param detail_urls_file: 详情页链接保存文件路径
    :return: 电影详情数据列表
    """
    session = httpx.Client()

    if detail_urls_file:
        detail_urls = read_file(detail_urls_file)
    else:
        detail_urls = []
        for i in range(10):
            urls = get_detail_url(session, 25 * i)
            if urls:
                detail_urls.extend(urls)

            time.sleep(3)  # 避免请求过快被封

        write_file(
            r'D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\tests\douban_movie_top250_urls.json',
            detail_urls)

    results = []
    if os.path.exists(save_path):
        old_data = read_file(save_path)
    else:
        old_data = None

    for detail_url in detail_urls:
        skip_url = False  # 标志变量，控制是否跳过当前的detail_url

        if old_data:
            for old in old_data:
                if old['detail_url'] == detail_url and old.get('title'):
                    log.info(f'跳过已存在的数据：{detail_url}')
                    results.append(old)  # 将已存在的数据添加到结果中
                    skip_url = True  # 设置标志为True，跳过当前detail_url
                    break  # 跳出内层循环

        if skip_url:
            continue  # 跳到下一个detail_url

        data = get_detail_url_data(detail_url, session=session, get_all_data=True)
        if data:
            results.append(data)
        # 保存每次结果
        write_file(save_path.replace('.json', '_temp.json'), results)
        time.sleep(3)  # 避免请求过快被封

    write_file(save_path, results)
    return results


if __name__ == '__main__':
    douban_movie_top250(
        r'D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\tests\douban_movie_top250.json',
        r'D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\tests\douban_movie_top250_detail_urls.json')
    # print(get_detail_url(25))
