#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''
import argparse
import logging
import threading

import requests
from lxml import html
from sqlalchemy import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from threadpool import ThreadPool, makeRequests

from one_analyse.lib.db.ormtables import Base
from one_analyse.lib.db.ormtables import OneORM, Period, User
from one_analyse.lib.http.get_records import RecordsParser

DBSession = sessionmaker()
DBScopedSession = scoped_session(
    DBSession
)
list_periods = []
periods_mutex = threading.Lock()
list_records = []
list_mutex = threading.Lock()
list_users = []

record_url_f = "http://1.163.com/record/getDuobaoRecord.do?pageNum=%d&pageSize=%d&totalCnt=0&gid=424&period=%s&token=29abd5f7-0872-465b-9868-fe701f34496d&t=1461049459688"
# url to access details of goods
good_detail_url = "http://1.163.com/detail/%d-%d.html"
user_detail_url = "http://1.163.com/user/duobao.do?cid=%d#join"


def request_records(request_url, period, period_i, period_count, page_num, total_page):
    global list_records, list_users
    logging.info("Getting period(%d/%d) records. Page %d, total page:%d", period_i, period_count, page_num, total_page)
    record_parser = RecordsParser(request_url)
    list_records_2, list_users_2, total_count = record_parser.get_response(period.pid)
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


# session.close()


def request_single_period_html(gid, pid):
    global good_detail_url, list_periods, periods_mutex

    try:
        # request period detail page
        url = good_detail_url % (gid, pid)
        response = requests.get(url)
        doc = html.fromstring(response.text)
        # parse html to get period
        luck_code = doc.cssselect(".code")[0].text
        # nick_name = doc.cssselect(".bd > a")[0]
        user_id = int(doc.cssselect("div.user-id > span:last-of-type")[0].text.split("（")[0])
        num = int(doc.cssselect("div.user-buyTimes > span:last-of-type")[0].text.split("人次")[0])
        calc_time = doc.cssselect("div.published-time > span.bd")[0].text
        buy_time = doc.cssselect("div.buy-time > span.bd")[0].text
        logging.info("period id : %d, luck code : %s, user id : %d, \tnum : %d", pid, luck_code, user_id, num)
        # request user's page
        url = user_detail_url % user_id
        response = requests.get(url)
        doc = html.fromstring(response.text)
        # parse html to get user nick name
        nick_name = doc.cssselect("div.m-user-comm-infoBox-cont > ul > li > span.txt")[0].text
        logging.info("user id : %d, nick name : %s", user_id, nick_name)
        user = User(cid=user_id, nick_name=nick_name)
        period = Period(pid, calc_time, num, buy_time, luck_code, user, gid)

        session = DBScopedSession()
        db2.add_user(user, session)
        db2.add_period(period, session)
        periods_mutex.acquire()
        session.expunge_all()
        list_periods.append(period)
        periods_mutex.release()

        return True
    except IndexError as e:
        # print("Invalid gid or pid!")
        print("except:",e)
    except requests.exceptions.ConnectionError as e:
        print("except:", e)
    finally:
        DBScopedSession.remove()


def request_period_html(gid, begin_pid, section):

    pid = begin_pid
    step = -1
    while pid > (begin_pid + section):
        logging.info("Requesting period id : %d", pid)
        res = request_single_period_html(gid, pid)
        if res:
            # Interval between adjacent period code is larger than 50.
            step = -50
        else:
            step = -1
        pid += step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure run mode.', prog='TestArgumentParse')
    parser.add_argument('-p', '--getperiodfrom', metavar='xxx', choices=['webpage', 'database'], required=True, default='webpage',
                        help='webpage: scraping from web page or database: fetching periods from database')
    parser.add_argument('--tps', dest='tps', default=50, type=int, help='the size of thread pool')
    parser.add_argument('--dbps', dest='dbps', default=50, type=int, help='the size of database thread pool')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = vars(parser.parse_args())
    getperiodfrom = args['getperiodfrom']
    thread_pool_size = args['tps']
    db_pool_size = args['dbps']

    one_engine = create_engine('mysql+mysqlconnector://one:83796737@127.0.0.1/one_db', pool_size=db_pool_size, max_overflow=100)
    DBSession.configure(bind=one_engine)
    DBScopedSession.configure(bind=one_engine)

    Base.metadata.create_all(one_engine)

    # Configure logging
    logging.basicConfig(filename="one_analyse.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

    db2 = OneORM(one_engine)
    db2.InitDB()

    # Initialize thread pool
    tp = ThreadPool(thread_pool_size)

    if getperiodfrom == 'webpage':
        # Get periods from web pages.

        # one_url = "http://1.163.com"
        # period_dir_f = "/win/getList.do?pageNum=%d&pageSize=%d&totalCnt=0&gid=424"
        # period_dir = period_dir_f % (1, 1000)
        # periods_parser = PeriodsParser(one_url+period_dir)
        # list_periods, list_owners = periods_parser.get_response()


        # good is Apple MacBook Air
        gid = 424
        data = []
        pid = first_pid = 302201602
        last_pid = 300001602
        group_count = 0
        step = -2000
        sections = list(range(first_pid, last_pid, step))
        # while pid > last_pid:
        #     data.append(([gid, pid], []))
        #     pid -= 1
        #     group_count += 1
        #     if group_count == 25:
        #         thread_requests = makeRequests(request_period_html, data)
        #         [tp.putRequest(req) for req in thread_requests]
        #         group_count = 0
        #         data.clear()
        logging.info("Generating period id section...")
        for pid in sections:
            data.append(([gid, pid, step], []))
            thread_requests = makeRequests(request_period_html, data)
        thread_requests = makeRequests(request_period_html, data)
        [tp.putRequest(req) for req in thread_requests]
        logging.info("Scraping details of periods...")
        tp.wait()
    elif getperiodfrom == 'database':
        # Get periods from database
        logging.info("Obtaining periods from database...")
        session = DBScopedSession()
        list_periods = session.query(Period).filter(Period.pid < 302201602).all()
        session.expunge_all()

    #     print(len(list_periods))
    #     print(len(list_owners))

    #     session = DBSession()
    #     session = DBScopedSession()

    #     session.begin(subtransactions=True)
    #     try:
    #         for user in list_owners:
    #             db2.add_user(user, session)
    #
    # #         session.commit()
    #
    #         for period in list_periods:
    #     #         db.insert_period(period)
    #             db2.add_period(period, session)
    #
    # #         session.commit()
    #     except:
    # #         session.rollback()
    #         raise

    #     session.close()

    # get period records
    period_count = len(list_periods)
    period_i = 0
    for period in list_periods:
        period_i += 1
        page_num = 1
        page_size = 50
        record_url = record_url_f % (page_num, page_size, period.pid)
        record_parser = RecordsParser(record_url)
        # get total count to cal total pages
        list_records, list_users, total_count = record_parser.get_response(period.pid)
        total_page = int(total_count / page_size) + 1

        #         page_threads = []
        #
        #         while page_num <= total_page:
        #             record_url = record_url_f % (page_num, page_size, pid.pid)
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
            record_url = record_url_f % (page_num, page_size, period.pid)
            param_list = [record_url, period, period_i, period_count, page_num, total_page]
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
    #             record_url = record_url_f % (page_num, page_size, pid.pid)
    #             record_parser = RecordsParser(record_url)
    #             list_records_2, list_users_2, total_count = record_parser.get_response(pid.pid)
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

    DBScopedSession.remove()
# session.close()
#     session.remove()

#     print(db.select_period())
#     periods = db2.get_periods()
#     for pid in periods:
#         print(pid)
