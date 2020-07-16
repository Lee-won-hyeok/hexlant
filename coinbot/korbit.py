from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb

class korbit(dynamicweb):
    def __init__(self):
        super().__init__('https://www.korbit.co.kr/notice/', "korbit|")

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find_all(class_ = "styled__Tr-l4nq3x-4")
            date = soup.find_all(class_ = "styled__Tr-l4nq3x-4")
            link = []
            num = []
            for i in range(len(title)):
                title[i] = title[i].find_all("td")[1].text
                date[i] = date[i].find_all("td")[2].text

            link.append(self.driver.current_url)
            num.append(self.driver.current_url.split('=')[1])
            
            for i in range(len(self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']"))):
                self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']")[i].click()
                sleep(0.5)
                link.append(self.driver.current_url)
                print(self.driver.current_url)
                num.append(self.driver.current_url.split('=')[1])
            for i in range(len(title)):
                self.noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 4, "num" : num[i]}
            
            if len(self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']")) != 9:
                break

            pagenum += 1
            self.driver.find_elements_by_xpath("//ul[@class = 'pagination']//li[@class]//a[text()='" + str(pagenum + 1) + "']")[0].click()
            sleep(2)
            self.driver.find_elements_by_xpath("//tr[@class = 'styled__Tr-l4nq3x-4 iAAYmx']")[0].click()

        self.driver.quit()
        return self.noticedic