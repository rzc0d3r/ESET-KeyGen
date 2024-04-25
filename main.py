from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver import Edge, EdgeOptions, EdgeService

from site_packages.pyperclip import paste as get_clipboard_text

import subprocess
import traceback
import platform
import datetime
import argparse
import requests
import zipfile
import shutil
import random
import string
import time
import sys
import os
import re

LOGO = """
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                Project Version: v1.4.4.1
                                                Project Devs: rzc0d3r, AdityaGarg8, k0re,
                                                              Fasjeit, alejanpa17, Ischunddu,
                                                              soladify, AngryBonk, Xoncia
"""
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

from colorama import Fore, Style, init

init()

class LoggerType:
    def __init__(self, sborder, eborder, title, color, fill_text):
        self.sborder = sborder
        self.eborder = eborder
        self.title = title
        self.color = color
        self.fill_text = fill_text

    @property
    def data(self):
        return self.sborder + self.color + self.title + Style.RESET_ALL + self.eborder

ERROR = LoggerType('[ ', ' ]', 'FAILED', Fore.RED, True)
OK = LoggerType('[   ', '   ]', 'OK', Fore.GREEN, False)
INFO = LoggerType('[  ', '  ]', 'INFO', Fore.LIGHTBLACK_EX, True)
DEVINFO = LoggerType('[ ', ' ]', 'DEBUG', Fore.CYAN, True)

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
            print(logger_type.data + ' ' + logger_type.color + text[ni:] + Style.RESET_ALL)
        else:
            print(logger_type.data + ' ' + text[ni:])
    else:
        print(text)

class SecEmailAPI(object):
    def __init__(self):
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

class Hi2inAPI(object):
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):
        self.driver.execute_script('window.open("https://hi2.in/#/", "_blank")')
        console_log(f'{Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{Fore.RESET}', INFO, False)
        input(f'[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Press Enter when you see the hi2in page...{Fore.RESET}')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.window_handle = self.driver.current_window_handle
        SharedTools.untilConditionExecute(
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
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):     
        self.driver.get('https://10minutemail.net/new.html?lang=en')
        self.window_handle = self.driver.current_window_handle
        SharedTools.untilConditionExecute(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBCN}("fc-button fc-cta-consent fc-primary-button")[0])')
        SharedTools.untilConditionExecute(self.driver, f'return fe_text !== null')
        self.email = self.driver.execute_script('return fe_text.value')
    
    def parse_inbox(self):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get('https://10minutemail.net/?lang=en')
        inbox = self.driver.execute_script('\n'.join([DEFINE_PARSE_10MINUTEMAIL_INBOX_FUNCTION, 'return '+PARSE_10MINUTEMAIL_INBOX]))
        return inbox

    def open_mail(self, id):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get(id)

