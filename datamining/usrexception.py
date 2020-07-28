class webtypeException(Exception):
    def __init__(self):
        super().__init__('properties.json -> Undifined web type')
        
class datecheckException(Exception):
    def __init__(self):
        super().__init__('date crawling Error')

class indexException(Exception):
    def __init__(self):
        super().__init__('length of title/date list is different')