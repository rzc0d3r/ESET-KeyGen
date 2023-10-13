# Version 1.0.8.2 (131023-2151)
VERSION = 'v1.0.8.2 (131023-2151) by rzc0d3r'
import modules.chrome_driver_installer as chrome_driver_installer
import modules.logger as logger

import datetime
import requests
import time
import os
import re

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from subprocess import check_output, PIPE
from string import ascii_letters
from random import choice

GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1

class EmailConnectError(Exception):
    pass

class Email:
    def __init__(self):
        self.__login = None
        self.__domain = None
        self.__api = 'https://www.1secmail.com/api/v1/'
        
    def register(self):
        url = f'{self.__api}?action=genRandomMailbox&count=1'
        try:
            r = requests.get(url)
        except:
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
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
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
        return r.json()
    
    def get_message(self, message_id):
        url = f'{self.__api}?action=readMessage&login={self.__login}&domain={self.__domain}&id={message_id}'
        try:
            r = requests.get(url)
        except:
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
        return r.json()

class SharedTools:
    def untilConditionExecute(driver: Chrome, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True):
        i = 0
        while True:
            try:
                if i > max_iter:
                    return False
                result = driver.execute_script(js)
                if result == positive_result:
                    return True
            except Exception as E:
                pass
            i += 1
            time.sleep(delay)

    def createPassword(length):
        return ''.join(['Xx0$']+[choice(ascii_letters) for _ in range(length)])

