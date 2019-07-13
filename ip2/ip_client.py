#
import random
from http import cookiejar
from urllib import request

import requests
from lxml import etree

__author__ = 'bob'
__date__ = '2019/7/13 11:21'


# 抓取西刺代理ip网站的ip
def get_ip_list():
    cj = cookiejar.CookieJar()  # 创建CookieJar对象
    handler = request.HTTPCookieProcessor(cj)   # 创建cookie处理器
    opener = request.build_opener(handler)  # 创建打开器
    url = 'https://www.xicidaili.com/?_id=015448211445'
    # 封装请求头参数
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://www.xicidaili.com/?_id=015448211445',
    }
    req = request.Request(url, headers=headers)
    response = opener.open(req)     # 发送请求，返回响应
    response = response.read().decode()
    node = etree.HTML(response)
    node1 = node.xpath('.//tr[@class="odd"]/td[2]/text()')  # xpath选取内容
    node2 = node.xpath('.//tr[@class="odd"]/td[3]/text()')
    ips = []
    for i in range(len(node1)):
        ips.append('http://' + node1[i] + ":" + node2[i])
    print('抓取成功')
    verify_ip_list(ips)


# 测试ip列表是否可以使用
def verify_ip_list(list_):
    ips = list_
    proxies = {}
    ips_ = []
    string = ''
    # 将可用ip存到ips.json文件中，不可用不存
    for ip in ips:
        proxies['http'] = ip
        try:
            res = requests.get('https://www.baidu.com',
                               proxies=proxies,)
            if res.status_code == 200:
                ips_.append(proxies['http'])
                string += proxies['http'] + "\n"
        except Exception as e:
            print('访问异常，原因：', e)
    print(string)
    with open('ips.txt', 'w')as f:
        f.write(str(string))
    print('测试结束，已保存,保存个数：', len(ips_))
    return ips_


# 从ips.json文件中读取所有ip，随机返回一个ip
def get_ip():
    with open('ips.txt', 'r') as f:
        ips = f.read()
    ips = ips.split("\n")
    ips.remove('')
    verify_ip_list(ips)
    with open('ips.txt', 'r') as f:
        ips = f.read()
    ips = ips.split("\n")
    ips.remove('')
    if ips:
        return random.choice(ips)

# get_ip_list()

print(get_ip())

# get_ip()
