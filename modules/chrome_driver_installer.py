import sys

from platform import processor
from subprocess import Popen, PIPE
from requests import get, head
from zipfile import ZipFile
from shutil import which
from os import remove

def get_platform_for_chrome_driver():
    result = ['', []]
    if sys.platform.startswith('win'):
        result[0] = 'win'
        if sys.maxsize > 2**32:
            result[1].append('win64')
        else:
            result[1].append('win32')
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
    platform = get_platform_for_chrome_driver()[0]
    chrome_version = None
    if platform == "linux":
        path = None
        for executable in ("google-chrome", "google-chrome-stable","google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"):
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
        chrome_version = [chrome_version]+chrome_version.split('.')
    else:
        chrome_version = [None, None, None, None, None]
    return chrome_version # [full, major, _, minor, micro]

def get_driver_download_url(chrome_major_version=None):
    _, archs = get_platform_for_chrome_driver()
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
        driver_url = 'https://chromedriver.storage.googleapis.com/index.html?path={0}/chromedriver_'.format(latest_old_driver_version)
        for arch in archs:
            if head(driver_url+arch).headers.get(['x-goog-stored-content-length'], None) is not None:
                return driver_url+arch

def download_chrome_driver(path, url=None):
    if url is None:
        url = get_driver_download_url()
    zip_path = path.replace('\\', '/')+'/data.zip'
    f = open(zip_path, 'wb')
    f.write(get(url).content)
    f.close()
    with ZipFile(zip_path, 'r') as zip:
        chromedriver_zip_path = ''
        chromedriver_name = 'chromedriver' # macOS, linux
        if sys.platform.startswith('win'): # windows
            chromedriver_name = 'chromedriver.exe'
        if len(zip.namelist()[0].split('/')) > 1: # for new zip driver format 
            chromedriver_zip_path = zip.namelist()[0].split('/')[0]+'/'
        with open(path+'/'+chromedriver_name, 'wb') as f:
            f.write(zip.read(chromedriver_zip_path+chromedriver_name))
    remove(zip_path)
    return True