class TempMailAPI(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.token = ""
        self.email = ""
        self.window_handle = None

    def init(self):
        self.driver.execute_script('window.open("https://temp-mail.org", "_blank")')
        console_log(f'{Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{Fore.RESET}', INFO, False)
        input(f'[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Press Enter when you see the TempMail page...{Fore.RESET}')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.window_handle = self.driver.current_window_handle
        self.driver: Chrome
        for _ in range(DEFAULT_MAX_ITER//2):
            copy_email_address_button = self.driver.find_element('xpath', "//button[starts-with(@data-clipboard-target, '#mail')]")
            if copy_email_address_button.is_enabled():
                copy_email_address_button.click()
                self.email = get_clipboard_text()
                return True
            time.sleep(DEFAULT_DELAY)
        raise RuntimeError('TempMailAPI: Your IP is blocked, try again later or try use VPN!')
    
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
        self.email = None

class SharedTools(object):
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

    def createPassword(length, only_numbers=False):
        if only_numbers:
            return [random.choice(string.digits) for _ in range(length)]
        return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])

    def initSeleniumWebDriver(browser_name: str, webdriver_path = None, browser_path = '', headless=True):
        if os.name == 'posix': # For Linux
            if sys.platform.startswith('linux'):
                console_log('Initializing chrome-webdriver for Linux', INFO)
            elif sys.platform == "darwin":
                console_log('Initializing chrome-webdriver for macOS', INFO)
        elif os.name == 'nt':
            console_log('Initializing chrome-webdriver for Windows', INFO)
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
            driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
        elif browser_name.lower() == 'firefox':
            driver_options = FirefoxOptions()
            driver_options.binary_location = browser_path
            driver_options.set_preference('intl.accept_languages', 'en-US')
            if headless:
                driver_options.add_argument('--headless')
            if os.name == 'posix': # For Linux
                driver_options.add_argument('--no-sandbox')
                driver_options.add_argument("--disable-dev-shm-usage")
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
        if args['custom_email_api']:
            while True:
                activated_href = input(f'\n[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Enter the link to activate your account, it will come to the email address you provide: {Fore.RESET}').strip()
                if activated_href is not None:
                    match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
                    if match is not None:
                        token = match.group()[6:]
                        if len(token) == 36:
                            return token
                console_log('Incorrect link syntax', ERROR)
        for _ in range(max_iter):
            if args['email_api'] == '1secmail':
                json = email_obj.read_email()
                if json != []:
                    message = json[-1]
                    if eset_business and message['subject'].find('activation') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
                    elif message['from'].find('product.eset.com') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
            elif args['email_api'] == 'hi2in':
                email_obj.open_inbox()
                try:
                    if eset_business:
                        activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://eba.eset.com')]").get_attribute('href')
                    else:
                        activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
                except:
                    pass
            elif args['email_api'] == '10minutemail':
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
            elif args['email_api'] == 'tempmail':
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

