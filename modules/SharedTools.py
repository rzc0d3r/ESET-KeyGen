from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver import Edge, EdgeOptions, EdgeService
from selenium.webdriver import Safari, SafariOptions, SafariService

import subprocess
import traceback
import colorama
import logging
import random
import string
import shutil
import time
import sys
import os
import re

I_AM_EXECUTABLE = (True if (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) else False)
PATH_TO_SELF = sys.executable if I_AM_EXECUTABLE else __file__
SILENT_MODE = '--silent' in sys.argv

DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1
GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
GET_EBTN = 'document.getElementsByTagName'
GET_EBAV = 'getElementByAttrValue'
CLICK_WITH_BOOL = 'clickWithBool'
DEFINE_GET_EBAV_FUNCTION = """
function getElementByAttrValue(tagName, attrName, attrValue, index=1) {
    let eindex = 0
    let elements = []
    for (let element of document.getElementsByTagName(tagName)) {
        if(element.getAttribute(attrName) === attrValue) {
            eindex += 1
            if (index == -1)
                elements.push(element)
            else if (index == eindex)
                return element } } 
    if (index == -1)    
        return elements }"""
DEFINE_CLICK_WITH_BOOL_FUNCTION = """
function clickWithBool(object) {
    try {
        object.click()
        return true }
    catch {
        return false } }"""

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

def console_log(text='', logger_type=None, fill_text=None, silent_mode=False):
    if silent_mode:
        return
    if isinstance(logger_type, LoggerType):
        ni = 0
        for i in range(0, len(text)):
            if text[i] != '\n':
                ni = i
                break
            print()
        if fill_text is None:
            fill_text = logger_type.fill_text
        if fill_text:
            print(logger_type.data + ' ' + logger_type.color + text[ni:] + colorama.Style.RESET_ALL)
        else:
            print(logger_type.data + ' ' + text[ni:])
    else:
        print(text)

from .WebDriverInstaller import GOOGLE_CHROME, MICROSOFT_EDGE, MOZILLA_FIREFOX, APPLE_SAFARI

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
        data = [ # 1 uppercase & lowercase letter, 1 number, 1 special character
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("""!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~""")
        ]
        characters = string.ascii_letters + string.digits + string.punctuation
        data += [random.choice(characters) for _ in range(length-3)]
        random.shuffle(data)
    return ''.join(data)

def initSeleniumWebDriver(browser_name: str, webdriver_path = None, browser_path = '', headless=True):
    if browser_path is None:
        browser_path = ''
    logging.info('-- Browsers Initializer --')
    console_log(f'{colorama.Fore.LIGHTMAGENTA_EX}-- Browsers Initializer --{colorama.Fore.RESET}\n', silent_mode=SILENT_MODE)
    if os.name == 'posix': # For Linux
        if sys.platform.startswith('linux'):
            logging.info(f'Initializing {browser_name} for Linux')
            console_log(f'Initializing {browser_name} for Linux', INFO, silent_mode=SILENT_MODE)
        elif sys.platform == "darwin":
            logging.info(f'Initializing {browser_name} for macOS')
            console_log(f'Initializing {browser_name} for macOS', INFO, silent_mode=SILENT_MODE)
    elif os.name == 'nt':
        logging.info(f'Initializing {browser_name} for Windows')
        console_log(f'Initializing {browser_name} for Windows', INFO, silent_mode=SILENT_MODE)
    driver_options = None
    driver = None
    if browser_name == GOOGLE_CHROME:
        driver_options = ChromeOptions()
        driver_options.binary_location = browser_path
        driver_options.debugger_address = ''
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_options.add_argument("--lang=en-US")
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        try:
            service = ChromeService(executable_path=webdriver_path)
            if os.name == 'nt' and headless:
                service.creation_flags = 0x08000000 # CREATE_NO_WINDOW (Process Creation Flags, WinBase.h) -> 'DevTools listening on' is not visible!!!
            driver = Chrome(options=driver_options, service=service)
        except Exception as e:
            logging.critical("EXC_INFO:", exc_info=True)
            if traceback.format_exc().find('only supports') != -1: # Fix for downloaded chrome update
                browser_path = traceback.format_exc().split('path')[-1].split('Stacktrace')[0].strip()
                if 'new_chrome.exe' in os.listdir(browser_path[:-10]):
                    logging.info('Downloaded Google Chrome update is detected! Using new chrome executable file!')
                    console_log('Downloaded Google Chrome update is detected! Using new chrome executable file!', INFO, silent_mode=SILENT_MODE)
                    browser_path = browser_path[:-10]+'new_chrome.exe'
                    driver_options.binary_location = browser_path
                    driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
            else:
                raise e
    elif browser_name == MICROSOFT_EDGE:
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
        service = EdgeService(executable_path=webdriver_path)
        if os.name == 'nt' and headless:
            service.creation_flags = 0x08000000 # CREATE_NO_WINDOW (Process Creation Flags, WinBase.h) -> 'DevTools listening on' is not visible!!!
        try:
            driver = Edge(options=driver_options, service=service)
        except Exception as e:
            logging.critical("EXC_INFO:", exc_info=True)
            if traceback.format_exc().find('--user-data-dir') != -1: # Fix for probably user data directory is already in use
                driver_options.add_argument("--user-data-dir=./edge_tmp")
                try:
                    shutil.rmtree("edge_tmp")
                except:
                    pass
                os.makedirs('edge_tmp', exist_ok=True)
                driver = Edge(options=driver_options, service=EdgeService(executable_path=webdriver_path))
            else:
                raise e
    elif browser_name == MOZILLA_FIREFOX:
        driver_options = FirefoxOptions()
        if browser_path.strip() != '':
            driver_options.binary_location = browser_path
        driver_options.set_preference('intl.accept_languages', 'en-US')
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument("--disable-dev-shm-usage")
        service = FirefoxService(executable_path=webdriver_path)
        if os.name == 'nt' and headless:
            service.creation_flags = 0x08000000 # CREATE_NO_WINDOW (Process Creation Flags, WinBase.h) -> 'DevTools listening on' is not visible!!!
        # Fix for: Your firefox profile cannot be loaded. it may be missing or inaccessible
        os.makedirs('firefox_tmp', exist_ok=True)
        os.environ['TMPDIR'] = (os.getcwd()+'/firefox_tmp').replace('\\', '/')
        driver = Firefox(options=driver_options, service=service)
    elif browser_name == APPLE_SAFARI:
        driver_options = SafariOptions()
        try:
            if os.name == 'nt':
                console_log('Apple Safari is not supported on Windows!!!', ERROR)
                return None
            elif os.name == 'posix' and sys.platform.startswith('linux'):
                console_log('Apple Safari is not supported on Linux!!!', ERROR)
                return None
            driver = Safari(options=driver_options, service=SafariService(executable_path=webdriver_path))
        except Exception as e:
            logging.critical("EXC_INFO:", exc_info=True)
            if traceback.format_exc().find("Allow Remote Automation") != -1:
                console_log(traceback.format_exc().split('Message: ')[-1].strip(), ERROR)
            else:
                raise e
    return driver

