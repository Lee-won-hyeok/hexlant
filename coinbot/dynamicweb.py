from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from exchanger import exchanger

class dynamicweb(exchanger):
    def __init__(self, url, nametag):
        super().__init__(nametag)
        self.url = url
        self.noticedic = {}
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        
    def _getnotice(self, flag = -1):
        #self.driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe')
        self.driver = webdriver.Chrome('C:/Users/LWH/Documents/VS/chromedriver.exe', chrome_options=self.options)
        self.driver.implicitly_wait(1)
        self.driver.get(self.url)
        sleep(7) #Pass 403