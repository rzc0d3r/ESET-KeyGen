from .EmailAPIs import *

import colorama
import platform
import time
import sys

class EsetRegister(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        console_log('\n[EMAIL] Register page loading...', INFO)
        if isinstance(self.email_obj, (Hi2inAPI, TenMinuteMailAPI, TempMailAPI, GuerRillaMailAPI)):
            self.driver.switch_to.new_window('EsetRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://login.eset.com/Register')
        uCE(self.driver, f"return {GET_EBID}('email') != null")
        console_log('[EMAIL] Register page is loaded!', OK)

        console_log('\nBypassing cookies...', INFO)
        if uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'id', 'cc-accept'))", max_iter=10, raise_exception_if_failed=False):
            console_log('Cookies successfully bypassed!', OK)
            time.sleep(1) # Once pressed, you have to wait a little while. If code do not do this, the site does not count the acceptance of cookies
        else:
            console_log("Cookies were not bypassed (it doesn't affect the algorithm, I think :D)", ERROR)

        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.email)
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
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        uCE = untilConditionExecute
        #uCE(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBAV}("ion-button", "data-r", "account-verification-email-modal-resend-email-btn"))') # accelerating the receipt of an eset token
        
        if isinstance(self.email_obj, CustomEmailAPI):
            token = parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{self.email_obj.class_name}] ESET-Token interception...', INFO)
            if isinstance(self.email_obj, (Hi2inAPI, TenMinuteMailAPI, TempMailAPI, GuerRillaMailAPI)):
                token = parseToken(self.email_obj, self.driver, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, max_iter=100, delay=3) # 1secmail, developermail
        console_log(f'ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver

class EsetKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        
        console_log('\nRequest sending...', INFO)
        self.driver.get('https://home.eset.com/subscriptions')
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'licenseAssociateHeaderAddNewBtn'))") # V2
        
        console_log('Waiting for permission to request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-fork-slide-trial-license-card-button'))")
        try:
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-fork-slide-continue-button'))")
            console_log('Access to the request was open!', OK)
        except:
            raise RuntimeError('Access to the request is denied, try again later!')
        console_log('\nPlatforms loading...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'device-protect-os-card-Windows-button'))")
        console_log('Windows platform is selected!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'device-protect-choose-platform-continue-btn'))")

        console_log('\nSending a request for a license...', INFO)
        uCE(self.driver, f"return typeof {GET_EBID}('email') === 'object'")
        try:
            exec_js(f"return {GET_EBID}('email')").click() # fix for ElementNotInteractableException: X is not reachable by keyboard
        except:
            pass
        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.email)
        exec_js(f"return {GET_EBAV}('button', 'data-label', 'device-protect-get-installer-send-email-btn')").click()
        for _ in range(DEFAULT_MAX_ITER):
            time.sleep(0.5)
            try:
                btn = exec_js(f"return {GET_EBAV}('button', 'data-label', 'device-protect-get-installer-send-email-btn')")
                if btn.text.lower() == 'send email':
                    console_log('Request successfully sent!', OK)
                    return True
            except:
                pass
        raise RuntimeError('Request sending error!!!')

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        console_log('\nLicense uploads...', INFO)
        if platform.release() == '7' and sys.platform.startswith('win'): # old browser versions
            for _ in range(DEFAULT_MAX_ITER):
                self.driver.get('https://home.eset.com/subscriptions') # refresh page
                try:
                    exec_js(f"{DEFINE_GET_EBAV_FUNCTION}\n{GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn').click()")
                    break
                except:
                    time.sleep(3)
        else: # new browser versions
            self.driver.get('https://home.eset.com/subscriptions')
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn'))")
        if self.driver.current_url.find('detail') != -1:
            console_log(f'License ID: {self.driver.current_url[-11:]}', OK)
        uCE(self.driver, f"return typeof {GET_EBAV}('div', 'class', 'LicenseDetailInfo') === 'object'")
        license_name = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-product-name').innerText")
        license_out_date = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-model-additional-info').innerText")
        license_key = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-key').innerText")
        console_log('\nInformation successfully received!', OK)
        return license_name, license_key, license_out_date


class EsetBusinessRegister(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.eset_password = eset_password
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        # STEP 0
        console_log('\nLoading EBA-ESET Page...', INFO)
        if isinstance(self.email_obj, (Hi2inAPI, TenMinuteMailAPI, TempMailAPI, GuerRillaMailAPI)):
            self.driver.switch_to.new_window('EsetBusinessRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://eba.eset.com/Account/Register?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("register-continue-1") != null')
        console_log('Successfully!', OK)

        # STEP 1
        console_log('\nData filling...', INFO)
        exec_js(f'return {GET_EBID}("register-email")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("register-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-confirm-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-continue-1")').click()

        # STEP 2
        uCE(self.driver, f'return {GET_EBID}("register-first-name") !== null')
        exec_js(f'return {GET_EBID}("register-first-name")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("register-last-name")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("register-phone")').send_keys(dataGenerator(12, True))
        exec_js(f'return {GET_EBID}("register-continue-2")').click()

        # STEP 3
        uCE(self.driver, f'return {GET_EBID}("register-company-name") !== null')
        exec_js(f'return {GET_EBID}("register-company-name")').send_keys(dataGenerator(10))
        exec_js(f'{GET_EBID}("register-country").value = "227: 230"') # Ukraine
        exec_js(f'return {GET_EBID}("register-continue-3")').click()
        console_log('Successfully!', OK)

        # STEP 4
        uCE(self.driver, f'return {GET_EBID}("register-back-4") !== null')
        console_log(f'\n{colorama.Fore.CYAN}Solve the captcha on the page manually!!!{colorama.Fore.RESET}', INFO, False)
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
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            if exec_js(f'return {GET_EBID}("registration-success") !== null'):
                console_log('Successfully!', OK)
                return True
            time.sleep(1)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        if isinstance(self.email_obj, CustomEmailAPI):
            token = parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{self.email_obj.class_name}] EBA-ESET-Token interception...', INFO)
            if isinstance(self.email_obj, (Hi2inAPI, TenMinuteMailAPI, TempMailAPI, GuerRillaMailAPI)):
                token = parseToken(self.email_obj, self.driver, True, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3) # 1secmail, developermail
        console_log(f'EBA-ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://eba.eset.com/Account/InitActivation?token={token}')
        untilConditionExecute(self.driver, f'return {GET_EBID}("username") !== null')
        console_log('Account successfully confirmed!', OK)

class EsetBusinessKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # Log in
        console_log('\nLogging in to the created account...', INFO)
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("dashboard-create-eca-trial") !== null', delay=2)
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
