#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''

import sqlite3
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean,\
    orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint, MetaData,\
    Table

from one_analyse import one_engine

Base = declarative_base()


class Period(Base):
    '''
    classdocs
    '''
    __tablename__ = "periods"
    
    period = Column(Integer, primary_key=True)
    calc_time = Column(DateTime)
    cost = Column(Integer)
    duobao_time = Column(DateTime)
    lucky_code = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.cid"), nullable=False)
    gid = Column(Integer, ForeignKey("goods.gid"), nullable=False)

    def __init__(self, period, calc_time, cost, duobao_time, lucky_code, owner, gid=424):
        '''

        :param period:
        :param calc_time:
        :param cost:
        :param duobao_time:
        :param lucky_code:
        :param owner:
        :param gid: default value is 424 (Apple MacBook Air 13.3" 128GB)
        '''
        self.period = period
        if isinstance(calc_time, str):
            self.calc_time= datetime.strptime(calc_time, "%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(calc_time, datetime):
            self.calc_time = calc_time
        self.cost = cost
        if isinstance(duobao_time, str):
            self.duobao_time = datetime.strptime(duobao_time, "%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(duobao_time, datetime):
            self.duobao_time = duobao_time
        self.lucky_code = lucky_code
        self.owner = owner
        self.owner_id = owner.cid
        self.gid = gid
        
    def __repr__(self):
        return '''<periods(period='%s',calc_time='%s',cost=%d,duobao_time='%s',lucky_code=%d,owner_id=%d)>'''%(
                            self.period,
                            self.calc_time,
                            self.cost,
                            self.duobao_time,
                            self.lucky_code,
                            self.owner_id)
         
#     def __conform__(self, protocol):
#         if protocol is sqlite3.PrepareProtocol:
#             return "%d,%s,%d,%s,%d,%d"%(self.period, self.calc_time, self.cost, self.duobao_time, self.lucky_code, self.owner)


class User(Base):
    '''
    classdocs
    '''
    
    __tablename__ = 'users'
    
    cid = Column(Integer, primary_key=True)
    ip = Column(String(256))
    ip_address = Column(String(256))
    avatar_prefix = Column(String(512))
    bonus_num = Column(Integer)
    coin = Column(Integer)
    is_first_login = Column(Boolean)
    mobile = Column(Integer)
    nick_name = Column(String(512))
    uid = Column(String(256))

    def __init__(self, cid, ip="", ip_address="", avatar_prefix="", bonus_num=0, coin=0, is_first_login=0, mobile="", nick_name="", uid=""):
        '''
        Constructor
        '''
        self.cid = cid
        self.ip = ip
        self.ip_address = ip_address
        self.avatar_prefix = avatar_prefix
        self.bonus_num = bonus_num
        self.coin = coin
        self.is_first_login = is_first_login
        self.mobile = mobile
        self.nick_name = nick_name
        self.uid = uid


class PeriodRecord(Base):
    __tablename__ = 'period_records'
    
    device = Column(String(128))
    num = Column(Integer)
    regular_buy = Column(Integer)
    rid = Column(Integer, index=True)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.cid"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.period"), nullable=False)
    codes = Column(String(4096))
    
    __table_args__ = (
                      PrimaryKeyConstraint('rid', 'user_id', 'period_id'),
                      )
    
    def __init__(self, rid, device, num, regular_buy, time, user_id, period_id, codes=""):
        '''
        Constructor
        '''
        self.rid = rid
        self.device = device
        self.num = num
        self.regular_buy = regular_buy
#         self.time = time
        if isinstance(time, str):
            self.time= datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(time, datetime):
            self.time = time
        self.user_id = user_id
        self.period_id = period_id
        self.codes = codes


