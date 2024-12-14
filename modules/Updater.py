from .SharedTools import console_log, INFO, OK, ERROR, WARN
from .ProgressBar import ProgressBar, DEFAULT_RICH_STYLE

import subprocess
import requests
import zipfile
import pathlib
import sys
import os

WINDOWS_EXTERNAL_UPDATER = """
@echo off

timeout 1 >nul 2>&1

echo.
echo --- ESET-KeyGen External-Updater ---
echo.

echo !!! Make sure you are running the program with elevated permissions, else update will fail !!!
echo.
echo !!! Do not interrupt the update, if you interrupt the update, the executable file will be corrupted !!!
echo.

where curl >nul 2>&1
if %ERRORLEVEL%==0 (
    curl -#L %1 -o %2
) else (
    powershell Invoke-WebRequest -Uri %1 -OutFile %2
)

echo.
echo Press Enter to exit the updater ... 
pause >nul
"""

MACOS_EXTERNAL_UPDATER = """
#!/bin/bash

sleep 1

echo -e '\n--- ESET-KeyGen External-Updater ---\n'
echo -e '!!! Make sure you are running the program with elevated permissions, else update will fail !!!\n'
echo -e '!!! Do not interrupt the update, if you interrupt the update, the executable file will be corrupted !!!\n'

curl -#L $1 -o $2
chmod 755 $2
echo -e "\nPress Enter to exit the updater ..."

exit
"""

class Updater:
    def __init__(self, disable_logging=False):
        self.disable_logging = disable_logging
        self.arch = None
        if sys.platform.startswith('win'):
            self.arch = 'win32'
            if sys.maxsize > 2**32: # 64bit 
                self.arch = 'win64'
        elif sys.platform == 'darwin':
            self.arch = 'macos' # prefix for universal macOS builds (arm64 + x86_64)
            #arch = 'macos_arm64'
            #if platform.machine() == "x86_64":
            #    arch = 'macos_amd64'
        self.releases = None
    
    def get_releases(self, version='latest'):
        url = 'https://api.github.com/repos/shadowcopyrz/ESET-KGEN-COPY/releases'
        if version == 'latest':
            url = 'https://api.github.com/repos/shadowcopyrz/ESET-KGEN-COPY/releases/latest'
        try:
            response = requests.get(url, timeout=5)
            update_json = response.json()
            try:
                if update_json.get('message') is not None and not self.disable_logging:
                    console_log('Your IP address has been blocked. try again later or use a VPN!', ERROR)
                    return None
            except AttributeError:
                pass
            if version == 'latest': # when requesting the latest version, the site returns json without a list. 
                update_json = [update_json]
            f_update_json = {}
            for release in update_json:
                f_update_json[release['name']] = {
                    'version': release['name'],
                    'src': release['zipball_url'],
                    'assets': {}
                }
                for asset in release['assets']:
                    if asset['name'] == 'src.zip':
                        f_update_json[release['name']]['src'] = asset['browser_download_url']
                    else:
                        f_update_json[release['name']]['assets'][asset['name']] = asset['browser_download_url']
            self.releases = f_update_json
            return f_update_json
        except:
            return None

    def find_suitable_data(self, datatype='source_code', version='latest'): # datatype: source_code OR executable_file
        if self.releases is None:
            self.releases = self.get_releases(version)
        if version == 'latest':
            if datatype == 'source_code':
                return self.releases[list(self.releases.keys())[0]]['src']
            elif datatype == 'executable_file':
                assets = self.releases[list(self.releases.keys())[0]]['assets']
        else:
            for release_name in self.releases:
                if release_name == version:
                    if datatype == 'source_code':
                        return self.releases[release_name]['src']
                    elif datatype == 'executable_file':
                        assets = self.releases[release_name]['assets']
                        break
        if datatype == 'executable_file':
            for asset_name, asset_url in assets.items():
                if asset_name.find(self.arch) != -1:
                    return asset_url
        
    def download_file(self, url):
        try:
            response = requests.get(url, stream=True)
            try:
                filename = response.headers.get('content-disposition').split('filename=')[1]
                if not self.disable_logging:
                    console_log(f'Downloading {filename}...', INFO)
            except:
                pass
            total_length = response.headers.get('content-length')
            if total_length is None: # No content length header
                with open(filename, 'wb') as f:
                    f.write(response.content)
            else:
                task = ProgressBar(int(total_length), '           ', DEFAULT_RICH_STYLE)
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            task.update(len(chunk))
                            task.render()
            return str(pathlib.Path(filename).resolve())
        except Exception as e:
            if not self.disable_logging:
                console_log(f"Error downloading file: {e}", ERROR)
            return False
    
    def extract_data(self, data_path: str, new_name=None):
        extracted_data_path = None
        if data_path.endswith('.zip'): # source code
            try:
                with zipfile.ZipFile(data_path, 'r') as zipf:
                    extracted_folder_name = zipf.filelist[0].filename[0:-1] # rzc0d3r-ESET-KeyGen-56a2c5b/ -> rzc0d3r-ESET-KeyGen-56a2c5b
                    zipf.extractall()
                    if not self.disable_logging:
                        console_log("Extraction completed successfully!", OK)
                    extracted_data_path = str(pathlib.Path(extracted_folder_name).resolve())
                if new_name is not None:
                    os.rename(extracted_folder_name, new_name)
                    extracted_data_path = str(pathlib.Path(new_name).resolve())
                else:
                    os.rename(extracted_folder_name, 'ESET-KeyGen-'+list(self.releases.keys())[0])
                    extracted_data_path = str(pathlib.Path('ESET-KeyGen-'+list(self.releases.keys())[0]))
            except Exception as e:
                if not self.disable_logging:
                    console_log(str(e), ERROR)
        if not data_path.endswith('.zip'): # executable file
            extracted_data_path = str(pathlib.Path(data_path).resolve())
            if new_name is not None:
                os.rename(data_path, new_name)
                extracted_data_path = str(pathlib.Path(new_name).resolve())
        if not self.disable_logging:
            console_log(f"Location of update: {extracted_data_path}", WARN)
        return extracted_data_path

    def updater_menu(self, i_am_executable, path_to_main_file):
        executable_file_url = self.find_suitable_data(datatype='executable_file')
        if i_am_executable: # run from the build [supported platform]
            if sys.platform.startswith('win'):
                updater_path = os.environ['TEMP']+'\\updater.bat'
                with open(updater_path, 'w') as f:
                    f.write(WINDOWS_EXTERNAL_UPDATER)
                subprocess.Popen([updater_path, executable_file_url, path_to_main_file], shell=True)
            elif sys.platform == 'darwin':
                updater_path = r'/tmp/updater.sh'
                with open(updater_path, 'w') as f:
                    f.write(MACOS_EXTERNAL_UPDATER)
                os.chmod(updater_path, 0o755)
                subprocess.Popen(['bash', updater_path, executable_file_url, path_to_main_file])
            sys.exit(0)
        elif executable_file_url is not None: # run from source [supported platform]
            executable_file_url = self.find_suitable_data(datatype='executable_file')
            self.extract_data(self.download_file(executable_file_url))
        else: # run from source [unsupported platform]
            console_log('No suitable executable file was found for your platform!!!', ERROR)
            console_log('Downloading the latest release source code...', INFO)
            self.extract_data(self.download_file(self.find_suitable_data()))