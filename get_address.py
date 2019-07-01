import json
import re
import time

import requests

cookies = {
    'ARRAffinity':
    'f116114b631b918c421369fff6db64490a3eebc3d66f5b72db24b9145e8b399c',
    'Hm_lvt_15b1a40a8d25f43208adae1c1e12a514':
    '1557823323',
    '__51cke__':
    '',
    'Hm_lpvt_15b1a40a8d25f43208adae1c1e12a514':
    '1557823489',
    '__tins__540082':
    '%7B%22sid%22%3A%201557823323013%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201557825288643%7D',
    '__51laig__':
    '2',
}

headers = {
    'DNT':
    '1',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Accept':
    'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Referer':
    'http://www.gpsspg.com/iframe/maps/qq_181109.htm?mapi=2',
    'X-Requested-With':
    'XMLHttpRequest',
    'Connection':
    'keep-alive',
}


def get_address(lat: str, lng: str) -> str:
    time.sleep(5)
    print(f'开始解析 {lat},{lng}')
    params = (
        ('output', 'jsonp'),
        ('lat', lat),
        ('lng', lng),
        ('type', '0'),
        ('callback', 'jQuery110200731110172882683_1557823488393'),
        ('_', '1557823488394'),
    )

    response = requests.get(
        'http://www.gpsspg.com/apis/maps/geo/',
        headers=headers,
        params=params,
        cookies=cookies)
    # print(response.text)
    match = re.search(r'({.*})', response.text)
    data = json.loads(match.group(0))
    # print(data)
    if len(data['result']):
        address = data['result'][0]['address']
        print(f'{lat},{lng} 的地址是: {address}')
        return address
    else:
        return None


if __name__ == "__main__":
    get_address('30.685528', '103.823166')
