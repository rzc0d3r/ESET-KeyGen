# v1.0.1 (171123-1541)
import modules.chrome_driver_installer as chrome_driver_installer
import modules.logger as logger

import modules.shared_tools as shared_tools
import modules.eset_register as eset_register
import modules.eset_keygen as eset_keygen
import modules.sec_email_api as sec_email_api

import datetime
import sys
import os

from subprocess import check_output, PIPE

def chrome_driver_installer_menu(): # auto updating or installing chrome driver
    logger.console_log('-- Chrome Driver Auto-Installer {0} --\n'.format(chrome_driver_installer.VERSION))
    chrome_version, _, _, _, _ = chrome_driver_installer.get_chrome_version()
    if chrome_version is None:
        raise RuntimeError('Chrome is not detected on your device!')
    current_chromedriver_version = None
    platform, _ = chrome_driver_installer.get_platform_for_chrome_driver()
    chromedriver_name = 'chromedriver.exe'
    if platform != 'win':
        chromedriver_name = 'chromedriver'
    if os.path.exists(chromedriver_name):
        os.chmod(chromedriver_name, 0o777)
        out = check_output([os.path.join(os.getcwd(), chromedriver_name), "--version"], stderr=PIPE)
        if out is not None:
            current_chromedriver_version = out.decode("utf-8").split(' ')[1]
    logger.console_log('Chrome version: {0}'.format(chrome_version), logger.INFO, False)
    logger.console_log('Chrome driver version: {0}'.format(current_chromedriver_version), logger.INFO, False)
    chromedriver_path = None
    if current_chromedriver_version is None:
        logger.console_log('\nChrome driver not detected, download attempt...', logger.ERROR)
    elif current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]: # major version match
        logger.console_log('\nChrome driver version doesn\'t match version of the installed chrome, trying to update...', logger.ERROR)
    if current_chromedriver_version is None or current_chromedriver_version.split('.')[0] != chrome_version.split('.')[0]:
        driver_url = chrome_driver_installer.get_driver_download_url()
        if driver_url is None:
            logger.console_log('\nCouldn\'t find the right version for your system!', logger.ERROR)
            if len(sys.argv) <= 1 or '--force' not in sys.argv:
                method = input('\nRun the program anyway? (y/n): ')
                if method == 'n':
                    return False
        else:
            logger.console_log('\nFound a suitable version for your system!', logger.OK)
            logger.console_log('\nDownload attempt...', logger.INFO)
            if chrome_driver_installer.download_chrome_driver('.', driver_url):
                logger.console_log('The Сhrome driver was successfully downloaded and unzipped!', logger.OK)
                chromedriver_path = os.path.join(os.getcwd(), chromedriver_name)
                if len(sys.argv) <= 1 or '--force' not in sys.argv:
                    input('\nPress Enter to continue...')
            else:
                logger.console_log('Error downloading or unpacking!', logger.ERROR)
                if len(sys.argv) <= 1 or '--force' not in sys.argv:
                    method = input('\nRun the program anyway? (y/n): ')
                    if method == 'n':
                        return False
    else:
        chromedriver_path = os.path.join(os.getcwd(), chromedriver_name)
    return chromedriver_path

if __name__ == '__main__':
    try:
        chromedriver_path = chrome_driver_installer_menu()
        only_account = False
        if len(sys.argv) > 1 and '--account' in sys.argv:
            logger.console_log('\n-- ESET Account Generator {0} --\n'.format(eset_register.VERSION))
            only_account = True
        else:
            logger.console_log('\n-- ESET KeyGen {0} --\n'.format(eset_keygen.VERSION))
        email_obj = sec_email_api.SecEmail()
        logger.console_log('Mail registration...', logger.INFO)
        email_obj.register()
        logger.console_log('Mail registration completed successfully!\n', logger.OK)
        eset_password = shared_tools.createPassword(6)
        EsetReg = eset_register.EsetRegister(email_obj, eset_password)
        EsetReg.initDriver(chromedriver_path)
        EsetReg.createAccount()
        EsetReg.confirmAccount()
        driver = EsetReg.returnDriver()
        output_line = f'\nEmail: {email_obj.get_full_login()}\nPassword: {eset_password}\n'
        output_filename = 'ESET ACCOUNTS.txt'
        if not only_account:
            EsetKeyG = eset_keygen.EsetKeygen(email_obj, driver)
            EsetKeyG.sendRequestForKey()
            license_name, license_out_date, license_key = EsetKeyG.getLicenseData()
            output_line = f'\nLicense Name: {license_name}\nLicense Out Date: {license_out_date}\nLicense Key: {license_key}\n'
            output_filename = 'ESET KEYS.txt'
        logger.console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
        f.write(output_line)
        f.close()
        driver.quit()
    except Exception as E:
        info = str(E)
        if str(type(E)).find('selenium') and info.find('Stacktrace:') != -1: # disabling stacktrace output
            logger.console_log(info.split('Stacktrace:', 1)[0], logger.ERROR)
        else:
            logger.console_log(str(E), logger.ERROR)
    input('Press Enter...')
