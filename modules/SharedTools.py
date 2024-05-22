from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver import Edge, EdgeOptions, EdgeService

import traceback
import colorama
import random
import string
import time
import sys
import os
import re

DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1
GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
GET_EBTN = 'document.getElementByTagName'
GET_EBAV = 'getElementByAttrValue'
CLICK_WITH_BOOL = 'clickWithBool'
PARSE_10MINUTEMAIL_INBOX = 'parse_10minutemail_inbox()'
DEFINE_GET_EBAV_FUNCTION = """
function getElementByAttrValue(tagName, attrName, attrValue) {
    for (let element of document.getElementsByTagName(tagName)) {
        if(element.getAttribute(attrName) === attrValue)
            return element } }"""
DEFINE_CLICK_WITH_BOOL_FUNCTION = """
function clickWithBool(object) {
    try {
        object.click()
        return true }
    catch {
        return false } }"""
DEFINE_PARSE_10MINUTEMAIL_INBOX_FUNCTION = """function parse_10minutemail_inbox() {
    updatemailbox()
    let mails = Array.from(document.getElementsByTagName('tr')).slice(1)
    let inbox = []
    for(let i=0; i < mails.length; i++) {
        let id = mails[i].children[0].children[0].href
        let from = mails[i].children[0].innerText
        let subject = mails[i].children[1].innerText
        inbox.push([id, from, subject]) }
    return inbox }"""
PARSE_GUERRILLAMAIL_INBOX = """
var email_list = document.getElementById('email_list').children
var inbox = []
for(var i=0; i < email_list.length-1; i++) {
    var mail = email_list[i].children
    var from = mail[1].innerText
    var subject = mail[2].innerText
    var mail_id = mail[0].children[0].value
    inbox.push([mail_id, from, subject])
}
return inbox
"""
GET_GUERRILLAMAIL_DOMAINS = """
var domains_options = document.getElementById('gm-host-select').options
var domains = [] 
for(var i=0; i < domains_options.length-1; i++) {
    domains.push(domains_options[i].value)
}
return domains
"""

colorama.init()

class LoggerType:
    def __init__(self, sborder, eborder, title, color, fill_text):
        self.sborder = sborder
        self.eborder = eborder
        self.title = title
        self.color = color
        self.fill_text = fill_text

    @property
    def data(self):
        return self.sborder + self.color + self.title + colorama.Style.RESET_ALL + self.eborder

ERROR = LoggerType('[ ', ' ]', 'FAILED', colorama.Fore.RED, True)
OK = LoggerType('[   ', '   ]', 'OK', colorama.Fore.GREEN, False)
INFO = LoggerType('[  ', '  ]', 'INFO', colorama.Fore.LIGHTBLACK_EX, True)
DEVINFO = LoggerType('[ ', ' ]', 'DEBUG', colorama.Fore.CYAN, True)
WARN = LoggerType('[  ', '  ]', 'WARN', colorama.Fore.YELLOW, False)

def console_log(text='', logger_type=None, fill_text=None):
    if isinstance(logger_type, LoggerType):
        ni = 0
        for i in range(0, len(text)):
            if text[i] != '\n':
                ni = i
                break
            print()
        if logger_type.fill_text and fill_text is None:
            fill_text = True
        if logger_type.fill_text and fill_text:
            print(logger_type.data + ' ' + logger_type.color + text[ni:] + colorama.Style.RESET_ALL)
        else:
            print(logger_type.data + ' ' + text[ni:])
    else:
        print(text)

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def untilConditionExecute(driver_obj, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True, raise_exception_if_failed=True, return_js_result=False):
    driver_obj.execute_script(f'window.{GET_EBAV} = {DEFINE_GET_EBAV_FUNCTION}')
    driver_obj.execute_script(f'window.{CLICK_WITH_BOOL} = {DEFINE_CLICK_WITH_BOOL_FUNCTION}')
    pre_js = [
        DEFINE_GET_EBAV_FUNCTION,
        DEFINE_CLICK_WITH_BOOL_FUNCTION
    ]
    js = '\n'.join(pre_js+[js])
    for _ in range(max_iter):
        try:
            result = driver_obj.execute_script(js)
            if return_js_result and result is not None:
                return result
            elif result == positive_result:
                return True
        except Exception as E:
            pass
        time.sleep(delay)
    if raise_exception_if_failed:
        raise RuntimeError('untilConditionExecute: the code did not return the desired value! TRY VPN!')

def dataGenerator(length, only_numbers=False):
    """generates a password by default. If only_numbers=True - phone number"""
    data = []
    if only_numbers: # phone number
        data = [random.choice(string.digits) for _ in range(length)]
    else: # password
        length += random.randint(1, 10)
        data = [ # 1 uppercase letter, 1 number, 1 special character
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]
        characters = string.ascii_letters + string.digits + string.punctuation
        data += [random.choice(characters) for _ in range(length-3)]
        random.shuffle(data)
    return ''.join(data)