class WebDriverInstaller(object):
    def __init__(self):
        self.platform = ['', []]
        if sys.platform.startswith('win'):
            self.platform[0] = 'win'
            if sys.maxsize > 2**32:
                self.platform[1] = ['win64', 'win32']
            else:
                self.platform[1] = ['win32']
        elif sys.platform.startswith('linux'):
            self.platform[0] = 'linux'
            if sys.maxsize > 2**32:
                self.platform[1].append('linux64')
            else:
                self.platform[1].append('linux32')
        elif sys.platform == "darwin":
            self.platform[0] = 'mac'
            if processor() == "arm":
                self.platform[1] = ['mac-arm64', 'mac_arm64', 'mac64_m1']
            elif processor() == "i386":
                self.platform[1] = ['mac64', 'mac-x64']
        if self.platform[0] == '' or self.platform[1] == []:
            raise RuntimeError('WebDriverInstaller: impossible to define the system!')
    
    def get_chrome_version(self):
        if self.platform[0] == "linux":
            path = None
            for executable in ("google-chrome", "google-chrome-stable", "google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"):
                path = shutil.which(executable)
                if path is not None:
                    with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
                        chrome_version = proc.stdout.read().decode("utf-8").replace("Chromium", "").replace("Google Chrome", "").strip().split()[0]
        elif self.platform[0] == "mac":
            process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=subprocess.PIPE)
            chrome_version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
        elif self.platform[0] == "win":
            paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\",
                os.environ.get('LOCALAPPDATA')+"\\Google\\Chrome\\Application\\"
            ]
            for path in paths:
                try:
                    with open(path+'chrome.VisualElementsManifest.xml', 'r') as f:
                        for line in f.readlines():
                            line = line.strip()
                            if line.startswith('Square150x150Logo'):
                                chrome_version = line.split('=')[1].split('\\')[0][1:] 
                                break
                except:
                    pass
        if chrome_version is not None:
            chrome_version = [chrome_version]+chrome_version.split('.') # [full, major, _, minor, micro]
        else:
            raise RuntimeError('WebDriverInstaller: google chrome is not detected installed on your device!')
        return chrome_version

    def get_chromedriver_download_url(self, chrome_major_version=None):
        if chrome_major_version is None:
            chrome_major_version = self.get_chrome_version()[1]
        if int(chrome_major_version) >= 115: # for new drivers ( [115.0.0000.0, ...] )
            drivers_data = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
            drivers_data = drivers_data.json()['versions'][::-1] # start with the latest version
            for driver_data in drivers_data:
                driver_version = driver_data['version']
                driver_major_version = driver_version.split('.')[0] # major, _, minor, micro
                if driver_major_version == chrome_major_version: # return latest driver version for current major chrome version
                    for driver_url in driver_data['downloads'].get('chromedriver', None):
                            if driver_url['platform'] in self.platform[1]:
                                return driver_url['url']
        else: # for old drivers ( [..., 115.0.0000.0) )
            latest_old_driver_version = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}'.format(chrome_major_version))
            if latest_old_driver_version.status_code != 200:
                raise RuntimeError('WebDriverInstaller: the required chrome driver was not found!')
            latest_old_driver_version = latest_old_driver_version.text
            driver_url = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_'.format(latest_old_driver_version)
            for arch in self.platform[1]:
                current_driver_url = driver_url+arch+'.zip'
                driver_size = requests.head(current_driver_url).headers.get('x-goog-stored-content-length', None)
                if driver_size is not None and int(driver_size) > 1024**2:
                    return current_driver_url
            raise RuntimeError('WebDriverInstaller: the required chrome driver was not found!')
    
    def download_webdriver(self, path: str, url=None, edge=False): # Only for Google Chrome (default) and Microsoft Edge (edge=True)
        if url is None:
            if edge:
                url = self.get_edgedriver_download_url()
            else:
                url = self.get_chromedriver_download_url()
        zip_path = path.replace('\\', '/')+'/data.zip'
        f = open(zip_path, 'wb')
        f.write(requests.get(url).content)
        f.close()
        if edge:
            webdriver_name = 'msedgedriver' # macOS, linux
        else:
            webdriver_name = 'chromedriver' # macOS, linux
        if self.platform[0].startswith('win'): # windows
            webdriver_name += '.exe'
        with zipfile.ZipFile(zip_path, 'r') as zip:
            webdriver_zip_path = ''
            if not edge:
                if len(zip.namelist()[0].split('/')) > 1: # for new Google Chrome webdriver zip format 
                    webdriver_zip_path = zip.namelist()[0].split('/')[0]+'/'
            with open(path+'/'+webdriver_name, 'wb') as f:
                f.write(zip.read(webdriver_zip_path+webdriver_name))
        try:
            os.remove(zip_path)
        except:
            pass
        return True
    
    def get_edge_version(self): # Only for windows
        cmd = 'powershell -Command "Get-ItemPropertyValue -Path "HKCU:\\SOFTWARE\\Microsoft\\Edge\\BLBeacon" -Name "version""'
        edge_version = None
        try:
            edge_version = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
            edge_version = [edge_version]+edge_version.split('.') # [full, major, _, minor, micro]
        except:
            raise RuntimeError('WebDriverInstaller: microsoft edge is not detected installed on your device!')
        return edge_version

    def get_edgedriver_download_url(self, edge_version=None):
        archs = self.platform[1]
        if edge_version is None:
            edge_version = self.get_edge_version()
        driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(edge_version[0])
        for arch in archs:
            current_driver_url = driver_url+arch+'.zip'
            driver_size = requests.head(current_driver_url).headers.get('Content-Length', None)
            if driver_size is not None and int(driver_size) > 1024**2:
                return current_driver_url
        raise RuntimeError('WebDriverInstaller: the required chrome driver was not found!')
            
    def webdriver_installer_menu(self, edge=False): # auto updating or installing google chrome or microsoft edge webdrivers
        if edge:
            browser_name = 'Microsoft Edge'
        else:
            browser_name = 'Google Chrome'
        console_log('-- WebDriver Auto-Installer --\n'.format(browser_name))
        if edge:
            browser_version = self.get_edge_version()
        else:
            browser_version = self.get_chrome_version()
        current_webdriver_version = None
        if edge:
            webdriver_name = 'msedgedriver'
        else:
            webdriver_name = 'chromedriver'
        if self.platform[0] == 'win':
            webdriver_name += '.exe'
        if os.path.exists(webdriver_name):
            os.chmod(webdriver_name, 0o777)
            out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
            if out is not None:
                if edge:
                    current_webdriver_version = out.decode("utf-8").split(' ')[3]
                else:
                    current_webdriver_version = out.decode("utf-8").split(' ')[1]
        console_log('{0} version: {1}'.format(browser_name, browser_version[0]), INFO, False)
        console_log('{0} webdriver version: {1}'.format(browser_name, current_webdriver_version), INFO, False)
        webdriver_path = None
        if current_webdriver_version is None:
            console_log('{0} webdriver not detected, download attempt...'.format(browser_name), INFO)
        elif current_webdriver_version.split('.')[0] != browser_version[1]: # major version match
            console_log('{0} webdriver version doesn\'t match version of the installed {1}, trying to update...'.format(browser_name, browser_name), ERROR)
        if current_webdriver_version is None or current_webdriver_version.split('.')[0] != browser_version[1]:
            if edge:
                driver_url = self.get_edgedriver_download_url()
            else:
                driver_url = self.get_chromedriver_download_url()
            if driver_url is not None:
                console_log('\nFound a suitable version for your system!', OK)
                console_log('Downloading...', INFO)
                if self.download_webdriver('.', driver_url, edge):
                    console_log('{0} webdriver was successfully downloaded and unzipped!\n'.format(browser_name), OK)
                    webdriver_path = os.path.join(os.getcwd(), webdriver_name)
                else:
                    console_log('Error downloading or unpacking!\n', ERROR)
        else:
            console_log('The driver has already been updated to the browser version!\n', OK)
            webdriver_path = os.path.join(os.getcwd(), webdriver_name)
        return webdriver_path

