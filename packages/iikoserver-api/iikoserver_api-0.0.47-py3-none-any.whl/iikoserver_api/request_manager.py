import hashlib
from datetime import datetime, timedelta

import requests


class RequestManager:
    _default_headers = {'Content-Type': 'application/xml'}

    def __init__(self, url: str = None, ):
        self.url = url
        self.token = None

    def send(self, action: str, method: str = 'GET', params: dict = None, headers: dict = None, data: any = None,
             json=None):
        if headers is None:
            headers = self._default_headers
        url = f'{self.url}{action}/'
        response = requests.request(method=method, url=url, params=params, headers=headers, data=data, json=json)

        if response.ok:
            return response.content
        else:
            error_info = {
                "response_status": response.status_code,
                "response_info": response.content.decode()
            }
            # if action not in ['logout', 'auth']:
            #     self.clear_token()
            raise ConnectionError(error_info)

    def test_send(self):
        params = {
            'key': self.token,
            'from': (datetime.now() - timedelta(days=1000)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
        }
        data = self.send(action='documents/export/incomingInvoice', params=params)

    def auth(self, login, password):
        password = hashlib.sha1(password.encode()).hexdigest()
        params = {
            'login': login,
            'pass': password,
        }
        response = self.send(action='auth', params=params)
        data = response.decode()
        self.token = data

    def clear_token(self):
        params = {
            'key': self.token
        }
        data = self.send(action='logout', params=params)
        self.token = None



