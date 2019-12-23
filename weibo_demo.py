'''
@Description: 采集微博数据
@Author: Steven
@Date: 2019-12-09 09:44:03
@LastEditors: Steven
@LastEditTime: 2019-12-09 13:56:02
'''
import time

from selenium import webdriver
from lxml import etree

url = 'https://weibo.com/xuwei1030?profile_ftype=1&is_all=1#_0'


def start_chrome():
    driver = webdriver.Chrome()
    driver.start_client()
    return driver


def find_info():
    urls = set()
    href_xpath = '//div[@class="WB_from S_txt2"]/a[1]/@href'
    content_xpath = '//div[@class="WB_text W_f14"]/text()'
    tree = etree.HTML(driver.page_source)
    hrefs = tree.xpath(href_xpath)
    contents = tree.xpath(content_xpath)

    for href, content in zip(hrefs, contents):
        if '伊婉' in content:
            urls.add(href)
        print(href, content)
    return urls


driver = start_chrome()
driver.get(url)
time.sleep(10)
info = find_info()
print(info)
driver.quit()
