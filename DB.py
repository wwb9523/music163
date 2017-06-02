#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

class MyDB(object):
    def __init__(self):
        self.db = pymysql.connect(
            host='98.142.140.54',
            #host='127.0.0.1',
            port = 3306,
            user='root',
            passwd='APTX4369',
          #  passwd='',
            db ='music',
            charset='utf8'
            )
        self.cursor=self.db.cursor()

    def insertAuthor(self,id,name):
        sql='insert into author(id,name) VALUES(%s,"%s")'%(id,name)
        return self.cursor.execute(sql)

    def insertSong(self,id,name):
        sql='insert into song(id,name) VALUES(%s,"%s")'%(id,name)
        return self.cursor.execute(sql)

    def insertRel(self,songId,authorId):
        sql='insert into song_author(songId,authorId) VALUES(%s,%s)'%(songId,authorId)
        return self.cursor.execute(sql)

    def getAuthor(self,id):
        sql='select name from author where id=%s'%id
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getSong(self,id):
        sql = 'select name from song where id=%s' % id
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getAllSong(self):
        sql = 'select id,name from song where statu=0'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def updateSong(self,id,statu):
        sql='update song set statu=%s where id=%s'%(statu,id)
        return self.cursor.execute(sql)



