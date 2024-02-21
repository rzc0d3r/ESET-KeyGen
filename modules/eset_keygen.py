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
        try: # first method (main)
            console_log('\n[V1] License uploads...', INFO)
            self.driver.get('https://home.eset.com/subscriptions')
            uCE(self.driver, f"return typeof {GET_EBAV}('ion-button', 'robot', 'license-list-open-detail-page-btn') === 'object'")
            license_tag = exec_js(f"return {GET_EBAV}('ion-button', 'robot', 'license-list-open-detail-page-btn').href")
            console_log('[V1] License is uploaded!', OK)
            console_log('\n[V1] Getting information from the license...', INFO)
            self.driver.get(f"https://home.eset.com{license_tag}")
            uCE(self.driver, f"return typeof {GET_EBAV}('div', 'class', 'LicenseDetailInfo') === 'object'")
            license_name = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-product-name').innerText")
            license_out_date = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-license-model-additional-info').innerText")
            license_key = exec_js(f"return {GET_EBAV}('p', 'data-r', 'license-detail-license-key').innerText")
            console_log('[V1] Information successfully received!', OK)
        except: # second method (emergency)
            console_log('[V1] Algorithm error, attempt through a new algorithm...', ERROR)
            console_log('\n[V2] License uploads...', INFO)
            for _ in range(DEFAULT_MAX_ITER*2):
                last_message = self.email_obj.read_email()[0]
                last_message_id = last_message['id']
                if last_message['from'] == 'noreply@orders.eset.com':
                    last_message_body = self.email_obj.get_message(last_message_id)['body']
                    f = open('license.html', 'wb')
                    f.write(last_message_body.encode('utf-8'))
                    f.close()
                    break
                time.sleep(DEFAULT_DELAY*2)
            console_log('[V2] License is uploaded!', OK)
            console_log('\n[V2] Getting information from the license...', INFO)
            self.driver.get(f"file://{os.getcwd()}/license.html")
            uCE(self.driver, f"return {GET_EBCN}('contents').length > 20")
            license_name = exec_js(f"return {GET_EBCN}('contents')[4].innerText")
            license_out_date = exec_js(f"return {GET_EBCN}('contents')[8].innerText")
            license_key = exec_js(f"return {GET_EBCN}('contents')[6].innerText")
            console_log('[V2] Information successfully received!', OK)
            try:
                os.remove('license.html')
            except:
                pass
        return license_name, license_out_date, license_key