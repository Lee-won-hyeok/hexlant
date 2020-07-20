from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb

class coinone(dynamicweb):
    def __init__(self):
        super().__init__('https://coinone.co.kr/talk/notice', "coinone|")
        self.titlexpath = "//*[@id='content_section']/div/talk-articles/div/div/talk-article-list/article/div[1]/a/div[1]/span[2]"
        self.datexpath = "//*[@id='content_section']/div/talk-articles/div/div/talk-article-list/article/div[2]/span/span[5]"
        self.linkxpath = "//*[@id='content_section']/div/talk-articles/div/div/talk-article-list/article/div[1]"
        self.titleattr = 'innerHTML'
        self.dateattr = 'innerHTML'

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category = soup.find_all(class_="card_category")

            title, date, link, num = self._crawl(self.driver, self.titlexpath, self.titleattr, self.datexpath, self.dateattr, self.linkxpath)
            #print(title, date, link, num)
            
            for i in range(len(title)):
                title[i] =  "[" + category[i].text.replace(' ','') + "]" + title[i]
                self.noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 2, "num" : num[i]}
            
            if soup.find_all(class_="pagination-next page-item ng-star-inserted disabled") != []:
                self.driver.quit()
                return self.noticedic
            pagenum += 1
            self.driver.find_elements_by_xpath("//a[@class = 'page-link']")[-1].click()
        
        self.driver.quit()
        return self.noticedic
