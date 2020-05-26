cookies = '''M_WEIBOCN_PARAMS=luicode=10000011&lfid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&fid=100103type%3D1%26q%3D%23%E5%AE%88%E6%8A%A4%E6%9C%80%E7%BE%8E%E9%80%86%E8%A1%8C%E5%A4%A9%E4%BD%BF%23&uicode=10000011; expires=Mon, 25-May-2020 05:05:43 GMT; Max-Age=600; path=/; domain=.weibo.cn; HttpOnly='''

cookie_list = []
for one in cookies.split('; '):
    k, v = one.split('=', 1)
    cookie_list.append({'name': k, 'value': v})
print(cookie_list)