def parseToken(email_obj, driver=None, eset_business=False, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
    activated_href = None
    if email_obj.class_name == 'custom':
        while True:
            activated_href = input(f'\n[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Enter the link to activate your account, it will come to the email address you provide: {colorama.Fore.RESET}').strip()
            logging.info(f'[  INPT  ] Enter the link to activate your account, it will come to the email address you provide: {activated_href}')
            if activated_href != '':
                if eset_business:
                    match = re.search(r'activation\/[a-zA-Z0-9-]+', activated_href)
                else:
                    match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
                if match is not None:
                    if eset_business:
                        token = match.group()[11:]
                    else:
                        token = match.group()[6:]
                    if len(token) == 36:
                        return token
            logging.error('Incorrect link syntax')
            console_log('Incorrect link syntax', ERROR)
    for _ in range(max_iter):
        if email_obj.class_name == '1secmail':
            json = email_obj.read_email()
            if json != []:
                for message in json:
                    if eset_business and message['subject'].find('ESET PROTECT Hub') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
                    elif message['from'].find('product.eset.com') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
        elif email_obj.class_name in ['developermail', 'inboxes']:
            messages = email_obj.get_messages()
            if messages is not None:
                for message in messages:
                    if eset_business and message['subject'].find('ESET PROTECT Hub') != -1:
                        activated_href = message['body']
                    elif message['from'].find('product.eset.com') != -1:
                        activated_href = message['body']
        elif email_obj.class_name in ['guerrillamail', 'mailticking', 'fakemail', 'incognitomail']:
            inbox = email_obj.parse_inbox()
            for mail in inbox:
                mail_id, mail_from, mail_subject = mail
                if mail_from.find('product.eset.com') != -1 or mail_from.find('ESET HOME') != -1 or mail_subject.find('ESET PROTECT Hub') != -1:
                    email_obj.open_mail(mail_id)
                    if email_obj.class_name in ['mailticking', 'incognitomail']:
                        time.sleep(1.5)
                    try:
                        if eset_business:
                            activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://protecthub.eset.com')]").get_attribute('href') 
                        else:
                            activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
                    except:
                        pass
        if activated_href is not None:
            if eset_business:
                match = re.search(r'activation\/[a-zA-Z0-9-]+', activated_href)
            else:
                match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
            if match is not None:
                if eset_business:
                    token = match.group()[11:]
                else:
                    token = match.group()[6:]
                if len(token) == 36:
                    return token
        time.sleep(delay)
    raise RuntimeError('Token retrieval error, try again later or change the Email API!!!')

def parseEPHKey(email_obj, driver=None, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
    for _ in range(max_iter):
        license_data = None
        if email_obj.class_name in ['developermail', 'inboxes']:
            messages = email_obj.get_messages()
            if messages is not None:
                for message in messages:
                    if message['subject'].find('Thank you for purchasing') != -1:
                        license_data = message['body']
                        break
        elif email_obj.class_name in ['mailticking', 'fakemail', 'incognitomail']:
            inbox = email_obj.parse_inbox()
            for mail in inbox:
                mail_id, mail_from, mail_subject = mail
                if mail_subject.find('Thank you for purchasing') != -1:
                    email_obj.open_mail(mail_id)
                    time.sleep(3)
                    license_data = email_obj.driver.page_source
                    break
        if license_data is not None:
            license_data = str(license_data)
            license_key = re.search(r'([A-Z0-9]){4}-([A-Z0-9]){4}-([A-Z0-9]){4}-([A-Z0-9]){4}-([A-Z0-9]){4}', license_data).group()
            license_id = re.search(r'[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{3}', license_data).group()
            license_out_date = re.findall(r'\d\d.\d\d.\d\d\d\d', license_data)[-1]
            return license_key, license_out_date, license_id
        time.sleep(delay)
    raise RuntimeError('ESET ProtectHub data waiting time has been exceeded!!!')

def parseVPNCodes(email_obj, driver=None, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
    for _ in range(max_iter):
        data = None
        if email_obj.class_name == '1secmail':
            json = email_obj.read_email()
            if json != []:
                for message in json:
                    if message['subject'].find('VPN - Setup instructions') != -1:
                        data = email_obj.get_message(message['id'])['body']
        elif email_obj.class_name in ['developermail', 'inboxes']:
            messages = email_obj.get_messages()
            if messages is not None:
                for message in messages:
                    if message['subject'].find('VPN - Setup instructions') != -1:
                        data = message['body']
        elif email_obj.class_name in ['guerrillamail', 'mailticking', 'fakemail', 'incognitomail']:
            inbox = email_obj.parse_inbox()
            for mail in inbox:
                mail_id, mail_from, mail_subject = mail
                if mail_subject.find('VPN - Setup instructions') != -1:
                    email_obj.open_mail(mail_id)
                    if email_obj.class_name == 'mailticking':
                        time.sleep(1.5)
                        try:
                            data = str(driver.execute_script(f'return {GET_EBCN}("email-content")[0].innerHTML'))
                        except:
                            pass
                    elif email_obj.class_name == 'guerrillamail':
                        try:
                            data = str(driver.execute_script(f'return {GET_EBCN}("email_body")[0].innerHTML'))
                        except:
                            pass
                    elif email_obj.class_name == 'incognitomail':
                        time.sleep(1.5)
                        try:
                            data = str(driver.execute_script(f'return {GET_EBCN}("MuiBox-root joy-1v8x7dw")[0].innerHTML'))
                        except:
                            pass
                    else:
                        data = driver.page_source
        if data is not None:
            match = re.findall(r'[A-Z0-9]{10}', data)
            if match is not None and len(match) == 10:
                return match
        time.sleep(delay)
    raise RuntimeError('VPN Codes retrieval error, try again later or change the Email API!!!')

class Installer:
    def __init__(self):
        self.install_path = None
        self.executable_path = None
        if sys.platform.startswith('win'):
            self.install_path = os.environ['SystemRoot']
            self.executable_path = self.install_path + '\\esetkeygen.exe'
        elif sys.platform == "darwin":
            self.install_path = '/usr/local/bin'
            self.executable_path = self.install_path + '/esetkeygen'

    def check_install(self):
        exit_code = None
        try:
            exit_code = subprocess.call([self.executable_path, '--return-exit-code', '999'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
        return (exit_code == 999)
    
    def install(self):
        if self.check_install():
            logging.info('The program is already installed!!!')
            logging.warning(f'Location: {self.executable_path}')
            console_log('The program is already installed!!!', OK, silent_mode=SILENT_MODE)
            console_log(f'Location: {self.executable_path}', WARN, silent_mode=SILENT_MODE)
            return True
        if sys.platform.startswith('win') or sys.platform == 'darwin':
            if I_AM_EXECUTABLE:
                try:
                    shutil.copy2(PATH_TO_SELF, self.executable_path)
                    logging.info(f'The program was successfully installed on the path: {self.executable_path}')
                    console_log(f'The program was successfully installed on the path: {self.executable_path}', OK, silent_mode=SILENT_MODE)
                    return True
                except PermissionError:
                    logging.error('No write access, try running the program with elevated permissions!!!')
                    console_log('No write access, try running the program with elevated permissions!!!', ERROR, silent_mode=SILENT_MODE)
                except Exception as e:
                    raise RuntimeError(e)
                except shutil.SameFileError:
                    logging.error('Installation is pointless from under an installed executable file!!!')
                    console_log('Installation is pointless from under an installed executable file!!!', ERROR, silent_mode=SILENT_MODE)
            else:
                logging.error('Installation from source is not possible!!!!')
                console_log('Installation from source is not possible!!!!', ERROR, silent_mode=SILENT_MODE)
            return False
