'''
@Description:
@Author: Steven
@Date: 2019-12-06 09:53:05
@LastEditors: Steven
@LastEditTime: 2019-12-06 16:11:18
'''
import io
import sys
from typing import Generator, List

import requests
from lxml import etree
from selenium import webdriver


class MeiTuanItem:
    """HN(https://bj.meituan.com/s/%E4%BC%8A%E5%A9%89/) 上的条目

    :param hospital: 医院
    :param link: 链接
    :param title: 标题
    :param price: 价格
    :param address: 地址
    :param city: 城市
    """

    def __init__(self,
                 hospital: str,
                 link: str,
                 title: str,
                 price: str,
                 address: str,
                 city: str):
        self.hospital = hospital
        self.link = link
        self.title = title
        self.price = float(price)
        self.address = address
        self.city = city


class ItemWriter:
    """负责将帖子列表写入到文件
    """

    def __init__(self, fp: io.TextIOBase, title: str):
        self.fp = fp
        self.title = title

    def write(self, items: List[MeiTuanItem]):
        self.fp.write(f'# {self.title}\n\n')
        # enumerate 接收第二个参数，表示从这个数开始计数（默认为 0）
        for i, item in enumerate(items, 1):
            self.fp.write(f'> 医院 {i}: {item.hospital}\n')
            self.fp.write(f'> 产品标题 {i}: {item.title} 价格：{item.price}\n')
            self.fp.write(f'> 链接：{item.link}\n')
            self.fp.write(f'> 地址： {item.address}\n')
            self.fp.write('------\n')


class MTSpider:
    """抓取 MEITUAN 内容条目

    :param fp: 存储抓取结果的目标文件对象
    :param limit: 限制条目数，默认为 5
    """
    ITEMS_URL = 'https://bj.meituan.com/s/%E4%BC%8A%E5%A9%89/'
    FILE_TITLE = '美团伊婉'
    HEADERS = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': 'https://www.meituan.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def __init__(self, limit: int = 5):
        self.limit = limit
        self.cookies = self.get_cookie()

    def fetch(self) -> Generator[MeiTuanItem, None, None]:
        """从 MT 抓取 伊婉 内容
        """
        resp = requests.get(
            self.ITEMS_URL, headers=self.HEADERS, cookies=self.cookies)

        print(resp.status_code)
        # print(resp.text)
        html = etree.HTML(resp.text)
        items = html.xpath('//*[@class="list-item-desc"]')
        for item in items:
            node_title = item.xpath(
                './div[@class="list-item-desc-top"]/a')[0]
            address_text = item.xpath(
                './/span[@class="address ellipsis"]/text()')[0]
            node_deal = item.xpath('./div/div/a[@class="link deal-content"]')

            for deal in node_deal:
                title_text = deal.xpath(
                    './div/span/span[@class="hlt-span"]/text()')
                price_text = deal.xpath(
                    './div/span[@class="deal-price"]/text()')[0]
                yield MeiTuanItem(
                    hospital=node_title.text,
                    link=node_title.get('href'),
                    title='伊婉'.join(title_text),
                    price=price_text,
                    address=address_text,
                    city='北京')

    def write_to_file(self, fp: io.TextIOBase):
        """以纯文本格式将 Item 内容写入文件
        实例化参数文件对象 fp 被挪到了 write_to_file 方法中
        """
        # 将文件写入逻辑托管给 ItemWriter 类处理
        writer = ItemWriter(fp, title=self.FILE_TITLE)
        writer.write(list(self.fetch()))

    def get_cookie(self) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=options)

        driver.get("http://nb.meituan.com/")
        cookies = driver.get_cookies()
        my_cookie = {}
        for el in cookies:
            my_cookie[el['name']] = el['value']
        print(my_cookie)
        driver.close()
        return my_cookie


def main():

    # with open('/tmp/hn_top5.txt') as fp:
    #     crawler = HNTopPostsSpider(fp)
    #     crawler.write_to_file()

    # 因为 HNTopPostsSpider 接收任何 file-like 的对象，所以我们可以把 sys.stdout 传进去
    # 实现往控制台标准输出打印的功能
    crawler = MTSpider()
    crawler.write_to_file(sys.stdout)


if __name__ == '__main__':
    main()
