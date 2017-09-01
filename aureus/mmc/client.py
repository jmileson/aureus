import requests
from .resource import Deployment, ServerGroup, Server
from aureus.mmc.app import Repository
from ..helpers import resource_join


class MMCClient(object):
    def __init__(self, base_url, credentials):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.credentials = tuple(credentials)
        self.repository = Repository(self)
        self.server_group = ServerGroup(self)
        self.server = Server(self)
        self.deployment = Deployment(self)

    def _request(self, method, resource_url, body=None, q=None, headers=None, form_data=None):
        url = resource_join(self.base_url, resource_url)
        res = requests.request(method, url, data=body, params=q, headers=headers, auth=self.credentials,
                               files=form_data)

        return res.json()

    def get(self, resource_url):
        return self._request('GET', resource_url)

    def post(self, resource_url, body=None, form_data=None):
        if body and form_data:
            raise ValueError('must specify either body or form_data')
        return self._request('POST', resource_url, body=body, form_data=form_data)

    def delete(self, resource_url):
        return self._request('DELETE', resource_url)
