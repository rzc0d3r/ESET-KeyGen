import datetime
import requests
import base64
import platform
import random
import json

class Statistics:
    def __init__(self):
        self.api_url = 'https://api.github.com/repos/rzc0d3r/ESET-KeyGen-Statistics'
        self.shared_data_url = 'https://raw.githubusercontent.com/rzc0d3r/ESET-KeyGen/main/modules/data.json'
        self.session = requests.Session()
        self.init()

    def init(self):
        self.st_tokens = ['']
        try:
            shared_data = self.session.get(self.shared_data_url).json()
            for st_token in shared_data.get('st_tokens', []):
                st_token = 'github_pat_'+st_token
                try:
                    r = self.session.get('https://api.github.com/user', headers={"Authorization": f"token {st_token}"})
                    if r.status_code == 200:
                        if self.st_tokens[0] == '':
                            self.st_tokens[0] = st_token
                        else:
                            self.st_tokens.append(st_token)
                except:
                    pass
        except:
            pass
    
    def get_repo_contents(self, path=''):
        url = f'{self.api_url}/contents/{path}?ref=main'
        headers = {'Authorization': f'token {random.choice(self.st_tokens)}'}
        return requests.get(url, headers=headers).json()
    
    def get_statistics(self, path=''):
        contents = self.get_repo_contents(path)
        runs, gens = 0, 0
        for item in contents:
            if item['type'] == 'file':
                if item['name'][0:4] == 'runs':
                    runs += 1
                elif item['name'][0:4] == 'gens':
                    gens += 1
            elif item['type'] == 'dir':
                nruns, ngens = self.get_statistics(item['path'])
                runs += nruns
                gens += ngens
        return [runs, gens]
    
    def send_statistics(self, name, value=''):
        data = {
            'date': str(datetime.datetime.now()),
            'additional_data': value,
            'platform': f'{platform.system()}_v{platform.version()}_{".".join(platform.architecture())}',
        }
        data = json.dumps(data)
        if name == 'runs':
            url = f'{self.api_url}/contents/runs/'
        elif name == 'gens':
            url = f'{self.api_url}/contents/gens/'

        name = f'{name}_{str(random.uniform(1, 9999)).replace(".", "")}.json'
        payload = {'message': 'statistics update', 'content': base64.b64encode(data.encode()).decode()}
        headers = {'Authorization': f'token {random.choice(self.st_tokens)}'}

        try:
            r = self.session.put(url+name, headers=headers, json=payload)
            if r.status_code == 201:
                return True
        except:
            pass
        return False