import csv
import datetime

import requests
from selenium import webdriver

from cityid import hot_city_id as city_id

KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}美团销售情况.csv'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://nb.meituan.com/")
cookies = driver.get_cookies()
my_cookie = {}
for el in cookies:
    my_cookie[el['name']] = el['value']
print(my_cookie)
driver.close()

headers = {
    'Connection':
        'keep-alive',
    'Cache-Control':
        'max-age=0',
    'Upgrade-Insecure-Requests':
        '1',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'DNT':
        '1',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':
        'gzip, deflate',
    'Accept-Language':
        'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('offset', '0'),
    ('q', KEYWORD),
)


def get_data(url):
    try:
        web = requests.get(
            url, headers=headers, cookies=my_cookie, params=params)
        # print(web.url)
        data = web.json()
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
        # print(item)
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
            print(f'>>> {url}\t总数是：{total}')
            # 3. 根据total_count重新生成url
            url += f'?limit={total}'
            # 4. 获取更新数据
            url, data = get_data(url)
            print(len(data))
            # 5. 解析数据
            for el in parse_data(data):
                print(el)
                writer.writerow(el)


if __name__ == '__main__':
    main()
