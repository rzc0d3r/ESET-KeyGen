import contextlib
import logging
import pathlib
import json
import sys
import io

I_AM_EXECUTABLE = (True if (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) else False)
PATH_TO_SELF = sys.executable if I_AM_EXECUTABLE else __file__
CONFIG_PATH = pathlib.Path(PATH_TO_SELF).parent.resolve().joinpath('eset-keygen-config.json')
LOG_PATH = pathlib.Path(PATH_TO_SELF).parent.resolve().joinpath('ESET-KeyGen.log')
SILENT_MODE = '--silent' in sys.argv
MBCI_MODE = len(sys.argv) == 1

def enable_logging():
    logging.basicConfig(
        level=logging.INFO,
        filemode='w',
        filename=LOG_PATH,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

if ('--disable-logging' not in sys.argv and not MBCI_MODE) or ('--disable-logging' in sys.argv and SILENT_MODE): # Here it is present to catch an error when parsing arguments using argparse
    enable_logging()

from modules.EmailAPIs import *

# ---- Quick settings [for Developers to quickly change behavior without changing all files] ----
VERSION = ['v1.5.5.5', 1555]
LOGO = f"""
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                Project Version: {VERSION[0]}
                                                Project Devs: rzc0d3r, AdityaGarg8, k0re,
                                                              Fasjeit, alejanpa17, Ischunddu,
                                                              soladify, AngryBonk, Xoncia,
                                                              Anteneh13, otre4, AHDR3
"""
if '--no-logo' in sys.argv:
    LOGO = f"ESET KeyGen {VERSION[0]} by rzc0d3r\n"

DEFAULT_PATH_TO_PROXY_FILE = 'proxies.txt'
DEFAULT_EMAIL_API = 'guerrillamail'
AVAILABLE_EMAIL_APIS = ('1secmail', 'guerrillamail', 'developermail', 'mailticking', 'fakemail', 'inboxes', 'incognitomail')
WEB_WRAPPER_EMAIL_APIS = ('guerrillamail', 'mailticking', 'fakemail', 'inboxes', 'incognitomail')
EMAIL_API_CLASSES = {
    'guerrillamail': GuerRillaMailAPI,    
    '1secmail': OneSecEmailAPI,
    'developermail': DeveloperMailAPI,
    'mailticking': MailTickingAPI,
    'fakemail': FakeMailAPI,
    'inboxes': InboxesAPI,
    'incognitomail': IncognitoMailAPI
}

args = {
    'auto_detect_browser': True,
    'chrome': False,
    'firefox': False,
    'edge': False,
    'safari': False,

    'key': True,
    'small_business_key': False,
    'advanced_key': False,
    'vpn_codes': False,
    'account': False,
    'protecthub_account': False,
    'only_webdriver_update': False,
    'update': False,
    'reset_eset_vpn': False,
    'install': False,
    'return_exit_code': 0,

    'skip_webdriver_menu': False,
    'no_headless': False,
    'custom_browser_location': '',
    'email_api': DEFAULT_EMAIL_API,
    'custom_email_api': False,
    'skip_update_check': False,
    'no_logo': False,
    'disable_progress_bar': False,
    'disable_output_file': False,
    'repeat': 1,
    'proxy_file': DEFAULT_PATH_TO_PROXY_FILE,
    
    'silent': False,
    'disable_logging': False
}

MBCI_BROWSERS_ARGS = ['auto-detect-browser', 'chrome', 'firefox', 'edge', 'safari']
MBCI_MODES_OF_OPERATION_ARGS = [
    'key', 'small-business-key', 'advanced-key', 'vpn-codes', 'account',
    'protecthub-account', 'only-webdriver-update', 'reset-eset-vpn', 'update', 'install'
]
MBCI_OTHER_ARGS = [
    'skip_webdriver_menu', 'no_headless', 'custom_browser_location', 'custom_email_api',
    'skip_update_check', 'disable_progress_bar', 'disable_output_file', 'repeat', 'disable_logging',
    'proxy_file'
]
MBCI_ARGS = MBCI_BROWSERS_ARGS + MBCI_MODES_OF_OPERATION_ARGS + MBCI_OTHER_ARGS
# -----------------------------------------------------------------------------------------------

from modules.WebDriverInstaller import *

from modules.EsetTools import EsetRegister as ER
from modules.EsetTools import EsetKeygen as EK
from modules.EsetTools import EsetVPN as EV
from modules.EsetTools import EsetProtectHubRegister as EPHR
from modules.EsetTools import EsetProtectHubKeygen as EPHK
from modules.EsetTools import EsetVPNResetWindows as EVRW
from modules.EsetTools import EsetVPNResetMacOS as EVRM
from modules.EsetTools import IPBlockedException

from modules.SharedTools import *
from modules.MBCI import *

from modules.Updater import Updater

import traceback
import colorama
import platform
import datetime
import argparse
import re

# -----------------------------------------------------------------------------------------------

PATH_TO_SELF = sys.executable if I_AM_EXECUTABLE else __file__ # importing modules removes the original value of the variable
DRIVER = None
PROXIES = []
PROXIES_LEN = 0
PROXY_COUNTER = 1
PROXY_ERROR_COUNTER = 0
PROXY_ERROR_COUNTER_LIMIT = 3
CHROME_PROXY_EXTENSION_PATH = ""

class MBCIConfigManager:
    def __init__(self, path=CONFIG_PATH):
        self.path = path

    def save(self, args):
        config = {
            'Browser': [key for key in MBCI_BROWSERS_ARGS if args[key.replace('-', '_')]][0],
            'Mode of operation': [key for key in MBCI_MODES_OF_OPERATION_ARGS if args[key.replace('-', '_')]][0],
            'Email API': args['email_api']
        }
        
        for key in MBCI_OTHER_ARGS:
            config[key] = args[key]
        
        json.dump(config, open(CONFIG_PATH, 'w'), indent=4)
    
    def load(self):
        config = json.load(open(self.path))
        try:
            filtered_config = {}
            browser = config.pop('Browser')
            mode_of_operation = config.pop('Mode of operation')
            email_api = config.pop('Email API')
            if browser in MBCI_BROWSERS_ARGS:
                filtered_config[browser] = True
            if mode_of_operation in MBCI_MODES_OF_OPERATION_ARGS:
                filtered_config[mode_of_operation] = True
            if email_api in AVAILABLE_EMAIL_APIS:
                filtered_config['email_api'] = email_api
            for key in config:
                if key in MBCI_OTHER_ARGS:
                    filtered_config[key] = config[key]
            return filtered_config
        except:
            return False
    
    @property
    def is_exists(self):
        return os.path.isfile(self.path)

def RunMenu():
    MainMenu = ViewMenu(LOGO+'\n---- Main Menu ----')

    SettingMenu = ViewMenu(LOGO+'\n---- Settings Menu ----')
    SettingMenu.add_item(
        OptionAction(
            args,
            title='Browsers',
            action='store_true',
            args_names=MBCI_BROWSERS_ARGS,
            default_value=[key for key in MBCI_BROWSERS_ARGS if args[key.replace('-', '_')]][0]
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='Modes of operation',
            action='store_true',
            args_names=MBCI_MODES_OF_OPERATION_ARGS,
            default_value=[key for key in MBCI_MODES_OF_OPERATION_ARGS if args[key.replace('-', '_')]][0]
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='Email APIs',
            action='choice',
            args_names='email-api',
            choices=AVAILABLE_EMAIL_APIS,
            default_value=args['email_api']
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--skip-webdriver-menu',
            action='bool_switch',
            args_names='skip-webdriver-menu'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--no-headless',
            action='bool_switch',
            args_names='no-headless'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--custom-browser-location',
            action='manual_input',
            args_names='custom-browser-location',
            default_value=args['custom_browser_location']
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--custom-email-api',
            action='bool_switch',
            args_names='custom-email-api'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--skip-update-check',
            action='bool_switch',
            args_names='skip_update_check'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--disable-progress-bar',
            action='bool_switch',
            args_names='disable_progress_bar'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--disable-output-file',
            action='bool_switch',
            args_names='disable_output_file'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--disable-logging',
            action='bool_switch',
            args_names='disable_logging'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--repeat',
            action='manual_input',
            args_names='repeat',
            default_value=args['repeat'],
            data_type=int
        )
    ),
    SettingMenu.add_item(
        OptionAction(
            args,
            title='--proxy-file',
            action='manual_input',
            args_names='proxy-file',
            default_value=args['proxy_file']
        )
    )

    def exit_with_save_config():
        MBCIConfigManager().save(args)
        sys.exit()

    SettingMenu.add_item(MenuAction('Back', SettingMenu.close))
    MainMenu.add_item(MenuAction('Settings', SettingMenu))
    MainMenu.add_item(MenuAction('Start', MainMenu.close))
    MainMenu.add_item(MenuAction('Exit', exit_with_save_config))
    MainMenu.view()

def parse_argv(sys_argv=None):
    if '--return-exit-code' not in sys.argv and not SILENT_MODE and sys_argv is None:
        print(LOGO)
    if MBCI_MODE and sys_argv is None: # for MBCI mode
        RunMenu()
    else: # CLI
        args_parser = argparse.ArgumentParser()
        ENABLE_REQUIRED_ARGUMENTS = True
        GLOBAL_OVERRIDE_ARGUMENTS = ['--reset-eset-vpn', '--update',  '--install', '--return-exit-code']
        for argv in GLOBAL_OVERRIDE_ARGUMENTS:
            ENABLE_REQUIRED_ARGUMENTS = (argv not in sys.argv)
            if not ENABLE_REQUIRED_ARGUMENTS:
                break
        # Required
        ## Browsers
        args_browsers = args_parser.add_mutually_exclusive_group(required=ENABLE_REQUIRED_ARGUMENTS)   
        args_browsers.add_argument('--chrome', action='store_true', help='Launching the program via Google Chrome browser')
        args_browsers.add_argument('--firefox', action='store_true', help='Launching the program via Mozilla Firefox browser')
        args_browsers.add_argument('--edge', action='store_true', help='Launching the program via Microsoft Edge browser')
        args_browsers.add_argument('--safari', action='store_true', help='Launching the program via Apple Safari browser')
        args_browsers.add_argument('--auto-detect-browser', action='store_true', help='The program itself will determine which browser to use (from the list of supported browsers)')
        
        ## Modes of operation
        args_modes = args_parser.add_mutually_exclusive_group(required=ENABLE_REQUIRED_ARGUMENTS)
        args_modes.add_argument('--key', action='store_true', help='muimerP ytiruceS tramS TESE rof yek esnecil a gnitaerC'[::-1])
        args_modes.add_argument('--small-business-key', action='store_true', help=')secived 5 - yek 1( ytiruceS ssenisuB llamS TESE rof yek esnecil a gnitaerC'[::-1])
        args_modes.add_argument('--advanced-key', action='store_true', help=')secived 52 - yek 1( decnavdA TCETORP TESE rof yek esnecil a gnitaerC'[::-1])
        args_modes.add_argument('--vpn-codes', action='store_true', help='yek ytiruceS ssenisuB llamS TESE 1 + NPV TESE rof sedoc 01 gnitaerC'[::-1])
        args_modes.add_argument('--account', action='store_true', help=')noisrev lairt eerf eht etavitca ot( tnuoccA EMOH TESE a gnitaerC'[::-1])
        args_modes.add_argument('--protecthub-account', action='store_true', help=')noisrev lairt eerf eht etavitca ot( tnuoccA buHtcetorP TESE a gnitaerC'[::-1])
        args_modes.add_argument('--only-webdriver-update', action='store_true', help='yek esnecil dna tnuocca gnitareneg tuohtiw sresworb dna srevirdbew sllatsni/setadpU'[::-1])
        args_modes.add_argument('--reset-eset-vpn', action='store_true', help='!!!elbaliava era taht stnemugra lla sedirrevO - )ylno SOcam & swodniW( noitacilppa NPV TESE eht ni esnecil eht teser ot gniyrT'[::-1])
        args_modes.add_argument('--update', action='store_true', help='Switching to program update mode - Overrides all arguments that are available!!!')
        args_modes.add_argument('--install', action='store_true', help='Installs the program and adds it to the environment variable (Windows & macOS only) - Overrides all arguments that are available!!!')   
        args_modes.add_argument('--return-exit-code', type=int, default=0, help='[For developers] Will make the program return the exit code you requested - Overrides all arguments that are available!!!')
        # Optional
        args_parser.add_argument('--skip-webdriver-menu', action='store_true', help='Skips installation/upgrade webdrivers through the my custom wrapper (the built-in selenium-manager will be used)')
        args_parser.add_argument('--no-headless', action='store_true', help='Shows the browser at runtime (the browser is hidden by default, but on Windows 7 this option is enabled by itself)')
        args_parser.add_argument('--custom-browser-location', type=str, default='', help='Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition)')
        args_parser.add_argument('--email-api', choices=AVAILABLE_EMAIL_APIS, default=DEFAULT_EMAIL_API, help=f'Specify which api to use for mail, default - {DEFAULT_EMAIL_API}')
        args_parser.add_argument('--custom-email-api', action='store_true', help='Allows you to manually specify any email, and all work will go through it. But you will also have to manually read inbox and do what is described in the documentation for this argument')
        args_parser.add_argument('--skip-update-check', action='store_true', help='Skips checking for program updates')
        args_parser.add_argument('--no-logo', action='store_true', help='Replaces ASCII-Art with plain text')
        args_parser.add_argument('--disable-progress-bar', action='store_true', help='Disables the webdriver download progress bar')
        args_parser.add_argument('--disable-output-file', action='store_true', help='Disables the output txt file generation')
        args_parser.add_argument('--repeat', type=int, default=1, help='Specifies how many times to repeat generation')
        args_parser.add_argument('--proxy-file', type=str, default=DEFAULT_PATH_TO_PROXY_FILE, help=f'Specifies the path from where the list of proxies will be read from, default - {DEFAULT_PATH_TO_PROXY_FILE}')

        # Logging
        args_logging = args_parser.add_mutually_exclusive_group()
        args_logging.add_argument('--silent', action='store_true', help='Disables message output, output called by the --custom-email-api argument will still be output!')
        args_logging.add_argument('--disable-logging', action='store_true', help='Disables logging')

        parsed_args = None
        captured_stderr = io.StringIO()
        with contextlib.redirect_stderr(captured_stderr):
            try:
                parsed_args = vars(args_parser.parse_args(sys_argv))
                parsed_args['repeat'] = abs(parsed_args['repeat'])
                if sys_argv is None:
                    logging.info(f'Parsed arguments: {parsed_args}')
            except SystemExit:
                captured_stderr = captured_stderr.getvalue().strip()
                if captured_stderr != '':
                    if sys_argv is None:
                        logging.error(captured_stderr)
                    console_log(captured_stderr, silent_mode=SILENT_MODE)
                if sys_argv is None:
                    exit_program(-1)
        return parsed_args

def exit_program(exit_code, driver=None):
    if MBCI_MODE and not SILENT_MODE:
        input('\nPress Enter to exit...')
    if driver is not None:
        driver.quit()
    sys.exit(exit_code)

def update():
    Updater().updater_menu(I_AM_EXECUTABLE, PATH_TO_SELF)
    exit_program(0)

def main(disable_exit=False):
    global PROXY_ERROR_COUNTER_LIMIT
    global PROXY_ERROR_COUNTER
    global DRIVER
    if args['return_exit_code'] != 0:
        sys.exit(args['return_exit_code'])
    if MBCI_MODE and not disable_exit:
        print()
    try:
        # changing input arguments for special cases
        if not args['update'] and not args['install'] and not args['reset_eset_vpn']:
            if platform.release() == '7' and sys.platform.startswith('win'): # fix for Windows 7
                args['no_headless'] = True
            elif args['advanced_key'] or args['protecthub_account']:
                args['no_headless'] = True
                if not args['custom_email_api']:
                    if args['email_api'] not in ['mailticking', 'fakemail', 'inboxes', 'incognitomail']:
                        raise RuntimeError('--advanced-key, --protecthub-account works ONLY if you use the --custom-email-api argument or the following Email APIs: mailticking, fakemail, inboxes!!!')
        # check program updates
        elif args['update']:
            logging.info('-- Updater --')
            console_log(f'{Fore.LIGHTMAGENTA_EX}-- Updater --{Fore.RESET}\n', silent_mode=SILENT_MODE)
            update()
        elif args['reset_eset_vpn']:
            logging.info('-- Reset ESET VPN --')
            console_log(f'{Fore.LIGHTMAGENTA_EX}-- Reset ESET VPN --{Fore.RESET}\n', silent_mode=SILENT_MODE)
            if sys.platform.startswith('win'):
                EVRW()
            elif sys.platform == "darwin":
                EVRM()
            else:
                logging.error('This feature is for Windows and macOS only!!!')
                console_log('This feature is for Windows and macOS only!!!', ERROR, silent_mode=SILENT_MODE)
            exit_program(-2)
        elif args['install']:
            logging.info('-- Installer --')
            console_log(f'{Fore.LIGHTMAGENTA_EX}-- Installer --{Fore.RESET}\n', silent_mode=SILENT_MODE)
            Installer().install()
            exit_program(0)
        if not args['skip_update_check'] and not args['update']:
            try:
                logging.info('-- Updater --')
                console_log(f'{Fore.LIGHTMAGENTA_EX}-- Updater --{Fore.RESET}\n', silent_mode=SILENT_MODE)
                updater = Updater()
                latest_cloud_version = list(updater.get_releases().keys())[0]
                latest_cloud_version_int = latest_cloud_version[1:].split('.')
                latest_cloud_version_int = int(''.join(latest_cloud_version_int[:-1])+latest_cloud_version_int[-1][0])
                if VERSION[1] > latest_cloud_version_int:
                    logging.warning(f'The project has an unreleased version, maybe you are using a build from the developer?')
                    console_log(f'The project has an unreleased version, maybe you are using a build from the developer?\n', WARN, True, SILENT_MODE)
                elif latest_cloud_version_int > VERSION[1]:
                    logging.info(f'Project update is available up to version: {latest_cloud_version}')
                    if not SILENT_MODE:
                        console_log(f'Project update is available up to version: {colorama.Fore.GREEN}{latest_cloud_version}{colorama.Fore.RESET}', WARN)
                        update_now = input(f'[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Do you want to update right now? (y/n): {colorama.Fore.RESET}').strip().lower()
                        if update_now == 'y':
                            update()
                        else:
                            console_log(f'The update has been ignored\n', INFO)
                else:
                    logging.info('Project up to date!!!')
                    console_log('Project up to date!!!\n', OK, silent_mode=SILENT_MODE)
            except Exception as e:
                logging.error("EXC_INFO:", exc_info=True)
                #console_log(e, ERROR, silent_mode=SILENT_MODE)
        
        # initialization and configuration of everything necessary for work            
        webdriver_path = None
        browser_name = GOOGLE_CHROME
        custom_browser_location = None if args['custom_browser_location'] == '' else args['custom_browser_location']
        webdriver_installer = WebDriverInstaller(browser_name, custom_browser_location)

        if args['auto_detect_browser']:
            result = webdriver_installer.detect_installed_browser()
            if result is not None:
                browser_name = result[0]
                webdriver_installer = WebDriverInstaller(browser_name, custom_browser_location)
            else: # if a supported browser was not found, we try to use Selenium Manager
                args['skip_webdriver_menu'] = True 
        else:
            if args['chrome']:
                browser_name = GOOGLE_CHROME
                global CHROME_PROXY_EXTENSION_PATH
                if PROXIES != []:
                    CHROME_PROXY_EXTENSION_PATH = ChromeProxyExtensionManager.create_extension(*PROXIES[0])
                else:
                    CHROME_PROXY_EXTENSION_PATH = ''
            elif args['firefox']:
                browser_name = MOZILLA_FIREFOX
            elif args['edge']:
                browser_name = MICROSOFT_EDGE
            elif args['safari']:
                browser_name = APPLE_SAFARI
            webdriver_installer = WebDriverInstaller(browser_name, custom_browser_location)

        if browser_name == APPLE_SAFARI:
            args['skip_webdriver_menu'] = True

        if not args['skip_webdriver_menu']: # updating or installing webdriver
            webdriver_path, custom_browser_location = webdriver_installer.menu(args['disable_progress_bar'])
        if not args['only_webdriver_update']:
            DRIVER = initSeleniumWebDriver(browser_name, webdriver_path, custom_browser_location, CHROME_PROXY_EXTENSION_PATH, (not args['no_headless']))
            if DRIVER is None:
                raise RuntimeError(f'{browser_name} initialization error!')
            if PROXIES != []:
                scheme, host, port, username, password = PROXIES[0]
                global PROXY_COUNTER
                if username != '' or password != '':
                    logging.info(f'[{PROXY_COUNTER}/{PROXIES_LEN}] Using proxy with authentication: {host}:{port}')
                    console_log(f'[{PROXY_COUNTER}/{PROXIES_LEN}] Using proxy with authentication: {host}:{port}', INFO, silent_mode=SILENT_MODE)
                else:
                    logging.info(f'[{PROXY_COUNTER}/{PROXIES_LEN}] Using proxy: {host}:{port}')
                    console_log(f'[{PROXY_COUNTER}/{PROXIES_LEN}] Using proxy: {host}:{port}', INFO, silent_mode=SILENT_MODE)
        else:
            sys.exit(0)

        # main part of the program
        logging.info(f'-- KeyGen --')
        console_log(f'\n{Fore.LIGHTMAGENTA_EX}-- KeyGen --{Fore.RESET}\n', silent_mode=SILENT_MODE)
        if not args['custom_email_api']:
            logging.info(f'[{args["email_api"]}] Mail registration...')
            console_log(f'[{args["email_api"]}] Mail registration...', INFO, silent_mode=SILENT_MODE)
            if args['email_api'] in WEB_WRAPPER_EMAIL_APIS: # WebWrapper API, need to pass the selenium object to the class initialization
                email_obj = EMAIL_API_CLASSES[args['email_api']](DRIVER)
            else: # real APIs without the need for a browser
                email_obj = EMAIL_API_CLASSES[args['email_api']]()
            try:
                email_obj.init()
                if email_obj.email is not None:
                    logging.info('Mail registration completed successfully!')
                    console_log('Mail registration completed successfully!', OK, silent_mode=SILENT_MODE)
            except:
                pass
            if email_obj.email is None:
                logging.critical('Mail registration was not completed, try using a different Email API!')
                console_log('Mail registration was not completed, try using a different Email API!\n', ERROR, silent_mode=SILENT_MODE)
                PROXY_ERROR_COUNTER += 1
        else:
            email_obj = CustomEmailAPI()
            while True:
                email = input(f'[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Enter the email address you have access to: {colorama.Fore.RESET}').strip()
                try:
                    matched_email = re.match(r'[-a-z0-9+.]+@[a-z]+(\.[a-z]+)+', email).group()
                    if matched_email == email:
                        email_obj.email = matched_email
                        console_log('Mail has the correct syntax!', OK)
                        break
                    else:
                        raise RuntimeError
                except:
                    console_log('Invalid email syntax!!!', ERROR)
        
        if email_obj.email is not None:
            e_passwd = dataGenerator(10)
            l_key = None
            obtained_from_site = False
            # ESET HOME
            if args['account'] or args['key'] or args['small_business_key'] or args['vpn_codes']:
                ER_obj = ER(email_obj, e_passwd, DRIVER)
                ER_obj.createAccount()
                ER_obj.confirmAccount()
                output_line = '\n'.join([
                    '',
                    '-------------------------------------------------',
                    '}{ :liamE tnuoccA'[::-1].format(email_obj.email),
                    '}{ :drowssaP tnuoccA'[::-1].format(e_passwd),
                    '-------------------------------------------------',
                    ''
                ])
                output_filename = 'ESET ACCOUNTS.txt'
                if args['key'] or args['small_business_key'] or args['vpn_codes']:
                    output_filename = 'ESET KEYS.txt'
                    EK_obj = EK(email_obj, DRIVER, 'ESET HOME' if args['key'] else 'SMALL BUSINESS')
                    EK_obj.sendRequestForKey()
                    l_name, l_key, l_out_date = EK_obj.getLD()
                    output_line = '\n'.join([
                        '',
                        '-------------------------------------------------',
                        '}{ :liamE tnuoccA'[::-1].format(email_obj.email),
                        '}{ :drowssaP tnuoccA'[::-1].format(e_passwd),
                        '',
                        '}{ :emaN esneciL'[::-1].format(l_name),
                        '}{ :yeK esneciL'[::-1].format(l_key),
                        '}{ :etaD tuO esneciL'[::-1].format(l_out_date),
                        '-------------------------------------------------',
                        ''
                    ])
                    if args['vpn_codes']:
                        EV_obj = EV(email_obj, DRIVER, ER_obj.window_handle)
                        EV_obj.sendRequestForVPNCodes()
                        vpn_codes = EV_obj.getVPNCodes()
                        if not args['custom_email_api']:
                            vpn_codes_line = ', '.join(vpn_codes)
                            output_line = '\n'.join([
                                '',
                                '-------------------------------------------------',
                                '}{ :liamE tnuoccA'[::-1].format(email_obj.email),
                                '}{ :drowssaP tnuoccA'[::-1].format(e_passwd),
                                '',
                                '}{ :emaN esneciL'[::-1].format(l_name),
                                '}{ :yeK esneciL'[::-1].format(l_key),
                                '}{ :etaD tuO esneciL'[::-1].format(l_out_date),
                                '',
                                '}{ :sedoC NPV'[::-1].format(vpn_codes_line),
                                '-------------------------------------------------',
                                ''
                            ])

            # ESET ProtectHub
            elif args['protecthub_account'] or args['advanced_key']:
                EPHR_obj = EPHR(email_obj, e_passwd, DRIVER)
                EPHR_obj.createAccount()
                EPHR_obj.confirmAccount()
                EPHR_obj.activateAccount()
                output_line = '\n'.join([
                    '',
                    '---------------------------------------------------------------------',
                    '}{ :liamE tnuoccA buHtcetorP TESE'[::-1].format(email_obj.email),
                    '}{ :drowssaP tnuoccA buHtcetorP TESE'[::-1].format(e_passwd),
                    '---------------------------------------------------------------------',
                    ''
                ])    
                output_filename = 'ESET ACCOUNTS.txt'
                if args['advanced_key']:
                    output_filename = 'ESET KEYS.txt'
                    EPHK_obj = EPHK(email_obj, e_passwd, DRIVER)
                    l_name, l_key, l_out_date, obtained_from_site = EPHK_obj.getLD()
                    if l_name is not None:
                        output_line = '\n'.join([
                            '',
                            '---------------------------------------------------------------------',
                            '}{ :liamE tnuoccA buHtcetorP TESE'[::-1].format(email_obj.email),
                            '}{ :drowssaP tnuoccA buHtcetorP TESE'[::-1].format(e_passwd),
                            '',
                            '}{ :emaN esneciL'[::-1].format(l_name),
                            '}{ :yeK esneciL'[::-1].format(l_key),
                            '}{ :etaD tuO esneciL'[::-1].format(l_out_date),
                            '---------------------------------------------------------------------',
                            ''
                        ])

            # end
            logging.info(output_line)
            console_log(output_line, silent_mode=SILENT_MODE)
            if not args['disable_output_file']:
                date = datetime.datetime.now()
                f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
                f.write(output_line)
                f.close()
            
            if l_key is not None and args['advanced_key'] and obtained_from_site:
                if not SILENT_MODE:
                    unbind_key = input(f'[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Do you want to unbind the key from this account? (y/n): {colorama.Fore.RESET}').strip().lower()
                    if unbind_key == 'y':
                        EPHK_obj.removeLicense()
                else:
                    EPHK_obj.removeLicense()
    except IPBlockedException:
        logging.critical("EXC_INFO:", exc_info=True)
        traceback_string = traceback.format_exc()
        if PROXIES != []:
            PROXIES.remove(PROXIES[0])
            if PROXY_COUNTER < PROXIES_LEN:
                PROXY_COUNTER += 1
        console_log(traceback_string, ERROR, silent_mode=SILENT_MODE)
    except Exception as E:
        PROXY_ERROR_COUNTER_LIMIT += 1
        logging.critical("EXC_INFO:", exc_info=True)
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        console_log(traceback_string, ERROR, silent_mode=SILENT_MODE)

    if PROXIES != [] and PROXY_ERROR_COUNTER == PROXY_ERROR_COUNTER_LIMIT:
        PROXY_ERROR_COUNTER = 0
        PROXIES.remove(PROXIES[0])
        if PROXY_COUNTER < PROXIES_LEN:
            PROXY_COUNTER += 1

    if globals().get('DRIVER', None) is not None:
        DRIVER.quit()
    if not disable_exit:
        exit_program(0)

if __name__ == '__main__':
    if MBCI_MODE:
        config_manager = MBCIConfigManager()
        if config_manager.is_exists:
            try:
                config_args = config_manager.load()
                # converting args(dict) to sys.argv for argparse
                config_sys_argv = []
                for key, value in config_args.items():
                    if isinstance(value, bool) and not value:
                        continue
                    config_sys_argv.append('--'+key.replace('_', '-'))
                    if not isinstance(value, bool):
                        config_sys_argv.append(str(value))
                # check config integrity with argparse
                parsed_args = parse_argv(config_sys_argv)
                if parsed_args is not None:
                    args = parsed_args
                else:
                    raise RuntimeError
            except:
                console_log("\nError loading the config, check its integrity!!!", WARN)
                input('\nPress Enter to continue...')
        parse_argv() # run MBCI
        args['repeat'] = abs(args['repeat'])
        try:
            config_manager.save(args)
        except:
            console_log("\nError saving configuration, check write access!!!", WARN)
            input('\nPress Enter to continue...')
    else:
        args = parse_argv() # CLI
    
    if args['disable_logging']:
        logging.basicConfig(level=logging.CRITICAL+1)
    else:
        enable_logging()

    logging.info(f'ESET-KeyGen Version: text={VERSION[0]}, index={VERSION[1]}')
    logging.info(f'I_AM_EXECUTABLE={I_AM_EXECUTABLE}, OS={os.name}')
    logging.info(f'sys.argv: {sys.argv}')

    # load proxies from file
    result = WebDriverInstaller(GOOGLE_CHROME).detect_installed_browser()
    if result is not None:
        browser_name = result[0]
    if browser_name == GOOGLE_CHROME and os.path.exists(args['proxy_file']) and os.path.isfile(args['proxy_file']):
        PROXIES = ChromeProxyExtensionManager.parse_proxies_from_file(args['proxy_file'])
        PROXIES_LEN = len(PROXIES)
        #random.shuffle(PROXIES)

    if args['repeat'] == 1 or args['repeat'] == 0:
        main()
    else:
        args['skip_update_check'] = True
        for i in range(args['repeat']):
            try:
                logging.info(f'------------ Initializing of {i+1} start ------------')
                console_log(f'\n{Fore.MAGENTA}------------ Initializing of {Fore.YELLOW}{i+1} {Fore.MAGENTA}start ------------{Fore.RESET}\n', silent_mode=SILENT_MODE)
                if i == 0: # the first run sets up the environment for subsequent runs, speeding them up
                    main(disable_exit=True)
                    args['skip_webdriver_menu'] = True
                elif i+1 == args['repeat']:
                    main()
                else:
                    main(disable_exit=True)
            except KeyboardInterrupt:
                exit_program(0, DRIVER)
