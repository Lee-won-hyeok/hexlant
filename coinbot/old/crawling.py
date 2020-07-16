from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re
import json
from datetime import datetime
from selenium import webdriver
from time import sleep

context = ssl._create_unverified_context()

def getsoup(url):
    #req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1;'})
    req = urllib.request.Request(url, headers = {'User-Agent':'Chrome/66.0.3359.181'})
    html = urllib.request.urlopen(req, context = context).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def bithumb_notice(flag = -1): #getnotice
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

#coinone 
def coinone_notice(flag = -1):
    noticedic = {}

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe', chrome_options=options)
    url = 'https://coinone.co.kr/talk/notice'
    driver.implicitly_wait(1)
    driver.get(url)
    sleep(7) #Pass 403

    pagenum = 0
    while(pagenum != flag):
        sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        category = soup.find_all(class_="card_category")
        title = soup.find_all(class_="card_summary_title")
        date = soup.find_all(class_="card_time")
        
        driver.find_elements_by_xpath("//a[@class = 'card_link']")[0].click()
        sleep(1)
        recentlink = driver.current_url
        num = re.compile('[0-9]+').findall(recentlink)[0]

        for i in range(len(title)):
            noticedic[int(num) - i] = {"title" : "[" + category[i].text.replace(' ','') + "]" + title[i].text, "date" : date[i].text, "link" : 'https://coinone.co.kr/talk/notice/detail/' + str(int(num) - i), "extype" : 2, "num" : int(num) - i}
            #print(noticedic[int(num) - i])
            if int(num) - i == 1:
                driver.quit()
                return noticedic
        driver.back()
        sleep(1)
        pagenum += 1
        driver.find_elements_by_xpath("//a[@class = 'page-link']")[-1].click()
    driver.quit()
    return noticedic

#upbit // 전체 긁어오기 구현안함
def upbit_notice(flag = -1):
    noticedic = {}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    url = 'https://upbit.com/service_center/notice'
    driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe', options = options)
    driver.implicitly_wait(1)
    driver.get(url)
    sleep(8)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find_all("td", {'class' : 'lAlign'})
    title = soup.find_all("td", {'class' : 'lAlign'})
    num = []
    for i in range(len(title)):
        title[i] = title[i].a.text
        link[i] = "https://upbit.com" + link[i].a['href']
        num.append(re.compile('[0-9]{1,4}').findall(link[i])[0])
    
    data = soup.find_all("td")
    date = []
    for i in data:
        cmplr = re.compile('[0-9]{4}[.][0-9]{2}[.][0-9]{2}')
        if cmplr.findall(i.text) != []:
            date.append(cmplr.findall(i.text)[0])
    for i in range(len(title) - len(date)):
        date.insert(0, 'null')
    #print(title)
    #print(date)
    #print(link)
    #print(num)
    for i in range(len(title)):
        noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 3, "num" : num[i]}
    return noticedic

#korbit // 전체 긁어오기 구현안함
def korbit_notice(flag = -1):
    noticedic = {}
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    url = 'https://www.korbit.co.kr/notice/'
    driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe', options = options)
    driver.implicitly_wait(1)
    driver.get(url)
    sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all(class_ = "styled__Tr-l4nq3x-4")
    date = soup.find_all(class_ = "styled__Tr-l4nq3x-4")
    link = []
    num = []
    for i in range(len(title)):
        title[i] = title[i].find_all("td")[1].text
        date[i] = date[i].find_all("td")[2].text

    link.append(driver.current_url)
    num.append(driver.current_url.split('=')[1])
    for i in range(len(driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']"))):
        driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']")[i].click()
        sleep(0.5)
        link.append(driver.current_url)
        num.append(driver.current_url.split('=')[1])
    for i in range(len(title)):
        noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 4, "num" : num[i]}
    return noticedic

#update:notice information
def note_start():
    new_db = []
    new_db.append(bithumb_notice())
    new_db.append(coinone_notice())
    new_db.append(upbit_notice())
    new_db.append(korbit_notice())

    return new_db
