# v1.0.9.2 (201123-1006)
VERSION = 'v1.0.9.2 (201123-1006) by rzc0d3r'

from modules.logger import *
from modules.shared_tools import *
from modules.sec_email_api import *

from selenium.webdriver import Chrome

import time
import re

class EsetKeygen:
    def __init__(self, registered_email_obj: SecEmail, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        console_log('\nHome page loading...', INFO)
        self.driver.get("https://home.eset.com")
        console_log('Home page is loaded!', OK)
        console_log('\nRequest sending...', INFO)

        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'home-overview-empty-add-license-btn'))")
        
        console_log('Waiting for permission to request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-card', 'robot', 'license-fork-slide-trial-license-card'))")
        console_log('Access to the request was open!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'license-fork-slide-continue-button'))")

        console_log('\nPlatforms loading...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-card', 'robot', 'device-protect-os-card-Windows'))")
        console_log('Windows platform is selected!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'device-protect-choose-platform-continue-btn'))")

        console_log('\nRequest license page loading...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input') === 'object'")
        
        console_log('Sending a request for a license...', INFO)
        exec_js(f"{GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input').value = '{self.email_obj.get_full_login()}'")
        exec_js(f"{GET_EBAV}('ion-button', 'robot', 'device-protect-get-installer-send-email-btn').click()")
        console_log('Waiting for confirmation of request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'common-base-modal-header-close-btn'))")
        console_log('Request was approved!', OK)

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        try: # Old method (V1)
            console_log('\n[V1] License uploads...', INFO)
            uCE(self.driver, f"return typeof {GET_EBAV}('ion-button', 'robot', 'license-list-open-detail-page-btn') === 'object'")
            license_tag = exec_js(f"return {GET_EBAV}('ion-button', 'robot', 'license-list-open-detail-page-btn').href")
            console_log('[V1] License is uploaded!', OK)
            self.driver.get(f"https://home.eset.com{license_tag}")

            console_log('\n[V1] Getting information from the license...', INFO)
            uCE(self.driver, f"return {GET_EBCN}('ion-color ion-color-dark md hydrated').length > 20")

            license_name = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-product-name').innerText")
            license_out_date = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-license-model-additional-info').innerText")
            license_key = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-license-key').innerText")
            console_log('[V1] Information successfully received!', OK)
            return license_name, license_out_date, license_key
        except: # New method (V2)
            console_log('\nFirst method of obtaining a license was unsuccessful!', ERROR)
            console_log('Attempting to obtain licenses by a new method...', INFO)
            console_log('\n[V2] License uploads...', INFO)
            for _ in range(DEFAULT_MAX_ITER*2):
                message = self.email_obj.read_email()[0]
                if message['from'] == 'noreply@orders.eset.com':
                    console_log('[V2] License is uploaded!', OK)
                    message_body = self.email_obj.get_message(message['id'])['body']
                    console_log('\n[V2] Getting information from the license...', INFO)
                    license_name = ('ESET'+re.findall(r'>[\s]+ESET([\w ]+)[\s]+</td>', message_body)[0])
                    license_key = ('-'.join(re.findall(r'([\dA-Z]{4})-', message_body)))
                    license_out_date = (''.join(re.findall(r'\d{1,2}.\d{1,2}.\d{4}', message_body)))
                    console_log('[V2] Information successfully received!', OK)
                    return license_name, license_out_date, license_key
                time.sleep(DEFAULT_DELAY)