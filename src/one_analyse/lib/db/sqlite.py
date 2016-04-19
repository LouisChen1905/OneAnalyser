#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: chensi
'''

import sqlite3

from sqlalchemy.orm.session import sessionmaker

from one_analyse.lib.db.ormtables import Period


class SQLiteDB(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def InitDB(self):
        self.conn = sqlite3.connect(':memory:')
        cur = self.conn.cursor()
        
        cur.execute('''DROP TABLE IF EXISTS users''')
        cur.execute('''DROP TABLE IF EXISTS records''')
        cur.execute('''DROP TABLE IF EXISTS periods''')
        cur.execute('''DROP TABLE IF EXISTS goods''')
        
        self.conn.commit()
        
        cur.execute('''CREATE TABLE users
                (cid integer primary key, 
                ip text not null, 
                ip_addr text,
                nickname text not null, 
                uid text not null,
                coin integer default 0 ,
                is_first_login integer default 0,
                free_coin integer default 0, 
                avatar_name text,
                avatar_prefix text not null)''')

        cur.execute('''CREATE TABLE records
                        (rid integer primary key,
                        cid integer,
                        device text,
                        num integer not null,
                        regular_buy integer default 0,
                        time datetime not null,
                        FOREIGN KEY(cid) REFERENCES users(cid)
                        )''')
        
        cur.execute('''CREATE TABLE periods
                        (pid INTEGER PRIMARY KEY,
                        status INTEGER,
                        gid integer,
                        is_limit boolean,
                        lucky_code integer not null,
                        calc_time datetime,
                        duobao_time datetime,
                        cost integer not null,
                        owner_id integer not null,
                        owner_all_code_time datetime,
                        owner_all_code text,
                        FOREIGN KEY(gid) REFERENCES goods(gid),
                        FOREIGN KEY(owner_id) REFERENCES users(cid)
                    )''')
        
        cur.execute('''CREATE TABLE goods
                        (gid INTEGER PRIMARY KEY,
                        gname TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        price_type INTEGER NOT NULL,
                        price_unit INTEGER NOT NULL,
                        buy_unit INTEGER NOT NULL,
                        wish_set_table INTEGER)''')
         
        self.conn.commit()
        return self.conn
    
    def Close(self):
        self.conn.close()
        
    def insert_period(self, period):
        cur = self.conn.cursor()
        cur.execute('''insert into periods(pid, lucky_code, calc_time, duobao_time, cost, owner_id)
                    values (?,?,?,?,?,?)''', (period.period, period.lucky_code, period.calc_time, period.duobao_time, period.cost, period.owner.cid))
        self.conn.commit()
        
    def select_period(self):
        cur = self.conn.cursor()
        cur.execute('''select * from periods''')
        return cur.fetchall()
        
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base

Base = declarative_base()

class SQLiteORM(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def InitDB(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(self.engine)
        
    def add_period(self, period):
        if isinstance(period, Period):
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            
            session.add(period)
            session.commit()
        
    def get_periods(self):
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        
        return session.query(Period)
        
    def close(self):
        self.engine.clos
