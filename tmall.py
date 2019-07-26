#! python3
# coding:utf-8
# tmall.py 天猫采集
import csv
import datetime
import time

import requests

KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}天猫销售情况.csv'

headers = {
    'dnt':
        "1",
    'accept-encoding':
        "gzip, deflate, br",
    'accept-language':
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'user-agent':
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36",
    'accept':
        "*/*",
    'referer':
        "https://list.tmall.com/search_product.htm?q=%D2%C1%CD%F1&type=p&tmhkh5=&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_searchbutton&searchType=&closedKey=",
    'authority':
        "list.tmall.com",
    'Cache-Control':
        "no-cache",
    'Host':
        "list.tmall.com",
    'Connection':
        "keep-alive",
    'cache-control':
        "no-cache"
}


def get_data(page_no=1):
    url = "https://list.tmall.com/m/search_items.htm"

    querystring = {
        "page_size": "20",
        "page_no": str(page_no),
        "q": KEYWORD,
        "type": "p",
        "from": "mallfp..m_1_searchbutton"
    }
    try:
        time.sleep(3)
        print(f'Start to get {page_no} ...')
        response = requests.get(
            url, headers=headers, params=querystring, timeout=15)
        return response.url, response.json()
    except Exception as e:
        raise e


def parse_data(data):
    if data is None:
        raise 'None error'
    items = data['item']
    for item in items:
        if '伊婉' in item['title']:
            info = {
                'link': f'https:{item["url"]}',
                'hospital_name': item['shop_name'],
                'title': item['title'],
                'price': item['price'],
                'address': item['location'],
                'city': item['seller_loc']
            }
            yield info


with open(file, "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ['link', 'hospital_name', 'title', 'price', 'address', 'city']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(1, 15):
        url, data = get_data(i)
        for item in parse_data(data):
            print(item)
            writer.writerow(item)
