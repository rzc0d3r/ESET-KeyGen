from .SharedTools import *

from email import policy, parser

import colorama
import requests
import time
import sys

class OneSecEmailAPI(object):
    def __init__(self):
        self.class_name = '1secmail'
        self.__login = None
        self.__domain = None
        self.email = None
        self.__api = 'https://www.1secmail.com/api/v1/'
        
    def init(self):
        url = f'{self.__api}?action=genRandomMailbox&count=1'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        self.__login, self.__domain = str(r.content, 'utf-8')[2:-2].split('@')
        self.email = self.__login+'@'+self.__domain
    
    def login(self, login, domain):
        self.__login = login
        self.__domain = domain
    
    def read_email(self):
        url = f'{self.__api}?action=getMessages&login={self.__login}&domain={self.__domain}'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        return r.json()
    
    def get_message(self, message_id):
        url = f'{self.__api}?action=readMessage&login={self.__login}&domain={self.__domain}&id={message_id}'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        return r.json()

class DeveloperMailAPI(object):
    def __init__(self):
        self.class_name = 'developermail'
        self.email = ''
        self.email_name = ''
        self.headers = {}
        self.api_url = 'https://www.developermail.com/api/v1'
    
    def init(self):
        r = requests.put(f'{self.api_url}/mailbox')
        self.email_name, token = list(r.json()['result'].values())
        self.email = self.email_name+'@developermail.com'
        self.headers = {'X-MailboxToken': token}

    def __parse_message(self, raw_message_body):
        message_bytes = raw_message_body.encode('utf-8')
        msg = parser.BytesParser(policy=policy.default).parsebytes(message_bytes)
        message_subject = msg['subject']
        message_from = msg['from']
        message_body = str(msg.get_payload(decode=True).decode(msg.get_content_charset())) # decoding MIME-Type to html
        return {'subject':message_subject, 'from':message_from, 'body':message_body}

    def get_messages(self):
        # get message IDs
        r = requests.get(
            f'{self.api_url}/mailbox/{self.email_name}',
            headers=self.headers
        )
        message_ids = r.json()['result']
        if message_ids == []:
            return None
        # parse messages
        messages = []
        for message_id in message_ids:
            r = requests.get(f'{self.api_url}/mailbox/{self.email_name}/messages/{message_id}', headers=self.headers)
            raw_message_body = r.json()['result']
            messages.append(self.__parse_message(raw_message_body))
        if messages == []:
            messages = None
        return messages

class Hi2inAPI(object):
    def __init__(self, driver):
        self.class_name = 'hi2in'
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):
        #self.driver.execute_script('window.open("https://hi2.in/#/", "_blank")')
        #if args['try_auto_cloudflare']:
        #    console_log(f'Attempting to pass cloudflare captcha automatically...', INFO)
        #    time.sleep(8)
        #else:
        #    console_log(f'{Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{Fore.RESET}', INFO, False)
        #    input(f'[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Press Enter when you see the hi2in page...{Fore.RESET}')
        #self.driver.switch_to.window(self.driver.window_handles[0])
        #self.driver.close()
        #self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://hi2.in/#/")
        self.window_handle = self.driver.current_window_handle
        #if args['try_auto_cloudflare']:
        #    try:
        #        self.driver.execute_script(f'{GET_EBCN}("mailtext mailtextfix")[0]')
        #        console_log('Successfully passed сloudflare captcha in automatic mode!!!', OK)
        #    except:
        #        console_log('Failed to pass сloudflare captcha in automatic mode!!!', ERROR)
        #        time.sleep(3) # exit-delay
        #        sys.exit(-1)
        untilConditionExecute(
            self.driver,
            f'return ({GET_EBCN}("mailtext mailtextfix")[0] !== null && {GET_EBCN}("mailtext mailtextfix")[0].value !== "")'
        )
        self.email = self.driver.execute_script(f'return {GET_EBCN}("mailtext mailtextfix")[0].value')
        # change domain to @telegmail.com
        if self.email.find('@telegmail.com') == -1:
            while True:
                self.email = self.driver.execute_script(f'return {GET_EBCN}("mailtext mailtextfix")[0].value')
                if self.email.find('@telegmail.com') != -1:
                    break
                self.driver.execute_script(f"{GET_EBCN}('genbutton')[0].click()")
                time.sleep(1.5)
    
    def open_inbox(self):
        self.driver.switch_to.window(self.window_handle)

