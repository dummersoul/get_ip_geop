# -*- coding: UTF-8 -*-
import json
import requests
from urllib.request import urlopen
from lxml import etree

key = '21c8ET627t6DXLhKX2666Wt5BS1oyySW9GAWhmspxUM5Pd9mYDbJk4zL0y4M0GYn'
global country, prov, city, longitude, latitude


# page = {'code': 'Success',
#         'data': {'continent': '亚洲', 'country': '中国', 'owner': '中国电信',
#         'zipcode': '230001', 'timezone': 'UTC+8', 'accuracy': '城市', 'source': '数据挖掘',
#                  'multiAreas': [{'lat': '31.863063', 'lng': '117.270667', 'prov': '安徽省', 'city': '合肥市'}]},
#         'charge': True, 'msg': '查询成功', 'ip': '36.5.132.158', 'coordsys': 'WGS84'}


def get_ip():  # 获取本地网络ip
    page = requests.get("https://ip.cn/")
    html_text = etree.HTML(page.text)
    ip = html_text.xpath('//span/text()')[5].replace(':', '').replace(' ', '')
    print(ip)
    return ip


def crawl_geo(ip):
    ip_geo_url = "https://api.ipplus360.com/ip/geo/v1/city/?key=%s&ip=%s&coordsys=WGS84" % (key, ip)
    print(ip_geo_url)
    page = requests.get(ip_geo_url).content.decode('utf-8')  # 网页text
    page = json.loads(page)  # 将str格式转换为dict格式
    # print(page)
    global country, prov, city, longitude, latitude
    if page['code'] == 'Success':
        country = page['data']['country']  # 国家
        prov = page['data']['multiAreas'][0]['prov']  # 州/省份
        city = page['data']['multiAreas'][0]['city']  # 城市
        longitude = page['data']['multiAreas'][0]['lng']  # 经度
        latitude = page['data']['multiAreas'][0]['lat']  # 纬度

    return {'ip': ip, 'country': country, 'prov': prov, 'city': city,
            'locate': '经度:%s 纬度:%s' % (longitude, latitude)}


if __name__ == '__main__':
    get_ip()
    print(crawl_geo('36.5.132.158'))  # 字典类型的地理信息
