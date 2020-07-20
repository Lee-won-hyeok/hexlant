class timeoutException(Exception):
    def __init__(self):
        super().__init__('Url load: TimeoutError')