class InvalidEncriptionKey(Exception):
    '''
    Encryption Key accepts a-z, A-Z and 0-9
    '''
    def __init__(self):
        self.message = 'Encryption Key accepts a-z, A-Z and 0-9'
        super().__init__(self.message)


    def __str__(self) -> str:
        return f'''{self.__class__.__name__}:{self.message}'''