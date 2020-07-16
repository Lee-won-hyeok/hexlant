from bs4 import BeautifulSoup
import re
from selenium import webdriver
from time import sleep

from dynamicweb import dynamicweb

class upbit(dynamicweb):
    def __init__(self):
        super().__init__('https://upbit.com/service_center/notice', "upbit|")

    def _getnotice(self, flag = -1):
        super()._getnotice(flag = -1)
        pagenum = 0
        while(pagenum != flag):
            sleep(1)
            html = self.driver.page_source
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

            for i in range(len(title)):
                self.noticedic[num[i]] = {"title" : title[i], "date" : date[i], "link" : link[i], "extype" : 3, "num" : num[i]}
            
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