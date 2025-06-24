from .EmailAPIs import *

from pathlib import Path

import subprocess
import colorama
import logging
import time
import sys

SILENT_MODE = '--silent' in sys.argv

class IPBlockedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class EsetRegister(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        
        logging.info('[EMAIL] Register page loading...')
        console_log('\n[EMAIL] Register page loading...', INFO, silent_mode=SILENT_MODE)
        if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
            self.driver.switch_to.new_window('tab')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://login.eset.com/Register')
        uCE(self.driver, f"return {GET_EBID}('email') != null")
        logging.info('[EMAIL] Register page is loaded!')
        console_log('[EMAIL] Register page is loaded!', OK, silent_mode=SILENT_MODE)

        logging.info('Bypassing cookies...')
        console_log('\nBypassing cookies...', INFO, silent_mode=SILENT_MODE)
        if uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'id', 'cc-accept'))", max_iter=10, raise_exception_if_failed=False):
            logging.info('Cookies successfully bypassed!')
            console_log('Cookies successfully bypassed!', OK, silent_mode=SILENT_MODE)
            time.sleep(1) # Once pressed, you have to wait a little while. If code do not do this, the site does not count the acceptance of cookies
        else:
            logging.info('Cookies were not bypassed (it doesn\'t affect the algorithm, I think :D)')
            console_log("Cookies were not bypassed (it doesn't affect the algorithm, I think :D)", ERROR, silent_mode=SILENT_MODE)

        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.email)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-continue-button'))")
        time.sleep(1)
        try:
            if exec_js(f"return {GET_EBAV}('div', 'data-label', 'register-email-formGroup-validation')") is not None:
                raise RuntimeError(f'Email: {self.email_obj.email} is already registered!')
        except:
            pass
  
        logging.info('[PASSWD] Register page loading...')
        console_log('\n[PASSWD] Register page loading...', INFO, silent_mode=SILENT_MODE)
        uCE(self.driver, f"return typeof {GET_EBAV}('button', 'data-label', 'register-create-account-button') === 'object'")
        logging.info('[PASSWD] Register page is loaded!')
        console_log('[PASSWD] Register page is loaded!', OK, silent_mode=SILENT_MODE)
        exec_js(f"return {GET_EBID}('password')").send_keys(self.eset_password)
        
        # Select Ukraine country
        logging.info('Selecting the country...')
        if exec_js(f"return {GET_EBCN}('select__single-value css-1dimb5e-singleValue')[0]").text != 'Ukraine':
            exec_js(f"return {GET_EBCN}('select__control css-13cymwt-control')[0]").click()
            for country in exec_js(f"return {GET_EBCN}('select__option css-uhiml7-option')"):
                if country.text == 'Ukraine':
                    country.click()
                    logging.info('Country selected!')
                    break

        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-create-account-button'))")
        
        for _ in range(DEFAULT_MAX_ITER):
            title = exec_js('return document.title')
            if title == 'Service not available':
                raise IPBlockedException('\nESET temporarily blocked your IP, try again later!!! Try to use VPN/Proxy or try to change Email API!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        raise IPBlockedException('\nESET temporarily blocked your IP, try again later!!! Try to use VPN/Proxy or try to change Email API!!!')

    def confirmAccount(self):
        uCE = untilConditionExecute
        #uCE(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBAV}("ion-button", "data-r", "account-verification-email-modal-resend-email-btn"))') # accelerating the receipt of an eset token
        
        if isinstance(self.email_obj, CustomEmailAPI):
            token = parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            logging.info(f'[{self.email_obj.class_name}] ESET-HOME-Token interception...')
            console_log(f'\n[{self.email_obj.class_name}] ESET-HOME-Token interception...', INFO, silent_mode=SILENT_MODE)
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                token = parseToken(self.email_obj, self.driver, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, max_iter=100, delay=3) # 1secmail, developermail
        logging.info(f'ESET-HOME-Token: {token}')
        logging.info('Account confirmation is in progress...')
        console_log(f'ESET-HOME-Token: {token}', OK, silent_mode=SILENT_MODE)
        console_log('\nAccount confirmation is in progress...', INFO, silent_mode=SILENT_MODE)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title.includes("ESET HOME")')
        try:
            uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        except:
            self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
            uCE(self.driver, 'return document.title.includes("ESET HOME")')
            uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        logging.info('Account successfully confirmed!')
        console_log('Account successfully confirmed!', OK, silent_mode=SILENT_MODE)
        return True

class EsetKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, driver: Chrome, mode='ESET HOME'):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.mode = mode.upper()
        if self.mode not in ['ESET HOME', 'SMALL BUSINESS']:
            raise RuntimeError('Undefined keygen mode!')
        
    def sendRequestForKey(self):
        uCE = untilConditionExecute

        logging.info(f'[{self.mode}] Request sending...')
        console_log(f'\n[{self.mode}] Request sending...', INFO, silent_mode=SILENT_MODE)
        self.driver.get('https://home.eset.com/subscriptions/choose-trial')
        uCE(self.driver, f"return {GET_EBAV}('button', 'data-label', 'subscription-choose-trial-ehsp-card-button') != null")
        if self.mode == 'ESET HOME':
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-ehsp-card-button'))")
        elif self.mode == 'SMALL BUSINESS':
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-esbs-card-button'))")
        try:
            for button in self.driver.find_elements('tag name', 'button'):
                if button.get_attribute('innerText').strip().lower() == 'continue':
                    button.click()
                    break
                time.sleep(0.05)
            else:
                raise RuntimeError('Continue button error!')
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-esbs-card-button'))")
            time.sleep(1)
            for button in self.driver.find_elements('tag name', 'button'):
                if button.get_attribute('innerText').strip().lower() == 'continue':
                    button.click()
                    break
                time.sleep(0.05)
            else:
                raise RuntimeError('Continue button error!')
            logging.info(f'[{self.mode}] Request successfully sent!')
            console_log(f'[{self.mode}] Request successfully sent!', OK, silent_mode=SILENT_MODE)
        except:
            raise RuntimeError('Request sending error!!!')

    def getLD(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        logging.info(f'License uploads...')
        console_log('\nLicense uploads...', INFO, silent_mode=SILENT_MODE)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-info') != null", raise_exception_if_failed=False)
        if self.driver.current_url.find('detail') != -1:
            logging.info(f'License ID: {self.driver.current_url[-11:]}')
            console_log(f'License ID: {self.driver.current_url[-11:]}', OK, silent_mode=SILENT_MODE)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-product-name') != null", max_iter=10)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-model-additional-info') != null", max_iter=10)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-key') != null", max_iter=10)
        license_name = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-product-name').innerText")
        license_out_date = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-model-additional-info').innerText")
        license_key = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-key').innerText")
        logging.info('Information successfully received!')
        console_log('Information successfully received!', OK, silent_mode=SILENT_MODE)
        return license_name, license_key, license_out_date

