from bs4 import BeautifulSoup
import urllib.request
import ssl
import re

context = ssl._create_unverified_context()
url = 'https://www.bithumb.com/'
req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0'})
html = urllib.request.urlopen(req, context = context).read()

soup = BeautifulSoup(html, 'html.parser')
name = soup.find_all(class_= 'blind')
essetrate = soup.find_all(class_= 'sort_change')
#essetrate = soup.find_all('strong', {'class':'sort_change'})
#essetrate = soup.select("strong.sort_change")

del name[:2]

tmp = 0
while(tmp < len(name)):
    essetrate[tmp] = essetrate[tmp].attrs['data-sorting']
    name[tmp] = name[tmp].text
    name[tmp] = re.sub('[0-9]?[A-Z]+[.]?[A-Z]*','', name[tmp])
    #print(name[tmp], essetrate[tmp])
    tmp += 1

