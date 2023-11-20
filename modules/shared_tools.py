# v1.0.1 (191123-1002)
from selenium.webdriver import Chrome

import time
import random
import string

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

import traceback

def untilConditionExecute(chrome_driver_obj: Chrome, js, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True):
    chrome_driver_obj.execute_script(f'window.{GET_EBAV} = {DEFINE_GET_EBAV_FUNCTION}')
    chrome_driver_obj.execute_script(f'window.{CLICK_WITH_BOOL} = {DEFINE_CLICK_WITH_BOOL_FUNCTION}')
    if isinstance(js, list):
        js = '\n'.join(js)
    for _ in range(max_iter):
        try:
            result = chrome_driver_obj.execute_script(js)
            if result == positive_result:
                return True
        except Exception as E:
            traceback_string = traceback.format_exc()
            if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
                print(traceback_string.split('Stacktrace:', 1)[0])
        time.sleep(delay)

def createPassword(length):
    return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])