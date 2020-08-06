class webtypeException(Exception):
    def __init__(self):
        super().__init__('properties.json -> Undifined web type')
        
class datecheckException(Exception):
    def __init__(self):
        super().__init__('date crawling Error')

class indexException(Exception):
    def __init__(self):
        super().__init__('length of title/date list is different')

class paginationException(Exception):
    def __init__(self):
        super().__init__('Could not find available xpath: innerHTML in xpath link (properties.json -> attribute : pagination -> link) should be pagenum')

class programmingException(Exception):
    def __init__(self):
        super().__init__('pagination working by Xpath Link needs "webdriver" parameter in function')

class scrollException(Exception):
    def __init__(self):
        super().__init__('scroll Error')

class NullException(Exception):
    def __init__(self):
        super().__init__()