class EsetRegister:
    def __init__(self, registered_email_obj: Email, eset_password: str):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = None

    def initDriver(self):
        driver_options = ChromeOptions()
        if os.name == 'posix': # For Linux
            logger.console_log('Initializing driver for Linux', logger.INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
            driver_options.add_argument('--headless')
        if os.name == 'nt':
            logger.console_log('Initializing driver for Windows', logger.INFO)
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = Chrome(options=driver_options)
        self.driver.set_window_size(600, 600)

    def getToken(self, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER) -> str:
        i = 0
        while True:
            json = self.email_obj.read_email()
            if json != []:
                message = json[-1]
                if message['from'].find('product.eset.com') != -1:
                    message_body = self.email_obj.get_message(message['id'])
                    match = re.search(r'token=[a-zA-Z\d:/-]*', message_body['body'])
                    if match is not None:
                        token = match.group()[6:]
                        return token
            i += 1
            if i == max_iter:
                logger.console_log('Token retrieval error!!!', logger.ERROR)
                self.driver.quit()
                return ''
            time.sleep(delay)

    def createAccount(self):
        logger.console_log('\n[EMAIL] Register page loading...', logger.INFO)
        self.driver.get(f'https://login.eset.com/Register')
        logger.console_log('[EMAIL] Register page is loaded!', logger.OK)
        self.driver.execute_script(f"{GET_EBID}('Email').value='{self.email_obj.get_full_login()}'\ndocument.forms[0].submit()")

        logger.console_log('\n[PASSWD] Register page loading...', logger.INFO)
        SharedTools.untilConditionExecute(self.driver, f"return typeof {GET_EBID}('Password') === 'object'")
        SharedTools.untilConditionExecute(self.driver, f"return typeof {GET_EBCN}('input-main input-main--notempty')[0] === 'object'")
        self.driver.execute_script(f"{GET_EBID}('Password').value='{self.eset_password}'")
        self.driver.execute_script(f"{GET_EBCN}('input-main input-main--notempty')[0].value='230'\ndocument.forms[0].submit()") # Change Account Region to Ukraine
        logger.console_log('[PASSWD] Register page is loaded!', logger.OK)
        
        while True:
            time.sleep(0.5)
            title = self.driver.execute_script('return document.title')
            if title == 'Service not available':
                logger.console_log('\nESET temporarily blocked your IP, try again later!!!', logger.ERROR)
                self.driver.quit()
                break
            url = self.driver.execute_script('return document.URL')
            if url == 'https://home.eset.com/':
                return True
        return False

    def confirmAccount(self):
        token = self.getToken()
        if token == '':
            return False
        logger.console_log(f'\nESET Token: {token}', logger.OK)
        logger.console_log('\nAccount confirmation is in progress...', logger.INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        SharedTools.untilConditionExecute(self.driver, 'return document.title === "ESET HOME"')
        SharedTools.untilConditionExecute(self.driver, f'return typeof {GET_EBCN}("verification-email_p")[1] === "object"', positive_result=False)
        logger.console_log('Account successfully confirmed!', logger.OK)
        return True

    def returnDriver(self) -> Chrome:
        return self.driver

class EsetKeygen:
    def __init__(self, registered_email_obj: Email, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        logger.console_log('\nLicense page loading...', logger.INFO)
        self.driver.get("https://home.eset.com/licenses")
        SharedTools.untilConditionExecute(self.driver, f"return {GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated').length > 1")
        logger.console_log('License page is loaded!', logger.OK)
        
        logger.console_log('\nRequest sending...', logger.INFO)
        self.driver.execute_script(f"{GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated')[1].click()")

        logger.console_log('Waiting for permission to request...', logger.INFO)
        SharedTools.untilConditionExecute(self.driver, f"return {GET_EBCN}('ion-cui-button ios button button-clear ion-activatable ion-focusable hydrated').length > 10")
        self.driver.execute_script(f"{GET_EBCN}('ion-cui-button ios button button-clear ion-activatable ion-focusable hydrated')[10].click()")
        logger.console_log('Access to the request was open!', logger.OK)

        logger.console_log('\nPlatforms loading...', logger.INFO)
        SharedTools.untilConditionExecute(self.driver, f"return {GET_EBCN}('ion-cui-card device-protect-os-card ios hydrated').length > 1")
        self.driver.execute_script(f"{GET_EBCN}('ion-cui-card device-protect-os-card ios hydrated')[1].click()")
        logger.console_log('Windows platform is selected!', logger.OK)
        SharedTools.untilConditionExecute(self.driver, f"return typeof {GET_EBCN}('ion-cui-button ios button button-block button-clear ion-activatable ion-focusable hydrated')[0] === 'object'")
        self.driver.execute_script(f"{GET_EBCN}('ion-cui-button protect-page--continue-button ion-color ion-color-secondary ios button button-block button-solid ion-activatable ion-focusable hydrated')[0].click()")
        
        logger.console_log('\nRequest license page loading...', logger.INFO)
        SharedTools.untilConditionExecute(self.driver, f"return typeof {GET_EBCN}('sc-ion-input-ios-h sc-ion-input-ios-s ios hydrated')[0] === 'object'")
        logger.console_log('Sending a request for a license...', logger.INFO)
        self.driver.execute_script(f"{GET_EBCN}('sc-ion-input-ios-h sc-ion-input-ios-s ios hydrated')[0].value = '{self.email_obj.get_full_login()}'")
        self.driver.execute_script(f"{GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated')[1].click()")
        logger.console_log('Waiting for confirmation of request...', logger.INFO)

        SharedTools.untilConditionExecute(self.driver, f"return typeof {GET_EBCN}('ProtectionSuccess')[0] === 'object'")
        logger.console_log('Request was approved!', logger.OK)

    def getLicenseData(self):
        try: # Old method (V1)
            logger.console_log('\n[V1] License uploads...', logger.INFO)
            self.driver.get("https://home.eset.com/licenses")
            SharedTools.untilConditionExecute(self.driver, f"return {GET_EBCN}('ion-cui-button license-preview_link-btn ios button button-block button-solid ion-activatable ion-focusable hydrated').length > 0", max_iter=20)

            license_tag = self.driver.execute_script(f"return {GET_EBCN}('ion-cui-button license-preview_link-btn ios button button-block button-solid ion-activatable ion-focusable hydrated')[0].href")
            logger.console_log('[V1] License is uploaded!', logger.OK)
            self.driver.get(f"https://home.eset.com{license_tag}")

            logger.console_log('\n[V1] Getting information from the license...', logger.INFO)
            SharedTools.untilConditionExecute(self.driver, f"return {GET_EBCN}('DetailInfoSectionItem__value').length > 15")

            license_name = self.driver.execute_script(f"return {GET_EBCN}('DetailInfoSectionItem__value')[0].textContent")
            license_out_date = self.driver.execute_script(f"return {GET_EBCN}('DetailInfoSectionItem__value')[2].textContent")
            license_key = self.driver.execute_script(f"return {GET_EBCN}('DetailInfoSectionItem__value')[4].textContent")
            logger.console_log('[V1] Information successfully received!', logger.OK)
            return license_name, license_out_date, license_key
        except: # New method (V2)
            logger.console_log('\nFirst method of obtaining a license was unsuccessful!', logger.ERROR)
            logger.console_log('Attempting to obtain licenses by a new method...', logger.INFO)
            logger.console_log('\n[V2] License uploads...', logger.INFO)
            for _ in range(DEFAULT_MAX_ITER*2):
                message = self.email_obj.read_email()[0]
                if message['from'] == 'noreply@orders.eset.com':
                    logger.console_log('[V2] License is uploaded!', logger.OK)
                    message_body = self.email_obj.get_message(message['id'])['body']
                    logger.console_log('\n[V2] Getting information from the license...', logger.INFO)
                    license_name = ('ESET'+re.findall(r'>[\s]+ESET([\w ]+)[\s]+</td>', message_body)[0])
                    license_key = ('-'.join(re.findall(r'([\dA-Z]{4})-', message_body)))
                    license_out_date = (''.join(re.findall(r'\d{1,2}.\d{1,2}.\d{4}', message_body)))
                    logger.console_log('[V2] Information successfully received!', logger.OK)
                    return license_name, license_out_date, license_key
                time.sleep(DEFAULT_DELAY)
        return None, None, None
    
if __name__ == '__main__':
    try:
        # auto updating or installing chrome driver
        logger.console_log('-- Chrome Driver Auto-Installer {0} --\n'.format(chrome_driver_installer.VERSION))
        chrome_version, _, chrome_major_version, _, _ = chrome_driver_installer.get_chrome_version()
        if chrome_version is None:
            raise RuntimeError('Chrome is not detected on your device!')
        current_chromedriver_version = None
        platform, arch = chrome_driver_installer.get_platform_for_chrome_driver()
        chromedriver_name = 'chromedriver.exe'
        if platform != 'win':
            chromedriver_name = 'chromedriver'
        if os.path.exists(chromedriver_name):
            os.chmod(chromedriver_name, 0o777)
            out = check_output([os.path.join(os.getcwd(), chromedriver_name), "--version"], stderr=PIPE)
            if out is not None:
                current_chromedriver_version = out.decode("utf-8").split(' ')[1]
        logger.console_log('Chrome version: {0}'.format(chrome_version), logger.INFO, False)
        logger.console_log('Chrome driver version: {0}'.format(current_chromedriver_version), logger.INFO, False)
        if current_chromedriver_version is None:
            logger.console_log('\nChrome driver not detected, download attempt...', logger.ERROR)
        elif current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]: # major version match
            logger.console_log('\nChrome driver version doesn\'t match version of the installed chrome, trying to update...', logger.ERROR)
        if current_chromedriver_version is None or current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]:
            driver_url = chrome_driver_installer.get_driver_download_url()
            if driver_url is None:
                logger.console_log('\nCouldn\'t find the right version for your system!', logger.ERROR)
                method = input('\nRun the program anyway? (y/n): ')
                if method == 'n':
                    exit(-1)
            else:
                logger.console_log('\nFound a suitable version for your system!', logger.OK)
                logger.console_log('\nDownload attempt...', logger.INFO)
                if chrome_driver_installer.download_chrome_driver('.', driver_url):
                    logger.console_log('The Сhrome driver was successfully downloaded and unzipped!', logger.OK)
                    input('\nPress Enter to continue...')
                else:
                    logger.console_log('Error downloading or unpacking!', logger.ERROR)
                    method = input('\nRun the program anyway? (y/n): ')
                    if method == 'n':
                        exit(-1)
        logger.console_log('\n-- ESET KeyGen {0} --\n'.format(VERSION))
        email_obj = Email()
        email_obj.register()
        eset_password = SharedTools.createPassword(6)
        EsetReg = EsetRegister(email_obj, eset_password)
        EsetReg.initDriver()
        if not EsetReg.createAccount():
            input('Press Enter...')
            exit()
        if not EsetReg.confirmAccount():
            input('Press Enter...')
            exit()
        driver = EsetReg.returnDriver()
        EsetKeyG = EsetKeygen(email_obj, driver)
        EsetKeyG.sendRequestForKey()
        license_name, license_out_date, license_key = EsetKeyG.getLicenseData()
        output_line = f"\nLicense Name: {license_name}\nLicense Out Date: {license_out_date}\nLicense Key: {license_key}\n"
        logger.console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - ESET KEYS.txt", 'a')
        f.write(output_line)
        f.close()
        driver.quit()
    except Exception as E:
        logger.console_log(str(E), logger.ERROR)
    input('Press Enter...')
