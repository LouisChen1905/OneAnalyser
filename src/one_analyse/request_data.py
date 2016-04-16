#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''

from one_analyse.lib.http.get_periods import PeriodsParser
from one_analyse.lib.db.ormtables import OneORM
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from sqlalchemy.orm.session import sessionmaker
from one_analyse.lib.db.ormtables import Base
from one_analyse.lib.http.get_records import RecordsParser
import threading
from one_analyse.mythread import  MyThread
from pip._vendor.requests.api import request
from one_analyse import one_engine
from sqlalchemy.orm.scoping import scoped_session
from threadpool import ThreadPool, makeRequests

DBSession = sessionmaker(bind=one_engine)
DBScopedSession = scoped_session(
                     sessionmaker(
                          autoflush=False,
                          autocommit=False,
                          bind=one_engine
                          )
                     )
Base.metadata.create_all(one_engine)
list_records = []
list_mutex = threading.Lock()
list_users = []
record_url_f = "http://1.163.com/record/getDuobaoRecord.do?pageNum=%d&pageSize=%d&totalCnt=0&gid=424&period=%s&token=81f863be-35b3-4abc-bf35-657802430a7a&t=1459047589564"


def request_records(request_url, period, period_i, period_count, page_num, total_page):
    global list_records, list_users
    print("Getting perioad(%d/%d) records. Page %d, total page:%d"%(period_i, period_count, page_num, total_page))
    record_parser = RecordsParser(request_url)
    list_records_2, list_users_2, total_count = record_parser.get_response(period.period)
    session = DBScopedSession()
    try:
        
        for user in list_users_2:
            db2.add_user(user, session)
        for record in list_records_2:
            db2.add_period_record(record, session)
    except:
        raise
    finally:
        DBScopedSession.remove()
#     session.close()
    

if __name__ == '__main__':
    db2 = OneORM()
    db2.InitDB()
    
    one_url = "http://1.163.com"
    period_dir_f = "/win/getList.do?pageNum=%d&pageSize=%d&totalCnt=0&gid=424"
    period_dir = period_dir_f % (1,1000)
    periods_parser = PeriodsParser(one_url+period_dir)
    list_periods, list_owners = periods_parser.get_response()
    
#     print(len(list_periods))
#     print(len(list_owners))
    
#     session = DBSession()
    session = DBScopedSession()

#     session.begin(subtransactions=True)
    try:
        for user in list_owners:
            db2.add_user(user, session)
        
#         session.commit()
        
        for period in list_periods:
    #         db.insert_period(period)
            db2.add_period(period, session)
        
#         session.commit()
    except:
#         session.rollback()
        raise
    
#     session.close()
    DBScopedSession.remove()

    # Initialize thread pool
    tp = ThreadPool(50)
    
    # get period records
    period_count = len(list_periods)
    period_i = 0
    for period in list_periods:
        period_i += 1
        page_num = 1
        page_size = 50
        record_url = record_url_f % (page_num, page_size, period.period)
        record_parser = RecordsParser(record_url)
        # get total count to cal total pages
        list_records, list_users, total_count = record_parser.get_response(period.period)
        total_page = int(total_count / page_size) + 1
        
#         page_threads = []
#         
#         while page_num <= total_page:
#             record_url = record_url_f % (page_num, page_size, period.period)
#             t = MyThread(request_records, 
#                          (record_url, period, period_i,period_count, page_num, total_page))
#             page_threads.append(t)
#             page_num = page_num + 1
#             
#         for t in page_threads:
#             t.start()

        # Use thread pool
        data = []
        while page_num <= total_page:
            record_url = record_url_f % (page_num, page_size, period.period)
            param_list = [record_url, period, period_i,period_count, page_num, total_page]
            param_kw = []
            data.append((param_list, param_kw))
            page_num += 1
        requests = makeRequests(request_records, data)
        [tp.putRequest(req) for req in requests]
#         tp.wait()
            
#         for t in page_threads:
#             t.join()
        
#         while page_num <= total_page:
#             print("Getting perioad(%d/%d) records. Page %d, total page:%d"%(period_i, period_count, page_num, total_page))
#             record_url = record_url_f % (page_num, page_size, period.period)
#             record_parser = RecordsParser(record_url)
#             list_records_2, list_users_2, total_count = record_parser.get_response(period.period)
#             # append list
#             list_records = list_records + list_records_2
#             list_users = list_users + list_users_2
#             page_num = page_num + 1

        # add to DB
#         for user in list_users:
#             db2.add_user(user, session)
#             
#         for record in list_records:
#             db2.add_period_record(record, session)
            
#         session.commit()
        
    tp.wait()
#     session.close()
#     session.remove()
    
#     print(db.select_period())
#     periods = db2.get_periods()
#     for period in periods:
#         print(period)
