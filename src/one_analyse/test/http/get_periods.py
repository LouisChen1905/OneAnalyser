#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''

import json
import urllib.request
import codecs

urlOne = "http://1.163.com"
dirHist = "/win/getList.do?pageNum=1&pageSize=50&totalCnt=0&gid=424&period=303251699&token=c9257d4f-5d28-4dd2-96bb-2734d1648b66&t=1458887812112"

response = urllib.request.urlopen(urlOne+dirHist)
# str_response = response.read_all().decode("utf-8")

hist_list = json.load(codecs.getreader("utf-8")(response))

# print(hist_list['result']['list'])
periods = hist_list['result']['list']
print(len(periods))

for period in periods:
    print(period['cost'])