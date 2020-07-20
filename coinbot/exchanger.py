from abc import ABCMeta, abstractmethod, ABC
from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re
import json
from datetime import datetime
from selenium import webdriver
from time import sleep

import telegram
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['coindb']
col = db['coincol']
bot = telegram.Bot(token = "1344514128:AAGLLNrfIgMME0CXcqDQbXFz7y--Hl7MJto")

class exchanger(metaclass = ABCMeta):
    def __init__(self, nametag): #constructor #override
        self.nametag = nametag

    @abstractmethod
    def _getnotice(self, flag = -1): #private #override
        raise NotImplementedError()

    def _newnotice(self): #private
        L = []
        for i in self._getnotice(1).values():
            if col.find_one({'num' : i['num']}) == None:
                title = self.nametag + i['title'] + "\n" + i['link']
                L.append(title)
                notice_id = col.insert_one(i).inserted_id
                print("refresh: added", notice_id)
        return L

    def dbbuild(self): #public
        token = self._getnotice()
        for i in token.values():
            notice_id = col.insert_one(i).inserted_id
            print("added", notice_id)

    def refresh(self): #public
        for j in self._newnotice():
            bot.sendMessage(chat_id = -1001493621312, text = j)
            print("sended")
