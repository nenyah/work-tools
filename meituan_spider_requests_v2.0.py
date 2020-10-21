import random

import requests
from lxml import etree

headers_list = [
    'Opera/7.10 (Windows NT 5.1; U)  [en]',
    'Opera/9.80 (X11; Linux i686; U; it) Presto/2.5.24 Version/10.54',
    'Opera/9.64 (X11; Linux i686; U; de) Presto/2.1.1',
    'Mozilla/5.0 (Windows NT 5.2; U; ru; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.70',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 GTB7.0',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-gb) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85.8.1',
]
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
        random.choice(headers_list),
    'DNT': '1',
    'Accept': '*/*',
    'Origin': 'https://bj.meituan.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://bj.meituan.com/s/%20%E4%BC%8A%E5%A9%89/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
url = 'http://i.meituan.com/s/-%E4%BC%8A%E5%A9%89/?p=1'
res = requests.get(url, headers=headers, cookies=cookies)
tree = etree.HTML(res.text)
hrefs = tree.xpath('//dl[contains(@class,"bd-deal-list")]/dd/a/@href')
titles = tree.xpath('//dl[contains(@class,"bd-deal-list")]//div[contains(@class,"title")]/text()')
prices = tree.xpath('//dl[contains(@class,"bd-deal-list")]//div[@class="price"]/span[1]/text()')
for href, title, price in zip(hrefs, titles, prices):
    print(href, title, price)
print(tree.xpath('//span[@class="poiname"]/text()'))
