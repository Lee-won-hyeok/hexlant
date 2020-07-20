from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb

class upbit(dynamicweb):
    def __init__(self):
        super().__init__('https://upbit.com/service_center/notice', "upbit|")
        self.titlexpath = "//*[@id='UpbitLayout']/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr/td[1]/a"
        self.datexpath = "//*[@id='UpbitLayout']/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr/td[2]"
        self.linkxpath = "//*[@id='UpbitLayout']/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr/td[1]/a"
        self.titleattr = 'text'
        self.dateattr = 'innerHTML'
        self.linkattr = 'href'

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            title, date, link, num = self._crawl(self.driver, self.titlexpath, self.titleattr, self.datexpath, self.dateattr, self.linkxpath, self.linkattr)

            for i in range(len(title) - len(date)):
                date.insert(0, 'null')

            for i in range(len(title)):
                self.noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 3, "num" : num[i]}
            
            #print(self.noticedic)
            
            pagenum += 1
            if((pagenum + 1)%5 == 1):
                if(self.driver.find_elements_by_xpath("//a[@href = '#' and @class='next']") == []):
                    break
                else:
                    self.driver.find_elements_by_xpath("//a[@href = '#' and @class='next']")[0].click()
            else:
                xpath = "//span[@class = 'paging']//*[text()='" + str(pagenum + 1) + "']"
                if(self.driver.find_elements_by_xpath(xpath) == []):
                    break
                else:
                    self.driver.find_elements_by_xpath(xpath)[0].click()

        self.driver.quit()
        return self.noticedic