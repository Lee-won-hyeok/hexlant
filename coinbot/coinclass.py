"""
class bithumb:
    def __init__(self):
        self.url = 'https://www.bithumb.com/'
    
    def getnotice(self):
        self.soup = getsoup(self.url)
        self.notice = self.soup.find_all('a', {'href': re.compile("https://cafe.bithumb.com/view/board-contents/[0-9]+")}, {'rel' : "noopener noreferrer"})
        self.notice_history = []
        del self.notice[:7]
        del self.notice[2:]
        tmp = 0
        while(tmp < len(self.notice)):
            self.notice[tmp] = self.notice[tmp].text
            tmp += 1
"""