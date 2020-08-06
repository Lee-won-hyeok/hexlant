from crldriver import crldriver
from SQLinterface import SQLinterface
from preprocessor import preprocessor

crldriver = crldriver(headless = True)
p = preprocessor()
interface = SQLinterface(passwd = '0000', dbname = 'mining')
#interface.push('keywords', type1 = 1, type2 = 1, word = 'test', count = 1, date = '2020.07.29')
#interface.showall('keywords')
#interface.init_table('keywords')
#interface.init_id('keywords')
#interface.delete_column('keywords', 'date')
#interface.add_column('keywords', 'date', 'DATE')
#interface.new_table('testtb')
#interface.show_table()
#interface.delete_table('testtb')

def dbupload(packet, type1, type2):
    for m in packet.keys():
        kwrds = interface.showall('Keywords')
        interface.init_table('Keywords')
        interface.init_id('Keywords')
        searched = {}
        for i in kwrds:
            searched[i['word']] = i['count']
        #print(searched)
        
        for n in packet[m]:
            L = list(p.keywording(n))
            for i in L:
                if i not in searched:
                    searched[i] = 1
                else:
                    searched[i] += 1
        print(m, searched)
        
        for key in searched:
            interface.push('keywords', type1 = type1, type2 = type2, word = key, count = searched[key], date = m)

packet = crldriver.gettitle('2020.08.06', ["coindeskkorea"])
dbupload(packet, 1, 0)
#packet = crldriver.gettitle('2020.08.06', ["cobak"])
#dbupload(packet, 2, 0)
#packet = crldriver.gettitle('2020.08.06', ["bitman"])
#dbupload(packet, 2, 1)
#packet = crldriver.gettitle('2020.08.06', ["coinpan"])
#dbupload(packet, 2, 2)
packet = crldriver.gettitle('2020.08.06', ["decenter"])
dbupload(packet, 1, 1)
packet = crldriver.gettitle('2020.08.06', ["joinD"])
dbupload(packet, 1, 2)




