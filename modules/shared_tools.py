# v1.0.2 (211123-1059)
from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService

from modules.logger import *

import subprocess
import time
import random
import string
import os

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

def untilConditionExecute(chrome_driver_obj: Chrome, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True):
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
            print(E)
        time.sleep(delay)

def createPassword(length):
    return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])

def initSeleniumWebDriver(browser_name: str, webdriver_path = None):
    driver_options = None
    driver = None
    if browser_name.lower() == 'chrome':
        driver_options = ChromeOptions()
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_options.add_argument("--log-level=3")
        driver_service = ChromeService(executable_path=webdriver_path)
        if os.name == 'posix': # For Linux
            console_log('Initializing chrome-driver for Linux', INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--disable-dev-shm-usage')
            driver_options.add_argument('--headless')
        elif os.name == 'nt':
            console_log('Initializing chrome-driver for Windows', INFO)
        driver = Chrome(options=driver_options, service=driver_service)
        driver.set_window_size(600, 600)
    elif browser_name.lower() == 'firefox':
        driver_options = FirefoxOptions()
        driver_options.log
        driver_service = FirefoxService(executable_path=webdriver_path)
        if os.name == 'posix': # For Linux
            console_log('Initializing firefox-driver for Linux', INFO)
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument("--disable-dev-shm-usage")
            driver_options.add_argument('-headless')
        else:
            console_log('Initializing firefox-driver for Windows', INFO)
        driver = Firefox(options=driver_options, service=driver_service)
        driver.set_window_size(600, 600)
    return driver