#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
import datetime
import logging
import os
import itertools

import requests
from requests import Response
from config import KEYWORD

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s- %(message)s')
log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


class SoyoungSpider:
    """docstring for SoyoungSpider"""
    root = 'http://www.soyoung.com/searchNew/'
    product_url = root + r'product?cityId=1&page_size=100&_json=1&sort=0'
    hospital_url = root + r'hospital?cityId=1&page_size=100&_json=1&sort=0'

    def __init__(self, keyword: str):
        self.keyword: str = keyword
        self.product_url: str = SoyoungSpider.product_url + '&keyword={}&page={}'
        self.hospital_url: str = SoyoungSpider.hospital_url + '&keyword={}&page={}'
        self.page: int = 1
        self.headers: dict = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'referer':
            'https://www.soyoung.com/',
            'Cookie':
            'PHPSESSID=89b5e6b3dc9357c1d0da860bbc6791f8; __usersign__=1589161223881482893; __postion__=a%3A4%3A%7Bs%3A6%3A%22cityId%22%3Bi%3A0%3Bs%3A8%3A%22cityName%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22cityCode%22%3Bi%3A0%3Bs%3A3%3A%22jwd%22%3Bi%3A0%3B%7D; _ga=GA1.2.1489774716.1589161703; _gid=GA1.2.1783629045.1589161703; Hm_lvt_b366fbb5465f5a86e1cc2871552e1fdb=1589161703; _gat=1; Hm_lpvt_b366fbb5465f5a86e1cc2871552e1fdb=1589162742'
        }
        self.item: list = []
        self.hospitals: list = []
        self.count: int = 1

    def get_base_info(self) -> None:
        url: str = self.product_url.format(self.keyword, self.page)
        try:
            r: Response = requests.get(url, headers=self.headers)
            hasmore = r.json()['responseData']['has_more']
            products = r.json()['responseData']['arr_product']
        except Exception:
            log(f"[x] err:{url} parse fail")
        if len(products) > 0:
            for product in products:
                info = {
                    'link': 'http://y.soyoung.com/cp' + product['pid'],
                    'hospital': product['hospital_name'],
                    'title': product['title'],
                    'price': product['price_online'],
                    'hospital_id': product['hospital_id']
                }
                self.item.append(info)
                log(f"[+] {self.count} Start to download {info['link']}")
                self.count += 1

        if hasmore:
            self.page += 1
            self.get_base_info()

    def get_hospital_info(self) -> None:
        url = self.hospital_url.format(self.keyword, self.page)
        try:
            r = requests.get(url, headers=self.headers)
            hospitals = r.json()['responseData']['hospital_list']
            hasmore = r.json()['responseData']['has_more']
        except Exception:
            log(f"[x] err:{url} parse fail")
        if len(hospitals) > 0:
            for hospital in hospitals:
                info = {
                    'hospital_id': hospital['hospital_id'],
                    'address': hospital['address']
                }
                self.hospitals.append(info)

        if hasmore:
            self.page += 1
            self.get_hospital_info()

    def match_address(self) -> None:
        for hospital, product in itertools.product(self.hospitals,
                                                   self.item.copy()):
            if hospital['hospital_id'] == product['hospital_id']:
                self.item.remove(product)
                product['address'] = hospital['address']
                self.item.append(product)

    def save(self, save_path: str) -> None:
        log(f'[+] Total item: {len(self.item)}')

        file = datetime.datetime.today().strftime('%Y-%m-%d') + \
            f'{self.keyword}新氧销售情况.csv'
        path = os.path.join(save_path, file)
        log(f'[+] Start to save file to {path}')
        with open(path, "w+", newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'title', 'price', 'link', 'address', 'hospital', 'hospital_id'
                # 'phone'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.item:
                writer.writerow(row)
        log('[+] Save success')

    def run(self, save_path: str) -> None:
        self.get_hospital_info()
        self.get_base_info()
        self.match_address()
        self.save(save_path)


def main():
    keyword = KEYWORD
    if os.name == 'nt':
        save_path = r'E:\玻尿酸销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    spider = SoyoungSpider(keyword)
    spider.run(save_path)


if __name__ == '__main__':
    main()
