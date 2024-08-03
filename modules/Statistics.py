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
    
    def get_statistics(self, path='', firstcall=True):
        contents = self.get_repo_contents(path)
        runs, gens = 0, 0
        for item in contents:
            if item['type'] == 'file':
                if item['name'][0:4] == 'runs':
                    runs += 1
                elif item['name'][0:4] == 'gens':
                    gens += 1
            elif item['type'] == 'dir':
                nruns, ngens = self.get_statistics(item['path'], firstcall=False)
                runs += nruns
                gens += ngens
        if firstcall:
            archived_statistics = self.get_repo_contents('archived_statistics.json')
            archived_statistics_raw_url = archived_statistics.get('download_url', None)
            if archived_statistics_raw_url is not None:
                try:
                    archived_statistics_data = self.session.get(archived_statistics_raw_url).json()
                    runs += archived_statistics_data['runs']
                    gens += archived_statistics_data['gens']
                except:
                    pass
        return [runs, gens]
    
    def archive_statistics(self, data=None, commit_message='update archived statistics', path='archived_statistics.json'):
        runs, gens = self.get_statistics()
        if runs+gens > 900:
            print(f'Sending {runs} runs & {gens} gens to archived_statistics.json')
        content = self.get_repo_contents(path)
        sha = content.get('sha', None)
        if sha is not None:
            if data is None:
                data = {'runs': runs, 'gens': gens}
                data = json.dumps(data)
            headers = {'Authorization': f'token {random.choice(self.st_tokens)}'}
            payload = {'message': commit_message, 'content': base64.b64encode(data.encode()).decode(), 'sha':sha}
            try:
                r = self.session.put(f'{self.api_url}/contents/{path}?ref=main', headers=headers, json=payload)
                if r.status_code == 200:
                    return True
            except:
                pass
        return False
        
    def send_statistics(self, name, additional_value=''):
        data = {
            'date': str(datetime.datetime.now()),
            'additional_data': additional_value,
            'platform': f'{platform.system()}_v{platform.version()}_{".".join(platform.architecture())}',
        }
        data = json.dumps(data)
        if name in ['runs', 'gens']:
            url = f'{self.api_url}/contents/{name}/'
            name = f'{name}_{str(random.uniform(1, 9999)).replace(".", "")}.json'
        else:
            return False
        
        headers = {'Authorization': f'token {random.choice(self.st_tokens)}'}
        payload = {'message': 'statistics update', 'content': base64.b64encode(data.encode()).decode()}

        try:
            r = self.session.put(url+name, headers=headers, json=payload)
            if r.status_code == 201:
                return True
        except:
            pass
        return False

#if __name__ == '__main__':
    #st = Statistics()
    #print('Current statistics:', st.get_statistics())
    #if input('Archive the current statistics? ').strip().lower() == 'y':
    #    print('    Successfully archived:', st.archive_statistics())