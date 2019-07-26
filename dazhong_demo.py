import re

import requests
from lxml import html


# 获取css的全部数据，并且一会通过正则表达式匹配出你想要的class
# css_name 你需要获取的css名称，例如ztkrgv
# css_url 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fa9df9a170bc400700f4c8f9cf42da0d.css'
# 这个地方是动态的，每次都要重新抓取一下
# .ztkrgv {  background: -523.0px -51.0px; }  编写正则表达式
def get_css_position(css_name, css_url):
    css_positon_html = requests.get(css_url).text

    str_css = (r'%s{background:-(\d+).0px -(\d+).0px' % css_name)
    css_re = re.compile(str_css)
    info_css = css_re.findall(css_positon_html)

    return info_css


if __name__ == '__main__':
    x, y = get_css_position(
        'ztkrgv',
        'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fa9df9a170bc400700f4c8f9cf42da0d.css'
    )[0]

    # url需要动态获取哦~
    result = requests.get(
        'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fab2c972c28d0b026576e791486243c7.svg'
    )
    tree = html.fromstring(result.content)

    a = tree.xpath('//text[@y="37"]/text()')[0]  # 纵坐标也是动的，需要动态
    b = tree.xpath('//text[@y="75"]/text()')[0]
    c = tree.xpath('//text[@y="106"]/text()')[0]

    x, y = int(x), int(y)
    print('ztkrgv的坐标是', x, y)
    if y <= 37:
        print('svg图片对应的数字：', a[x // 12])
    elif y <= 75:
        print('svg图片对应的数字：', b[x // 12])
    else:
        print('svg图片对应的数字：', c[x // 12])
