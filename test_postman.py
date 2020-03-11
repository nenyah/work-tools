#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client

conn = http.client.HTTPConnection("www.soyoung.com")

headers = {
    'Cookie': "__order_time__=undefined; msg_time=undefined; back_order_time=undefined; complain_time=undefined; PHPSESSID=1865087c95cda1ca9a528fb481cee2e2; __usersign__=1555319257066415481; Hm_lvt_b366fbb5465f5a86e1cc2871552e1fdb=1555319260; _ga=GA1.2.1411489942.1555319260; _gid=GA1.2.601613975.1555319260; __postion__=a%3A4%3A%7Bs%3A6%3A%22cityId%22%3Bs%3A3%3A%22176%22%3Bs%3A8%3A%22cityName%22%3Bs%3A9%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%22%3Bs%3A8%3A%22cityCode%22%3Bs%3A3%3A%22180%22%3Bs%3A3%3A%22jwd%22%3Bi%3A0%3B%7D; Hm_lpvt_b366fbb5465f5a86e1cc2871552e1fdb=1555319315",
    'DNT': "1",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Referer': "https://www.soyoung.com/searchNew/product?keyword=%E4%BC%8A%E5%A9%89",
    'X-Requested-With': "XMLHttpRequest",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
    'Postman-Token': "a421a56e-c748-4d7c-9a9c-23281f00cb31"
}

conn.request("GET", "/searchNew/product", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
