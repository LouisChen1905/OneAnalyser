#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''
import codecs
import json
import urllib.request

from one_analyse.lib.db.ormtables import Period, User


class PeriodsParser(object):
    '''
    Parse periods from http response.
    '''


    def __init__(self, request_url):
        '''
        Constructor
        '''
        self.url = request_url
        
    def get_response(self):
        list_periods = []
        list_owners = []
        response = urllib.request.urlopen(self.url)
        result = json.load(codecs.getreader("utf-8")(response))
        periods = result['result']['list']
        for dict_period in periods:
            if 'owner' in dict_period:
                dict_owner = dict_period['owner']
                owner = User(dict_owner['cid'], dict_owner['IP'], dict_owner['IPAddress'], dict_owner['avatarPrefix'], dict_owner['bonusNum'], dict_owner['coin'], dict_owner['isFirstLogin'], dict_owner['mobile'], dict_owner['nickname'], dict_owner['uid'])
                period = Period(dict_period['period'], dict_period['calcTime'], dict_period['cost'], dict_period['duobaoTime'], dict_period['luckyCode'], owner)
                list_periods.append(period)
                list_owners.append(owner)
        return list_periods, list_owners
            