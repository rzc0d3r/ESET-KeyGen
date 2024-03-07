from .logger import *
from .shared_tools import *
from .sec_email_api import *

import time
import re

class EsetBusinessRegister(object):
    def __init__(self, registered_email_obj: SecEmail, eset_password: str, driver):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.eset_password = eset_password

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # STEP 0
        console_log('\nLoading EBA-ESET Page...', INFO)
        self.driver.get('https://eba.eset.com/Account/Register?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("register-email") !== null')
        console_log('Successfully!', OK)

        # STEP 1
        console_log('\n[STEP 1] Data filling...', INFO)
        exec_js(f'return {GET_EBID}("register-email")').send_keys(self.email_obj.get_full_login())
        exec_js(f'return {GET_EBID}("register-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-confirm-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-continue-1")').click()
        console_log('Successfully!', OK)

        # STEP 2
        console_log('\n[STEP 2] Data filling...', INFO)
        uCE(self.driver, f'return {GET_EBID}("register-first-name") !== null')
        exec_js(f'return {GET_EBID}("register-first-name")').send_keys(createPassword(10))
        exec_js(f'return {GET_EBID}("register-last-name")').send_keys(createPassword(10))
        exec_js(f'return {GET_EBID}("register-phone")').send_keys(createPassword(12, True))
        exec_js(f'return {GET_EBID}("register-continue-2")').click()
        console_log('Successfully!', OK)

        # STEP 3
        console_log('\n[STEP 3] Data filling...', INFO)
        uCE(self.driver, f'return {GET_EBID}("register-company-name") !== null')
        exec_js(f'return {GET_EBID}("register-company-name")').send_keys(createPassword(10))
        exec_js(f'{GET_EBID}("register-country").value = "227: 230"') # Ukraine
        exec_js(f'return {GET_EBID}("register-continue-3")').click()
        console_log('Successfully!', OK)

        # STEP 4
        console_log('\n[STEP 4] Data filling...', INFO)
        uCE(self.driver, f'return {GET_EBID}("register-back-4") !== null')
        console_log('[STEP 4] Solve the captcha on the page manually!!!', INFO, False)
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
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!!')
            if exec_js(f'return {GET_EBID}("registration-success") !== null'):
                console_log('Successfully!', OK)
                return True
            time.sleep(DEFAULT_DELAY)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!!')

    def getToken(self, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
        i = 0
        while True:
            json = self.email_obj.read_email()
            if json != []:
                message = json[-1]
                if message['subject'].find('ESET BUSINESS ACCOUNT - Account activation') != -1:
                    message_body = self.email_obj.get_message(message['id'])
                    match = re.search(r'token=[a-zA-Z\d:/-]*', message_body['body'])
                    if match is not None:
                        token = match.group()[6:]
                        return token
            i += 1
            if i == max_iter:
                raise RuntimeError('Token retrieval error!!!')
            time.sleep(delay)

    def confirmAccount(self):
        uCE = untilConditionExecute

        console_log('\nEBA-ESET-Token interception...', INFO)
        token = self.getToken(max_iter=DEFAULT_MAX_ITER*2)
        console_log(f'EBA-ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://eba.eset.com/Account/InitActivation?token={token}')
        for _ in range(DEFAULT_MAX_ITER):
            if self.driver.page_source.find("Your account has been successfully activated") != -1:
                console_log('Account successfully confirmed!', OK)
                break
            time.sleep(DEFAULT_DELAY)
        RuntimeError('Account confirmation error!!!')
