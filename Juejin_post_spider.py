#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Description: 
Author: Steven
Date: 2020-08-06 11:32:27
LastEditors: Steven
LastEditTime: 2020-09-29 09:17:41
'''

import io
import sys
from typing import Generator, List, Optional

import requests
from lxml import etree


class Post:
    """HN(https://news.ycombinator.com/) 上的条目

    :param title: 标题
    :param link: 链接
    :param points: 当前得分
    :param comments_cnt: 评论数
    """
    def __init__(self, title: str, link: str, pub_time: str):
        self.title = title
        self.link = link
        self.pub_time = pub_time


class BLNewsPostsSpider:
    """抓取 北仑新闻 内容条目

    :param limit: 限制条目数，默认为 5
    :param filter_by_link_keywords: 过滤结果的关键词列表，默认为 None 不过滤
    """
    ITEMS_URL = 'http://blnews.cnnb.com.cn/xwzx/bdxw/'

    def __init__(self,
                 limit: int = 5,
                 filter_by_link_keywords: Optional[List[str]] = None):
        self.limit = limit
        self.filter_by_link_keywords = filter_by_link_keywords

    def fetch(self) -> Generator[Post, None, None]:
        """从 北仑新闻 抓取内容
        """
        resp = requests.get(self.ITEMS_URL)
        resp.encoding = 'gb2312'
        # 使用 XPath 可以方便的从页面解析出你需要的内容，以下均为页面解析代码
        # 如果你对 xpath 不熟悉，可以忽略这些代码，直接跳到 yield Post() 部分
        html = etree.HTML(resp.content)
        items = html.xpath('//td[@class="text4"]/a')
        counter = 0
        for item in items:
            if counter >= self.limit:
                break
            node_title = item.text
            link = item.get('href')
            pub_time = '-'.join(link.split('/')[2:5])

            post = Post(title=node_title, link=link, pub_time=pub_time)
            if self.filter_by_link_keywords is None:
                counter += 1
                yield post
            # 当 link 中出现任意一个关键词时，返回结果
            elif any(keyword in post.title.lower()
                     for keyword in self.filter_by_link_keywords):
                counter += 1
                yield post


def write_posts_to_file(posts: List[Post], fp: io.TextIOBase, title: str):
    """负责将帖子列表写入文件
    """
    fp.write(f'# {title}\n\n')
    for i, post in enumerate(posts, 1):
        fp.write(f'> TOP {i}: {post.title}\n')
        fp.write(f'> 发布时间：{post.pub_time}\n')
        fp.write(f'> 地址：{post.link}\n')
        fp.write('------\n')


def main():
    link_keywords = None
    crawler = BLNewsPostsSpider(filter_by_link_keywords=link_keywords)

    posts = list(crawler.fetch())
    file_title = 'Top news on Beilun News'
    write_posts_to_file(posts, sys.stdout, file_title)


if __name__ == '__main__':
    main()
