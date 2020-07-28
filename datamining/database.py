from preprocessor import preprocessor

import pymysql

db = pymysql.connect(
    user = 'root',
    passwd = 'hexlant0724',
    host = 'localhost',
    db = 'MySQL',
    charset = 'utf8'
)

cursor = db.cursor(pymysql.cursors.DictCursor)

#sql = "select * from db"
sql = """insert into db(type1, type2, word, count, date)
         values (%s, %s, %s, %s, %s)"""
cursor.execute(sql, (1, 1001, 'a', 3, '2020.07.24'))
db.commit()