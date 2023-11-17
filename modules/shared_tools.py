# v1.0.0 (191023-2057)
import time
import random
import string

GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'

DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1

def untilConditionExecute(chrome_driver_obj, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True):
    for _ in range(max_iter):
        try:
            result = chrome_driver_obj.execute_script(js)
            if result == positive_result:
                return True
        except Exception as E:
            pass
        time.sleep(delay)

def createPassword(length):
    return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])