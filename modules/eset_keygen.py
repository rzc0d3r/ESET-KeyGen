from .logger import *
from .shared_tools import *
from .sec_email_api import *

import time

class EsetKeygen:
    def __init__(self, registered_email_obj: SecEmail, driver):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        
        console_log('\nRequest sending...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'home-overview-empty-add-license-btn'))")
        
        console_log('Waiting for permission to request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-card', 'robot', 'license-fork-slide-trial-license-card'))")
        console_log('Access to the request was open!', OK)
        try:
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'license-fork-slide-continue-button'))")
        except:
            raise RuntimeError('Access to the request is denied, try again later!')
        console_log('\nPlatforms loading...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-card', 'robot', 'device-protect-os-card-Windows'))")
        console_log('Windows platform is selected!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'device-protect-choose-platform-continue-btn'))")

        console_log('\nSending a request for a license...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input') === 'object'")
        exec_js(f"{GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input').value = '{self.email_obj.get_full_login()}'")
        exec_js(f"{GET_EBAV}('ion-button', 'robot', 'device-protect-get-installer-send-email-btn').click()")
        console_log('Request successfully sent!', OK)

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        console_log('\n[V2] License uploads...', INFO)
        for _ in range(DEFAULT_MAX_ITER*2):
            last_message = self.email_obj.read_email()[0]
            last_message_id = last_message['id']
            if last_message['from'] == 'noreply@orders.eset.com':
                console_log('[V2] License is uploaded!', OK)
                console_log('\n[V2] Getting information from the license...', INFO)
                last_message_body = self.email_obj.get_message(last_message_id)['body']
                license_data = last_message_body.split('\n')[6:12]
                license_data = '\n'.join(license_data).replace('\t', '').replace('\r', '')
                console_log('[V2] Information successfully received!', OK)
                break
            time.sleep(DEFAULT_DELAY*2) 
        return '\n'+license_data