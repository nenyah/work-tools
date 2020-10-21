#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Description: 美团数据采集
@Author: Steven
@Date: 2019-12-06 16:15:49
@LastEditors  : Steven
@LastEditTime : 2019-12-31 09:38:18
'''
import csv
import datetime
import math

import requests

from cityid import hot_city_id as city_id
from config import KEYWORD

# from selenium import webdriver

_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}美团销售情况.csv'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--log-level=3')
# chrome_options.add_experimental_option('excludeSwitches',
#                                        ['enable-automation'])
# driver = webdriver.Chrome(options=chrome_options)

# driver.get("http://nb.meituan.com/")
# cookies = driver.get_cookies()
# my_cookies = {el['name']: el['value'] for el in cookies}
# print(my_cookies)
# driver.close()

cookies = {
    'uuid': 'f424126a28a84a1c9512.1583117027.1.0.0',
    '_lxsdk_cuid': '1709920ccf8c8-0243b6f1f79d42-c383f64-1fa400-1709920ccf8a6',
    'ci': '1',
    'rvct': '1',
    '_lxsdk_s': '1709920b301-144-ca1-831%7C%7C108',
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'DNT': '1',
    'Accept': '*/*',
    'Origin': 'https://bj.meituan.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://bj.meituan.com/s/%20%E4%BC%8A%E5%A9%89/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
proxies = {'http': 'http://104.129.183.20:1024'}
LIMIT_NUM = 32


def get_data(url: str, OFFSET: int = 0):

    params = (
        ('uuid', cookies['uuid']),
        ('userid', '-1'),
        ('limit', str(LIMIT_NUM)),
        ('offset', str(OFFSET)),
        ('cateId', '-1'),
        ('q', '\u4F0A\u5A49'),
    )
    try:
        web = requests.get(url,
                           headers=headers,
                           params=params,
                           cookies=cookies)
        print(f'>>> Start to get {web.url}')
        data = web.json()
        print(f'>>> Success to get {len(data)}')
        return url, data['data']
    except Exception as e:
        raise e


def parse_total(data: dict):
    if data is None:
        raise Exception('None error')
    return int(data['totalCount'])


def parse_data(data: dict):
    if data is None:
        raise Exception('None error')

    items = data['searchResult']
    for item in items:
        # print(item)
        if item['deals']:
            for deal in item['deals']:
                if '伊婉' in deal['title']:
                    info = {
                        'link':
                        'https://www.meituan.com/jiankangliren/' +
                        str(item['id']),
                        'hospital_name':
                        item['title'],
                        'title':
                        deal['title'],
                        'price':
                        deal['price'],
                        'address':
                        item['address'],
                        'city':
                        item['city']
                    }
                    yield info


def main():
    # 1. 根据city_id 生成url
    urls = (f'http://apimobile.meituan.com/group/v4/poi/pcsearch/{cid}/'
            for cid in sorted(city_id.keys()))

    # 6. 存储数据
    with open(file, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'link', 'hospital_name', 'title', 'price', 'address', 'city'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for url in urls:
            print(f'>>> 开始抓取 {url}')
            # 2. 获取total_count
            url, data = get_data(url)
            total = parse_total(data)
            page = math.ceil(total / LIMIT_NUM)
            print(f'>>> Page {page}')
            for p in range(page):
                # 4. 获取更新数据
                url, data = get_data(url, p * LIMIT_NUM)
                # print(len(data))
                # 5. 解析数据
                for el in parse_data(data):
                    print(el)
                    writer.writerow(el)


if __name__ == '__main__':
    main()