class EsetVPN(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, driver: Chrome, EsetRegister_window_handle=None):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.window_handle = EsetRegister_window_handle
        
    def sendRequestForVPNCodes(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        
        logging.info('Sending a request for VPN subscriptions...')
        console_log('\nSending a request for VPN subscriptions...', INFO, silent_mode=SILENT_MODE)
        self.driver.get("https://home.eset.com/security-features")
        try:
            uCE(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBAV}("button", "data-label", "security-feature-explore-button"))', max_iter=10)
        except:
            raise RuntimeError('Explore-feature-button error!')
        time.sleep(0.5)
        for profile in exec_js(f'return {GET_EBAV}("button", "data-label", "choose-profile-tile-button", -1)'): # choose Me profile
            if profile.get_attribute("innerText").find(self.email_obj.email) != -1: # Me profile contains an email address
                profile.click()
        uCE(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBAV}("button", "data-label", "choose-profile-continue-btn"))', max_iter=5)
        uCE(self.driver, f'return {GET_EBAV}("button", "data-label", "choose-device-counter-increment-button") != null', max_iter=10)
        for _ in range(9): # increasing 'Number of devices' (to 10)
            exec_js(f'{GET_EBAV}("button", "data-label", "choose-device-counter-increment-button").click()')
        exec_js(f'{GET_EBAV}("button", "data-label", "choose-device-count-submit-button").click()')
        uCE(self.driver, f'return {GET_EBAV}("button", "data-label", "pwm-instructions-sent-download-button") != null', max_iter=15)
        logging.info('Request successfully sent!')
        console_log('Request successfully sent!', OK, silent_mode=SILENT_MODE)
        return True
    
    def getVPNCodes(self):
        if isinstance(self.email_obj, CustomEmailAPI):
            logging.warning('Wait for a message to your e-mail about instructions on how to set up the VPN!!!')
            console_log('\nWait for a message to your e-mail about instructions on how to set up the VPN!!!', WARN, True, SILENT_MODE)
            return None
        else:
            logging.info(f'[{self.email_obj.class_name}] VPN Codes interception...')
            console_log(f'\n[{self.email_obj.class_name}] VPN Codes interception...', INFO, silent_mode=SILENT_MODE) # timeout 1.5m
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                vpn_codes = parseVPNCodes(self.email_obj, self.driver, delay=2, max_iter=45)
                self.driver.switch_to.window(self.window_handle)
            else:
                vpn_codes = parseVPNCodes(self.email_obj, self.driver, delay=2, max_iter=45) # 1secmail, developermail
                logging.info('Information successfully received!')
                console_log('Information successfully received!', OK, silent_mode=SILENT_MODE)
        return vpn_codes

