#!/usr/bin/env python 2.7.12
#coding=utf-8
#author=yexiaozhu
import MySQLdb
import pymysql
import time
import urllib2

import datetime
from lxml import etree


class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        self.header = {"User-Agent": self.user_agent}
        self.dbname = "proxy.db"
        self.now = time.strftime("%Y-%m-%d")

    def getContent(self, num):
        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        # 国内高匿
        req = urllib2.Request(nn_url, headers=self.header)
        # resq = urllib2.urlopen(req, timeout=10)
        resq = urllib2.urlopen(req)
        content = resq.read()
        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        # 因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        # 刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        # 使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]
            print "IP:%s\tPort:%s" % (t1[0], t1[1])
            if self.isAlive(t1[0], t1[1]):
                self.insert_db(self.now, t1[0], t1[1])
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            print "IP:%s\tPort:%s" % (t2[0], t2[1])
            if self.isAlive(t2[0], t2[1]):
                self.insert_db(self.now, t2[0], t2[1])

    def insert_db(self, date, ip, port):
        dbname = self.dbname
        try:
            conn = pymysql.connect(
                host='192.168.1.75',
                port=3306,
                user='root',
                passwd='w123456',
                db='proxy',
                # charset='utf8mb4'
            )
        except:
            print "Error to open database proxy"
        create_tb='''
        CREATE TABLE IF NOT EXISTS PROXY
        (DATE TEXT,
        IP TEXT,
        PORT TEXT
        );'''
        conn.cursor().execute(create_tb)
        insert_db_cmd='''INSERT INTO PROXY (DATE,IP,PORT) VALUES ('%s','%s','%s');
        ''' %(date,ip,port) #写入时间，ip和端口'''
        conn.cursor().execute(insert_db_cmd)
        conn.commit()#记录commit
        conn.close()

    #查看爬到的代理IP是否可用
    def isAlive(self, ip, port):
        proxy = {'http':ip+':'+port}
        print proxy

        #使用方法时全局方法
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #使用代理访问腾讯官网,进行验证代理是否有效
        test_url = "http://www.qq.com"
        req = urllib2.Request(test_url, headers=self.header)
        try:
            resp = urllib2.urlopen(req, timeout=100)
            #timeout 设置100s
            if resp.code == 200:
                print "work"
                return True
            else:
                print "not work"
                return False
        except:
            print "Not work"
            return False

    def loop(self, page):
        for i in range(1, page):
            self.getContent(i)

if __name__ == "__main__":
    now = datetime.datetime.now()
    print "Start at %s" % now
    obj = getProxy()
    obj.loop(5)