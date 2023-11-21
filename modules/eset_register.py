# v1.0.9.2 (211123-1059)
VERSION = 'v1.0.9.2 (211123-1059) by rzc0d3r'

from modules.logger import *
from modules.shared_tools import *
from modules.sec_email_api import *

import re
import time

class EsetRegister:
    def __init__(self, registered_email_obj: SecEmail, eset_password: str, driver):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def getToken(self, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
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
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        console_log('\n[EMAIL] Register page loading...', INFO)
        self.driver.get('https://login.eset.com/Register')
        console_log('[EMAIL] Register page is loaded!', OK)
        exec_js(f"{GET_EBID}('Email').value='{self.email_obj.get_full_login()}'")
        exec_js('document.forms[0].submit()')

        console_log('\n[PASSWD] Register page loading...', INFO)
        uCE(self.driver, f"return typeof {GET_EBID}('Password') === 'object'")
        uCE(self.driver, f"return typeof {GET_EBCN}('input-main input-main--notempty')[0] === 'object'")
        exec_js(f"{GET_EBID}('Password').value='{self.eset_password}'")
        exec_js(f"{GET_EBCN}('input-main input-main--notempty')[0].value='230'") # Change Account Region to Ukraine
        exec_js('document.forms[0].submit()')
        console_log('[PASSWD] Register page is loaded!', OK)
        
        for _ in range(DEFAULT_MAX_ITER):
            title = exec_js('return document.title')
            if title == 'Service not available':
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        return False

    def confirmAccount(self):
        uCE = untilConditionExecute

        token = self.getToken()
        console_log(f'\nESET Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        uCE(self.driver, f'return typeof {GET_EBCN}("verification-email_p")[1] !== "object"')
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver