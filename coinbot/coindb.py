import pymongo
import crawling
import json

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['coindb']
bithumb_col = db['bithumb']
upbit_col = db['upbit']
coinone_col = db['coinone']
korbit_col = db['korbit']

def startdb():
    tokens = crawling.note_update()
    
    #bithumb
    bithumb_token = tokens[0]
    for i in bithumb_token.values():
        notice_id = bithumb_col.insert_one(i).inserted_id
        print("added", notice_id)
    
    #
    #
    #

def new_notice():
    #bithumb
    L = []
    for i in crawling.bithumb_notice(1).values():
        if bithumb_col.find_one({'num' : i['num']}) == None:
            title = "bithumb|" + i['title']
            L.append(title)
            notice_id = bithumb_col.insert_one(i).inserted_id
            print("refresh: added", notice_id)
    return L

def init_col(collection):
    collection.remove()

#init_col(bithumb_col)
#startdb()