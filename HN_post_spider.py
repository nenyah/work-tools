#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: HN爬虫
Author: Steven
Date: 2019-07-09 13:38:08
LastEditors: Steven
LastEditTime: 2020-09-29 09:17:14
"""

import io
import re
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

    def __init__(self, title: str, link: str, points: str, comments_cnt: str):
        self.title = title
        self.link = link
        self.points = int(points)
        self.comments_cnt = int(comments_cnt)


class HNTopPostsSpider:
    """抓取 HackerNews Top 内容条目

    :param limit: 限制条目数，默认为 5
    :param filter_by_link_keywords: 过滤结果的关键词列表，默认为 None 不过滤
    """
    ITEMS_URL = 'https://wolley.io/'

    def __init__(self,
                 limit: int = 5,
                 filter_by_link_keywords: Optional[List[str]] = None):
        self.limit = limit
        self.filter_by_link_keywords = filter_by_link_keywords

    def fetch(self) -> Generator[Post, None, None]:
        """从 HN 抓取 Top 内容
        """
        resp = requests.get(self.ITEMS_URL)

        # 使用 XPath 可以方便的从页面解析出你需要的内容，以下均为页面解析代码
        # 如果你对 xpath 不熟悉，可以忽略这些代码，直接跳到 yield Post() 部分
        html = etree.HTML(resp.text)
        items = html.xpath('//*[@class="news-item"]/div[@class="item-text"]')
        counter = 0
        for item in items:
            if counter >= self.limit:
                break
            node_title = item.xpath('./span[@class="title"]/a')[0]
            points_text = item.xpath('.//span[@class="by"]/text()')
            comments_text = item.xpath(
                './/span[@class="comments-link"]/a/text()')[0]
            post = Post(
                title=node_title.text,
                link=node_title.get('href'),
                # 条目可能会没有评分
                points=re.findall(r"\d+", points_text[0])[0] if points_text else '0',
                comments_cnt=re.findall(r"\d+", comments_text)[0] if "前往讨论" not in comments_text else '0')
            if self.filter_by_link_keywords is None:
                counter += 1
                yield post
            # 当 link 中出现任意一个关键词时，返回结果
            elif any(keyword in post.link
                     for keyword in self.filter_by_link_keywords):
                counter += 1
                yield post


def write_posts_to_file(posts: List[Post], fp: io.TextIOBase, title: str):
    """负责将帖子列表写入文件
    """
    fp.write(f'# {title}\n\n')
    for i, post in enumerate(posts, 1):
        fp.write(f'> TOP {i}: {post.title}\n')
        fp.write(f'> 分数：{post.points} 评论数：{post.comments_cnt}\n')
        fp.write(f'> 地址：{post.link}\n')
        fp.write('------\n')


def main():
    link_keywords = ['sspai.com', 'qq.com']
    crawler = HNTopPostsSpider(filter_by_link_keywords=link_keywords)

    posts = list(crawler.fetch())
    file_title = 'Top news on HN'
    write_posts_to_file(posts, sys.stdout, file_title)


if __name__ == '__main__':
    main()
