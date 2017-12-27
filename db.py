# -*- coding: utf-8 -*-
'''
数据入库
'''
import os
import sqlite3
import time

class Db():

    def __init__(self):
        dbpath = 'live.db'
        self.conn = sqlite3.connect(dbpath)
        self.cursor = self.conn.cursor()
    
    def createUser(self):
        self.cursor.execute("""create table user (id int(20) primary key,
            rid int(20),
            category varchar(150),
            number int(20),
            name varchar(50),
            uid int(20),
            url varchar(250),
            source varchar(50),
            create_time varchar(30)
            )""")
        self.conn.commit()

    def insert(self,data):
        sqlstr = "insert into user (rid,category,number,name,uid,url,source,create_time) values (%s,'%s',%s,'%s',%s,'%s','%s','%s')"
        timestr = str( int(time.time()) )
        sqlval = ( data['rid'],str(data['category']),data['number'],str(data['name']),data['uid'],str(data['url']),str(data['source']),timestr )
        sql = sqlstr % sqlval
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def select(self,sql):
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        return rs

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = Db()
    db.createUser()
