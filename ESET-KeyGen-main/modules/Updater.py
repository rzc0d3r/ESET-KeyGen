from .SharedTools import console_log, INFO, OK, ERROR, WARN
from .ProgressBar import ProgressBar, DEFAULT_RICH_STYLE

import argparse
import requests
import zipfile
import json
import sys
import os
import platform

def parse_update_json(json_path='', from_main=False):
    if json_path == '':
        url = 'https://api.github.com/repos/rzc0d3r/ESET-KeyGen/releases'
        try:
            response = requests.get(url, timeout=3)
            update_json = response.json()
            try:
                if update_json.get('message') is not None:
                    if not from_main:
                        console_log('Your IP address has been blocked. try again later or use a VPN!', ERROR)
                        sys.exit(-1)
                    return None
            except AttributeError:
                pass
            f_update_json = {}
            for release in update_json:
                f_update_json[release['name']] = {
                    'version': release['name'],
                    'src': release['zipball_url'],
                    'assets': {},
                    'changelog': release['body'].strip()
                }
                for asset in release['assets']:
                    f_update_json[release['name']]['assets'][asset['name']] = asset['browser_download_url']
            return f_update_json
        except requests.RequestException as e:
            return None
    else:
        try:
            with open(json_path, 'r') as f:
                update_json = json.loads(f.read().strip())
            return update_json
        except IOError:
            console_log(f"Error: Could not read file {json_path}", ERROR)
            return None

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
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
        return True
    except Exception as e:
        console_log(f"Error downloading file: {e}", ERROR)
        return False

def download_and_extract(url, extract_to='.', force_zip=False):
    filename = url.split('/')[-1]
    if download_file(url, filename):
        extracted_folder_name = ''
        if force_zip or filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    extracted_folder_name = zip_ref.filelist[0].filename[0:-1] # rzc0d3r-ESET-KeyGen-56a2c5b/ -> rzc0d3r-ESET-KeyGen-56a2c5b
                    zip_ref.extractall(extract_to)
                os.remove(filename)
                console_log("Extraction completed successfully!", OK)
            except zipfile.BadZipFile:
                console_log("Downloaded file is not a valid zip file!", ERROR)
                return False
        if extracted_folder_name != '':
            try:
                os.rename(extracted_folder_name, 'ESET-KeyGen-'+filename)
                filename = 'ESET-KeyGen-'+filename
            except:
                filename = extracted_folder_name
        update_location = os.getcwd()+'/'+filename # for python < 3.8
        update_location = update_location.replace('\\', '/')
        console_log(f"Location of update: {update_location}", WARN)
        return True
    else:
        return False

def update_src_code(update_json):
    download_url = update_json['src']
    console_log(f"Downloading and updating the source code of version {update_json['version']}...", INFO)
    if download_and_extract(download_url, force_zip=True):
        console_log("Source code update completed successfully!", OK)
    else:
        console_log("Source code update failed!", ERROR)

def update_binary(update_json):
    assets = update_json['assets']
    if assets:
        # detect OS
        arch = ''
        if os.name == 'nt': # Windows
            arch = 'win32' # 32bit
            if sys.maxsize > 2**32: # 64bit 
                arch = 'win64'
        elif sys.platform == "darwin":
            arch = 'macos_arm64'
            if platform.machine() == "x86_64":
                arch = 'macos_amd64'
        # downloading
        if arch != '':
            for asset_name, asset_url in assets.items():
                if asset_name.find(arch) != -1:
                    console_log(f"Downloading and updating to {update_json['version']}...", INFO)
                    if download_and_extract(asset_url):
                        console_log("Update completed successfully!", OK)
                    else:
                        console_log("Update failed!", ERROR)
                    break
        else: # for another OS, only update source code
            console_log("No suitable binary URL was found for download!", ERROR)
            console_log("So I'm updating the source code...", INFO, False)
            update_src_code(update_json)

def get_assets_from_version(update_json, version):
    if update_json is not None:   
        if version == 'latest':
            return update_json[list(update_json.keys())[0]]
        for release_name in update_json:
            if release_name == version:
                return update_json[release_name]
    return None

def updater_main(from_main=False):
    args = {}
    if not from_main:
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('--version', type=str, default='latest', help='Specify the version to be installed')
        args_parser.add_argument('--custom-json', type=str, default='', help='Specify a custom path to the json file with update data')
        args_parser.add_argument('--src', action='store_true', help='Download source code instead of binary files')
        args_parser.add_argument('--list', action='store_true', help='Shows which versions are available')
        args = vars(args_parser.parse_args())
    else:
        args = {
            'version': 'latest',
            'custom_json': '',
            'src': False,
            'list': False
        }
    update_json = parse_update_json(args['custom_json'])
    if args['list']:
        for release in update_json:
            print(release['name'])
        sys.exit(1)
    if update_json is None:
        console_log("Failed to parse update JSON!", ERROR)
        sys.exit(1)
    update_data = get_assets_from_version(update_json, args['version'])
    if update_data is not None:
        if args['src']:
            update_src_code(update_data)
        else:
            update_binary(update_data)
    else:
        console_log(f"Version {args['version']} not found!", ERROR)

if __name__ == '__main__':
    updater_main()