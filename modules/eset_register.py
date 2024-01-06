from .logger import *
from .shared_tools import *
from .sec_email_api import *

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

        console_log('\nBypassing cookies...', INFO)
        if uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'id', 'cc-accept'))", max_iter=10, raise_exception_if_failed=False):
            console_log('Cookies successfully bypassed!', OK)
            time.sleep(1.5) # Once pressed, you have to wait a little while. If code do not do this, the site does not count the acceptance of cookies
        else:
            console_log("Cookies were not bypassed (it doesn't affect the algorithm, I think :D)", ERROR)

        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.get_full_login())
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
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        return False

    def confirmAccount(self):
        uCE = untilConditionExecute

        console_log(f'\nESET-Token interception...', INFO)
        token = self.getToken()
        console_log(f'ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        uCE(self.driver, f'return typeof {GET_EBCN}("verification-email_p")[1] !== "object"')
        uCE(self.driver, f"return typeof {GET_EBAV}('ion-button', 'robot', 'home-overview-empty-add-license-btn') === 'object'")
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver
