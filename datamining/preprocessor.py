from crldriver import crldriver
from konlpy.tag import Okt
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
import re

class preprocessor:
    def __init__(self):
        pass

    def keywording(self, string):
        fp = open("dic.txt", 'a')
        #print(string)
        hannanum = Hannanum()
        partition1 = set(hannanum.nouns(re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』“”\\‘’|\(\)\[\]\<\>`\'…》x]', ' ', string)))
        
        komoran = Komoran(userdic = "dic.txt")
        try: #utf-8 디코딩 에러시 except
            partition2 = set(komoran.nouns(string))
        except:
            partition2 = set()
        keyword = partition1 & partition2
        diff1 = list(partition1 - partition2)
        diff2 = list(partition2 - partition1)
        for i in range(len(diff1)):
            for j in range(len(diff2)):
                if (diff1[i] in diff2[j]) and (diff1[i] != diff2[j]):
                    diff1[i] = ''
        for i in range(len(diff2)):
            for j in range(len(diff1)):
                if diff2[i] in diff1[j]:
                    diff2[i] = ''

        diff = set(diff1) | set(diff2)
        for i in diff:
            if re.compile('^[0-9./&+-]*$').findall(i) == []:
                keyword.add(i)
                try:
                    fp.write(i)
                    fp.write("\n")
                except:
                    pass
        fp.close()
        print(keyword)
        return keyword
"""
crldriver = crldriver(headless = True)
p = preprocessor()
packet = crldriver.gettitle('2020.08.06', ["coindeskkorea", "cobak", "bitman", "coinpan", "decenter", "joinD"])
#"bitman", "cobak", "coinpan", 
for m in packet.keys():
    for n in packet[m]:
        print(p.keywording(n))"""