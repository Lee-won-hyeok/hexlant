from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb
from timeoutException import timeoutException

class korbit(dynamicweb):
    def __init__(self):
        super().__init__('https://www.korbit.co.kr/notice/', "korbit|")
        self.titlexpath = '//*[@id="gatsby-focus-wrapper"]/div[1]/main/div/div[1]/div/table/tbody/tr/td[2]'
        self.datexpath = '//*[@id="gatsby-focus-wrapper"]/div[1]/main/div/div[1]/div/table/tbody/tr/td[3]'
        self.titleattr = 'innerHTML'
        self.dateattr = 'innerHTML'
        self.linkxpath = '//*[@id="gatsby-focus-wrapper"]/div[1]/main/div/div[1]/div/table/tbody/tr'

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title, date, link, num = self._crawl(self.driver, self.titlexpath, self.titleattr, self.datexpath, self.dateattr, self.linkxpath)
            #print(title, date, link, num)

            for i in range(len(title)):
                self.noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 4, "num" : num[i]}
            
            if soup.find_all(class_= "next") == []:
                break

            pagenum += 1
            self.driver.find_elements_by_xpath("//ul[@class = 'pagination']//li[@class]//a[text()='" + str(pagenum + 1) + "']")[0].click()
            sleep(2)
            self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']")[0].click()

            if self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 gyfcrI']") == []:
                raise timeoutException

        self.driver.quit()
        return self.noticedic