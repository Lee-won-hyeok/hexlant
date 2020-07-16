from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb

class coinone(dynamicweb):
    def __init__(self):
        super().__init__('https://coinone.co.kr/talk/notice', "coinone|")

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            category = soup.find_all(class_="card_category")
            title = soup.find_all(class_="card_summary_title")
            date = soup.find_all(class_="card_time")
        
            self.driver.find_elements_by_xpath("//a[@class = 'card_link']")[0].click()
            sleep(1)
            recentlink = self.driver.current_url
            num = re.compile('[0-9]+').findall(recentlink)[0]

            for i in range(len(title)):
                self.noticedic[int(num) - i] = {"title" : "[" + category[i].text.replace(' ','') + "]" + title[i].text, "date" : date[i].text, "link" : 'https://coinone.co.kr/talk/notice/detail/' + str(int(num) - i), "extype" : 2, "num" : int(num) - i}
            
                if int(num) - i == 1:
                    self.driver.quit()
                    return self.noticedic
            self.driver.back()
            sleep(1)
            pagenum += 1
            self.driver.find_elements_by_xpath("//a[@class = 'page-link']")[-1].click()
        self.driver.quit()
        return self.noticedic