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

    def _crawl(self, driver, titlexpath, titleattr, datexpath, dateattr, linkxpath, linkattr = None):
        print(driver.current_url)
        title = driver.find_elements_by_xpath(titlexpath)
        date = driver.find_elements_by_xpath(datexpath)
        for i in title:
            title[title.index(i)] = i.get_attribute(titleattr)
        for i in date:
            date[date.index(i)] = i.get_attribute(dateattr)

        if linkattr != None:
            link = driver.find_elements_by_xpath(linkxpath)
        else:
            link = []
            linker = driver.find_elements_by_xpath(linkxpath)
            for i in range(len(linker)):
                linker[i].click()
                sleep(1)
                link.append(self.driver.current_url)
                self.driver.back()
            sleep(1)
        num = []
        for i in link:
            if linkattr != None:
                tmp = i.get_attribute(linkattr)
                link[link.index(i)] = tmp
            else:
                tmp = i
            num.append(tmp.replace('=', '/').split("/")[-1])

        return title, date, link, num