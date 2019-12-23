import random
import time
from datetime import datetime

import pandas as pd
import pymongo
import requests
from lxml import etree
from selenium import webdriver

from config import DAZHONG_COLLECTION, DAZHONG_DB, MONGODB_HOST, MONGODB_PORT

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[DAZHONG_DB]
collection = db[DAZHONG_COLLECTION]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://www.dianping.com/ningbo")
cookies = driver.get_cookies()
my_cookie = {}
for el in cookies:
    my_cookie[el['name']] = el['value']
print(my_cookie)
driver.quit()

headers = {
    'Connection':
        'keep-alive',
    'Cache-Control':
        'max-age=0',
    'Upgrade-Insecure-Requests':
        '1',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'DNT':
        '1',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,\
            image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':
        'gzip, deflate, br',
    'Accept-Language':
        'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def get_link(cityid=1):
    flag = True
    page = 1
    while flag:
        try:
            print(f'>>> 开始爬取列表，城市ID是{cityid}, 第{page}页 ...')
            time.sleep(random.randint(1, 4))
            response = requests.get(
                f'https://www.dianping.com/search/keyword/{cityid}' +
                f'/0_%E4%BC%8A%E5%A9%89/p{page}',
                headers=headers,
                cookies=my_cookie)
        except Exception:
            get_link(page)
        page += 1
        if response.status_code == 200:
            tree = etree.HTML(response.text)
            nodes = tree.xpath('//*[@class="svr-info"]//a')
            no_exist = tree.xpath('//div[@class="not-found"]')
            if no_exist:
                print(f'>>> 当前是列表，{page}页，没有内容了，停止爬取！')
                flag = False

            for node in nodes:
                product_name = node.xpath('./@title')[0]
                if '伊婉' in product_name and '商品' in product_name:
                    info = {
                        'title': product_name,
                        'link': node.xpath('./@href')[0]
                    }

                    yield info


# https://g.dianping.com/fuse/HktMNFLCM?pf=dppc&productid=3829715&shopid=58387941
def get_detail(url):
    try:
        time.sleep(random.randint(1, 4))
        response = requests.get(url, headers=headers, cookies=my_cookie)
    except Exception:
        get_detail(url)
    if 'm.dianping.com' in response.url:
        return None
    # print(response.status_code)
    print(f'>>> 开始解析 {url}')
    if response.status_code == 200:
        tree = etree.HTML(response.text)
        info = {
            'link': url,
            'title': get_el(tree, '//*[@class="product-name bold"]/text()')[0],
            'price': ' '.join(get_el(tree, '//*[@class="price"]//text()')),
            'hospital_name': get_el(tree, '//*[@class="shop-name"]/text()')[0],
            'addr': get_el(tree, '//*[@class="shop-addr"]/text()')[0],
            'phone': get_el(tree, '//*[@class="shop-phone"]/text()')[0],
            'crawl_date': datetime.today().strftime('%Y-%m-%d')
        }
        print('>>> 解析成功')
        # print(info)
        save_to_mongodb(info)
        # return info


def get_el(tree, rule):
    node = tree.xpath(rule)
    if node:
        return node
    else:
        raise Exception("Node can't find")


def save_to_mongodb(result):
    try:
        res = collection.update_one({
            "link": result["link"]
        }, {"$set": result},
            upsert=True)
        if res.matched_count or res.upserted_id:
            print(">>> 存储到数据成功")
    except Exception:
        print(">>> 存储到数据库失败")


def out_to_csv(date, file):
    df = pd.DataFrame(collection.find())
    df = df[df['crawl_date'] == date][[
        'addr', 'crawl_date', 'hospital_name', 'link', 'phone', 'price',
        'title'
    ]]
    df.to_csv(file, index=False)


def main():
    cityid = [2, 1, 4, 7, 10, 3, 5, 6, 8, 16, 9, 17]
    city_ids = cityid[:]
    for cid in city_ids:
        for info in get_link(cid):
            try:
                get_detail(info['link'])
            except Exception:
                print(f">>> {info['link']}解析出错！！！")

    today = datetime.today().strftime('%Y-%m-%d')
    file = f'E:/玻尿酸销售情况/{today}伊婉点评销售状况.csv'
    out_to_csv(today, file)


if __name__ == "__main__":
    main()
