import requests

class SecEmailConnectError(Exception):
    pass

class SecEmail:
    def __init__(self):
        self.__login = None
        self.__domain = None
        self.__api = 'https://www.1secmail.com/api/v1/'
        
    def register(self):
        url = f'{self.__api}?action=genRandomMailbox&count=1'
        try:
            r = requests.get(url)
        except:
            raise SecEmailConnectError
        if r.status_code != 200:
            raise SecEmailConnectError
        self.__login, self.__domain = str(r.content, 'utf-8')[2:-2].split('@')
    
    def login(self, login, domain):
        self.__login = login
        self.__domain = domain
    
    def get_full_login(self):
        return self.__login+'@'+self.__domain
        
    def read_email(self):
        url = f'{self.__api}?action=getMessages&login={self.__login}&domain={self.__domain}'
        try:
            r = requests.get(url)
        except:
            raise SecEmailConnectError
        if r.status_code != 200:
            raise SecEmailConnectError
        return r.json()
    
    def get_message(self, message_id):
        url = f'{self.__api}?action=readMessage&login={self.__login}&domain={self.__domain}&id={message_id}'
        try:
            r = requests.get(url)
        except:
            raise SecEmailConnectError
        if r.status_code != 200:
            raise SecEmailConnectError
        return r.json()