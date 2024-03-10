from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver import Edge, EdgeOptions, EdgeService

from .logger import *

import time
import random
import string
import os
import sys

GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
GET_EBTN = 'document.getElementByTagName'
GET_EBAV = 'getElementByAttrValue'

CLICK_WITH_BOOL = 'clickWithBool'

DEFINE_GET_EBAV_FUNCTION = """
function getElementByAttrValue(tagName, attrName, attrValue) {
    for (let element of document.getElementsByTagName(tagName)) {
        if(element.getAttribute(attrName) === attrValue)
            return element
    }
}
"""

DEFINE_CLICK_WITH_BOOL_FUNCTION = """
function clickWithBool(object) {
    try {
        object.click()
        return true
    }
    catch {
        return false
    }
}
"""

DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1

def untilConditionExecute(chrome_driver_obj: Chrome, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True, raise_exception_if_failed=True):
    chrome_driver_obj.execute_script(f'window.{GET_EBAV} = {DEFINE_GET_EBAV_FUNCTION}')
    chrome_driver_obj.execute_script(f'window.{CLICK_WITH_BOOL} = {DEFINE_CLICK_WITH_BOOL_FUNCTION}')
    pre_js = [
        DEFINE_GET_EBAV_FUNCTION,
        DEFINE_CLICK_WITH_BOOL_FUNCTION
    ]
    js = '\n'.join(pre_js+[js])
    for _ in range(max_iter):
        try:
            result = chrome_driver_obj.execute_script(js)
            if result == positive_result:
                return True
        except Exception as E:
            pass
        time.sleep(delay)
    if raise_exception_if_failed:
        raise RuntimeError('untilConditionExecute: the code did not return the desired value! TRY VPN!')

def createPassword(length, only_numbers=False):
    if only_numbers:
        return [random.choice(string.digits) for _ in range(length)]
    return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])

def initSeleniumWebDriver(browser_name: str, webdriver_path = None, browser_path = '', headless=True):
    driver_options = None
    driver = None
    if browser_name.lower() == 'chrome':
        driver_options = ChromeOptions()
        driver_options.binary_location = browser_path
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_options.add_argument("--lang=en-US")
        if headless:
            driver_options.add_argument('--headless')
        driver_service = ChromeService(executable_path=webdriver_path)
        if os.name == 'posix': # For Linux
            if sys.platform.startswith('linux'):
                console_log('Initializing chrome-webdriver for Linux', INFO)
            elif sys.platform == "darwin":
                console_log('Initializing chrome-webdriver for macOS', INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        elif os.name == 'nt':
            console_log('Initializing chrome-webdriver for Windows', INFO)
        driver = Chrome(options=driver_options, service=driver_service)
    elif browser_name.lower() == 'firefox':
        driver_options = FirefoxOptions()
        driver_options.binary_location = browser_path
        driver_service = FirefoxService(executable_path=webdriver_path)
        driver_options.set_preference('intl.accept_languages', 'en-US')
        if headless:
            driver_options.add_argument('--headless')
        if os.name == 'posix': # For Linux
            if sys.platform.startswith('linux'):
                console_log('Initializing firefox-webdriver for Linux', INFO)
            elif sys.platform == "darwin":
                console_log('Initializing firefox-webdriver for macOS', INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument("--disable-dev-shm-usage")
        else:
            console_log('Initializing firefox-webdriver for Windows', INFO)
        driver = Firefox(options=driver_options, service=driver_service,)
    elif browser_name.lower() == 'edge':
        driver_options = EdgeOptions()
        driver_options.use_chromium = True
        driver_options.binary_location = browser_path
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_options.add_argument("--lang=en-US")
        if headless:
            driver_options.add_argument('--headless')
        driver_service = EdgeService(executable_path=webdriver_path)
        if os.name == 'posix': # For Linux
            if sys.platform.startswith('linux'):
                console_log('Initializing edge-webdriver for Linux', INFO)
            elif sys.platform == "darwin":
                console_log('Initializing edge-webdriver for macOS', INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
        elif os.name == 'nt':
            console_log('Initializing edge-webdriver for Windows', INFO)
        driver = Edge(options=driver_options, service=driver_service)
    return driver
