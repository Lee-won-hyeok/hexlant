from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re
from datetime import datetime

from staticweb import staticweb

class bithumb(staticweb):
    def __init__(self):
        super().__init__('https://cafe.bithumb.com/view/boards/43?pageNumber=', "bithumb|")
        
    def _getnotice(self, flag = -1):
        super()._getnotice()
        pagenum = 0
        while(pagenum != flag):
            url = self.url + str(pagenum)
            print("page :", url)
            soup = super()._getsoup(url)
            notice = soup.find_all(class_= 'col-20')
            if notice == []:
                return self.noticedic
            for i in notice[3:]:
                address_compiler = re.compile('[0-9]+')
                address = 'https://cafe.bithumb.com/view/board-contents/' + str(address_compiler.findall(i.attrs['onclick'])[0])
        
                num = i.find_all('td')[0].text        
                title = i.find_all('td')[1].text
                date = i.find_all('td')[2].text

                if re.compile('[0-9]{4}[.][0-9]{2}[.][0-9]{2}').match(date) == None:
                    date = datetime.today().strftime("%Y.%m.%d")

                self.noticedic[num] = []
                self.noticedic[num] = {"title" : title, "date" : date, "link" : address, "extype" : 1, "num" : num}
            pagenum += 1
        return self.noticedic