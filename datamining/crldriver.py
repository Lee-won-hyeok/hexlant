import pymysql
import selenium
import json
import urllib.request
from bs4 import BeautifulSoup
import requests
import ssl
#from lxml.html import etree, fromstring, tostring
import lxml.html
from selenium import webdriver
from time import sleep
import sys
from usrexception import webtypeException, datecheckException, indexException, paginationException, programmingException, scrollException, NullException
import re
from datetime import datetime, timedelta

def aftertouch(string):
    return string.replace("\n", "").strip()

def dateformcheck(string):
    if re.compile('[0-9]{4}[-,.][0-9]{2}[-,.][0-9]{2}').findall(string) != []:
        tmp = re.compile('[0-9]{4}[-,.][0-9]{2}[-,.][0-9]{2}').findall(string)[0]
        return tmp.replace("-", ".")
    elif string != None:
        if re.compile('[0-9(an)]+[\s]hour').findall(string) != [] or re.compile('[0-9(an)]+[\s]시간').findall(string) != []:
            tmp = re.compile('[0-9(an)]+').findall(string)[0]
            tmp = 1 if tmp == 'an' else int(tmp)
            if datetime.today().hour >= tmp:
                return datetime.today().strftime("%Y.%m.%d")
            else:
                return (datetime.today() - timedelta(1)).strftime("%Y.%m.%d")
        elif re.compile('[0-9a]+[\s]day').findall(string) != [] or re.compile('[0-9a]+[\s]일').findall(string) != []:
            td = re.compile('[0-9a]+').findall(string)[0]
            td = 1 if td == 'a' else int(td)
            return (datetime.today() - timedelta(td)).strftime("%Y.%m.%d")
        else:
            return datetime.today().strftime("%Y.%m.%d")

    else:
        raise datecheckException

class crldriver:
    def __init__(self, headless = True):
        with open('datamining/properties.json', 'r') as fp:
            self.properties = json.load(fp)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
        self.options.add_experimental_option('prefs', prefs)
        self.headless = headless
    
    def getproperties(self, site = None):
        site = self.properties.keys() if site == None else site
        for i in site:
            print(i, ":", self.properties[i])

    def _driverload(self, url):
        if self.headless:
            driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe', chrome_options=self.options)
        else:
            driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get(url)
        #self.isloaded()
        return driver

    def _getsoup(self, url):
        headers    = {'User-Agent':'Chrome/83.0.4103.116'}
        response   = requests.get(url, headers=headers)
        tree = lxml.html.fromstring(response.text)
        return tree

    def gettitle(self, flagdate, site = None):
        site = self.properties.keys() if site == None else site
        dic = {}
        title = []
        date = []
        flagdatetime = datetime.strptime(flagdate, '%Y.%m.%d')

        for i in site:
            print("==============", i, "================")
            if(self.properties[i]['webtype'] == 'static'):
                pagenum = 1
                while(1):
                    soup = self._getsoup(self._paginate(i, pagenum = pagenum))
                    for j in soup.xpath(self.properties[i]['attribute']['title']):
                        title.append(aftertouch(j.text_content()))

                    for j in soup.xpath(self.properties[i]['attribute']['date']):
                        date.append(dateformcheck(j.text_content()))
                        
                    lastdate = datetime.strptime(date[-1], '%Y.%m.%d')
                    if flagdatetime > lastdate:
                        break

                    pagenum += 1
                
            elif(self.properties[i]['webtype'] == 'dynamic'):
                try:
                    self.properties[i]['pagination']['link']
                    pagenum = 1
                    flag = 0
                except:
                    self.properties[i]['pagination']['scroll']
                    flag = 1

                index = 0
                
                driver = self._driverload(self.properties[i]['url'])
                while(1):
                    driver.switch_to_default_content()

                    if self.properties[i]['iframe'] != '':
                        driver.switch_to_frame(self.properties[i]['iframe'])

                    for j in driver.find_elements_by_xpath(self.properties[i]['attribute']['title'])[index:]:
                        try:
                            if j.get_attribute('text') == None: raise NullException
                            title.append(aftertouch(j.get_attribute('text')))
                            #print(aftertouch(j.get_attribute('text')))
                        except:
                            title.append(aftertouch(j.get_attribute('innerHTML')))
                            #print(aftertouch(j.get_attribute('innerHTML')))

                    for j in driver.find_elements_by_xpath(self.properties[i]['attribute']['date'])[index:]:
                        if flag: index += 1
                        try:
                            if j.get_attribute('text') == None: raise NullException
                            date.append(dateformcheck(j.get_attribute('text')))
                            #print(dateformcheck(j.get_attribute('text')))
                        except:
                            date.append(dateformcheck(j.get_attribute('innerHTML')))
                            #print(dateformcheck(j.get_attribute('innerHTML')))

                    lastdate = datetime.strptime(date[-1], '%Y.%m.%d')
                    if flagdatetime > lastdate:
                        print("======crawled=======")
                        break

                    if flag: 
                        self._paginate(i, driver = driver)
                    else:
                        pagenum += 1
                        self._paginate(i, pagenum = pagenum, driver = driver).click()

            else:
                raise webtypeException

        if len(title) != len(date): raise indexException
        for i in range(len(title)):
            try:
                dic[date[i]].append(title[i])
            except:
                if not (flagdatetime > datetime.strptime(date[i], '%Y.%m.%d')):
                    dic[date[i]] = []
                    dic[date[i]].append(title[i])

        for i in dic:
            dic[i] = list(set(dic[i]))  #중복 제목 제거
        #print(dic)
        return dic
        
    def isloaded(self):
        pass

    def _paginate(self, site, pagenum = None, driver = None):
        try:
            tmp = self.properties[site]['pagination']['url']
            print("use url pagination")
            return self.properties[site]['url'] + str(pagenum)
        except:
            if driver == None:
                raise programmingException
            try:
                xlink = self.properties[site]['pagination']['link']
                for i in driver.find_elements_by_xpath(xlink):
                    if i.get_attribute('innerHTML') == str(pagenum):
                        print("use xpath link pagination")
                        return i
                try:
                    return driver.find_element_by_xpath(self.properties[site]['pagination']['link2'])
                except:
                    raise paginationException
            except:
                try:
                    scroll = self.properties[site]['pagination']['scroll']
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("use scroll pagination")
                    return
                except:
                    raise scrollException

#crldriver = crldriver(headless = False)
#crldriver.gettitle('2020.07.20', ["joinD"])

#"coindeskkorea", "cobak", "bitman", "coinpan", "decenter", "joinD"