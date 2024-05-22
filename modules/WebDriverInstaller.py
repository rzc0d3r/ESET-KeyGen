from .SharedTools import console_log, INFO, OK, ERROR
from rich.progress import Progress

import subprocess
import platform
import requests
import zipfile
import tarfile
import shutil
import sys
import os

class WebDriverInstaller(object):
    def __init__(self, for_firefox=False):
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
            if for_firefox:
                self.platform[1] = ['macos']
            elif platform.processor() == "arm":
                self.platform[1] = ['mac-arm64', 'mac_arm64', 'mac64_m1']
            elif platform.processor() == "i386":
                self.platform[1] = ['mac64', 'mac-x64']
        if self.platform[0] == '' or self.platform[1] == []:
            raise RuntimeError('WebDriverInstaller: impossible to define the system!')
    
    def get_chrome_version(self):
        chrome_version = None
        if self.platform[0] == "linux":
            path = None
            for executable in ("google-chrome", "google-chrome-stable", "google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"):
                path = shutil.which(executable)
                if path is not None:
                    with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
                        chrome_version = proc.stdout.read().decode("utf-8").replace("Chromium", "").replace("Google Chrome", "").strip().split()[0]
        elif self.platform[0] == "mac":
            process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=subprocess.PIPE)
            chrome_version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
        elif self.platform[0] == "win":
            paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\",
                os.environ.get('LOCALAPPDATA')+"\\Google\\Chrome\\Application\\"
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
            raise RuntimeError('WebDriverInstaller: Google Chrome is not detected installed on your device!')
        return chrome_version

    def get_chromedriver_download_url(self, chrome_major_version=None):
        if chrome_major_version is None:
            chrome_major_version = self.get_chrome_version()[1]
        if int(chrome_major_version) >= 115: # for new drivers ( [115.0.0000.0, ...] )
            drivers_data = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
            drivers_data = drivers_data.json()['versions'][::-1] # start with the latest version
            for driver_data in drivers_data:
                driver_version = driver_data['version']
                driver_major_version = driver_version.split('.')[0] # major, _, minor, micro
                if driver_major_version == chrome_major_version: # return latest driver version for current major chrome version
                    for driver_url in driver_data['downloads'].get('chromedriver', None):
                            if driver_url['platform'] in self.platform[1]:
                                return driver_url['url']
        else: # for old drivers ( [..., 115.0.0000.0) )
            latest_old_driver_version = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}'.format(chrome_major_version))
            if latest_old_driver_version.status_code != 200:
                raise RuntimeError('WebDriverInstaller: the required chrome-webdriver was not found!')
            latest_old_driver_version = latest_old_driver_version.text
            driver_url = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_'.format(latest_old_driver_version)
            for arch in self.platform[1]:
                current_driver_url = driver_url+arch+'.zip'
                driver_size = requests.head(current_driver_url).headers.get('x-goog-stored-content-length', None)
                if driver_size is not None and int(driver_size) > 1024**2:
                    return current_driver_url
            raise RuntimeError('WebDriverInstaller: the required chrome-webdriver was not found!')
    
    def get_latest_geckodriver_download_url(self, only_version=False):
        r = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
        r_json = r.json()
        # note for: r_json['assets'][::-1]
        # in the initialization of WebDriverInstaller for 64bit is also suitable for 32bit, but
        # in the list of assets first go 32bit and it comes out that for 64bit gives a 32bit release, turning the list fixes it
        if only_version:
            return r_json['name']
        for asset in r_json['assets'][::-1]:
            if asset['name'].find('asc') == -1: # ignoring GPG Keys
                asset_arch = asset['name'].split('-', 2)[-1].split('.')[0] # package architecture parsing; geckodriver-v0.34.0-win32.zip -> ['geckodriver', 'v0.34.0', 'win32.zip'] -> ['win32', 'zip'] -> win32
                if asset_arch in self.platform[1]:
                    return asset['browser_download_url']

    def download_webdriver(self, path='.', url=None, edge=False, firefox=False):
        file_extension = '.zip'
        if url is None:
            if edge:
                url = self.get_edgedriver_download_url()
            elif firefox:
                url = self.get_latest_geckodriver_download_url()
            else:
                url = self.get_chromedriver_download_url()
        if url.find('.tar.gz') != -1:
            file_extension = '.tar.gz'
        # downloading
        zip_path = path.replace('\\', '/')+'/data'+file_extension
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:  # No content length header
            with open(zip_path, 'wb') as f:
                f.write(response.content)
        else:
            total_length = int(total_length)
            with Progress() as progress:
                task = progress.add_task("          ", total=total_length)
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
        if edge:
            webdriver_name = 'msedgedriver' # macOS, linux
        elif firefox:
            webdriver_name = 'geckodriver' # macOS, linux
        else:
            webdriver_name = 'chromedriver' # macOS, linux
        if self.platform[0].startswith('win'): # windows
            webdriver_name += '.exe'
        # extracting
        if file_extension == '.zip':
            with zipfile.ZipFile(zip_path, 'r') as zip:
                webdriver_zip_path = ''
                if not edge and not firefox: # Google Chrome
                    if len(zip.namelist()[0].split('/')) > 1: # for new Google Chrome webdriver zip format 
                        webdriver_zip_path = zip.namelist()[0].split('/')[0]+'/'
                with open(path+'/'+webdriver_name, 'wb') as f: # for Google Chrome and Microsoft Edge
                    f.write(zip.read(webdriver_zip_path+webdriver_name))
        elif file_extension == '.tar.gz':
            tar = tarfile.open(zip_path)
            tar.extractall()
            tar.close()
        try:
            os.remove(zip_path)
        except:
            pass
        return True
    
    def get_edge_version(self): # Only for windows
        edge_version = None
        paths = [
            'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
            'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
        ]
        for path in paths:
            if not os.path.exists(path):
                continue
            f = open(path, 'rb')
            for line in f.readlines()[::-1]:
                if line.find(b'" version="') != -1:
                    # <assemblyIdentity type="win32" name="124.0.2478.80" version="124.0.2478.80" language="*"/> ->
                    # ['<assemblyIdentity type="win32" name="124.0.2478.80" version', '="124.0.2478.80" language="*"/>'] ->
                    # ="124.0.2478.80" language="*"/> -> ['="', '124.0.2478.80', '" language="*"/>']
                    # 124.0.2478.80
                    edge_version = str(line).split('version')[-1].split('"')[1]
                    edge_version = [edge_version]+edge_version.split('.')
                    break
            f.close()
        if edge_version is None:
            raise RuntimeError('WebDriverInstaller: Microsoft Edge is not detected installed on your device!')
        return edge_version

    def get_edgedriver_download_url(self, edge_version=None):
        archs = self.platform[1]
        if edge_version is None:
            edge_version = self.get_edge_version()
        driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(edge_version[0])
        if requests.head(driver_url+'win32.zip').status_code != 200:
            console_log('Webdriver with identical version as the browser is not detected!!!', ERROR)
            console_log('Script runs an advanced search for a suitable webdriver...', INFO)
            for i in range(0, 150):
                tmp_edge_version = edge_version
                tmp_edge_version[-1] = str(i)
                tmp_edge_version = '.'.join(tmp_edge_version[1:])
                if requests.head(f'https://msedgedriver.azureedge.net/{tmp_edge_version}/edgedriver_win32.zip').status_code == 200:
                    # console_log('Another suitable version has been found!', OK)
                    driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(tmp_edge_version)
                    break
        for arch in archs:
            current_driver_url = driver_url+arch+'.zip'
            driver_size = requests.head(current_driver_url).headers.get('Content-Length', None)
            if driver_size is not None and int(driver_size) > 1024**2:
                return current_driver_url
        raise RuntimeError('WebDriverInstaller: the required edge-webdriver was not found!')
            
    def webdriver_installer_menu(self, edge=False, firefox=False): # auto updating or installing webdrivers
        if edge:
            browser_name = 'Microsoft Edge'
        elif firefox:
            browser_name = 'Mozilla Firefox'
        else:
            browser_name = 'Google Chrome'
        console_log('-- WebDriver Auto-Installer --\n'.format(browser_name))
        if edge:
            browser_version = self.get_edge_version()
        elif firefox:
            browser_version = ['Ignored', 'Ignored']
        else:
            browser_version = self.get_chrome_version()
        current_webdriver_version = None
        if edge:
            webdriver_name = 'msedgedriver'
        elif firefox:
            webdriver_name = 'geckodriver'
        else:
            webdriver_name = 'chromedriver'
        if self.platform[0] == 'win':
            webdriver_name += '.exe'
        webdriver_path = None
        if os.path.exists(webdriver_name):
            os.chmod(webdriver_name, 0o777)
            out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
            if out is not None:
                if edge:
                    current_webdriver_version = out.decode("utf-8").split(' ')[3]
                else: 
                    current_webdriver_version = out.decode("utf-8").split(' ')[1]
        console_log('{0} version: {1}'.format(browser_name, browser_version[0]), INFO, False)
        console_log('{0} webdriver version: {1}'.format(browser_name, current_webdriver_version), INFO, False)
        if firefox:
            latest_geckodriver_version = self.get_latest_geckodriver_download_url(True)
            if current_webdriver_version == latest_geckodriver_version:
                console_log('The webdriver has already been updated to the latest version!\n', OK)
                return os.path.join(os.getcwd(), webdriver_name)
            elif current_webdriver_version is not None:
                console_log(f'Updating the webdriver from {current_webdriver_version} to {latest_geckodriver_version} version...', INFO)
        if current_webdriver_version is None:
            console_log('{0} webdriver not detected, download attempt...'.format(browser_name), INFO)
        elif current_webdriver_version.split('.')[0] != browser_version[1] and not firefox: # major version match
            console_log('{0} webdriver version doesn\'t match version of the installed {1}, trying to update...'.format(browser_name, browser_name), ERROR)
        if (current_webdriver_version is None or current_webdriver_version.split('.')[0] != browser_version[1]) or firefox:
            if edge:
                driver_url = self.get_edgedriver_download_url()
            elif firefox:
                driver_url = self.get_latest_geckodriver_download_url()
            else:
                driver_url = self.get_chromedriver_download_url()
            if driver_url is not None:
                console_log('\nFound a suitable version for your system!', OK)
                console_log('Downloading...', INFO)
                if self.download_webdriver('.', driver_url, edge, firefox):
                    console_log('{0} webdriver was successfully downloaded and unzipped!\n'.format(browser_name), OK)
                    webdriver_path = os.path.join(os.getcwd(), webdriver_name)
                else:
                    console_log('Error downloading or unpacking!\n', ERROR)
        else:
            console_log('The webdriver has already been updated to the browser version!\n', OK)
            webdriver_path = os.path.join(os.getcwd(), webdriver_name)
        return webdriver_path