class EsetRegister(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        console_log('\n[EMAIL] Register page loading...', INFO)
        if args['email_api'] in ['hi2in', '10minutemail', 'tempmail']:
            self.driver.switch_to.new_window('EsetRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://login.eset.com/Register')
        uCE(self.driver, f"return {GET_EBID}('email') != null")
        console_log('[EMAIL] Register page is loaded!', OK)

        console_log('\nBypassing cookies...', INFO)
        if uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'id', 'cc-accept'))", max_iter=10, raise_exception_if_failed=False):
            console_log('Cookies successfully bypassed!', OK)
            time.sleep(1.5) # Once pressed, you have to wait a little while. If code do not do this, the site does not count the acceptance of cookies
        else:
            console_log("Cookies were not bypassed (it doesn't affect the algorithm, I think :D)", ERROR)

        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.email)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-continue-button'))")

        console_log('\n[PASSWD] Register page loading...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('button', 'data-label', 'register-create-account-button') === 'object'")
        console_log('[PASSWD] Register page is loaded!', OK)
        exec_js(f"return {GET_EBID}('password')").send_keys(self.eset_password)
        # Select Ukraine country
        if exec_js(f"return {GET_EBCN}('select__single-value ltr-1dimb5e-singleValue')[0]").text != 'Ukraine':
            exec_js(f"return {GET_EBID}('country-select-control')").click()
            for country in exec_js(f"return {GET_EBCN}('select__option ltr-gaqfzi-option')"):
                if country.text == 'Ukraine':
                    country.click()
                    break
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-create-account-button'))")

        for _ in range(DEFAULT_MAX_ITER):
            title = exec_js('return document.title')
            if title == 'Service not available':
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        uCE = SharedTools.untilConditionExecute
        
        if args['custom_email_api']:
            token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{args["email_api"]}] ESET-Token interception...', INFO)
            if args['email_api'] in ['hi2in', '10minutemail', 'tempmail']:
                token = SharedTools.parseToken(self.email_obj, self.driver, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3) # 1secmail
        console_log(f'ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver

class EsetKeygen(object):
    def __init__(self, registered_email_obj: SecEmailAPI, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        
        console_log('\nRequest sending...', INFO)
        self.driver.get('https://home.eset.com/subscriptions')
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'licenseAssociateHeaderAddNewBtn'))") # V2
        
        console_log('Waiting for permission to request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-fork-slide-trial-license-card-button'))")
        console_log('Access to the request was open!', OK)
        try:
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'license-fork-slide-continue-button'))")
        except:
            raise RuntimeError('Access to the request is denied, try again later!')
        console_log('\nPlatforms loading...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'device-protect-os-card-Windows-button'))")
        console_log('Windows platform is selected!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'device-protect-choose-platform-continue-btn'))")

        console_log('\nSending a request for a license...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input') === 'object'")
        exec_js(f"{GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input').value = '{self.email_obj.email}'")
        exec_js(f"{GET_EBAV}('ion-button', 'robot', 'device-protect-get-installer-send-email-btn').click()")
        console_log('Request successfully sent!', OK)

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        console_log('\nLicense uploads...', INFO)
        if platform.release() == '7' and webdriver_installer.platform[0] == 'win': # old browser versions
            for _ in range(DEFAULT_MAX_ITER):
                self.driver.get('https://home.eset.com/subscriptions') # refresh page
                try:
                    exec_js(f"{DEFINE_GET_EBAV_FUNCTION}\n{GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn').click()")
                    break
                except:
                    time.sleep(3)
        else: # new browser versions
            self.driver.get('https://home.eset.com/subscriptions')
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn'))")
        if self.driver.current_url.find('detail') != -1:
            console_log(f'License ID: {self.driver.current_url[-11:]}', OK)
        uCE(self.driver, f"return typeof {GET_EBAV}('div', 'class', 'LicenseDetailInfo') === 'object'")
        license_name = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-product-name').innerText")
        license_out_date = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-model-additional-info').innerText")
        license_key = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-key').innerText")
        console_log('\nInformation successfully received!', OK)
        return license_name, license_key, license_out_date

class EsetBusinessRegister(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.eset_password = eset_password
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        # STEP 0
        console_log('\nLoading EBA-ESET Page...', INFO)
        if args['email_api'] in ['hi2in', '10minutemail', 'tempmail']:
            self.driver.switch_to.new_window('EsetBusinessRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://eba.eset.com/Account/Register?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("register-email") !== null')
        console_log('Successfully!', OK)
        time.sleep(1)

        # STEP 1
        console_log('\nData filling...', INFO)
        exec_js(f'return {GET_EBID}("register-email")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("register-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-confirm-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-continue-1")').click()
        time.sleep(2)

        # STEP 2
        uCE(self.driver, f'return {GET_EBID}("register-first-name") !== null')
        exec_js(f'return {GET_EBID}("register-first-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'return {GET_EBID}("register-last-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'return {GET_EBID}("register-phone")').send_keys(SharedTools.createPassword(12, True))
        exec_js(f'return {GET_EBID}("register-continue-2")').click()
        time.sleep(2)

        # STEP 3
        uCE(self.driver, f'return {GET_EBID}("register-company-name") !== null')
        exec_js(f'return {GET_EBID}("register-company-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'{GET_EBID}("register-country").value = "227: 230"') # Ukraine
        exec_js(f'return {GET_EBID}("register-continue-3")').click()
        console_log('Successfully!', OK)
        time.sleep(1)

        # STEP 4
        uCE(self.driver, f'return {GET_EBID}("register-back-4") !== null')
        console_log(f'\n{Fore.CYAN}Solve the captcha on the page manually!!!{Fore.RESET}', INFO, False)
        while True: # captcha
            try:
                mtcaptcha_solved_token = exec_js(f'return {GET_EBCN}("mtcaptcha-verifiedtoken")[0].value')
                if mtcaptcha_solved_token != '':
                    break
            except Exception as E:
                pass
            time.sleep(1)
        exec_js(f'{GET_EBID}("isAgreedToTerms").click()')
        exec_js(f'return {GET_EBID}("register-back-4")').click()
        for _ in range(DEFAULT_MAX_ITER):
            if exec_js(f'return {GET_EBID}("registration-error") !== null'):
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            if exec_js(f'return {GET_EBID}("registration-success") !== null'):
                console_log('Successfully!', OK)
                return True
            time.sleep(1.5)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        if args['custom_email_api']:
            token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{args["email_api"]}] EBA-ESET-Token interception...', INFO)
            if args['email_api'] in ['hi2in', '10minutemail', 'tempmail']:
                token = SharedTools.parseToken(self.email_obj, self.driver, True, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = SharedTools.parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3) # 1secmail
        console_log(f'EBA-ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://eba.eset.com/Account/InitActivation?token={token}')
        SharedTools.untilConditionExecute(self.driver, f'return {GET_EBID}("username") !== null')
        console_log('Account successfully confirmed!', OK)

class EsetBusinessKeygen(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        # Log in
        console_log('\nLogging in to the created account...', INFO)
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("dashboard-create-eca-trial") !== null', delay=2)
        console_log('Successfully!', OK)
        console_log('\nSending a request for a get license...', INFO)
        exec_js(f'{GET_EBID}("dashboard-create-eca-trial").click()')
        uCE(self.driver, f'return {GET_EBID}("add-license-key-Agree-edtd-terms") !== null')
        exec_js(f'{GET_EBID}("add-license-key-Agree-edtd-terms").click()')
        exec_js(f'{GET_EBID}("edtd-eula-continue").click()')
        uCE(self.driver, f'return {GET_EBID}("btn-eca-eula-accept") !== null')
        console_log('Request successfully sent!', OK)
    
    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        console_log('\nLicense uploads...', INFO)
        self.driver.get('https://eba.eset.com/ba/licenses')
        for _ in range(DEFAULT_MAX_ITER):
            try:
                license_full_tag = self.driver.find_element('xpath', '//span[starts-with(@id, "license-list-license")]').get_attribute('id')
                break
            except:
                pass
            time.sleep(DEFAULT_DELAY)
        if license_full_tag is not None:     
            license_full_tag = license_full_tag[21:-1].split('-') # license-list-license-3B3-B8J-VA3-2017 -> [3B3, B8J, VA3, 2017]
            license_tag = '-'.join(license_full_tag[0:3]) # 3B3-B8J-VA3
            license_year = license_full_tag[-1] # 2017
            self.driver.get(f'https://eba.eset.com/ba/licenses/license/{license_tag}/{license_year}/overview')
            uCE(self.driver, f'return {GET_EBID}("specific-license-overview-license-key") !== null')
            console_log('License is uploaded!', OK)     
            console_log('\nGetting information from the license...', INFO)
            license_name = 'ESET Endpoint Security + ESET Server Security - Universal License'
            license_key = exec_js(f'return {GET_EBID}("specific-license-overview-license-key").innerText').strip()
            license_out_date = exec_js(f'return {GET_EBID}("specific-license-overview-expiration-date").innerText').strip()
            console_log('Information successfully received!', OK)
            return license_name, license_key, license_out_date
        else:
            raise RuntimeError('Error!')

if __name__ == '__main__':
    print(LOGO)
    args_parser = argparse.ArgumentParser()
    # Required
    ## Browsers
    args_browsers = args_parser.add_mutually_exclusive_group(required=True)
    args_browsers.add_argument('--chrome', action='store_true', help='Launching the project via Google Chrome browser')
    args_browsers.add_argument('--firefox', action='store_true', help='Launching the project via Mozilla Firefox browser')
    args_browsers.add_argument('--edge', action='store_true', help='Launching the project via Microsoft Edge browser')
    ## Modes of operation
    args_modes = args_parser.add_mutually_exclusive_group(required=True)
    args_modes.add_argument('--key', action='store_true', help='Generating an ESET-HOME license key (example as AGNV-XA2V-EA89-U546-UVJP)')
    args_modes.add_argument('--account', action='store_true', help='Generating an ESET HOME Account (To activate the free trial version)')
    args_modes.add_argument('--business-account', action='store_true', help='Generating an ESET BUSINESS Account (To huge businesses) - Requires manual captcha input!!!')
    args_modes.add_argument('--business-key', action='store_true', help='Generating an ESET BUSINESS Account and creating a universal license key for ESET products (1 key - 75 devices) - Requires manual captcha input!!!')
    args_modes.add_argument('--only-update', action='store_true', help='Updates/installs webdrivers and browsers without generating account and license key')
    # Optional
    args_parser.add_argument('--skip-webdriver-menu', action='store_true', help='Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)')
    args_parser.add_argument('--no-headless', action='store_true', help='Shows the browser at runtime (The browser is hidden by default, but on Windows 7 this option is enabled by itself)')
    args_parser.add_argument('--custom-browser-location', type=str, default='', help='Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition)')
    args_parser.add_argument('--email-api', choices=['1secmail', 'hi2in', '10minutemail', 'tempmail'], default='1secmail', help='Specify which api to use for mail')
    args_parser.add_argument('--custom-email-api', action='store_true', help='Allows you to manually specify any email, and all work will go through it. But you will also have to manually read inbox and do what is described in the documentation for this argument')
    try:
        try:
            args = vars(args_parser.parse_args())
        except:
            time.sleep(3)
            sys.exit(-1)
        
        # initialization and configuration of everything necessary for work
        webdriver_installer = WebDriverInstaller()
        # changing input arguments for special cases
        if platform.release() == '7' and webdriver_installer.platform[0] == 'win': # fix for Windows 7
            args['no_headless'] = True
        elif args['business_account'] or args['business_key'] or args['email_api'] == 'tempmail':
            args['no_headless'] = True
        
        driver = None
        webdriver_path = None
        browser_name = 'chrome'
        if args['firefox']:
            browser_name = 'firefox'
        if args['edge']:
            browser_name = 'edge'
        if not args['skip_webdriver_menu'] and browser_name != 'firefox': # updating or installing microsoft edge webdriver
            webdriver_path = webdriver_installer.webdriver_installer_menu(args['edge'])
            if webdriver_path is not None:
                os.chmod(webdriver_path, 0o777)
        if not args['only_update']:
            driver = SharedTools.initSeleniumWebDriver(browser_name, webdriver_path, args['custom_browser_location'], (not args['no_headless']))
        else:
            sys.exit(0)

        # main part of the programd
        if not args['custom_email_api']:
            console_log(f'\n[{args["email_api"]}] Mail registration...', INFO)
            if args['email_api'] == '10minutemail':
                email_obj = TenMinuteMailAPI(driver)
            elif args['email_api'] == 'hi2in':
                email_obj = Hi2inAPI(driver)
            elif args['email_api'] == 'tempmail':
                email_obj = TempMailAPI(driver)
            else:
                email_obj = SecEmailAPI()
            email_obj.init()
            console_log('Mail registration completed successfully!', OK)
        else:
            email_obj = CustomEmailAPI()
            while True:
                email = input(f'\n[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Enter the email address you have access to: {Fore.RESET}').strip()
                try:
                    matched_email = re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email).group()
                    if matched_email == email:
                        email_obj.email = matched_email
                        console_log('Mail has the correct syntax!', OK)
                        break
                    else:
                        raise RuntimeError
                except:
                    console_log('Invalid email syntax!!!', ERROR)
        eset_password = SharedTools.createPassword(10)
        
        # standart generator
        if args['account'] or args['key']:
            EsetReg = EsetRegister(email_obj, eset_password, driver)
            EsetReg.createAccount()
            EsetReg.confirmAccount()
            output_line = f'\nEmail: {email_obj.email}\nPassword: {eset_password}\n'
            output_filename = 'ESET ACCOUNTS.txt'
            if args['key']:
                output_filename = 'ESET KEYS.txt'
                EsetKeyG = EsetKeygen(email_obj, driver)
                EsetKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetKeyG.getLicenseData()
                output_line = f'\nLicense Name: {license_name}\nLicense Key: {license_key}\nLicense Out Date: {license_out_date}\n'
        
        # new generator
        elif args['business_account'] or args['business_key']:
            EsetBusinessReg = EsetBusinessRegister(email_obj, eset_password, driver)
            EsetBusinessReg.createAccount()
            EsetBusinessReg.confirmAccount()
            output_line = f'\nBusiness-Email: {email_obj.email}\nBusiness-Password: {eset_password}\n'
            output_filename = 'ESET ACCOUNTS.txt'
            if args['business_key']:
                output_filename = 'ESET KEYS.txt'
                EsetBusinessKeyG = EsetBusinessKeygen(email_obj, eset_password, driver)
                EsetBusinessKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetBusinessKeyG.getLicenseData()
                output_line = f'\nLicense Name: {license_name}\nLicense Key: {license_key}\nLicense Out Date: {license_out_date}\n'
        
        # end
        console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
        f.write(output_line)
        f.close()
        driver.quit()
    
    except Exception as E:
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        console_log(traceback_string, ERROR)
        time.sleep(3) # exit-delay