def initSeleniumWebDriver(browser_name: str, webdriver_path = None, browser_path = '', headless=True):
    if os.name == 'posix': # For Linux
        if sys.platform.startswith('linux'):
            console_log(f'Initializing {browser_name}-webdriver for Linux', INFO)
        elif sys.platform == "darwin":
            console_log(f'Initializing {browser_name}-webdriver for macOS', INFO)
    elif os.name == 'nt':
        console_log(f'Initializing {browser_name}-webdriver for Windows', INFO)
    driver_options = None
    driver = None
    if browser_name.lower() == 'chrome':
        driver_options = ChromeOptions()
        driver_options.binary_location = browser_path
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_options.add_argument("--lang=en-US")
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        try:
            driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
        except Exception as E:
            if traceback.format_exc().find('only supports') != -1: # Fix for downloaded chrome update
                browser_path = traceback.format_exc().split('path')[-1].split('Stacktrace')[0].strip()
                if 'new_chrome.exe' in os.listdir(browser_path[:-10]):
                    console_log('Downloaded Google Chrome update is detected! Using new chrome executable file!', INFO)
                    browser_path = browser_path[:-10]+'new_chrome.exe'
                    driver_options.binary_location = browser_path
                    driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
            else:
                raise E
    elif browser_name.lower() == 'firefox':
        driver_options = FirefoxOptions()
        driver_options.binary_location = browser_path
        driver_options.set_preference('intl.accept_languages', 'en-US')
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument("--disable-dev-shm-usage")
        # Fix for: Your firefox profile cannot be loaded. it may be missing or inaccessible
        try:
            os.makedirs('firefox_tmp')
        except:
            pass
        os.environ['TMPDIR'] = (os.getcwd()+'/firefox_tmp').replace('\\', '/')
        driver = Firefox(options=driver_options, service=FirefoxService(executable_path=webdriver_path))
    elif browser_name.lower() == 'edge':
        driver_options = EdgeOptions()
        driver_options.use_chromium = True
        driver_options.binary_location = browser_path
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_options.add_argument("--lang=en-US")
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        driver = Edge(options=driver_options, service=EdgeService(executable_path=webdriver_path))
    #driver.set_window_position(0, 0)
    #driver.set_window_size(640, 640)
    return driver

def parseToken(email_obj, driver=None, eset_business=False, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
    activated_href = None
    if email_obj.class_name == 'custom':
        while True:
            activated_href = input(f'\n[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Enter the link to activate your account, it will come to the email address you provide: {colorama.Fore.RESET}').strip()
            if activated_href is not None:
                match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
                if match is not None:
                    token = match.group()[6:]
                    if len(token) == 36:
                        return token
            console_log('Incorrect link syntax', ERROR)
    for _ in range(max_iter):
        if email_obj.class_name == '1secmail':
            json = email_obj.read_email()
            if json != []:
                message = json[-1]
                if eset_business and message['subject'].find('activation') != -1:
                    activated_href = email_obj.get_message(message['id'])['body']
                elif message['from'].find('product.eset.com') != -1:
                    activated_href = email_obj.get_message(message['id'])['body']
        elif email_obj.class_name == 'developermail':
            messages = email_obj.get_messages()
            if messages is not None:
                message = messages[-1]
                if eset_business and message['subject'].find('activation') != -1:
                    activated_href = message['body']
                elif message['from'].find('product.eset.com') != -1:
                    activated_href = message['body']
        elif email_obj.class_name == 'hi2in':
            email_obj.open_inbox()
            try:
                if eset_business:
                    activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://eba.eset.com')]").get_attribute('href')
                else:
                    activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
            except:
                pass
        elif email_obj.class_name in ['guerrillamail', '10minutemail']:
            inbox = email_obj.parse_inbox()
            for mail in inbox:
                mail_id, mail_from, mail_subject = mail
                if mail_from.find('product.eset.com') != -1 or mail_subject.find('activation') != -1:
                    email_obj.open_mail(mail_id)
                    try:
                        if eset_business:
                            activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://eba.eset.com')]").get_attribute('href') 
                        else:
                            activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
                    except:
                        pass
        elif email_obj.class_name == 'tempmail':
            email_obj.auth()
            messages = email_obj.get_messages()
            try:
                for message in messages:
                    if message["from"].find("product.eset.com") != -1 or message["subject"].find("activation") != -1:
                        activated_href = email_obj.get_message(message["_id"])["bodyHtml"]
            except:
                pass
        if activated_href is not None:
            match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
            if match is not None:
                token = match.group()[6:]
                return token
        time.sleep(delay)
    raise RuntimeError('Token retrieval error!!!')
