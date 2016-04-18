#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月27日

@author: chensi
'''
import codecs
import json
import urllib.request

from one_analyse.lib.db.ormtables import PeriodRecord
from one_analyse.lib.db.ormtables import User


class RecordsParser(object):
    '''
    classdocs
    '''


    def __init__(self, request_url):
        '''
        Constructor
        '''
        self.url = request_url
        
    def get_response(self, period_id):
        list_records = []
        list_users = []
        tried = 0
        reponse = None
        while (tried < 10):
            try:
                response = urllib.request.urlopen(self.url)
                break
            except urllib.error.URLError as e:
                print(e)
                tried = tried + 1
                continue
            
        result = json.load(codecs.getreader("utf-8")(response))
        records = result['result']['list']
        total_count = int(result['result']['totalCnt'])
        for dict_record in records:
            if 'user' in dict_record:
                dict_user = dict_record['user']
                user = User(dict_user['cid'], dict_user['IP'], dict_user['IPAddress'], dict_user['avatarPrefix'], dict_user['bonusNum'], dict_user['coin'], dict_user['isFirstLogin'], dict_user['mobile'], dict_user['nickname'], dict_user['uid'])
                record = PeriodRecord(dict_record['rid'], dict_record['device'], dict_record['num'], dict_record['regularBuy'], dict_record['time'], user.cid, period_id)
                list_records.append(record)
                list_users.append(user)
        return list_records, list_users, total_count