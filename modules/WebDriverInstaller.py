GOOGLE_CHROME = 'Google Chrome'
MICROSOFT_EDGE = 'Microsoft Edge'
MOZILLA_FIREFOX = 'Mozilla Firefox'

GOOGLE_CHROME_RE = r'(\d+\.\d+\.\d+\.\d+)'
MICROSOFT_EDGE_RE = r'(\d+\.\d+\.\d+\.\d+)'
MOZILLA_FIREFOX_RE = r'(\d+\.\d+\.\d+)|(\d+\.\d+)'

from .SharedTools import console_log, INFO, OK, ERROR, WARN
from .ProgressBar import ProgressBar, DEFAULT_RICH_STYLE

from pathlib import Path

from colorama import Fore, init
init()

import subprocess
import platform
import requests
import zipfile
import tarfile
import shutil
import sys
import re
import os

class WebDriverInstaller(object):
    def __init__(self, browser_name: str, custom_browser_location=None):
        self.browsers_data = {
            GOOGLE_CHROME: [self.get_chromedriver_url, 'chromedriver.exe' if sys.platform.startswith('win') else 'chromedriver', self.get_chrome_version, GOOGLE_CHROME_RE],
            MICROSOFT_EDGE: [self.get_msedgedriver_url, 'msedgedriver.exe' if sys.platform.startswith('win') else 'msedgedriver', self.get_edge_version, MICROSOFT_EDGE_RE],
            MOZILLA_FIREFOX: [self.get_geckodriver_url, 'geckodriver.exe' if  sys.platform.startswith('win') else 'geckodriver', self.get_firefox_version, MOZILLA_FIREFOX_RE]
        }
        self.browser_name = browser_name
        self.custom_browser_location = custom_browser_location
        if self.browser_name not in self.browsers_data:
            raise RuntimeError('WebDriverInstaller: invalid browser_name!')
        self.browser_data = self.browsers_data[self.browser_name]
        self.platform = ['', []] # [OC name, [webdriver architectures]]
        if sys.platform.startswith('win'):
            self.platform[0] = 'win'
            if sys.maxsize > 2**32:
                self.platform[1] = ['win64', 'win32']
            else:
                self.platform[1] = ['win32']
        elif sys.platform.startswith('linux'):
            self.platform[0] = 'linux'
            if sys.maxsize > 2**32:
                self.platform[1].append('linux64')
            else:
                self.platform[1].append('linux32')
        elif sys.platform == "darwin":
            self.platform[0] = 'mac'
            if self.browser_name == MOZILLA_FIREFOX:
                self.platform[1] = ['macos']
            elif platform.processor() == "arm":
                self.platform[1] = ['mac-arm64', 'mac_arm64', 'mac64_m1']
                if self.browser_name == MOZILLA_FIREFOX:
                    self.platform[1] = ['macos-aarch64']
            elif platform.processor() == "i386":
                self.platform[1] = ['mac64', 'mac-x64']
    
    def get_browser_version_from_cmd(self, path: str, re_pattern: str):
        try:
            with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
                return re.search(re_pattern, proc.communicate()[0].decode("utf-8")).group()
        except:
            pass

    def get_chrome_version(self):
        browser_version = None
        browser_path = None
        if self.platform[0] == "linux":
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, GOOGLE_CHROME_RE)
                browser_path = self.custom_browser_location
            else:
                for executable in ["google-chrome", "google-chrome-stable", "google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"]:
                    browser_version = self.get_browser_version_from_cmd(shutil.which(executable), GOOGLE_CHROME_RE)
                    if browser_version is not None:
                        browser_path = shutil.which(executable)
                        break
        elif self.platform[0] == "mac":
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, GOOGLE_CHROME_RE)
                browser_path = self.custom_browser_location
            else:
                browser_version = self.get_browser_version_from_cmd('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', GOOGLE_CHROME_RE)
                browser_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        elif self.platform[0] == "win":
            paths = [
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files\\Google\\Chrome\\Application',
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files (x86)\\Google\\Chrome\\Application',
                f'{os.environ.get("LOCALAPPDATA")}\\Google\\Chrome\\Application'
            ]
            if self.custom_browser_location is not None:
                paths = [str(Path(self.custom_browser_location).parent)]
            for path in paths:
                try:
                    with open(path+'\\chrome.VisualElementsManifest.xml', 'r') as f:
                        browser_version = re.search(GOOGLE_CHROME_RE, f.read()).group()
                        browser_path = path+'\\chrome.exe'
                        break
                except:
                    pass
        return [browser_version, browser_path]

    def get_chromedriver_url(self, chrome_major_version=None):
        if chrome_major_version is None:
            chrome_major_version = self.get_chrome_version()[0]
            if chrome_major_version is None:
                return None
            chrome_major_version = self.get_chrome_version()[0].split('.')[0]
        if int(chrome_major_version) >= 115: # for new drivers ( [115.0.0000.0, ...] )
            drivers_data = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
            drivers_data = drivers_data.json()['versions'][::-1] # start with the latest version
            for driver_data in drivers_data:
                driver_major_version = driver_data['version'].split('.')[0] # major, _, minor, micro
                if driver_major_version == chrome_major_version: # return latest driver version for current major chrome version
                    for driver_url in driver_data['downloads'].get('chromedriver', []):
                        if driver_url['platform'] in self.platform[1]:
                            return driver_url['url']
        else: # for old drivers ( [..., 115.0.0000.0) )
            latest_old_driver_version = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}'.format(chrome_major_version))
            if latest_old_driver_version.status_code == 200:
                latest_old_driver_version = latest_old_driver_version.text
                driver_url = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_'.format(latest_old_driver_version)
                for arch in self.platform[1]:
                    current_driver_url = driver_url+arch+'.zip'
                    driver_size = requests.head(current_driver_url).headers.get('x-goog-stored-content-length', None)
                    if driver_size is not None and int(driver_size) > 1024**2:
                        return current_driver_url
   
    def get_edge_version(self):
        browser_version = None
        browser_path = None
        if self.platform[0] == 'linux':
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, MICROSOFT_EDGE_RE)
                browser_path = self.custom_browser_location
            else:
                for executable in ['microsoft-edge']:
                    browser_version = self.get_browser_version_from_cmd(shutil.which(executable), MICROSOFT_EDGE_RE)
                    if browser_version is not None:
                        browser_path = shutil.which(executable)
                        break
        elif self.platform[0] == "mac":
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, MICROSOFT_EDGE_RE)
                browser_path = self.custom_browser_location
            else:
                browser_version = self.get_browser_version_from_cmd('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', MICROSOFT_EDGE_RE)
                browser_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
        elif self.platform[0] == 'win':
            paths = [
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files\\Microsoft\\Edge\\Application',
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files (x86)\\Microsoft\\Edge\\Application'
            ]
            if self.custom_browser_location is not None:
                paths = [str(Path(self.custom_browser_location).parent)]
            for path in paths:
                try:
                    with open(path+'\\msedge.VisualElementsManifest.xml', 'r') as f:
                        browser_version = re.search(MICROSOFT_EDGE_RE, f.read()).group()
                        browser_path = path+'\\msedge.exe'
                        break
                except:
                    pass
        return [browser_version, browser_path]

    def get_msedgedriver_url(self, edge_version=None):
        archs = self.platform[1]
        if edge_version is None:
            edge_version, _ = self.get_edge_version()
        major_version = edge_version.split('.')[0]
        if self.platform[0] == 'win':
            r = requests.get(f'https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}_WINDOWS')
        elif self.platform[0] == 'linux':
            r = requests.get(f'https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}_LINUX')
        elif self.platform[0] == 'mac':
            r = requests.get(f'https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}_MACOS')
        if r.status_code == 200:
            webdriver_version = r.text.strip()
            for arch in archs:
                driver_url = f'https://msedgedriver.azureedge.net/{webdriver_version}/edgedriver_{arch}.zip'
                driver_size = requests.head(driver_url).headers.get('Content-Length', None)
                if driver_size is not None and int(driver_size) > 1024**2:
                    return driver_url
    
    def get_firefox_version(self):
        browser_version = None
        browser_path = None
        if self.platform[0] == 'linux':
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, MOZILLA_FIREFOX_RE)
                browser_path = self.custom_browser_location
            else:
                for executable in ['firefox']:
                    browser_version = self.get_browser_version_from_cmd(shutil.which(executable), MOZILLA_FIREFOX_RE)
                    if browser_version is not None:
                        browser_path = shutil.which(executable)
                        break
        elif self.platform[0] == "mac":
            if self.custom_browser_location is not None:
                browser_version = self.get_browser_version_from_cmd(self.custom_browser_location, MOZILLA_FIREFOX_RE)
                browser_path = self.custom_browser_location
            else:
                for path in ['/Applications/Firefox.app/Contents/MacOS/firefox', '/application/firefox.app']:
                    if browser_version is not None:
                        browser_version = self.get_browser_version_from_cmd(path, MOZILLA_FIREFOX_RE)
                        browser_path = path
                        break
        elif self.platform[0] == 'win':
            paths = [
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files\\Mozilla Firefox',
                f'{os.environ.get("SYSTEMDRIVE")}\\Program Files (x86)\\Mozilla Firefox',
            ]
            if self.custom_browser_location is not None:
                paths = [str(Path(self.custom_browser_location).parent)]
            for path in paths:
                try:
                    with open(path+'\\application.ini', 'r') as f:
                        browser_version = re.search(MOZILLA_FIREFOX_RE, f.read()).group()
                        browser_path = path+'\\firefox.exe'
                        break
                except:
                    pass
        return [browser_version, browser_path]

    def get_geckodriver_url(self, only_version=False):
        r = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
        r_json = r.json()
        api_rate_limit = (True if r_json.get('name', None) is None else False)
        if api_rate_limit: # bypass for API rate limit exceeded for your IP
            r = requests.head("https://github.com/mozilla/geckodriver/releases/latest", allow_redirects=True)
            geckodriver_version = r.url.split('/')[-1][1:]
        else:
            geckodriver_version = r_json['name']
        if only_version:
            return geckodriver_version
        if not api_rate_limit:
            #https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-macos.tar.gz
            # note for: r_json['assets'][::-1]
            # in the initialization of WebDriverInstaller for 64bit is also suitable for 32bit, but
            # in the list of assets first go 32bit and it comes out that for 64bit gives a 32bit release, turning the list fixes it
            for asset in r_json['assets'][::-1]:
                if asset['name'].find('asc') == -1: # ignoring GPG Keys
                    asset_arch = asset['name'].split('-', 2)[-1].split('.')[0] # package architecture parsing; geckodriver-v0.34.0-win32.zip -> ['geckodriver', 'v0.34.0', 'win32.zip'] -> ['win32', 'zip'] -> win32
                    if asset_arch in self.platform[1]:
                        return asset['browser_download_url']
        else:
            # bypass for API rate limit exceeded for your IP
            extension = '.zip' if self.platform[0] == 'win' else '.tar.gz'
            for arch in self.platform[1]:
                url = f'https://github.com/mozilla/geckodriver/releases/download/v{geckodriver_version}/geckodriver-v{geckodriver_version}-{arch}{extension}'
                r = requests.get(url, stream=True)
                if int(r.headers.get('Content-Length', 0)) > 1024**2:
                    return url
                
    def download_webdriver(self, url=None, path='.', disable_progress_bar=False):
        # init
        webdriver_name = self.browser_data[1]
        file_extension = '.zip'
        if url is None:
            url = self.browser_data[0]()
            if url is None:
                return None
        if url.split('.')[-1] == 'gz':
            file_extension = '.tar.gz'
        # downloading
        archive_path = str(Path(f'{path}/data{file_extension}').resolve())
        response = requests.get(url, stream=True)
        if not disable_progress_bar:
            total_length = int(response.headers.get('Content-Length', 0))
            total_length = int(response.headers.get('content-length', total_length))
        else:
            total_length = 0
        if total_length == 0: # No content length header
            with open(archive_path, 'wb') as f:
                f.write(response.content)
        else:
            task = ProgressBar(int(total_length), '           ', DEFAULT_RICH_STYLE)
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks    
                        f.write(chunk)
                        task.update(len(chunk))
                        task.render()
        # extracting
        archive, info = None, []
        if file_extension == '.zip':
            archive = zipfile.ZipFile(archive_path)
            archive_info = archive.infolist()
        elif file_extension == '.tar.gz':
            archive = tarfile.open(archive_path)
            archive_info = archive.getnames()
        if archive is not None:
            for info in archive_info:
                archive_filename, archive_filepath = None, None
                if file_extension == '.zip':
                    archive_filename, archive_filepath = info.filename.split('/')[-1], info.filename
                else:
                    archive_filename, archive_filepath = info.split('/')[-1], info
                if archive_filename is not None and archive_filename == webdriver_name:
                    try:
                        archive.extract(info)
                        archive.close()
                        webdriver_path = str(Path(archive_filepath).resolve())
                        if Path(archive_filepath).resolve().parent != Path(os.getcwd()):
                            webdriver_path = shutil.copy2(str(Path(archive_filepath).resolve()), os.getcwd())
                        try:
                            shutil.rmtree(archive_filepath.split('/')[0], ignore_errors=True)
                            os.remove(archive_path)
                        except:
                            pass
                        os.chmod(webdriver_path, 0o777)
                        return webdriver_path
                    except:
                        return None
            
    def menu(self, disable_progress_bar=False): # auto updating or installing webdrivers
        def download():
            driver_url = self.browser_data[0]()
            if driver_url is not None:
                console_log('\nFound a suitable version for your system!', OK)
                console_log('Downloading...', INFO)
                if self.download_webdriver(driver_url, disable_progress_bar=disable_progress_bar):
                    console_log('{0} webdriver was successfully downloaded and unzipped!\n'.format(self.browser_name), OK)
                    return os.path.join(os.getcwd(), webdriver_name)
                else:
                    console_log('Error downloading or unpacking!\n', ERROR)
            else:
                console_log('\nA suitable version for your system was not found!\n', ERROR)
        console_log(f'{Fore.LIGHTMAGENTA_EX}-- WebDriver Auto-Installer --{Fore.RESET}\n')
        browser_version, browser_path = self.browser_data[2]()
        if browser_version is None:
            if self.custom_browser_location is None or self.custom_browser_location == '':
                raise RuntimeError(f'{self.browser_name} was not found in the standard catalogs!')
            raise RuntimeError(f'{self.custom_browser_location} is not a valid executable file of {self.browser_name}!')
        webdriver_name = self.browser_data[1]
        current_webdriver_version = None
        webdriver_path = None
        if os.path.exists(webdriver_name):
            try:
                out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
                out = re.search(self.browser_data[3], out.decode('utf-8'))
                if out is not None:
                    current_webdriver_version = out.group()
                    webdriver_path = os.path.join(os.getcwd(), webdriver_name)
            except:
                pass
        console_log('{0} version: {1}'.format(self.browser_name, browser_version), INFO, False)
        console_log('{0} webdriver version: {1}'.format(self.browser_name, current_webdriver_version), INFO, False)
        if self.browser_name == MOZILLA_FIREFOX:
            latest_geckodriver_version = self.browser_data[0](True)
            if current_webdriver_version == latest_geckodriver_version:
                console_log('The webdriver has already been updated to the latest version!\n', OK)
                webdriver_path = os.path.join(os.getcwd(), webdriver_name)
            else:
                console_log(f'Updating the webdriver from {current_webdriver_version} to {latest_geckodriver_version} version...', INFO)
                webdriver_path = download()
        else:
            if current_webdriver_version is None or (current_webdriver_version.split('.')[0] != browser_version.split('.')[0]): # major version match
                console_log('{0} webdriver version doesn\'t match version of the installed {1}, trying to download...'.format(self.browser_name, self.browser_name), WARN, True)
                webdriver_path = download()
            else:
                console_log('The webdriver has already been updated to the browser version!\n', OK)
        try:
            os.chmod(webdriver_path, 0o755)
        except:
            pass
        return [str(Path(webdriver_path).resolve()), str(Path(browser_path).resolve())]