class EsetProtectHubRegister(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.eset_password = eset_password
        self.window_handle = None
        
    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        # STEP 0

        logging.info('Loading ESET ProtectHub Page...')
        console_log('\nLoading ESET ProtectHub Page...', INFO, silent_mode=SILENT_MODE)
        if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
            self.driver.switch_to.new_window('tab')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://protecthub.eset.com/public/registration?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("continue") != null')
        logging.info('Successfully!')
        console_log('Successfully!', OK, silent_mode=SILENT_MODE)

        # STEP 1
        logging.info('Data filling...')
        console_log('\nData filling...', INFO, silent_mode=SILENT_MODE)
        exec_js(f'return {GET_EBID}("email-input")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("company-name-input")').send_keys(dataGenerator(10))
        # Select country
        exec_js(f"return {GET_EBID}('country-select')").click()
        selected_country = 'Ukraine'
        logging.info('Selecting the country...')
        for country in self.driver.find_elements('xpath', '//div[starts-with(@class, "select")]'):
            if country.text == selected_country:
                country.click()
                logging.info('Country selected!')
                break
        exec_js(f'return {GET_EBID}("company-vat-input")').send_keys(dataGenerator(10, True))
        exec_js(f'return {GET_EBID}("company-crn-input")').send_keys(dataGenerator(10, True))
        logging.warning('Solve the captcha on the page manually!!!')
        console_log(f'\n{colorama.Fore.CYAN}Solve the captcha on the page manually!!!{colorama.Fore.RESET}', INFO, False, SILENT_MODE)
        while True: # captcha
            try:
                mtcaptcha_solved_token = exec_js(f'return {GET_EBCN}("mtcaptcha-verifiedtoken")[0].value')
                if mtcaptcha_solved_token.strip() != '':
                    break
            except Exception as E:
                pass
            time.sleep(1)
        exec_js(f'return {GET_EBID}("continue").click()')
        try:
            uCE(self.driver, f'return {GET_EBID}("registration-email-sent").innerText === "We sent you a verification email"', max_iter=10)
            logging.info('Successfully!')
            console_log('Successfully!', OK, silent_mode=SILENT_MODE)
        except:
            raise IPBlockedException('\nESET temporarily blocked your IP, try again later!!! Try to use VPN/Proxy or try to change Email API!!!')
        return True

    def activateAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # STEP 1
        logging.info('Data filling...')
        console_log('\nData filling...', INFO, silent_mode=SILENT_MODE)
        exec_js(f'return {GET_EBID}("first-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("last-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("first-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("password-input")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("password-repeat-input")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("continue").click()')

        # STEP 2
        uCE(self.driver, f'return {GET_EBID}("phone-input") != null')
        exec_js(f'return {GET_EBID}("phone-input")').send_keys(dataGenerator(10, True))
        time.sleep(0.5)
        exec_js(f'return {GET_EBID}("continue").click()')
        uCE(self.driver, f'return {GET_EBID}("activated-user-title").innerText === "Your account has been successfully activated"', max_iter=15)
        logging.info('Successfully!')
        console_log('Successfully!', OK, silent_mode=SILENT_MODE)

    def confirmAccount(self):
        if isinstance(self.email_obj, CustomEmailAPI):
            token = parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3)
        else:
            logging.info(f'[{self.email_obj.class_name}] ProtectHub-Token interception...')
            console_log(f'\n[{self.email_obj.class_name}] ProtectHub-Token interception...', INFO, silent_mode=SILENT_MODE)
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                token = parseToken(self.email_obj, self.driver, True, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3) # 1secmail
        logging.info(f'ProtectHub-Token: {token}')
        logging.info('Account confirmation is in progress...')
        console_log(f'ProtectHub-Token: {token}', OK, silent_mode=SILENT_MODE)
        console_log('\nAccount confirmation is in progress...', INFO, silent_mode=SILENT_MODE)
        self.driver.get(f'https://protecthub.eset.com/public/activation/{token}/?culture=en-US')
        untilConditionExecute(self.driver, f'return {GET_EBID}("first-name-input") != null')
        logging.info('Account successfully confirmed!')
        console_log('Account successfully confirmed!', OK, silent_mode=SILENT_MODE)

class EsetProtectHubKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def getLD(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # Log in
        logging.info('Logging in to the created account...')
        console_log('\nLogging in to the created account...', INFO, silent_mode=SILENT_MODE)
        self.driver.get('https://protecthub.eset.com')
        uCE(self.driver, f'return {GET_EBID}("username") != null')
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("welcome-dialog-generate-trial-license") != null', delay=3)
        logging.info('Successfully!')
        logging.info('Sending a request for a get license...')
        console_log('Successfully!', OK, silent_mode=SILENT_MODE)
        console_log('\nSending a request for a get license...', INFO, silent_mode=SILENT_MODE)
        try:
            exec_js(f'return {GET_EBID}("welcome-dialog-generate-trial-license").click()')
            exec_js(f'return {GET_EBID}("welcome-dialog-generate-trial-license")').click()
        except:
            pass
        
        # Waiting for a response from the site
        license_is_being_generated = False
        for _ in range(DEFAULT_MAX_ITER):
            try:
                r = exec_js(f"return {GET_EBCN}('Toastify__toast-body toastBody')[0].innerText").lower()
                if r.find('is being generated') != -1:
                    license_is_being_generated = True
                    logging.info('Request successfully sent!')
                    console_log('Request successfully sent!', OK, silent_mode=SILENT_MODE)
                    try:
                        exec_js(f'return {GET_EBID}("welcome-dialog-skip-button").click()')
                        exec_js(f'return {GET_EBID}("welcome-dialog-skip-button")').click()
                    except:
                        pass
                    break
            except Exception as E:
                pass
            time.sleep(DEFAULT_DELAY)
        
        if not license_is_being_generated:
            raise RuntimeError('The request has not been sent!')
        
        logging.info('Waiting for a back response...')
        console_log('\nWaiting for a back response...', INFO, silent_mode=SILENT_MODE)
        license_was_generated = False
        for _ in range(DEFAULT_MAX_ITER*10): # 5m
            try:
                r = exec_js(f"return {GET_EBCN}('Toastify__toast-body toastBody')[0].innerText").lower()
                if r.find('couldn\'t be generated') != -1:
                    break
                elif r.find('was generated') != -1:
                    logging.info('Successfully!')
                    console_log('Successfully!', OK, silent_mode=SILENT_MODE)
                    license_was_generated = True
                    break
            except Exception as E:
                pass
            time.sleep(DEFAULT_DELAY)

        if not license_was_generated:
            raise RuntimeError('The license cannot be generated, try again later!')

        # Obtaining license data from the site
        logging.info('[Site] License uploads...')
        console_log('\n[Site] License uploads...', INFO, silent_mode=SILENT_MODE)
        license_name = 'ESET PROTECT Advanced'
        try:
            self.driver.get('https://protecthub.eset.com/licenses')
            uCE(self.driver, f'return {GET_EBAV}("div", "data-label", "license-list-body-cell-renderer-row-0-column-0").innerText != ""')
            license_id = exec_js(f'{DEFINE_GET_EBAV_FUNCTION}\nreturn {GET_EBAV}("div", "data-label", "license-list-body-cell-renderer-row-0-column-0").innerText')
            logging.info(f'License ID: {license_id}')
            logging.info('Getting information from the license...')
            console_log(f'License ID: {license_id}', OK, silent_mode=SILENT_MODE)
            console_log('\nGetting information from the license...', INFO, silent_mode=SILENT_MODE)
            self.driver.get(f'https://protecthub.eset.com/licenses/details/2/{license_id}/overview')
            uCE(self.driver, f'return {GET_EBAV}("div", "data-label", "license-overview-validity-value") != null')
            license_out_date = exec_js(f'{DEFINE_GET_EBAV_FUNCTION}\nreturn {GET_EBAV}("div", "data-label", "license-overview-validity-value").children[0].children[0].innerText')
            # Obtaining license key
            exec_js(f'{DEFINE_GET_EBAV_FUNCTION}\n{GET_EBAV}("div", "data-label", "license-overview-key-value").children[0].children[0].click()')
            uCE(self.driver, f'return {GET_EBID}("show-license-key-auth-modal-password-input") != null')
            exec_js(f'return {GET_EBID}("show-license-key-auth-modal-password-input")').send_keys(self.eset_password)
            try:
                exec_js(f'return {GET_EBID}("show-license-key-auth-modal-authenticate").click()')
                exec_js(f'return {GET_EBID}("show-license-key-auth-modal-authenticate")').click()
            except:
                pass
            for _ in range(DEFAULT_MAX_ITER):
                try:
                    license_key = exec_js(f'return {GET_EBAV}("div", "data-label", "license-overview-key-value").children[0].textContent.trim()')
                    if license_key is not None and not license_key.startswith('XXXX-XXXX-XXXX-XXXX-XXXX'): # ignoring XXXX-XXXX-XXXX-XXXX-XXXX
                        license_key = license_key.split(' ')[0]
                        logging.info('Information successfully received!')
                        console_log('Information successfully received!', OK, silent_mode=SILENT_MODE)
                        return license_name, license_key, license_out_date, True # True - License key obtained from the site
                except:
                    pass
                time.sleep(DEFAULT_DELAY)
        except Exception as E:
            logging.critical("EXC_INFO:", exc_info=True)
            console_log('Error when obtaining a license key from the site!!!', ERROR, silent_mode=SILENT_MODE)
        # Obtaining license data from the email
        logging.info('[Email] License uploads...')
        console_log('\n[Email] License uploads...', INFO, silent_mode=SILENT_MODE)
        if self.email_obj.class_name == 'custom':
            logging.warning('Wait for a message to your e-mail about successful key generation!!!')
            console_log('\nWait for a message to your e-mail about successful key generation!!!', WARN, True, SILENT_MODE)
            return None, None, None, None
        else:    
            license_key, license_out_date, license_id = parseEPHKey(self.email_obj, self.driver, delay=5, max_iter=30) # 2.5m 
            logging.info(f'License ID: {license_id}')
            logging.info('Getting information from the license...')
            logging.info('Information successfully received!')
            console_log(f'License ID: {license_id}', OK, silent_mode=SILENT_MODE)
            console_log('\nGetting information from the license...', INFO, silent_mode=SILENT_MODE)
            console_log('Information successfully received!', OK, silent_mode=SILENT_MODE)
            return license_name, license_key, license_out_date, False # False - License key obtained from the email
    
    def removeLicense(self):
        logging.info('Deleting the key from the account, the key will still work...')
        console_log('Deleting the key from the account, the key will still work...', INFO, silent_mode=SILENT_MODE)
        try:
            self.driver.execute_script(f'return {GET_EBID}("license-actions-button")').click()
            time.sleep(1)
            button = self.driver.find_element('xpath', '//a[.//div[text()="Remove license"]]')
            if button is not None:
                button.click()
            untilConditionExecute(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBID}("remove-license-dlg-remove-btn"))', max_iter=15)
            time.sleep(2)
            for _ in range(DEFAULT_MAX_ITER//2):
                try:
                    self.driver.execute_script(f'return {GET_EBID}("remove-license-dlg-remove-btn")').click()
                except:
                    pass
                if self.driver.page_source.lower().find('to keep the solutions up to date') == -1:
                    time.sleep(1)
                    logging.info('Key successfully deleted!!!')
                    console_log('Key successfully deleted!!!', OK, silent_mode=SILENT_MODE)
                    return True
                time.sleep(DEFAULT_DELAY)
        except:
            pass
        logging.error('Failed to delete key, this error has no effect on the operation of the key!!!')
        console_log('Failed to delete key, this error has no effect on the operation of the key!!!', ERROR, silent_mode=SILENT_MODE)

def EsetVPNResetWindows(key_path='SOFTWARE\\ESET\\ESET VPN', value_name='authHash'):
    """Deletes the authHash value of ESET VPN"""
    try:
        subprocess.check_output(['taskkill', '/f', '/im', 'esetvpn.exe'], stderr=subprocess.DEVNULL)
    except:
        pass
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, value_name)
        logging.info('ESET VPN has been successfully reset!!!')
        console_log('ESET VPN has been successfully reset!!!', OK, silent_mode=SILENT_MODE)
    except FileNotFoundError:
        logging.error(f'The registry value or key does not exist: {key_path}\\{value_name}')
        console_log(f'The registry value or key does not exist: {key_path}\\{value_name}', ERROR, silent_mode=SILENT_MODE)
    except PermissionError:
        logging.error(f'Permission denied while accessing: {key_path}\\{value_name}')
        console_log(f'Permission denied while accessing: {key_path}\\{value_name}', ERROR, silent_mode=SILENT_MODE)
    except Exception as e:
        raise RuntimeError(e)

def EsetVPNResetMacOS(app_name='ESET VPN', file_name='Preferences/com.eset.ESET VPN.plist'):
    try:
        # Use AppleScript to quit the application
        script = f'tell application "{app_name}" to quit'
        subprocess.run(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    try:
        time.sleep(2)
        # Get the full path to the file in the Library folder
        library_path = Path.home() / "Library" / file_name
        # Check if the file exists and remove it
        if library_path.is_file():
            library_path.unlink()
            logging.info('ESET VPN has been successfully reset!!!')
            console_log('ESET VPN has been successfully reset!!!', OK, silent_mode=SILENT_MODE)
        else:
            logging.error(f"File '{file_name}' does not exist!!!")
            console_log(f"File '{file_name}' does not exist!!!", ERROR, silent_mode=SILENT_MODE)
    except Exception as e:
        raise RuntimeError(e)
