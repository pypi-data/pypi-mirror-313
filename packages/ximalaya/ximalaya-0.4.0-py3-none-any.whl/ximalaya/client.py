import json
import urllib.request


class XimalayaClient:
    def __init__(self, host: str = 'www.ximalaya.com', headers: dict = None):
        self.host = host

        self.headers = {} if headers is None else headers

        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = ''

    def get(self, path: str, method: str = 'GET'):
        url = f'https://{self.host}/{path.lstrip("/")}'

        req = urllib.request.Request(url, headers=self.headers, method=method)

        with urllib.request.urlopen(req) as fp:
            return json.loads(fp.read().decode('utf-8'))
