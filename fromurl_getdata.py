#coding:utf-8
from urllib import urlopen
from bs4 import BeautifulSoup

import re
import os
import os.path
import json

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

rootdir = "D:\实体关系抽取实验\影视数据\hyperlinks"  # 指明被遍历的文件夹
i=1

for parent,dirnames,filenames in os.walk(rootdir):     #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                     #输出文件信息
            sourceDir = os.path.join(parent,filename)  #输出文件路径信息
            fopen = open(sourceDir,'r')
            while True:
                datadic={}
                line = fopen.readline()
                if line == "":
                    break
                try:
                    html = urlopen(line).read()
                    soup = BeautifulSoup(html)
                    filestr ="D:/实体关系抽取实验/影视数据/raw_data/" + str(i)+ ".txt"
                    titlestr =""
                    fromstr=""
                    articlestr=""

                    tilist = soup.find_all("h1", id="main_title")
                    if len(tilist):#不空
                        titlestr=str(tilist[0])#标题

                    sourlist = soup.find_all("span",id="media_name")
                    if len(sourlist):
                        fromstr =str(sourlist[0])#来源

                    arlist = soup.find_all("div",id="artibody")
                    if len(arlist):
                        for z in range(len(arlist[0].find_all('p'))):
                            articlestr = articlestr + str(arlist[0].find_all('p')[z])#正文

                    soup_title = BeautifulSoup(titlestr)
                    soup_from = BeautifulSoup(fromstr)
                    soup_article = BeautifulSoup(articlestr)           
                    datadic['title']=soup_title.get_text()
                    datadic['from']=soup_from.get_text()
                    datadic['article']=soup_article.get_text()
                    if not (not datadic['title'].strip() and not datadic['from'].strip() and not datadic['article'].strip()):
                        json.dump(datadic, open(filestr, 'w'),encoding="UTF-8", ensure_ascii=False)
                        i = i+1
                except IOError,e:
                    print ("*** file open error",e)
            fopen.close()
   