class Good(Base):
    '''
    Information of a good with a gid can be retrieved by requesting a url like "http://1.163.com/goods/query.do?gid=424&token=2cdd2ab8-a95a-4360-ab48-b1d5c02aabe7&t=1460796707711"
    '''
    __tablename__ = 'goods'

    gid = Column(Integer, primary_key=True)
    brand = Column(String(512))
    buyUnit = Column(Integer)
    buyable = Column(Boolean)
    gname = Column(String(512))
    goodsType = Column(Integer)
    gpic = Column(String(512))
    price = Column(Integer)
    priceBase = Column(Integer)
    priceType = Column(Integer)
    priceUnit = Column(Integer)
    regularBuyMax = Column(Integer)
    showPicNum = Column(Integer)
    tag = Column(String(128))
    totalTimes = Column(Integer)
    typeId = Column(Integer)
    wishSetable = Column(Boolean)

    def __int__(self, gid, brand, buyUnit, buyable, gname,  goodsType, gpic, price, priceBase, priceType, priceUnit, regularBuyMax, showPicNum, tag, totalIimes, typeId, wishSetable):
        '''

        :param gid:
        :param brand:
        :param buyUnit:
        :param buyable:
        :param gname:
        :param goodsType:
        :param gpic:
        :param price:
        :param priceBase:
        :param priceType:
        :param priceUnit:
        :param property:
        :param regularBuyMax:
        :param showPicNum:
        :param tag:
        :param totalIimes:
        :param typeId:
        :param wishSetable:
        :return:
        '''
        self.gid = gid
        self.brand = brand
        self.buyUnit = buyUnit
        self.buyable = buyable
        self.gname = gname
        self.goodsType = goodsType
        self.gpic = gpic
        self.price = price
        self.priceBase = priceBase
        self.priceType = priceType
        self.priceUnit = priceUnit
        self.regularBuyMax = regularBuyMax
        self.showPicNum = showPicNum
        self.tag = tag
        self.totalTimes = totalIimes
        self.typeId = typeId
        self.wishSetable = wishSetable
        
class UserTotalNum(object):
    def __init__(self, name):
        self.name = name

class OneORM(object):
    '''
    classdocs
    '''
    
    meta = MetaData(bind=one_engine)

    user_period_total_num = Table("user_period_total_cost", meta, autoload=True)

    def __init__(self):
        '''
        Constructor
        '''
        
    def InitDB(self):
        orm.mapper(UserTotalNum, self.user_period_total_num, primary_key=[self.user_period_total_num.c.period_id])
        
    def add_period(self, period, session):
        try:
            periodq = session.query(Period).filter(Period.period==period.period).first()
            if periodq==None:
                session.add(period)
                session.commit()
        except orm.exc.FlushError as e:
            print("except:", e)
        except sqlalchemy.exc.InvalidRequestError as e:
            print("except:", e)
        
    def get_periods(self, session):
        return session.query(Period).all()
    
    def get_periods_cost(self, session):
        return session.query(Period.period, Period.cost).all()
    
    def get_periods_max_cost(self, session):
        return session.query(Period.cost, func.max(UserTotalNum.total_num).label("max_num")).\
                filter(Period.period==UserTotalNum.period_id).\
                group_by(Period.period).all()
    
    def count_periods_const(self, session, cost_filter):
        low = 1
        high = 100
        count = []
        for n in cost_filter:
            high = n
            count.append(session.query(func.count(Period.period)).filter(Period.cost >= low, Period.cost < high).all())
            low = high
            
        return count
    
    def add_user(self, user, session):
        try:
            userq = session.query(User).filter(User.cid==user.cid).first()
            if userq is None:
                session.add(user)
                session.commit()
        except orm.exc.FlushError as e:
            print("except:", e)
        except sqlalchemy.exc.InvalidRequestError as e:
            print("except:", e)
        except sqlite3.IntegrityError as e:
            print("except:", e)
        except sqlalchemy.exc.IntegrityError as e:
            print("except:", e)
            
        
    def get_users(self, session):
        return session.query(User).all()
    
    def add_period_record(self, record, session):
        
        try:
            recordq = session.query(PeriodRecord).filter(PeriodRecord.period_id==record.period_id, PeriodRecord.user_id==record.user_id, PeriodRecord.rid==record.rid).first()
            if recordq is None:
                session.add(record)
            session.commit()
        except orm.exc.FlushError as e:
            print("except:", e)
        except sqlalchemy.exc.InvalidRequestError as e:
            print("except:", e)
        except sqlite3.IntegrityError as e:
            print("except:", e)
            
    def get_period_records(self, session):
        return session.query(PeriodRecord).all()
    
    def get_period_record(self, rid, session):
        return session.query(PeriodRecord).filter(PeriodRecord.rid==rid).first()
        
    def close(self):
        pass