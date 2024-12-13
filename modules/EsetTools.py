from .EmailAPIs import *

from pathlib import Path

import subprocess
import colorama
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
        if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
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
            exec_js(f"return {GET_EBCN}('select__control ltr-13cymwt-control')[0]").click()
            for country in exec_js(f"return {GET_EBCN}('select__option ltr-uhiml7-option')"):
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
            console_log(f'\n[{self.email_obj.class_name}] ESET-HOME-Token interception...', INFO)
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                token = parseToken(self.email_obj, self.driver, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, max_iter=100, delay=3) # 1secmail, developermail
        console_log(f'ESET-HOME-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        try:
            uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        except:
            self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
            uCE(self.driver, 'return document.title === "ESET HOME"')
            uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver

class EsetKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, driver: Chrome, mode='ESET HOME'):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.mode = mode.upper()
        if self.mode not in ['ESET HOME', 'SMALL BUSINESS']:
            raise RuntimeError('Undefined keygen mode!')
        
    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
    
        console_log(f'\n[{self.mode}] Request sending...', INFO)
        self.driver.get('https://home.eset.com/subscriptions/choose-trial')
        uCE(self.driver, f"return {GET_EBAV}('button', 'data-label', 'subscription-choose-trial-ehsp-card-button') != null")
        if self.mode == 'ESET HOME':
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-ehsp-card-button'))")
        elif self.mode == 'SMALL BUSINESS':
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-esbs-card-button'))")
        try:
            for button in self.driver.find_elements('tag name', 'button'):
                if button.get_attribute('innerText').strip().lower() == 'continue':
                    exec_js(f'{GET_EBCN}("{button.get_attribute("class")}")[0].click()')
                    break
            else:
                raise RuntimeError('Continue button error!')
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'subscription-choose-trial-esbs-card-button'))")
            time.sleep(1)
            for button in self.driver.find_elements('tag name', 'button'):
                if button.get_attribute('innerText').strip().lower() == 'continue':
                    exec_js(f'{GET_EBCN}("{button.get_attribute("class")}")[0].click()')
                    break
            else:
                raise RuntimeError('Continue button error!')
            console_log(f'[{self.mode}] Request successfully sent!', OK)
        except:
            raise RuntimeError('Request sending error!!!')

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        console_log('\nLicense uploads...', INFO)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-info') != null", raise_exception_if_failed=False)
        if self.driver.current_url.find('detail') != -1:
            console_log(f'License ID: {self.driver.current_url[-11:]}', OK)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-product-name') != null", max_iter=10)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-model-additional-info') != null", max_iter=10)
        uCE(self.driver, f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-key') != null", max_iter=10)
        license_name = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-product-name').innerText")
        license_out_date = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-model-additional-info').innerText")
        license_key = exec_js(f"return {GET_EBAV}('div', 'data-label', 'license-detail-license-key').innerText")
        console_log('Information successfully received!', OK)
        return license_name, license_key, license_out_date

class EsetVPN(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, driver: Chrome, EsetRegister_window_handle=None):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.window_handle = EsetRegister_window_handle
        
    def sendRequestForVPNCodes(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute
        
        console_log('\nSending a request for VPN subscriptions...', INFO)
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
        uCE(self.driver, f'return {GET_EBAV}("ion-button", "robot", "choose-device-counter-increment-button") != null', max_iter=10)
        for _ in range(9): # increasing 'Number of devices' (to 10)
            exec_js(f'{GET_EBAV}("ion-button", "robot", "choose-device-counter-increment-button").click()')
        exec_js(f'{GET_EBAV}("button", "data-label", "choose-device-count-submit-button").click()')
        uCE(self.driver, f'return {GET_EBAV}("button", "data-label", "pwm-instructions-sent-download-button") != null', max_iter=15)
        console_log('Request successfully sent!', OK)
        return True
    
    def getVPNCodes(self):
        if isinstance(self.email_obj, CustomEmailAPI):
            console_log('\nWait for a message to your e-mail about instructions on how to set up the VPN!!!', WARN, True)
            return None
        else:
            console_log(f'\n[{self.email_obj.class_name}] VPN Codes interception...', INFO) # timeout 1.5m
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                vpn_codes = parseVPNCodes(self.email_obj, self.driver, delay=2, max_iter=45)
                self.driver.switch_to.window(self.window_handle)
            else:
                vpn_codes = parseVPNCodes(self.email_obj, self.driver, delay=2, max_iter=45) # 1secmail, developermail
                console_log('Information successfully received!', OK)
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
        console_log('\nLoading ESET ProtectHub Page...', INFO)
        if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
            self.driver.switch_to.new_window('EsetBusinessRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://protecthub.eset.com/public/registration?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("continue") != null')
        console_log('Successfully!', OK)

        # STEP 1
        console_log('\nData filling...', INFO)
        exec_js(f'return {GET_EBID}("email-input")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("company-name-input")').send_keys(dataGenerator(10))
        # Select country
        exec_js(f"return {GET_EBID}('country-select')").click()
        selected_country = 'Ukraine'
        for country in self.driver.find_elements('xpath', '//div[starts-with(@class, "select")]'):
            if country.text == selected_country:
                country.click()
                break
        exec_js(f'return {GET_EBID}("company-vat-input")').send_keys(dataGenerator(10, True))
        exec_js(f'return {GET_EBID}("company-crn-input")').send_keys(dataGenerator(10, True))
        console_log(f'\n{colorama.Fore.CYAN}Solve the captcha on the page manually!!!{colorama.Fore.RESET}', INFO, False)
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
            console_log('Successfully!', OK)
        except:
            raise RuntimeError('ESET has blocked your IP or email, try again later!!! Try to use VPN or try to change Email API!!!')
        return True

    def activateAccount(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # STEP 1
        console_log('\nData filling...', INFO)
        exec_js(f'return {GET_EBID}("first-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("last-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("first-name-input")').send_keys(dataGenerator(10))
        exec_js(f'return {GET_EBID}("password-input")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("password-repeat-input")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("continue").click()')

        # STEP 2
        uCE(self.driver, f'return {GET_EBID}("phone-input") != null')
        exec_js(f'return {GET_EBID}("phone-input")').send_keys(dataGenerator(10, True))
        exec_js(f'{GET_EBID}("tou-checkbox").click()')
        time.sleep(0.3)
        exec_js(f'return {GET_EBID}("continue").click()')
        uCE(self.driver, f'return {GET_EBID}("activated-user-title").innerText === "Your account has been successfully activated"', max_iter=15)
        console_log('Successfully!', OK)

    def confirmAccount(self):
        if isinstance(self.email_obj, CustomEmailAPI):
            token = parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3)
        else:
            console_log(f'\n[{self.email_obj.class_name}] ProtectHub-Token interception...', INFO)
            if isinstance(self.email_obj, WEB_WRAPPER_EMAIL_APIS_CLASSES):
                token = parseToken(self.email_obj, self.driver, True, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3) # 1secmail
        console_log(f'ProtectHub-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://protecthub.eset.com/public/activation/{token}/?culture=en-US')
        untilConditionExecute(self.driver, f'return {GET_EBID}("first-name-input") != null')
        console_log('Account successfully confirmed!', OK)

class EsetProtectHubKeygen(object):
    def __init__(self, registered_email_obj: OneSecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = untilConditionExecute

        # Log in
        console_log('\nLogging in to the created account...', INFO)
        self.driver.get('https://protecthub.eset.com')
        uCE(self.driver, f'return {GET_EBID}("username") != null')
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("welcome-dialog-generate-trial-license") != null', delay=3)
        console_log('Successfully!', OK)
        console_log('\nSending a request for a get license...', INFO)
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
                    console_log('Request successfully sent!', OK)
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
        
        console_log('\nWaiting for a back response...', INFO)
        license_was_generated = False
        for _ in range(DEFAULT_MAX_ITER*10): # 5m
            try:
                r = exec_js(f"return {GET_EBCN}('Toastify__toast-body toastBody')[0].innerText").lower()
                if r.find('couldn\'t be generated') != -1:
                    break
                elif r.find('was generated') != -1:
                    console_log('Successfully!', OK)
                    license_was_generated = True
                    break
            except Exception as E:
                pass
            time.sleep(DEFAULT_DELAY)

        if not license_was_generated:
            raise RuntimeError('The license cannot be generated, try again later!')

        # Obtaining license data from the site
        console_log('\n[Site] License uploads...', INFO)
        license_name = 'ESET PROTECT Advanced'
        try:
            self.driver.get('https://protecthub.eset.com/licenses')
            uCE(self.driver, f'return {GET_EBAV}("div", "data-label", "license-list-body-cell-renderer-row-0-column-0").innerText != ""')
            license_id = exec_js(f'{DEFINE_GET_EBAV_FUNCTION}\nreturn {GET_EBAV}("div", "data-label", "license-list-body-cell-renderer-row-0-column-0").innerText')
            console_log(f'License ID: {license_id}', OK)
            console_log('\nGetting information from the license...', INFO)
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
                        console_log('Information successfully received!', OK)
                        return license_name, license_key, license_out_date, True # True - License key obtained from the site
                except:
                    pass
                time.sleep(DEFAULT_DELAY)
        except Exception as E:
            console_log('Error when obtaining a license key from the site!!!', ERROR)
        # Obtaining license data from the email
        console_log('\n[Email] License uploads...', INFO)
        if self.email_obj.class_name == 'custom':
            console_log('\nWait for a message to your e-mail about successful key generation!!!', WARN, True)
            return None, None, None, None
        else:    
            license_key, license_out_date, license_id = parseEPHKey(self.email_obj, self.driver, delay=5, max_iter=30) # 2.5m 
            console_log(f'License ID: {license_id}', OK)
            console_log('\nGetting information from the license...', INFO)
            console_log('Information successfully received!', OK)
            return license_name, license_key, license_out_date, False # False - License key obtained from the email
    
    def removeLicense(self):
        console_log('Deleting the key from the account, the key will still work...', INFO)
        try:
            self.driver.execute_script(f'return {GET_EBID}("license-actions-button")').click()
            time.sleep(1)
            self.driver.execute_script(f'return {GET_EBID}("3-0-action_remove_license")').click()
            untilConditionExecute(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBID}("remove-license-dlg-remove-btn"))', max_iter=15)
            self.driver.execute_script(f'return {GET_EBID}("remove-license-dlg-remove-btn")').click()
            for _ in range(DEFAULT_MAX_ITER//2):
                if self.driver.page_source.lower().find('to keep the solutions up to date') == -1:
                    time.sleep(1)
                    console_log('Key successfully deleted!!!\n', OK)
                    return True
                time.sleep(DEFAULT_DELAY)
        except:
            pass
        console_log('Failed to delete key, this error has no effect on the operation of the key!!!\n', ERROR)

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
        console_log(f'ESET VPN has been successfully reset!!!', OK)
    except FileNotFoundError:
        console_log(f'The registry value or key does not exist: {key_path}\\{value_name}', ERROR)
    except PermissionError:
        console_log(f'Permission denied while accessing: {key_path}\\{value_name}', ERROR)
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
            console_log(f'ESET VPN has been successfully reset!!!', OK)
        else:
            console_log(f"File '{file_name}' does not exist!!!", ERROR)
    except Exception as e:
        raise RuntimeError(e)
