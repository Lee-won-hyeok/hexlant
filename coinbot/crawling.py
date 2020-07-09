from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re

context = ssl._create_unverified_context()

#getsoup
def getsoup(url):
    req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0'})
    html = urllib.request.urlopen(req, context = context).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#bithumb
"""
class bithumb:
    def __init__(self):
        self.url = 'https://www.bithumb.com/'
    
    def getnotice(self):
        self.soup = getsoup(self.url)
        self.notice = self.soup.find_all('a', {'href': re.compile("https://cafe.bithumb.com/view/board-contents/[0-9]+")}, {'rel' : "noopener noreferrer"})
        self.notice_history = []
        del self.notice[:7]
        del self.notice[2:]
        tmp = 0
        while(tmp < len(self.notice)):
            self.notice[tmp] = self.notice[tmp].text
            tmp += 1
"""
notice_history = []

def new_notice():
    L = []
    for i in bithumb_notice():
        if i not in notice_history:
            notice_history.append(i)
            L.append(i)
    return L

def bithumb_notice():
    url = 'https://www.bithumb.com/'
    soup = getsoup(url)
    
    notice = soup.find_all('a', {'href': re.compile("https://cafe.bithumb.com/view/board-contents/[0-9]+")}, {'rel' : "noopener noreferrer"})
    del notice[:7]
    del notice[2:]
    tmp = 0
    while(tmp < len(notice)):
        notice[tmp] = notice[tmp].text
        tmp += 1
    return notice

def new_coinchart():
    url = 'https://www.bithumb.com/'
    soup = getsoup(url)

    name = soup.find_all(class_= 'blind')
    essetrate = soup.find_all(class_= 'sort_change')
    del name[:2]
    #essetrate = soup.find_all('strong', {'class':'sort_change'})
    #essetrate = soup.select("strong.sort_change")

    tmp = 0
    chartdic={}
    while(tmp < len(name)):
        essetrate[tmp] = essetrate[tmp].attrs['data-sorting']
        name[tmp] = name[tmp].text
        name[tmp] = re.sub('[0-9]?[A-Z]+[.]?[A-Z]*','', name[tmp])
        chartdic[name[tmp]] = essetrate[tmp]
        tmp += 1
        
    return chartdic

#upbit
