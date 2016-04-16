#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 20160324

@author: chensi
'''
import json
import urllib.request
import codecs

urlOne = "http://1.163.com"
dirHist = "/record/getDuobaoRecord.do?pageNum=1&pageSize=100&totalCnt=0&gid=424&period=303246300&token=d3509460-e597-4f26-b263-1d0d3b5accd2&t=1458820103591"

response = urllib.request.urlopen(urlOne+dirHist)
# str_response = response.read_all().decode("utf-8")

dataJson = json.load(codecs.getreader("utf-8")(response))

# print(dataJson)

# print(dataJson['result']['list'][0])

for record in dataJson['result']['list']:
    print(record['num'])


