'''
@Description: 美团数据采集
@Author: Steven
@Date: 2019-12-06 16:15:49
@LastEditors: Steven
@LastEditTime: 2019-12-09 09:08:06
'''
import csv
import datetime
import math

import requests
from selenium import webdriver

from cityid import hot_city_id as city_id

KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}美团销售情况.csv'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option(
    'excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(chrome_options=chrome_options)


driver.get("http://nb.meituan.com/")
cookies = driver.get_cookies()
my_cookies = {}
for el in cookies:
    my_cookies[el['name']] = el['value']
print(my_cookies)
driver.close()

cookies = {
    'uuid': '6f810ad1c4fb494aa841.1575594096.1.0.0',
    '_lxsdk_cuid': '16ed8ba0341c8-087a97ce95c10c-7711b3e-1fa400-16ed8ba0341c8',
    'ci': '1',
    'rvct': '1',
    '_lxsdk_s': '16eda194ea6-86e-255-e9d%7C%7C302',
}

headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://bj.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'DNT': '1',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://bj.meituan.com/s/%E4%BC%8A%E5%A9%89/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

LIMIT_NUM = 32


def get_data(url: str, OFFSET: int = 0):

    params = (
        ('uuid', my_cookies['uuid']),
        ('userid', '-1'),
        ('limit', str(LIMIT_NUM)),
        ('offset', str(OFFSET)),
        ('cateId', '-1'),
        ('q', '\u4F0A\u5A49'),
    )
    try:
        web = requests.get(
            url, headers=headers, params=params, cookies=my_cookies)
        # print(web.url)
        data = web.json()
        print(len(data))
        return url, data['data']
    except Exception as e:
        raise e


def parse_total(data):
    if data is None:
        raise 'None error'
    return data['totalCount']


def parse_data(data):
    if data is None:
        raise 'None error'

    items = data['searchResult']
    for item in items:
        print(item)
        if item['deals']:
            for deal in item['deals']:
                if '伊婉' in deal['title']:
                    info = {
                        'link':
                            'https://www.meituan.com/jiankangliren/' + str(
                                item['id']),
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
            print(f'开始抓取 {url}')
            # 2. 获取total_count
            url, data = get_data(url)
            total = parse_total(data)
            page = math.ceil(total / LIMIT_NUM)
            for p in range(page+1):
                # 4. 获取更新数据
                url, data = get_data(url, p*LIMIT_NUM)
                print(len(data))
                # 5. 解析数据
                for el in parse_data(data):
                    print(el)
                    writer.writerow(el)


if __name__ == '__main__':
    main()
