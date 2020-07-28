from crldriver import crldriver
from konlpy.tag import Okt
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
import re

class preprocessor:
    def __init__(self):
        pass

    def keywording(self, string):
        #string = re.sub('[^\w\s]', '', string)
        #string = re.sub('[\"\']', '', string)
        #string.replace("’", " ").replace('"', " ").replace("[", " ").replace("]", " ")
        fp = open("dic.txt", 'a')
        hannanum = Hannanum()
        hannanum.nouns
        partition1 = set(hannanum.nouns(string))
        
        komoran = Komoran(userdic = "dic.txt")
        partition2 = set(komoran.nouns(string))

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
                fp.write(i)
                fp.write("\n")
        fp.close()
        return keyword
"""
crldriver = crldriver(headless = True)
p = preprocessor()
packet = crldriver.gettitle(["decenter", "coindeskkorea"])
#"bitman", "cobak", "coinpan", 
for m in packet.keys():
    for n in packet[m]:
        print(p.keywording(n))"""