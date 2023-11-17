# v1.0.9.1 (171123-1541)
VERSION = 'v1.0.9.1 (171123-1541) by rzc0d3r'
import modules.logger as logger
import modules.shared_tools as shared_tools

import time
import re

class EsetKeygen:
    def __init__(self, registered_email_obj, driver):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        logger.console_log('\nHome page loading...', logger.INFO)
        self.driver.get("https://home.eset.com/")
        shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated').length > 1")
        logger.console_log('Home page is loaded!', logger.OK)
        
        logger.console_log('\nRequest sending...', logger.INFO)
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated')[1].click()")
        
        logger.console_log('Waiting for permission to request...', logger.INFO)
        shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('ion-cui-card LabeledCard ios hydrated').length > 2")
        logger.console_log('Access to the request was open!', logger.OK)

        js = [
            f"{shared_tools.GET_EBCN}('ion-cui-card LabeledCard ios hydrated')[2].click()",
            f"{shared_tools.GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated')[2].click()"
        ]
        self.driver.execute_script('\n'.join(js))

        logger.console_log('\nPlatforms loading...', logger.INFO)
        shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('ion-cui-card device-protect-os-card ios hydrated').length > 1")
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('ion-cui-card device-protect-os-card ios hydrated')[1].click()")
        logger.console_log('Windows platform is selected!', logger.OK)
        shared_tools.untilConditionExecute(self.driver, f"return typeof {shared_tools.GET_EBCN}('ion-cui-button ios button button-block button-clear ion-activatable ion-focusable hydrated')[0] === 'object'")
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('ion-cui-button protect-page--continue-button ion-color ion-color-secondary ios button button-block button-solid ion-activatable ion-focusable hydrated')[0].click()")
        
        logger.console_log('\nRequest license page loading...', logger.INFO)
        shared_tools.untilConditionExecute(self.driver, f"return typeof {shared_tools.GET_EBCN}('sc-ion-input-ios-h sc-ion-input-ios-s ios hydrated')[0] === 'object'")
        logger.console_log('Sending a request for a license...', logger.INFO)
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('sc-ion-input-ios-h sc-ion-input-ios-s ios hydrated')[0].value = '{self.email_obj.get_full_login()}'")
        self.driver.execute_script(f"{shared_tools.GET_EBCN}('ion-cui-button ios button button-solid ion-activatable ion-focusable hydrated')[2].click()")
        logger.console_log('Waiting for confirmation of request...', logger.INFO)

        shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('protect-sent-installer-modal--content').length > 0")
        logger.console_log('Request was approved!', logger.OK)

    def getLicenseData(self):
        try: # Old method (V1)
            logger.console_log('\n[V1] License uploads...', logger.INFO)
            self.driver.get("https://home.eset.com/subscriptions")
            shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('ion-cui-button license-preview_link-btn ios button button-block button-solid ion-activatable ion-focusable hydrated').length > 0", max_iter=20)

            license_tag = self.driver.execute_script(f"return {shared_tools.GET_EBCN}('ion-cui-button license-preview_link-btn ios button button-block button-solid ion-activatable ion-focusable hydrated')[0].href")
            logger.console_log('[V1] License is uploaded!', logger.OK)
            self.driver.get(f"https://home.eset.com{license_tag}")

            logger.console_log('\n[V1] Getting information from the license...', logger.INFO)
            shared_tools.untilConditionExecute(self.driver, f"return {shared_tools.GET_EBCN}('ion-color ion-color-dark md hydrated').length > 20")

            license_name = self.driver.execute_script(f"return {shared_tools.GET_EBCN}('ion-color ion-color-dark md hydrated')[10].innerText")
            license_out_date = self.driver.execute_script(f"return {shared_tools.GET_EBCN}('ion-color ion-color-dark md hydrated')[12].innerText")
            license_key = self.driver.execute_script(f"return {shared_tools.GET_EBCN}('ion-color ion-color-dark md hydrated')[14].innerText")
            logger.console_log('[V1] Information successfully received!', logger.OK)
            return license_name, license_out_date, license_key
        except: # New method (V2)
            logger.console_log('\nFirst method of obtaining a license was unsuccessful!', logger.ERROR)
            logger.console_log('Attempting to obtain licenses by a new method...', logger.INFO)
            logger.console_log('\n[V2] License uploads...', logger.INFO)
            for _ in range(shared_tools.DEFAULT_MAX_ITER*2):
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
                time.sleep(shared_tools.DEFAULT_DELAY)