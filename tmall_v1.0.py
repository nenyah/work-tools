#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from datetime import datetime

import pandas as pd
import pymongo
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (MONGODB_COLLECTION, MONGODB_DB, MONGODB_HOST, MONGODB_PORT,
                    KEYWORD)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option('excludeSwitches',
                                       ['enable-automation'])
browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]


def login():
    print("正在登录")
    # 需要用手机淘宝扫二维码登录才能搜索
    browser.get(url='https://login.taobao.com')
    # 10s用来扫码登录
    # browser.implicitly_wait(200)
    time.sleep(10)


def search(KEYWORD):
    print("正在查找", KEYWORD)
    try:
        input_node = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "#J_TSearchForm > div.search-button > button")))
        input_node.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#mainsrp-pager > div > div > div > div.total")))
        get_goods()
        return total.text
    except TimeoutError:
        return search(KEYWORD)


def next_page(page_number):
    print("正在换页", page_number)
    submit_pat = "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"
    try:
        input_node = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#mainsrp-pager > div > div > div > div.form > input")))

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_pat)))
        input_node.clear()
        input_node.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((
                By.CSS_SELECTOR,
                '#mainsrp-pager > div > div > div > ul > li.item.active > span'
            ), str(page_number)))
        get_goods()
    except Exception:
        next_page(page_number)


def get_goods():
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        html = browser.page_source
        doc = pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()
        for item in items:
            goods = {
                'pid': item.find('.pic .img').attr('id').split('_')[-1],
                'img': item.find('.pic .img').attr('data-src'),
                'price': item.find('.price').text().replace('\n', ' '),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.title').text().replace('\n', ''),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
                'crawl_date': datetime.today().strftime('%Y-%m-%d')
            }
            save_to_mongodb(goods)
    except Exception:
        print("获取商品失败")


def save_to_mongodb(info):
    try:
        if collection.insert_one(info):
            print("存储到数据成功", info)
    except Exception:
        print("存储到数据库失败", info)


def out_to_csv(date, file):
    df = pd.DataFrame(collection.find())
    df = df[df['crawl_date'] == date][[
        'crawl_date', 'deal', 'img', 'location', 'pid', 'price', 'shop',
        'title'
    ]]
    df['link'] = 'https://detail.tmall.com/item.htm?id=' + df['pid']
    df.to_csv(file, index=False)


def main():
    _path = r"E:\玻尿酸销售情况"
    today = datetime.today().strftime('%Y-%m-%d')
    file = f'{_path}/{today}{KEYWORD}天猫销售情况.csv'
    login()
    search(KEYWORD)
    total = 12
    for i in range(2, total):
        if i % 3 == 0:
            time.sleep(random.randint(1, 20))
        next_page(i)

    out_to_csv(today, file)

    browser.quit()


if __name__ == '__main__':
    main()
