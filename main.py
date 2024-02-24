LOGO = """
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                Project Version: v1.3.2.1
                                                Project Devs: rzc0d3r, AdityaGarg8, k0re,
                                                              Fasjeit, alejanpa17, Ischunddu,
                                                              soladify
"""

import modules.webdriver_installer as webdriver_installer
import modules.logger as logger

import modules.shared_tools as shared_tools
import modules.eset_register as eset_register
import modules.eset_keygen as eset_keygen
import modules.sec_email_api as sec_email_api

import subprocess
import traceback
import platform
import datetime
import argparse
import sys
import os


def webdriver_installer_menu(edge=False): # auto updating or installing google chrome or microsoft edge webdrivers
    if edge:
        browser_name = 'Microsoft Edge'
    else:
        browser_name = 'Google Chrome'
    logger.console_log('-- WebDriver Auto-Installer --\n'.format(browser_name))
    if edge:
        browser_version = webdriver_installer.get_edge_version()
    else:
        browser_version = webdriver_installer.get_chrome_version()
    if browser_version is None:
        raise RuntimeError('{0} is not detected on your device!'.format(browser_name))
    current_webdriver_version = None
    platform = webdriver_installer.get_platform()[0]
    if edge:
        webdriver_name = 'msedgedriver'
    else:
        webdriver_name = 'chromedriver'
    if platform == 'win':
        webdriver_name += '.exe'
    if os.path.exists(webdriver_name):
        os.chmod(webdriver_name, 0o777)
        out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
        if out is not None:
            if edge:
                current_webdriver_version = out.decode("utf-8").split(' ')[3]
            else:
                current_webdriver_version = out.decode("utf-8").split(' ')[1]
    logger.console_log('{0} version: {1}'.format(browser_name, browser_version[0]), logger.INFO, False)
    logger.console_log('{0} webdriver version: {1}'.format(browser_name, current_webdriver_version), logger.INFO, False)
    webdriver_path = None
    if current_webdriver_version is None:
        logger.console_log('{0} webdriver not detected, download attempt...'.format(browser_name), logger.INFO)
    elif current_webdriver_version.split('.')[0] != browser_version[1]: # major version match
        logger.console_log('{0} webdriver version doesn\'t match version of the installed {1}, trying to update...'.format(browser_name, browser_name), logger.ERROR)
    if current_webdriver_version is None or current_webdriver_version.split('.')[0] != browser_version[1]:
        if edge:
            driver_url = webdriver_installer.get_edgedriver_download_url()
        else:
            driver_url = webdriver_installer.get_chromedriver_download_url()
        if driver_url is None:
            logger.console_log('\nCouldn\'t find the right version for your system!\n', logger.ERROR)
        else:
            logger.console_log('\nFound a suitable version for your system!', logger.OK)
            logger.console_log('Downloading...', logger.INFO)
            if webdriver_installer.download_webdriver('.', driver_url, edge):
                logger.console_log('{0} webdriver was successfully downloaded and unzipped!\n'.format(browser_name), logger.OK)
                webdriver_path = os.path.join(os.getcwd(), webdriver_name)
            else:
                logger.console_log('Error downloading or unpacking!\n', logger.ERROR)
    else:
        logger.console_log('The driver has already been updated to the browser version!\n', logger.OK)
        webdriver_path = os.path.join(os.getcwd(), webdriver_name)
    return webdriver_path

if __name__ == '__main__':
    print(LOGO)
    args_parser = argparse.ArgumentParser()
    # Required
    ## Browsers
    args_browsers = args_parser.add_mutually_exclusive_group(required=True)
    args_browsers.add_argument('--chrome', action='store_true', help='Launching the project via Google Chrome browser')
    args_browsers.add_argument('--firefox', action='store_true', help='Launching the project via Mozilla Firefox browser')
    args_browsers.add_argument('--edge', action='store_true', help='Launching the project via Microsoft Edge browser')
    ## Modes of operation
    args_modes = args_parser.add_mutually_exclusive_group(required=True)
    args_modes.add_argument('--key', action='store_true', help='Generating an antivirus license key')
    args_modes.add_argument('--account', action='store_true', help='Generating an antivirus account')
    args_modes.add_argument('--only-update', action='store_true', help='Updates/installs webdrivers and browsers without generating account and license key')
    # Optional
    args_parser.add_argument('--skip-webdriver-menu', action='store_true', help='Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)')
    args_parser.add_argument('--no-headless', action='store_true', help='Shows the browser at runtime (The browser is hidden by default, but on Windows 7 this option is enabled by itself)')
    args_parser.add_argument('--custom-browser-location', type=str, default='', help='Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition)')
    try:
        # changing input arguments for special cases
        if platform.release() == '7' and webdriver_installer.get_platform()[0] == 'win': # fix for Windows 7
            sys.argv.append('--no-headless')
        # initialization and configuration of everything necessary for work
        args = vars(args_parser.parse_args())
        driver = None
        webdriver_path = None
        browser_name = 'chrome'
        if args['firefox']:
            browser_name = 'firefox'
        if args['edge']:
            browser_name = 'edge'
        if not args['skip_webdriver_menu'] and browser_name != 'firefox': # updating or installing microsoft edge webdriver
            webdriver_path = webdriver_installer_menu(args['edge'])
            if webdriver_path is not None:
                os.chmod(webdriver_path, 0o777)
            if not args['only_update']:
                driver = shared_tools.initSeleniumWebDriver(browser_name, webdriver_path, args['custom_browser_location'], (not args['no_headless']))
            else:
                sys.exit(0)
        # main part of the program
        if args['account']:
            logger.console_log('\n-- Account Generator --\n')
        else:
            logger.console_log('\n-- KeyGen --\n')
        email_obj = sec_email_api.SecEmail()
        logger.console_log('Mail registration...', logger.INFO)
        email_obj.register()
        logger.console_log('Mail registration completed successfully!', logger.OK)
        eset_password = shared_tools.createPassword(6)
        EsetReg = eset_register.EsetRegister(email_obj, eset_password, driver)
        EsetReg.createAccount()
        EsetReg.confirmAccount()
        driver = EsetReg.returnDriver()
        output_line = f'\nEmail: {email_obj.get_full_login()}\nPassword: {eset_password}\n'
        output_filename = 'ESET ACCOUNTS.txt'
        if args['key']:
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
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        logger.console_log(traceback_string, logger.ERROR)
