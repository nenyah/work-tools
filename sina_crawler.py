import json
import re
import sys
import time

import jsonpath
import pandas as pd
from lxml import etree
from selenium.webdriver import Chrome


class Spider:
    def __init__(self, index_url: str):
        self.index_url: str = index_url
        self.raw_htmls: list = []
        self.boot()

    def boot(self):
        self.chrome = Chrome()
        self.chrome.start_client()
        self.check_cookie()

    def check_cookie(self):
        raise NotImplementedError

    def crawl(self, target_url: str) -> list:
        self.chrome.get(target_url)
        print('wait for page loading')
        time.sleep(2)
        self.raw_htmls.append(self.chrome.page_source)


class SinaSpider(Spider):
    def check_cookie(self):
        from utils import cookie_list
        if cookie_list:
            self.chrome.get(self.index_url)
            time.sleep(5)
            self.chrome.delete_all_cookies()
            print('clear')
            for c in cookie_list:
                self.chrome.add_cookie(c)
            print('Done')
        else:
            print('pls add cookie first')
            sys.exit()


class Parser:
    def __init__(self):
        self.content: list = []
        self._ids: set = set()

    def parse(self, html_list: list, page_type='list'):
        for html in html_list:
            re_res = re.findall(r'({.*})', html)
            data = json.loads(re_res[0])
            if page_type == 'list':
                try:
                    users: list = jsonpath.jsonpath(data, '$..user')
                    _ids: list = jsonpath.jsonpath(data, '$..mblog.id')
                    for user, _id in zip(users, _ids):
                        print(user)
                        self.content.append(user)
                        self._ids.add(_id)
                except Exception:
                    pass

            else:
                try:
                    users: list = jsonpath.jsonpath(data, '$..user')
                    for user in users:
                        print(user)
                        self.content.append(user)
                except Exception:
                    pass


## download --> parse --> save
s = SinaSpider('https://m.weibo.cn/')
## https://s.weibo.com/weibo?q=#守护最美逆行天使#&nodup=1&page=1
for i in range(1, 9):
    s.crawl(
        f'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&page_type=searchall&page={i}'
    )
p = Parser()
p.parse(s.raw_htmls)
s.raw_htmls = []
for _id in list(p._ids):
    s.crawl(
        f'https://m.weibo.cn/comments/hotflow?id={_id}&mid={_id}&max_id_type=0'
    )
    s.crawl(
        f'https://m.weibo.cn/api/statuses/repostTimeline?id={_id}'
    )
p.parse(s.raw_htmls, page_type='detail')
df = pd.DataFrame(p.content)
df.to_csv('./sina.csv', index=False)