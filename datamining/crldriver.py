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
from usrexception import webtypeException, datecheckException, indexException
import re
from datetime import datetime

def aftertouch(string):
    return string.replace("\n", "").strip()

def dateformcheck(string):
    if re.compile('[0-9]{4}[-,.][0-9]{2}[-,.][0-9]{2}').findall(string) != []:
        #print(re.compile('[0-9]{4}[-,.][0-9]{2}[-,.][0-9]{2}').findall(string))
        tmp = re.compile('[0-9]{4}[-,.][0-9]{2}[-,.][0-9]{2}').findall(string)[0]
        return tmp.replace("-", ".")
    elif string != None:
        return datetime.today().strftime("%Y.%m.%d")
    else:
        raise datecheckException

class crldriver:
    def __init__(self, headless = True):
        with open('VS/datamining/properties.json', 'r') as fp:
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

    def gettitle(self, site = None):
        site = self.properties.keys() if site == None else site
        dic = {}
        title = []
        date = []

        for i in site:
            print("==============", i, "================")
            if(self.properties[i]['webtype'] == 'static'):
                soup = self._getsoup(self.properties[i]['url'] + str("1"))
                for j in soup.xpath(self.properties[i]['attribute']['title']):
                    title.append(aftertouch(j.text_content()))
                    #print(aftertouch(j.text_content()))

                for j in soup.xpath(self.properties[i]['attribute']['date']):
                    date.append(dateformcheck(j.text_content()))
                    #print(dateformcheck(j.text_content()))
                
            elif(self.properties[i]['webtype'] == 'dynamic'):
                driver = self._driverload(self.properties[i]['url'] + str("1"))
                if self.properties[i]['iframe'] != '':
                    driver.switch_to_frame(self.properties[i]['iframe'])

                for j in driver.find_elements_by_xpath(self.properties[i]['attribute']['title']):
                    try:
                        title.append(aftertouch(j.get_attribute('text')))
                        #print(aftertouch(j.get_attribute('text')))
                    except:
                        title.append(aftertouch(j.get_attribute('innerHTML')))
                        #print(aftertouch(j.get_attribute('innerHTML')))

                for j in driver.find_elements_by_xpath(self.properties[i]['attribute']['date']):
                    try:
                        date.append(dateformcheck(j.get_attribute('text')))
                        #print(dateformcheck(j.get_attribute('text')))
                    except:
                        date.append(dateformcheck(j.get_attribute('innerHTML')))
                        #print(dateformcheck(j.get_attribute('innerHTML')))

            else:
                raise webtypeException

        if len(title) != len(date): raise indexException
        for i in range(len(title)):
            try:
                dic[date[i]].append(title[i])
            except:
                dic[date[i]] = []
                dic[date[i]].append(title[i])
        #print(dic)
        return dic
        
    def isloaded(self):
        pass

#crldriver = crldriver(headless = False)
#crldriver.gettitle(["decenter", "bitman", "cobak", "coinpan", "coindeskkorea"])