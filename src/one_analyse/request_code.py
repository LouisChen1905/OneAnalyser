#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年4月10日

@author: chensi
'''
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from one_analyse import one_engine
from threadpool import ThreadPool, makeRequests
from one_analyse.lib.db.ormtables import OneORM
import urllib.request
import json
import codecs
from one_analyse.lib.db.ormtables import PeriodRecord

DBScopedSession = scoped_session(
                     sessionmaker(
                          autoflush=False,
                          autocommit=False,
                          bind=one_engine
                          )
                     )

code_url_format = "http://1.163.com/code/get.do?gid=424&period=%s&cid=%s"

def request_code(period_id, user_id, rid, num):
    url = code_url_format % (period_id, user_id)
    response = urllib.request.urlopen(url)
    result = json.load(codecs.getreader("utf-8")(response))
    codes = result['result']['list'][0]['code']
        
    session = DBScopedSession()
    session.query(PeriodRecord).\
        filter(PeriodRecord.rid==rid).\
        filter(PeriodRecord.period_id==period_id).\
        filter(PeriodRecord.user_id==user_id).\
        update({'codes':','.join(codes)})
    session.commit()
    DBScopedSession.close()

if __name__ == '__main__':
    db2 = OneORM()
    db2.InitDB()
    
    # Initialize thread pool
    tp = ThreadPool(50)
    
    # Get all period records from database
    session = DBScopedSession()
    period_records = db2.get_period_records(session)
    DBScopedSession.remove()
    
    data = []
    for r in period_records:
        param_list = [r.period_id, r.user_id, r.rid, r.num]
        data.append((param_list, []))
    requests = makeRequests(request_code, data)
    [tp.putRequest(req) for req in requests]
    
    tp.wait()