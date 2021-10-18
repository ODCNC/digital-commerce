import json
import time
from datetime import datetime
from urllib import parse

from decouple import config
from oauthlib.oauth2 import WebApplicationClient
from requests.models import HTTPError
from requests_oauthlib import OAuth2Session

MALL_ID = config('CAFE24_MALL_ID')
CLIENT_ID = config('CAFE24_CLIENT_ID')
CLIENT_SECRET = config('CAFE24_CLIENT_SECRET')
SCOPE = ['mall.write_category', 'mall.read_category']
VERSION = config('CAFE24_VERSION', '2021-03-01')
API_V2 = lambda path: parse.urljoin(f'https://{MALL_ID}.cafe24api.com/api/v2/', path)
TOKEN_URL = API_V2('oauth/token')


class Cafe24Client(WebApplicationClient):
    def __init__(self, client_id=CLIENT_ID, **kwargs):
        super().__init__(client_id, **kwargs)
        self.session = self._session(token_updater=kwargs.get('token_updater'))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

    def _session(self, **kwargs):
        session = OAuth2Session(
            CLIENT_ID,
            self,
            TOKEN_URL,
            {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
            SCOPE,
            token=self.token,
            **kwargs,
        )
        session.headers.update({
           'X-Cafe24-Api-Version': VERSION,
        })
        return session

    def close(self):
        self.session.close()

    def fetch_token(self, authorization_response):
        return self.session.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            authorization_response=authorization_response,
        )

    def populate_token_attributes(self, response):
        if 'expires_at' in response:
            response = response.copy()
            expires_at = response.pop('expires_at')
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            if isinstance(expires_at, datetime):
                expires_at = expires_at.timestamp()
            response['expires_at'] = expires_at
        return super().populate_token_attributes(response)

    def request(self, method, path, data=None, headers={}, **kwargs):
        if isinstance(data, dict):
            data = json.dumps(data)
            headers.setdefault('Content-Type', 'application/json')
        response = self.session.request(
            method,
            API_V2(path),
            data,
            headers={'Authorization': f'Bearer {self.access_token}', **headers},
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            **kwargs,
        )
        if response.headers.get('X-Api-Call-Limit') == '39/40':
            time.sleep(1)
        try:
            return response.json()
        except:
            raise HTTPError(response=response)
