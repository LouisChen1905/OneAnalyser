#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年3月25日

@author: ChenSi
'''

import sqlite3;

conn = sqlite3.connect(':memory:')
cur = conn.cursor()

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
                gid integer not null,
                is_limit boolean,
                lucky_code integer not null,
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
 
conn.commit()

cur.execute("SELECT * FROM sqlite_master;")

print(cur.fetchall())

# cur.execute("insert into users(cid, ip, nickname, uid) values (123, '192.168.1.22', 'ccc', 'adf9832jkhdf')")
# 
# cur.execute("select * from users")
# 
# print cur.fetchall();

conn.close()