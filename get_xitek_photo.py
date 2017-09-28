#!/usr/bin/env python 2.7.12
#coding=utf-8
#author=yexiaozhu
import StringIO
import gzip
import os
import re
import urllib
import urllib2

from bs4 import BeautifulSoup


class Xitek():
    def __init__(self):
        self.url = "http://photo.xitek.com/"
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        self.headers = {"User-Agent": user_agent}
        self.last_page = self.__get_last_page()

    def __get_last_page(self):
        html = self.__getContentAuto(self.url)
        bs = BeautifulSoup(html, "html.parser")
        page = bs.find_all('a', class_="blast")
        last_page = page[0]['href'].split('/')[-1]
        return int(last_page)

    def __getContentAuto(self, url):
        req = urllib2.Request(url, headers=self.headers)
        resp = urllib2.urlopen(req)
        #time.sleep(2*random.random())
        content = resp.read()
        info = resp.info().get("Content-Encoding")
        if info == None:
            return content
        else:
            t = StringIO.StringIO(content)
            gziper = gzip.GzipFile(fileobj=t)
            html = gziper.read()
            return html

    def __download(self, url):
        p = re.compile(r'href="(/photoid/\d+)"')
        html = self.__getContentAuto(url)
        content = p.findall(html)
        for i in content:
            print i

            photoid = self.__getContentAuto(self.url+i)
            bs = BeautifulSoup(photoid, "html.parser")
            final_link = bs.find('img', class_="mimg")['src']
            print final_link
            pic_stream = self.__getContentAuto(final_link)
            title = bs.title.string.strip()
            filename = re.sub('[\/:*?"<>|]', '-', title)
            filename = filename+'.jpg'
            urllib.urlretrieve(final_link, filename)
            f = open(filename, 'w')
            f.write(pic_stream)
            f.close()
        print bs.title
        element_link = bs.find_all('div', class_="element")
        print len(element_link)
        k = 1
        for href in element_link:
            print type(href)
            print href.tag
            if href.children[0]:
                print href.children[0]
            t = 0
            for i in href.children:
                if t == 0:
                    print k
                    if i['href']:
                        print '1'
                        # print link
                        # if p.findall(link):
    def getPhoto(self):
        start = 0
        photo_url = "http://photo.xitek.com/style/0/p/"
        for i in range(start,self.last_page+1):
            url=photo_url+str(i)
            print url
            #time.sleep(1)
            self.__download(url)


def main():
    sub_folder = os.path.join(os.getcwd(), "content")
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    os.chdir(sub_folder)
    obj=Xitek()
    obj.getPhoto()


if __name__=="__main__":
    main()