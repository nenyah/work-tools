#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from pathlib import Path
from typing import List

import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class MeituanItem:
    city: str = ''
    address: str = ''
    price: int = -1
    link: str = ''
    hospital_name: str = ''
    title: str = ''

    def __init__(self, link: str = '', hospital_name: str = '', title: str = '', price: int = -1, address: str = '',
                 city: str = ''):
        self.city = city
        self.address = address
        self.price = price
        self.link = link
        self.hospital_name = hospital_name
        self.title = title

    @staticmethod
    def keys():
        """对象属性
        Returns:
            city,address,price,link,hospital_name,title
        """
        return 'city', 'address', 'price', 'link', 'hospital_name', 'title'

    def __getitem__(self, key):
        return getattr(self, key)


class MeituanSpider:
    """美团爬虫"""
    base_url = 'https://bj.meituan.com/'

    def __init__(self,
                 limit: int = None,
                 urls=None
                 ):
        """Constructor for MeituanSpider"""
        if urls is None:
            urls = {'北京': "https://bj.meituan.com/s/%E4%BC%8A%E5%A9%89/"}
        self.urls = urls
        self.limit = limit
        self.page = 1
        self.driver, self.wait = MeituanSpider.start_client()
        self.items = []

    def run(self):
        """运行爬虫
        """
        for city, url in self.urls.items():
            self.fetch(city, url)
            self.page = 1

    def fetch(self, city: str, url: str):
        """从美团抓取伊婉内容
        """
        try:
            print(f">>> 下载{url}， 第{self.page}页...")
            if self.page == 1:
                self.driver.get(url)
        except Exception:
            print(f"下载{url},第{self.page}页，失败")
            self.fetch(city, url)
        self.page += 1

        html = etree.HTML(self.driver.page_source)
        items = html.xpath('//*[contains(@class,"default-list-item")]')
        is_active = html.xpath('//li[contains(@class,"pagination-item next-btn active")]')
        for item in items:
            hospital_name = item.xpath('.//a[@class="link item-title"]/text()')
            address = item.xpath('.//span[contains(@class,"address")]/text()')
            products = item.xpath('.//*[@class="deal-wrapper"]/a')

            if products:
                for product in products:
                    title = ''.join(product.xpath('./div[@class="deal-title"]//text()'))
                    if '伊婉' in title:
                        item = MeituanItem(
                            hospital_name=hospital_name[0],
                            address=address[0],
                            link=product.xpath('./@href')[0],
                            title=''.join(product.xpath('./div[@class="deal-title"]//text()')),
                            price=product.xpath('.//span[@class="deal-price"]//text()')[-1],
                            city=city
                        )
                        self.items.append(item)
        if is_active:
            self.next_page(self.wait)
            self.fetch(city, url)

    @staticmethod
    def next_page(driver_wait: WebDriverWait):
        """翻页
        Args:
            wait WebDriverWait
        """
        next_page_node = driver_wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class,"right-arrow")]')))
        next_page_node.click()

    @staticmethod
    def start_client() -> (WebDriver, WebDriverWait):
        """开启selenium
        Returns:
            chrome_driver WebDriver
            driver_wait WebDriverWait
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option('excludeSwitches',
                                               ['enable-automation'])
        chrome_driver = webdriver.Chrome(options=chrome_options)
        chrome_driver.start_client()
        driver_wait = WebDriverWait(chrome_driver, 10)
        chrome_driver.get(MeituanSpider.base_url)
        return chrome_driver, driver_wait


def write_posts_to_file(posts: List[MeituanItem], file: str):
    """负责将帖子列表写入文件
    """
    df = pd.DataFrame(dict(post) for post in posts)
    print(df.head())
    df.to_csv(file, index=False)


def main():
    _path = Path(r"E:\玻尿酸销售情况")
    today = datetime.date.today()
    urls = {
        '北京': "https://bj.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '上海': "https://sh.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '广州': "https://gz.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '深圳': "https://sz.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '天津': "https://tj.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '西安': "https://xa.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '重庆': "https://cq.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '杭州': "https://hz.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '南京': "https://nj.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '武汉': "https://wh.meituan.com/s/%E4%BC%8A%E5%A9%89/",
        '成都': "https://cd.meituan.com/s/%E4%BC%8A%E5%A9%89/",
    }
    mt = MeituanSpider(urls=urls)
    mt.run()
    posts = mt.items
    file_title = '美团伊婉销售数据'
    file = _path / f'{today}{file_title}.csv'
    write_posts_to_file(posts, file)
    mt.driver.close()
    print("所有爬虫执行完毕!")


if __name__ == '__main__':
    main()
