import sys

from platform import processor
from subprocess import Popen, check_output, PIPE, DEVNULL
from requests import get, head
from zipfile import ZipFile
from shutil import which
from os import remove

def get_platform():
    result = ['', []]
    if sys.platform.startswith('win'):
        result[0] = 'win'
        if sys.maxsize > 2**32:
            result[1] = ['win64', 'win32']
        else:
            result[2] = ['win32']
    elif sys.platform.startswith('linux'):
        result[0] = 'linux'
        if sys.maxsize > 2**32:
            result[1].append('linux64')
        else:
            result[1].append('linux32')
    elif sys.platform == "darwin":
        result[0] = 'mac'
        if processor() == "arm":
            result[1] = ['mac-arm64', 'mac_arm64', 'mac64_m1']
        elif processor() == "i386":
            result[1] = ['mac64', 'mac-x64']
    if result == ['', []]:
        return None
    return result

def get_chrome_version():
    platform = get_platform()[0]
    chrome_version = None
    if platform == "linux":
        path = None
        for executable in ("google-chrome", "google-chrome-stable", "google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"):
            path = which(executable)
            if path is not None:
                with Popen([path, "--version"], stdout=PIPE) as proc:
                    chrome_version = proc.stdout.read().decode("utf-8").replace("Chromium", "").replace("Google Chrome", "").strip().split()[0]
    elif platform == "mac":
        process = Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=PIPE)
        chrome_version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
    elif platform == "win":
        paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\"
        ]
        for path in paths:
            try:
                with open(path+'chrome.VisualElementsManifest.xml', 'r') as f:
                    for line in f.readlines():
                        line = line.strip()
                        if line.startswith('Square150x150Logo'):
                            chrome_version = line.split('=')[1].split('\\')[0][1:] 
                            break
            except:
                pass
    if chrome_version is not None:
        chrome_version = [chrome_version]+chrome_version.split('.') # [full, major, _, minor, micro]
    else:
        chrome_version = None
    return chrome_version

def get_chromedriver_download_url(chrome_major_version=None):
    _, archs = get_platform()
    if chrome_major_version is None:
        _, chrome_major_version, _, _, _ = get_chrome_version()
    if int(chrome_major_version) >= 115: # for new drivers ( [115.0.0000.0, ...] )
        drivers_data = get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
        drivers_data = drivers_data.json()['versions'][::-1] # start with the latest version
        for driver_data in drivers_data:
            driver_version = driver_data['version']
            driver_major_version, _, _, _ = driver_version.split('.') # major, _, minor, micro
            if driver_major_version == chrome_major_version: # return latest driver version for current major chrome version
                for driver_url in driver_data['downloads'].get('chromedriver', None):
                        if driver_url['platform'] in archs:
                            return driver_url['url']
    else: # for old drivers ( [..., 115.0.0000.0) )
        latest_old_driver_version = get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}'.format(chrome_major_version))
        if latest_old_driver_version.status_code != 200:
            return None
        latest_old_driver_version = latest_old_driver_version.text
        driver_url = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_'.format(latest_old_driver_version)
        for arch in archs:
            current_driver_url = driver_url+arch+'.zip'
            driver_size = head(current_driver_url).headers.get('x-goog-stored-content-length', None)
            if driver_size is not None and int(driver_size) > 1024**2:
                return current_driver_url

def download_webdriver(path, url=None, edge=False): # Only for Google Chrome (default) and Microsoft Edge (edge=True)
    if url is None:
        if edge:
            url = get_edgedriver_download_url()
        else:
            url = get_chromedriver_download_url()
    zip_path = path.replace('\\', '/')+'/data.zip'
    f = open(zip_path, 'wb')
    f.write(get(url).content)
    f.close()
    if edge:
        webdriver_name = 'msedgedriver' # macOS, linux
    else:
        webdriver_name = 'chromedriver' # macOS, linux
    if sys.platform.startswith('win'): # windows
        webdriver_name += '.exe'
    with ZipFile(zip_path, 'r') as zip:
        webdriver_zip_path = ''
        if not edge:
            if len(zip.namelist()[0].split('/')) > 1: # for new Google Chrome webdriver zip format 
                webdriver_zip_path = zip.namelist()[0].split('/')[0]+'/'
        with open(path+'/'+webdriver_name, 'wb') as f:
            f.write(zip.read(webdriver_zip_path+webdriver_name))
    remove(zip_path)
    return True

def get_edge_version(): # Only for windows
    cmd = 'powershell -Command "Get-ItemPropertyValue -Path "HKCU:\\SOFTWARE\\Microsoft\\Edge\\BLBeacon" -Name "version""'
    edge_version = None
    try:
        edge_version = check_output(cmd, stderr=DEVNULL).decode('utf-8').strip()
        edge_version = [edge_version]+edge_version.split('.') # [full, major, _, minor, micro]
    except:
        pass
    return edge_version

def get_edgedriver_download_url(edge_version=None):
    _, archs = get_platform()
    if edge_version is None:
        edge_version = get_edge_version()
    driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(edge_version[0])
    for arch in archs:
        current_driver_url = driver_url+arch+'.zip'
        driver_size = head(current_driver_url).headers.get('Content-Length', None)
        if driver_size is not None and int(driver_size) > 1024**2:
            return current_driver_url