class TenMinuteMailAPI(object):
    def __init__(self, driver: Chrome):
        self.class_name = '10minutemail'
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):     
        self.driver.get('https://10minutemail.net/new.html?lang=en')
        self.window_handle = self.driver.current_window_handle
        untilConditionExecute(self.driver, f'return {GET_EBID}("fe_text") != null')
        self.email = self.driver.execute_script(f'return {GET_EBID}("fe_text").value')
    
    def parse_inbox(self):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get('https://10minutemail.net/?lang=en')
        inbox = self.driver.execute_script('\n'.join([DEFINE_PARSE_10MINUTEMAIL_INBOX_FUNCTION, 'return '+PARSE_10MINUTEMAIL_INBOX]))
        return inbox

    def open_mail(self, id):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get(id)

class GuerRillaMailAPI(object):
    def __init__(self, driver: Chrome):
        self.class_name = 'guerrillamail'
        self.driver = driver
        self.email = None
        self.window_handle = None

    def init(self):     
        self.driver.get('https://www.guerrillamail.com/')
        self.window_handle = self.driver.current_window_handle
        untilConditionExecute(self.driver, f'return {GET_EBID}("email-widget") != null')
        self.email = self.driver.execute_script(f'return {GET_EBID}("email-widget").innerText')
        # change to random available domain
        self.email = self.email.split('@')[0]+'@'+random.choice(self.driver.execute_script(GET_GUERRILLAMAIL_DOMAINS))
    
    def parse_inbox(self):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get('https://www.guerrillamail.com/')
        inbox = self.driver.execute_script(PARSE_GUERRILLAMAIL_INBOX)
        return inbox

    def open_mail(self, id):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get(f'https://www.guerrillamail.com/inbox?mail_id={id}')

class TempMailAPI(object):
    def __init__(self, driver=None):
        self.class_name = 'tempmail'
        self.driver = driver
        self.token = ""
        self.email = ""
        self.window_handle = None
        #self.try_auto_cloudflare = try_auto_cloudflare

    def init(self):
        self.driver.execute_script('window.open("https://temp-mail.org", "_blank")')
        #if self.try_auto_cloudflare:
        #    console_log(f'Attempting to pass cloudflare captcha automatically...', INFO)
        #    time.sleep(8)
        #else:
        console_log(f'{colorama.Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{colorama.Fore.RESET}', INFO, False)
        input(f'[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Press Enter when you see the TempMail page...{colorama.Fore.RESET}')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.window_handle = self.driver.current_window_handle
        #if self.try_auto_cloudflare:
        #    try:
        #        self.driver.execute_script(f"return {GET_EBID}('mail').value")
        #        console_log('Successfully passed сloudflare captcha in automatic mode!!!', OK)
        #    except:
        #        console_log('Failed to pass сloudflare captcha in automatic mode!!!', ERROR)
        #        time.sleep(3) # exit-delay
        #        sys.exit(-1)
        for _ in range(DEFAULT_MAX_ITER):
            self.email = self.driver.execute_script(f"return {GET_EBID}('mail').value")
            if self.email == '':
                raise RuntimeError('TempMailAPI: Your IP is blocked, try again later or try use VPN!')
            elif self.email.find('@') != -1:
                break
            time.sleep(DEFAULT_DELAY)
    
    def auth(self):
        if self.token != "":
            return True
        self.driver.switch_to.window(self.window_handle)
        for _ in range(DEFAULT_MAX_ITER):
            try:
                self.token = self.driver.get_cookie('token')['value']
                return True
            except:
                time.sleep(1)
        raise RuntimeError('TempMailAPI: Error during authorization!')

    def get_messages(self):
        try:
            self.driver.switch_to.window(self.window_handle)
            return self.driver.execute_script(f"""
                var req = new XMLHttpRequest()
                req.open("GET", "https://web2.temp-mail.org/messages", false)
                req.setRequestHeader("Authorization", "Bearer {self.token}")
                req.send(null)
                return JSON.parse(req.response)
            """)["messages"]
        except Exception as E:
            return None

    def get_message(self, message_id):
        try:
            self.driver.switch_to.window(self.window_handle)
            return self.driver.execute_script(f"""
                var req = new XMLHttpRequest()
                req.open("GET", "https://web2.temp-mail.org/messages/{message_id}", false)
                req.setRequestHeader("Authorization", "Bearer {self.token}")
                req.send(null)
                return JSON.parse(req.response)
            """)
        except:
            return None

class CustomEmailAPI(object):
    def __init__(self):
        self.class_name = 'custom'
        self.email = None