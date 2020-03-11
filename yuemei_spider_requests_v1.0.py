#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os
import random
import sys
import time
from datetime import datetime

import pandas as pd
import pymongo
import requests
from lxml import etree

from config import (MONGODB_HOST, MONGODB_PORT, YUEMEI_COLLECTION, YUEMEI_DB,
                    KEYWORD)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s- %(message)s')

log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


cookies = {
    'Hm_lvt_bbb28c93aca8fe7e95a44b2908aabce7': '1560909709',
    'ym_onlyk': '1560909707979701',
    'ym_onlyknew': '15609097079822',
    '_yma': '1560909709802',
    'YUEMEI': 'enjl9bc870p4oggmt1lmp551l6',
    'acw_tc': '2760820815609954808364573e57d3193f25259be9e37baace9d9c1ff3c193',
    'yuemei_city': 'ningbo',
    'Hm_lpvt_bbb28c93aca8fe7e95a44b2908aabce7': '1560995593',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
            image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://so.yuemei.com/tao/%E4%BC%8A%E5%A9%89/city/all/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


class YueMeiSpider:
    """悦美爬虫"""
    def __init__(self, keyword: str):
        self.root = r'https://so.yuemei.com'
        self.keyword = keyword
        self.start_url = self.root + '/tao/' + self.keyword
        self.page_urls = (self.root + f'/tao/{self.keyword}/city/all/p{i}.html'
                          for i in range(1, 36))
        self.detail_url = set()

        self.count = 0

        self.client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client[YUEMEI_DB]
        self.collection = self.db[YUEMEI_COLLECTION]
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.file = self.get_file_path()

    def __get(self, url: str) -> str:
        """随机延时下载数据"""
        try:
            log(f'[+] {self.count:4d} Start to get {url}')
            r = requests.get(url, headers=headers, cookies=cookies)
            time.sleep(random.randint(1, 5))
            r.encoding = 'utf-8'
            self.count += 1
            return r.text
        except Exception:
            log("Can't get page", url)
            return None

    def parse_url(self, response: str):
        """解析列表目录的详情地址"""
        tree = etree.HTML(response)
        urls = tree.xpath('//a[contains(@class,"taoItem")]/@href')
        for url in urls:
            if url not in self.detail_url:
                self.detail_url.add(url)
                # self.parse_detal(url)

        # 判断有没有下一页
        # next_url = tree.xpath('//*[@class="next-page-btn"]/@href')

        # if next_url:
        #     next_page_url = self.root + next_url[0]
        #     self.parse_url(self.__get(next_page_url))

    def parse_detal(self, url: str):
        """解析详情内容"""
        log(f'[+] Start to parse {url}')
        response = self.__get(url)
        try:
            if response:
                tree = etree.HTML(response)
                title = self.__get_title(tree)
                price = self.__get_price(tree)
                link = url
                address = self.__get_address(tree)
                hospital = self.__get_hospital(tree)
                phone = self.__get_phone(tree)
                info = {
                    'title': title,
                    'price': price,
                    'link': link,
                    'address': address,
                    'hospital': hospital,
                    'phone': phone,
                    'crawl_date': self.date
                }
                log(info)
                self.save_to_mongodb(info)
        except Exception:
            pass

    def __get_title(self, tree: etree.Element):
        """获取标题"""
        if tree is None:
            raise Exception("Null exception", tree)

        title_parent = tree.xpath('//div[@class="mainTit"]')[0]
        title = clean_text(title_parent.xpath('string(.)'))
        return title

    def __get_price(self, tree: etree.Element):
        """获取价格"""
        if tree is None:
            raise Exception("Null exception", tree)
        price_node = tree.xpath(
            '//i[@class="ft36"]/text() | //*[@class="fs-20"]/text()')
        if price_node:
            price = clean_text(price_node[0])
            return price
        else:
            raise Exception("Null exception", tree)

    def __get_address(self, tree: etree.Element):
        """获取地址"""
        if tree is None:
            raise Exception("Null exception", tree)
        pat1 = '//p[@class="item3"]/text()'
        pat2 = '//*[@class="hospital"]//table//tr[3]/td[last()]/text()'
        rule = pat1 + ' | ' + pat2
        address_node = tree.xpath(rule)
        if address_node:
            address = clean_text(address_node[0]).replace('地址：', '')
            return address
        return None

    def __get_hospital(self, tree: etree.Element):
        """获取医院名"""
        if tree is None:
            raise Exception("Null exception", tree)
        hospital_node = tree.xpath('//p[@class="item1"]/a/text()')
        if hospital_node:
            hospital = clean_text(hospital_node[0])
            return hospital
        return None

    def __get_phone(self, tree: etree.Element):
        """获取电话号码"""
        if tree is None:
            raise Exception("Null exception", tree)
        phone_node = tree.xpath('//div[@class="hosInfo"]/p[last()]/text()')
        if phone_node:
            phone = clean_text(phone_node[0])
            return phone
        return None

    def crawl(self):
        """爬虫运行主体"""
        for url in self.page_urls:
            self.parse_url(self.__get(url))
        while len(self.detail_url):
            detail_url = self.detail_url.pop()
            self.parse_detal(detail_url)
        self.out_to_csv(self.date, self.file)

    def save_to_mongodb(self, result: dict):
        """存储数据到数据库"""
        try:
            res = self.collection.update_one({"link": result["link"]},
                                             {"$set": result},
                                             upsert=True)
            if res.matched_count or res.upserted_id:
                log(f'[+] 存储到数据成功')
        except Exception:
            log(f'[+] 存储到数据库失败')

    def out_to_csv(self, date: str, file: str):
        """从数据库导出数据到csv"""
        df = pd.DataFrame(self.collection.find())
        df = df[df['crawl_date'] == date][[
            'address', 'crawl_date', 'hospital', 'link', 'phone', 'price',
            'title'
        ]]
        df.to_csv(file, index=False)

    def get_file_path(self):
        """根据不同系统生成文件存储路径"""
        if os.name == 'nt':
            save_path = r'E:\玻尿酸销售情况'
        else:
            save_path = '/home/steven/sales_collect'
        file_name = f'{self.date}伊婉悦美销售状况.csv'

        file_path = os.path.join(save_path, file_name)
        return file_path


def main():
    # 1. 创建一个爬虫
    # 2. 给爬虫一个关键词
    # 3. 爬虫运行
    # 4. 保存数据
    if len(sys.argv) == 1:
        keyword = KEYWORD
    else:
        keyword = sys.argv[1]

    spider = YueMeiSpider(keyword)
    spider.crawl()


if __name__ == '__main__':
    main()
