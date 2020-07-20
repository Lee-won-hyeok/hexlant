import pymongo
import crawling
import json

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['coindb']
"""
bithumb_col = db['bithumb']
upbit_col = db['upbit']
coinone_col = db['coinone']
korbit_col = db['korbit']"""
coin_col = db['coincol']


def startdb(): #dbbuild
    tokens = crawling.note_start()
    
    #bithumb
    bithumb_token = tokens[0]
    for i in bithumb_token.values():
        notice_id = coin_col.insert_one(i).inserted_id
        print("added", notice_id)
    
    #coinone
    coinone_token = tokens[1]
    for i in coinone_token.values():
        notice_id = coin_col.insert_one(i).inserted_id
        print("added", notice_id)

    #upbit
    upbit_token = tokens[1]
    for i in upbit_token.values():
        notice_id = coin_col.insert_one(i).inserted_id
        print("added", notice_id)
    
    #korbit
    korbit_token = tokens[1]
    for i in korbit_token.values():
        notice_id = coin_col.insert_one(i).inserted_id
        print("added", notice_id)

def new_notice(): #dbupload
    #bithumb
    L = []
    for i in crawling.bithumb_notice(1).values():
        if coin_col.find_one({'num' : i['num']}) == None:
            title = "bithumb|" + i['title'] + "\n" + i['link']
            L.append(title)
            notice_id = coin_col.insert_one(i).inserted_id
            print("refresh: added", notice_id)

    #coinone
    for i in crawling.coinone_notice(1).values():
        if coin_col.find_one({'num' : i['num']}) == None:
            title = "coinone|" + i['title'] + "\n" + i['link']
            L.append(title)
            notice_id = coin_col.insert_one(i).inserted_id
            print("refresh: added", notice_id)
    
    #upbit
    for i in crawling.upbit_notice(1).values():
        if coin_col.find_one({'num' : i['num']}) == None:
            title = "upbit|" + i['title'] + "\n" + i['link']
            L.append(title)
            notice_id = coin_col.insert_one(i).inserted_id
            print("refresh: added", notice_id)

    #korbit
    for i in crawling.korbit_notice(1).values():
        if coin_col.find_one({'num' : i['num']}) == None:
            title = "korbit|" + i['title'] + "\n" + i['link']
            L.append(title)
            notice_id = coin_col.insert_one(i).inserted_id
            print("refresh: added", notice_id)

    return L

def init_db():
    coin_col.remove()

"""
def init_db():
    init_col(bithumb_col)
    init_col(coinone_col)
    init_col(upbit_col)
    init_col(korbit_col)
    """