import datetime
import os
import re
import shutil
import time

import requests
import xlwt

# rbook = xlrd.open_workbook("C:\\Users\\1\\Desktop\\meibei.xls")
# ws=copy(rbook)
exc = xlwt.Workbook()
sheet = exc.add_sheet('伊婉低价', True)
rowname = ['名称', '单价', '链接', '机构']
for row in range(0, 4):
    sheet.write(0, row, rowname[row])


def read_data(url):
    headers = {

        "authority": "www.meb.com",
        "method": "GET",
        "path": "/search/productlist/%e4%bc%8a%e5%a9%89/",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": 'scode={"Success":true,"Content":{"Scod":"www.meb.com"}}; PcDeviceId=81d4a300-b599-4f52-b3c0-ae7020afa85e; AT_UID=77423280-e72f-4266-b740-c08cdbd9d199; SGK=eyJTR1AiOiIzIiwiU0dSIjoiMCIsIlNHTSI6IjAiLCJTR1QiOiJSU1QiLCJTR0siOiJTR18zXzBfMF9SU1QifQ%3D%3D; sajssdk_2015_cross_new_user=1; UM_distinctid=174cea8a1655fc-02d17970820729-4313f6f-1fa400-174cea8a16677d; CNZZDATA1259812800=1381676153-1601194991-https%253A%252F%252Fwww.baidu.com%252F%7C1601194991; CNZZDATA1263206038=645326662-1601193183-https%253A%252F%252Fwww.baidu.com%252F%7C1601193183; DeviceIdkey=21336497-0dbd-4017-a94b-f3388c8ed9f0; Hm_lvt_5c27e468e91bb0071850df5a355e0475=1601194992; _ga=GA1.2.1452298647.1601194992; _gid=GA1.2.1331445124.1601194992; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2277423280-e72f-4266-b740-c08cdbd9d199%22%2C%22%24device_id%22%3A%22174cea8a14c7e8-0234525dc965e4-4313f6f-2073600-174cea8a14db8b%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gat_gtag_UA_120516963_1=1; Hm_lpvt_5c27e468e91bb0071850df5a355e0475=1601195280',
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"

    }
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    for n in range(1, 20):
        url_read = requests.get(url=url + str(n), headers=headers).text
        # 爬取名称
        pat1 = '<a target="_blank" class="text_one" href="/product/.*?">(.*?)</a>'
        alldata1 = re.compile(pat1).findall(url_read)
        a1.extend(alldata1)
        for i in range(0, len(a1)):
            sheet.write(i + 1, 0, a1[i])

        # 爬取单价
        pat2 = '<span class="now_my"><span>￥(.*?)</span></span>'
        alldata2 = re.compile(pat2).findall(url_read)
        a2.extend(alldata2)
        for i in range(0, len(a2)):
            sheet.write(i + 1, 1, a2[i])

        # 爬取链接
        pat3 = '<a target="_blank" class="need_yy" href="(.*?)">查看详情</a>'
        alldata3 = re.compile(pat3).findall(url_read)
        a3.extend(alldata3)
        for i in range(0, len(a3)):
            sheet.write(i + 1, 2, "https://www.meb.com" + a3[i])

        # 爬取机构信息
        pat4 = '<span class="text_two">(.*?)   </span>'
        alldata4 = re.compile(pat4).findall(url_read)
        a4.extend(alldata4)
        for i in range(0, len(a4)):
            sheet.write(i + 1, 3, a4[i])

        time.sleep(5)

        # 当爬取到某一页无数据时，则跳出循环
        if len(alldata1) == 0:
            break
        else:
            continue


url = "https://www.meb.com/search/productlist/%e4%bc%8a%e5%a9%89_"
read_data(url)
data = exc.save(datetime.datetime.today().strftime('%Y-%m-%d') + '伊婉美呗销售状况.xls')
aa = os.getcwd()
# 获取当前文件路径
file_path = os.path.join(aa, datetime.datetime.today().strftime('%Y-%m-%d') + '伊婉美呗销售状况.xls')
# 移动文件到E盘地方
target_path = r'E:\玻尿酸销售情况'
# 使用shutil包的move方法移动文件
shutil.move(file_path, target_path)
