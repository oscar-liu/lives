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
    
    def checkStr(self,s):
        tmp = 'None'
        if s:
            tmp = str(s)
            if tmp.find("'") >= 0 :
                tmp = tmp.replace("'","-官方号")
        return tmp

    def checkInt(self,i):
        tmp = 0
        if i:
            if type(i) == int:
                tmp = int(i)
        return tmp

    def insert(self,data):
        timestr = str( int(time.time()) )
        # print(self.checkStr(data['name']))
        sqlstr = "insert into user (rid,category,number,name,uid,url,source,create_time) values (%s,'%s',%s,'%s',%s,'%s','%s','%s')"
        sqlval = ( self.checkInt(data['rid']), self.checkStr(data['category']),self.checkInt(data['number']),self.checkStr(data['name']),self.checkInt(data['uid']),self.checkStr(data['url']),self.checkStr(data['source']),timestr )
        # print(sqlstr % sqlval)
        self.cursor.execute("insert into user (rid,category,number,name,uid,url,source,create_time) values (%s,'%s',%s,'%s',%s,'%s','%s','%s')" % ( self.checkInt(data['rid']), self.checkStr(data['category']),self.checkInt(data['number']),self.checkStr(data['name']),self.checkInt(data['uid']),self.checkStr(data['url']),self.checkStr(data['source']),timestr ) )
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
