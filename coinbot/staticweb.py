from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
from datetime import datetime

from exchanger import exchanger

class staticweb(exchanger):
    def __init__(self, url, nametag):
        super().__init__(nametag)
        self.url = url
        self.noticedic = {}

    def _getsoup(self, url):
        #req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1;'})
        req = urllib.request.Request(url, headers = {'User-Agent':'Chrome/66.0.3359.181'})
        context = ssl._create_unverified_context()
        html = urllib.request.urlopen(req, context = context).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def _getnotice(self, flag = -1):
        pass