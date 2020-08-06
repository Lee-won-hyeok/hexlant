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
sql_showall = "select * from keywords"
sql_insert = """insert into keywords (type1, type2, word, count, date)
        values (%s, %s, %s, %s, %s)"""
sql_initid = """ALTER TABLE keywords AUTO_INCREMENT=1;
        SET @COUNT = 0;
        UPDATE keywords SET ID = @COUNT:=@COUNT+1;"""

class SQLinterface:
    def __init__(self, dbname, passwd, user = 'root', host = 'localhost', charset = 'utf8'):
        self.charset = charset
        try:
            self.db = pymysql.connect(
                user = user,
                passwd = passwd,
                host = host,
                db = dbname,
                charset = charset
            )
            print(dbname, ": connected")
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except:
            print("unable to connect db")

    def new_table(self, tablename = 'keywords'):
        try:
            sql = "CREATE TABLE " + tablename + """(
ID INT(11) NOT NULL AUTO_INCREMENT,
primary KEY(ID)
) Engine='innoDB' default charset='""" + self.charset + "';"
            self.cursor.execute(sql)
            self.db.commit()
            print("New table:", tablename)
        except:
            print("Failed")
        
    def add_column(self, table_name, col_name, col_type, null=False, option = ''):
        try:
            if null:
                sql = "ALTER TABLE " + table_name + " ADD COLUMN " + col_name + " " + col_type + " " + option + ";"
            else:
                sql = "ALTER TABLE " + table_name + " ADD COLUMN " + col_name + " " + col_type + " NOT NULL " + option + ";"
            self.cursor.execute(sql)
            self.db.commit()
            print(sql)
        except:
            print("failed")

    def modify_column(self, table_name, col_name, col_type, null=False, option = ''):
        try:
            if null:
                sql = "ALTER TABLE " + table_name, " MODIFY COLUMN " + col_name + " " + col_type + " " + option + ";"
            else:
                sql = "ALTER TABLE " + table_name, " MODIFY COLUMN " + col_name + " " + col_type + " NOT NULL " + option + ";"
            self.cursor.execute(sql)
            self.db.commit()
            print(sql)
        except:
            print("failed")

    def delete_column(self, table_name, col_name):
        try:
            sql = "ALTER TABLE " + table_name + " Drop COLUMN " + col_name + ";"
            self.cursor.execute(sql)
            self.db.commit()
            print(sql)
        except:
            print("failed")

    def init_id(self, table_name):
        try:
            sql =  "ALTER TABLE " + table_name + " AUTO_INCREMENT=1;"
            self.cursor.execute(sql)
            self.db.commit()
            print("initialized")
        except:
            print("failed")
    
    def showall(self, table_name):
        try:
            sql = "select * from " + table_name + ";"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
            #print(rows)
        except:
            print("failed")

    def push(self, tablename, **kwargs):
        try:
            attr = []
            sql = "INSERT INTO " + tablename + " ("
            for i in kwargs:
                sql = sql + i + ", "
                attr.append(kwargs[i])
            sql = sql[:-2] + """)
    values ("""
            for i in kwargs:
                sql = sql + "%s, "
            sql = sql[:-2] + ");"
            self.cursor.execute(sql, tuple(attr))
            self.db.commit()
            print("pushed")
        except:
            print("failed")

    def init_table(self, tablename):
        sql = "delete from " + tablename
        self.cursor.execute(sql)
        self.db.commit()
        print("deleted")

    def show_table(self):
        self.cursor.execute('SHOW TABLES;')
        for i in self.cursor.fetchall():
            print(i.values())

    def delete_table(self, tablename):
        try:
            sql = "DROP TABLE " + tablename + ";"
            self.cursor.execute(sql)
            self.db.commit()
            print("table deleted")
        except:
            print("failed")

    def find(self, tablename, key):
        sql = "select * from CAT_TREE where cate_name like '" + key + "';"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        print(rows)
        return rows

#crldriver = crldriver(headless = True)
#p = preprocessor()
#interface = SQLinterface(passwd = '0000', dbname = 'mining')
#interface.push('keywords', type1 = 1, type2 = 1, word = 'test', count = 1, date = '2020.07.29')
#interface.showall('keywords')
#interface.init_table('keywords')
#interface.init_id('keywords')
#interface.delete_column('keywords', 'date')
#interface.add_column('keywords', 'date', 'DATE')
#interface.new_table('testtb')
#interface.show_table()
#interface.delete_table('testtb')

#packet = crldriver.gettitle(["coindeskkorea"])
#packet = crldriver.gettitle(["decenter"])
#packet = crldriver.gettitle(["coinpan"])
#packet = crldriver.gettitle(["cobak"])
#packet = crldriver.gettitle(["bitman"])
"""
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
        cursor.execute(sql_insert, (1, 1, key, searched[key], m))"""
"""
def get_table():
    cursor.execute(sql_showall)
    rows = cursor.fetchall()
    print(rows)

db.commit()"""

