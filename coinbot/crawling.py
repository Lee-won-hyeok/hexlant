from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re
import json
from datetime import datetime

context = ssl._create_unverified_context()

def getsoup(url):
    #req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1;'})
    req = urllib.request.Request(url, headers = {'User-Agent':'Chrome/66.0.3359.181'})
    html = urllib.request.urlopen(req, context = context).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def bithumb_notice(flag = -1):
    pagenum = 0
    noticedic = {}
    while(pagenum != flag):
        url = 'https://cafe.bithumb.com/view/boards/43?pageNumber=' + str(pagenum)
        soup = getsoup(url)
        notice = soup.find_all(class_= 'col-20')
        if notice == []:
            return noticedic
        for i in notice[3:]:
            address_compiler = re.compile('[0-9]+')
            address = 'https://cafe.bithumb.com/view/board-contents/' + str(address_compiler.findall(i.attrs['onclick'])[0])
        
            num = i.find_all('td')[0].text        
            title = i.find_all('td')[1].text
            date = i.find_all('td')[2].text

            if re.compile('[0-9]{4}[.][0-9]{2}[.][0-9]{2}').match(date) == None:
                date = datetime.today().strftime("%Y.%m.%d")

            noticedic[num] = []
            noticedic[num] = {"title" : title, "date" : date, "link" : address, "extype" : 1, "num" : num}
        pagenum += 1
    return noticedic

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


#update:notice information
def note_update():
    new_db = []
    new_db.append(bithumb_notice())

    return new_db