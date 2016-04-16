#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月24日

@author: chensi
'''

import urllib.request
import codecs
from html.parser import HTMLParser

urlOne = "http://1.163.com/detail/424-303246300.html"

response = urllib.request.urlopen(urlOne)
str_reponse = response.read().decode('utf-8')

# print(str_reponse)

class LuckNumberHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        
        if tag == 'div':
#             print("Start tag:", tag)
            for attr in attrs:
    #             print("     attr:", attr)
                if attr[0] == 'class' and 'code' == attr[1]:
                    print("     attr:", attr)
                    
    def handle_data(self, data):
        print("Encountered some data  :", data)
    
                
parser = LuckNumberHTMLParser()
parser.feed(str_reponse)
