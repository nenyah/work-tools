'''
Author: Steven
Date: 2020-10-21 10:24:11
LastEditTime: 2020-12-14 11:21:06
LastEditors: Please set LastEditors
Description: cookie parser
FilePath: /work-tools/utils.py
'''

sina_cookies = '''M_WEIBOCN_PARAMS=luicode=10000011&lfid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&fid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&uicode=10000011; expires=Mon, 25-May-2020 05:05:43 GMT; Max-Age=600; path=/; domain=.weibo.cn; HttpOnly='''
dianping_cookies = '''fspop=test; cy=11; cye=ningbo; _lxsdk_cuid=1765ecd94bec8-0c478a49f88208-5a301e42-1fa400-1765ecd94bec8; _lxsdk=1765ecd94bec8-0c478a49f88208-5a301e42-1fa400-1765ecd94bec8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1607908301; _hc.v=deb9a9cb-1005-0114-5c8a-3b2c1c1d2c4e.1607908301; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1607908317; _lxsdk_s=1765f3b2217-b3-e58-7f2%7C%7C2'''


def parse_cookie(cookies: str) -> list:
    cookie_list = []
    for one in cookies.split('; '):
        k, v = one.split('=', 1)
        cookie_list.append({'name': k, 'value': v})
    print(cookie_list)
    return cookie_list


# cookie_list = parse_cookie(dianping_cookies)
PROVINCE_URL = 'http://www.dianping.com/ajax/citylist/getAllDomesticProvince'
