'''
@Description: 大众点评价格采集
@Author: Steven
@Date: 2020-06-02 09:57:08
@LastEditors: Steven
@LastEditTime: 2020-06-04 09:22:40
'''

import sys
import time
from datetime import datetime

import pandas as pd
from lxml import etree
from selenium.webdriver import Chrome

KEYWORD = '伊婉'


class Spider:
    def __init__(self, index_url: str):
        self.index_url: str = index_url
        self.raw_htmls: list = []
        self.boot()

    def boot(self):
        self.chrome = Chrome()
        self.chrome.start_client()
        self.check_cookie()

    def check_cookie(self):
        raise NotImplementedError

    def crawl(self, target_url: str, page_type='list') -> tuple:
        self.chrome.get(target_url)
        print('wait for page loading')
        time.sleep(2)
        self.raw_htmls.append((target_url, self.chrome.page_source, page_type))
        return target_url, self.chrome.page_source, page_type


class DazhongSpider(Spider):
    def check_cookie(self):
        from utils import parse_cookie, dianping_cookies
        cookie_list = parse_cookie(dianping_cookies)
        if cookie_list:
            self.chrome.get(self.index_url)
            time.sleep(5)
            self.chrome.delete_all_cookies()
            print('clear')
            for c in cookie_list:
                self.chrome.add_cookie(c)
            print('Done')
        else:
            print('pls add cookie first')
            sys.exit()


class Parser:
    def __init__(self):
        self.content: list = []
        self._ids: set = set()

    def parse(self, link: str, html: str, page_type: str) -> str:
        # for link, html, page_type in html_list:
        tree = etree.HTML(html)
        if page_type == 'list':
            return self._parse_list(tree)
        else:
            return self._parse_item(tree, link)

    def _parse_list(self, tree: etree) -> str:
        nomore: list = tree.xpath('//div[@class="not-found"]')
        if nomore:
            return 'nomore'
        try:
            products: list = tree.xpath(
                '//div[@id="shop-all-list"]//div[@class="svr-info"]//a[@data-click-name="shop_info_gooddeal_click"]/@title'
            )
            product_link: list = tree.xpath(
                '//div[@id="shop-all-list"]//div[@class="svr-info"]//a[@data-click-name="shop_info_gooddeal_click"]/@href'
            )
            for product, link in zip(products, product_link):
                if '伊婉' in product:
                    self._ids.add(link)
            return 'hasmore'
        except Exception:
            pass

    def _parse_item(self, tree: etree, link: str):
        try:
            item = {}
            item['product'] = tree.xpath(
                '//p[@class="product-name bold"]/text()')[0]
            item['link'] = link
            item['price'] = tree.xpath('//div[@class="price"]//text()')[-1]
            item['hospital'] = tree.xpath(
                '//div[@class="shop-item"]/p[@class="shop-name"]/text()')[0]
            item['address'] = tree.xpath(
                '//div[@class="shop-item"]/p[@class="shop-addr"]/text()'
            )[0].replace('地址：', '')
            item['phone'] = tree.xpath(
                '//div[@class="shop-item"]/p[@class="shop-phone"]/text()'
            )[0].replace('电话：', '')
            print(item)
            self.content.append(item)
            return 'success'
        except Exception:
            pass


def main():
    s = DazhongSpider("http://www.dianping.com/")
    p = Parser()
    city_list = list(range(1, 20))
    for cid in city_list:
        url = f'https://www.dianping.com/search/keyword/{cid}/0_{KEYWORD}'
        for link in [f'{url}/p{page}' for page in range(1, 12)]:
            link, html, page_type = s.crawl(link, 'list')
            res = p.parse(link, html, page_type)
            if res == 'nomore':
                break
    for link in p._ids:
        link, html, page_type = s.crawl(link, 'page')
        res = p.parse(link, html, page_type)
        if res != 'success':
            continue

    today = datetime.today().strftime('%Y-%m-%d')
    file = f'E:/玻尿酸销售情况/{today}{KEYWORD}点评销售状况.csv'
    df = pd.DataFrame(p.content)
    df.to_csv(file, index=False)
    s.chrome.close()


if __name__ == '__main__':
    main()
