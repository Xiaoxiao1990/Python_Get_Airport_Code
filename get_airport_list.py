#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-30 13:48:20
# @Author  : Little Fish (461146760@qq.com)
# @Link    : http://www.lxins.com
# @Version : $Id$

import os
import requests
import json
from bs4 import BeautifulSoup

def get_html_text(url, timeout=5):
    '模拟get请求，获取页面'
    try:
        r = requests.get(url)
        print(r.status_code)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'GET Error!'


def get_html_text_with_post(url, timeout=5):
    '''模拟post请求，获取页面'''
    try:
        r = requests.post(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'POST Error!'

def parse_url_list(url):
    '''
    返回chest页面下
    所有diary的超链接
    rtype： list
    '''
    url_list = []
    html = get_html_text_with_post(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'html.parser')
        urls = soup.find_all('a', class_='list-link')
        for url in urls:
            # 针对 //www.yuemei.com/c/1711873.html 格式进行特殊处理
            url_list.append('http:' + url['href'])
    else:
        print('错误发生了！')
    return url_list

def save_text(file_name, contents, mode = 'w'):
    '''
     Try to save a list variable in txt file.
    '''
    file = open(file_name, mode)
    for i in range(len(contents)):
    	file.write(str(contents[i]) + '\n')
    file.close()

def main():
	url = 'https://baike.baidu.com/item/%E6%9C%BA%E5%9C%BA%E4%BB%A3%E7%A0%81/1235719?fr=aladdin'
	html = get_html_text(url).replace('\n', '')
	soup = BeautifulSoup(html, 'html.parser')
	tables = soup.find_all('table')
	Mainland = tables[:7]
	Others = tables[7:]
	Mainland_List = []

	for table in Mainland:
		for tr in table.find_all('tr'):
			tds = tr.find_all('td')
			Mainland_List.append([tds[0].get_text(), tds[1].get_text()])
	print(Mainland_List)
	save_text("China_Airport_Name_And_Code", Mainland_List)

	print("\n")

	Mainland_List = []

	country = ''

	for table in Others:
		for tr in table.find_all('tr'):
			tds = tr.find_all('td')
			print(tds)
			if len(tds) == 4:
				country = tds[0].get_text()
				Mainland_List.append([country, tds[1].get_text(), tds[2].get_text(), tds[3].get_text()])
			elif len(tds) == 3:
				Mainland_List.append([country, tds[0].get_text(), tds[1].get_text(), tds[2].get_text()])
	print(Mainland_List)
	save_text("Global_Airport_Name_And_Code", Mainland_List)

if __name__ == '__main__':
	main()
