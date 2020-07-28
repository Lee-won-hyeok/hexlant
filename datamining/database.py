from preprocessor import preprocessor
from crldriver import crldriver
import pymysql

sql_newtable = """CREATE TABLE keywords (
    -> ID INT(11) NOT NULL,
    -> word VARCHAR(30) NOT NULL,
    -> type1 CHAR(1) NOT NULL,
    -> type2 CHAR(4) NOT NULL,
    -> count INT(11) NOT NULL,
    -> date DATE NOT NULL,
    -> primary KEY (ID)
    -> ) Engine='innoDB' default charset='utf8';"""

db = pymysql.connect(
    user = 'root',
    passwd = '0000',
    host = 'localhost',
    db = 'mining',
    charset = 'utf8'
)

cursor = db.cursor(pymysql.cursors.DictCursor)

sql_showall = "select * from keywords"
sql_insert = """insert into keywords (type1, type2, word, count, date)
         values (%s, %s, %s, %s, %s)"""
sql_initid = """ALTER TABLE keywords AUTO_INCREMENT=1;
        SET @COUNT = 0;
        UPDATE keywords SET ID = @COUNT:=@COUNT+1;"""

#cursor.execute(sql_newtable)

crldriver = crldriver(headless = True)
p = preprocessor()

#packet = crldriver.gettitle(["decenter"])
packet = crldriver.gettitle(["coindeskkorea"])
for m in packet.keys():
    searched = {}
    for n in packet[m]:
        L = list(p.keywording(n))
        for i in L:
            if i not in searched:
                searched[i] = 1
            else:
                searched[i] += 1
    print(m, searched)
    for key in searched:
        cursor.execute(sql_insert, (1, 1002, key, searched[key], m))
"""
packet = crldriver.gettitle(["coindeskkorea"])
for m in packet.keys():
    for n in packet[m]:
        print(m, p.keywording(n))"""


cursor.execute(sql_showall)
rows = cursor.fetchall()
print(rows)
db.commit()