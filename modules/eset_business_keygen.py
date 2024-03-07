from .logger import *
from .shared_tools import *
from .sec_email_api import *

import time

class EsetBusinessKeygen:
    def __init__(self, registered_email_obj: SecEmail, eset_password: str, driver):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # Log in
        console_log('\nLogging in to the created account...', INFO)
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.get_full_login())
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("dashboard-create-eca-trial") !== null')
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
        uCE = untilConditionExecute

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