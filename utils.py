import requests

sina_cookies = '''M_WEIBOCN_PARAMS=luicode=10000011&lfid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&fid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&uicode=10000011; expires=Mon, 25-May-2020 05:05:43 GMT; Max-Age=600; path=/; domain=.weibo.cn; HttpOnly='''
dianping_cookies = '''cy=11; cye=ningbo; _lxsdk_cuid=171e7bdd080c8-08f1315d6ee0b3-71657d60-1fa400-171e7bdd080c8; _lxsdk=171e7bdd080c8-08f1315d6ee0b3-71657d60-1fa400-171e7bdd080c8; _hc.v=7be34015-5935-6418-2a07-605288936e09.1588730909; t_lxid=171e7bdd0b81b-0067f6fc1ca743-71657d60-1fa400-171e7bdd0b9c8-tid; ua=sixinfive; s_ViewType=10; ctu=ae68056abd6e8c0288d77d0f8cda7c3791d4c6b09fd31b55fa9e832b5a9b0de4; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1591063174; td_cookie=1623454537; lgtoken=00f5b8a83-5809-406f-9af8-d43774803c2d; dplet=145236087d47c14723ba8b54ab642ec7; dper=0596ad4a7904a1c0bcd7ae06ae5d1c0a9d0332b05dc89080f961a14f185f102540c4fb99c4b70891b8c59b2e68b39a440f4f3d4e0e1ef11c856d40e414467e7225f6f0506103e4bd56b7b34b6ad5c03716c17b500aa8c1960474e0921ea558e5; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=17272c15a13-3e9-c67-e6f%7C%7C31; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1591064812'''


def parse_cookie(cookies: str) -> list:
    cookie_list = []
    for one in cookies.split('; '):
        k, v = one.split('=', 1)
        cookie_list.append({'name': k, 'value': v})
    print(cookie_list)
    return cookie_list


# cookie_list = parse_cookie(dianping_cookies)
PROVINCE_URL = 'http://www.dianping.com/ajax/citylist/getAllDomesticProvince'
