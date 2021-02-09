#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import re
import sys
from datetime import datetime

import requests
from typing import Generator, List, Optional

from lxml import etree
import pandas as pd

class Item:
    """MB(https://www.meb.com/) 上的条目

    :param title: 标题
    :param link: 链接
    :param img: 图片
    :param hospital: 医院
    :param price: 价格
    :param sold: 销量
    """

    def __init__(self, title: str, link: str, img: str, hospital: str, price: float, sold: int):
        """初始化
        """
        self.title = title
        self.link = link
        self.img = img
        self.hospital = hospital
        self.price = price
        self.sold = sold


class MBItemSpider:
    """抓取 HackerNews Top 内容条目

    :param limit: 限制条目数，默认为 5
    :param filter_by_link_keywords: 过滤结果的关键词列表，默认为 None 不过滤
    """
    ROOT_URL = 'https://www.meb.com'

    def __init__(self,
                 limit: int = 5,
                 page: int = 5,
                 filter_by_link_keywords: Optional[List[str]] = None):
        self.limit = limit
        self.page = page
        self.urls = [f'{MBItemSpider.ROOT_URL}/search/productlist/%E4%BC%8A%E5%A9%89_{str(i)}' for i in
                     range(1, self.page)]
        self.filter_by_link_keywords = filter_by_link_keywords
        self.products: List[Item] = []

    def fetch(self):
        """从 MB 抓取产品内容
        """
        url = self.urls.pop()
        print(f'start to get {url}...')
        resp = requests.get(url)

        # 使用 XPath 可以方便的从页面解析出你需要的内容，以下均为页面解析代码
        # 如果你对 xpath 不熟悉，可以忽略这些代码，直接跳到 yield Post() 部分
        html = etree.HTML(resp.text)
        items = html.xpath('//div[@class="content_list"]')
        counter = 0
        for item in items:
            if counter >= self.limit:
                break
            title = item.xpath('.//a[@class="text_one"]/text()')[0]
            link = item.xpath('.//a[@class="lists_img"]/@href')[0]
            img = item.xpath('.//img/@src')[0]
            hospital = item.xpath('.//span[@class="text_two"]/text()')[0]
            price = item.xpath('.//span[@class="now_my"]//text()')[0]
            sold_text = item.xpath('.//div[@class="grade_box"]/text()')
            product = Item(
                title=title,
                link=MBItemSpider.ROOT_URL + link,
                img=MBItemSpider.ROOT_URL + img,
                hospital=hospital.strip(),
                price=float(price.replace('￥', '')),
                # 可能会没有销量
                sold=re.findall(r"\d+", sold_text[0])[0] if sold_text else '0'
            )
            if self.filter_by_link_keywords is None:
                counter += 1
                self.products.append(product)
            # 当 link 中出现任意一个关键词时，返回结果
            elif any(keyword in product.title
                     for keyword in self.filter_by_link_keywords):
                counter += 1
                self.products.append(product)

    def run(self):
        """运行爬虫
        """
        num = len(self.urls)
        for _ in range(num):
            self.fetch()


def write_posts_to_file(items: List[Item], fp: io.TextIOBase, title: str):
    """负责将帖子列表写入文件
    """
    fp.write(f'# {title}\n\n')
    for i, item in enumerate(items, 1):
        fp.write(f'> Item {i}: {item.title}\n')
        fp.write(f'> sold：{item.sold} price：{item.price}\n')
        fp.write(f'> hospital：{item.hospital}\n')
        fp.write(f'> link：{item.link}\n')
        fp.write(f'> img：{item.img}\n')
        fp.write('------\n')


def main():
    link_keywords = ['伊婉']
    crawler = MBItemSpider(limit=20, filter_by_link_keywords=link_keywords)
    crawler.run()
    items = [product.__dict__ for product in crawler.products]
    KEYWORD = '伊婉'
    today = datetime.today().strftime('%Y-%m-%d')
    file = f'E:/玻尿酸销售情况/{today}{KEYWORD}美呗销售状况.csv'
    df = pd.DataFrame(items)
    df.to_csv(file, index=False)


if __name__ == "__main__":
    main()
