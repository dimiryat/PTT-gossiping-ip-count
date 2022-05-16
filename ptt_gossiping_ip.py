# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:09:50 2022

@author: DennisLin
"""

API_KEY = "f65a74eee6b066b5fe4dd125dc358dbb"
PTT_URL = "https://www.ptt.cc"

import re
from ptt_gossiping import get_web_page, get_articles
import requests
import time

def get_ip(dom):
    pattern = "來自: \d+\.\d+\.\d+\.\d+"
    match = re.search(pattern, dom)
    if match:
        return match.group(0).replace("來自: ", "")
    else:
        return None
    
def get_country(ip):
    if ip:
        url = 'http://api.ipstack.com/{}?access_key={}'.format(ip, API_KEY)
        data = requests.get(url).json()
        country_name = data['country_name'] if data['country_name'] else None
        return country_name
    else:
        return None

if __name__=="__main__":
    print("取得今日文章... ")
    current_page = get_web_page(PTT_URL + '/bbs/Gossiping/index.html')
    if current_page:
        articles = []
        today = time.strftime('%m/%d').lstrip('0')
        current_articles, prev_url = get_articles(current_page, today)
        while current_articles:
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)
        print("共 %d 篇文章" % (len(articles)))
        
        print('取得前100篇文章')
        country_to_count = dict()
        for article in articles[:100]:
            print("查詢 IP:", article['title'])
            page = get_web_page(PTT_URL + article['href'])
            if page:
                ip = get_ip(page)
                country = get_country(ip)
                if country in country_to_count.keys():
                    country_to_count[country] += 1
                else:
                    country_to_count[country] = 1
                    
        print("各國IP分佈")
        for k, v in country_to_count.items():
            print(k, v)