import csv
import datetime

import requests

from get_address import get_address

KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}河狸家销售情况.csv'

cookies = {
    'beacon_id':
        'MTAxLjI1MS4yMTQuMTMwLTVFMjMtNTg4NDY2RTlEMkUxOC0xMw',
    'search_sort_plan':
        'rank_new',
    'track':
        'eyJjb29raWVfaWQiOiIxNTU3MjEwOTY5MTk1NDdndiIsInNlc3Npb25faWQiOjE1NTcyMTI4MzIzMTksInBhZ2Vfc3RlcCI6MSwic2Vzc2lvbl9maXJzdCI6MTU1NzIxMDk2OTE5NCwic2Vzc2lvbl9sYXN0IjoxNTU3MjEwOTY5MTk0LCJzZXNzaW9uX2NvdW50IjoyLCJ2aWV3X2xhc3QiOm51bGwsInZpZXdfdGhpcyI6MTU1NzIxMjg2NTY4NH0%3D',
}

headers = {
    'Connection':
        'keep-alive',
    'Pragma':
        'no-cache',
    'Cache-Control':
        'no-cache',
    'Upgrade-Insecure-Requests':
        '1',
    'User-Agent':
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
    'DNT':
        '1',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':
        'gzip, deflate, br',
    'Accept-Language':
        'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def get_data(startNum):
    params = (
        ('query', '\u4F0A\u5A49'),
        ('type', 'product'),
        ('hiddenCross', '1'),
        ('start', str(startNum)),
        ('num', '50'),
    )
    url = 'https://search-api.helijia.com/search-api/search/item_query'
    try:
        web = requests.get(
            url, headers=headers, cookies=cookies, params=params)
        data = web.json()
        return web.url, data['data']
    except Exception as e:
        raise e


def parse_data(data):
    if data is None:
        raise 'None error'
    # res = re.sub(r' |\n', '', web)
    # res_json = json.loads(res)
    result = data["resultList"]
    if len(result) > 0:
        for el in result:
            if '伊婉' in el['name']:
                info = {
                    # 'hospital_id': hospital['hospital_id'],
                    'hospital': el['artisanNick'],
                    'address': get_address(*el['location'].split(',')),
                    'title': el['name'],
                    'price': el['price'],
                    'link':
                        'https://m.helijia.com/product.html?id=' + el['id'],
                }
                yield info


def main():
    isEmpty = False
    # 6. 存储数据
    with open(file, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['hospital', 'address', 'title', 'price', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        startNum = 0
        while not isEmpty:
            print(f'开始抓取 {startNum}到{startNum + 50}的内容')
            # 2. 获取数据
            url, data = get_data(startNum)
            if data['num'] != 0:
                print(f'>>> 开始解析 {url} ...')
                # 3. 解析数据
                for el in parse_data(data):
                    print(el)
                    writer.writerow(el)
                startNum += 50
            else:
                isEmpty = True


if __name__ == "__main__":
    main()
