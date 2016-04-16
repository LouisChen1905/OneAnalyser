#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月2日

@author: chensi
'''

import threading
from one_analyse.lib.http.get_records import RecordsParser

class MyThread(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, func, args, name=''):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        
    def getResult(self):
        return self.res
    
    def run(self):
        self.res = self.func(*self.args)