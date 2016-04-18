#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''
from one_analyse.lib.db.ormtables import Period, User

def user_decoder(json):
    if 'cid' in json and 'nickname' in json:
        return User(json['cid'], json['IP'], json['IPAddress'], json['avatarPrefix'], json['bonusNum'], json['coin'], json['isFirstLogin'], json['mobile'], json['nickname'], json['total'], json['uid'])
    
def periods_decoder(json):
    print(json)
    if 'result' in json and 'list' in json['result']:
        owner = user_decoder(json['owner'])
        return Period(json['period'], json['calcTime'], json['cost'], json['duobaoTime'], json['luckyCode'], owner)
