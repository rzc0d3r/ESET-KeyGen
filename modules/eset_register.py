# v1.0.9 (191023-2057)
VERSION = 'v1.0.9 (191023-2057) by rzc0d3r'
import modules.logger as logger
import modules.shared_tools as shared_tools

from selenium.webdriver import Chrome, ChromeOptions, ChromeService

import os
import re
import time

class EsetRegister:
    def __init__(self, registered_email_obj, eset_password: str):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = None

    def initDriver(self, chromedriver_path=None):
        driver_options = ChromeOptions()
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_service = ChromeService(executable_path=chromedriver_path)
        if os.name == 'posix': # For Linux
            logger.console_log('Initializing driver for Linux', logger.INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
            driver_options.add_argument('--headless')
        elif os.name == 'nt':
            logger.console_log('Initializing driver for Windows', logger.INFO)
        self.driver = Chrome(options=driver_options, service=driver_service)
        self.driver.set_window_size(600, 600)

    def getToken(self, delay=shared_tools.DEFAULT_DELAY, max_iter=shared_tools.DEFAULT_MAX_ITER) -> str:
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
                raise RuntimeError('Token retrieval error!!!')
            time.sleep(delay)

    def createAccount(self):
        logger.console_log('\n[EMAIL] Register page loading...', logger.INFO)
        self.driver.get(f'https://login.eset.com/Register')
        logger.console_log('[EMAIL] Register page is loaded!', logger.OK)
        self.driver.execute_script(f"{shared_tools.GET_EBID}('Email').value='{self.email_obj.get_full_login()}'\ndocument.forms[0].submit()")

        logger.console_log('\n[PASSWD] Register page loading...', logger.INFO)
        shared_tools.untilConditionExecute(self.driver, f"return typeof {shared_tools.GET_EBID}('Password') === 'object'")
        shared_tools.untilConditionExecute(self.driver, f"return typeof {shared_tools.GET_EBCN}('input-main input-main--notempty')[0] === 'object'")
        self.driver.execute_script(f"{shared_tools.GET_EBID}('Password').value='{self.eset_password}'")
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('input-main input-main--notempty')[0].value='230'\ndocument.forms[0].submit()") # Change Account Region to Ukraine
        logger.console_log('[PASSWD] Register page is loaded!', logger.OK)
        
        for _ in range(shared_tools.DEFAULT_MAX_ITER):
            title = self.driver.execute_script('return document.title')
            if title == 'Service not available':
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!!\n')
            url = self.driver.execute_script('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(shared_tools.DEFAULT_DELAY)
        return False

    def confirmAccount(self):
        token = self.getToken()
        logger.console_log(f'\nESET Token: {token}', logger.OK)
        logger.console_log('\nAccount confirmation is in progress...', logger.INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        shared_tools.untilConditionExecute(self.driver, 'return document.title === "ESET HOME"')
        shared_tools.untilConditionExecute(self.driver, f'return typeof {shared_tools.GET_EBCN}("verification-email_p")[1] === "object"', positive_result=False)
        logger.console_log('Account successfully confirmed!', logger.OK)
        return True

    def returnDriver(self):
        return self.driver