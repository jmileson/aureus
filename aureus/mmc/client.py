import requests

from aureus.mmc.resource import Repository, Deployment, ServerGroup


class MMCClient(object):
    def __init__(self, base_url, credentials):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.credentials = tuple(credentials)
        self.repository = Repository(self)
        self.server_group = ServerGroup(self)
        self.deployment = Deployment(self)

    def _request(self, method, url, body=None, q=None, headers=None, form_data=None):
        res = requests.request(method, url, data=body, params=q, headers=headers, auth=self.credentials,
                               files=form_data)

        return res.json()

    def get(self, url):
        return self._request('GET', url)

    def post(self, url, body=None, form_data=None):
        if body and form_data:
            raise ValueError('must specify either body or form_data')
        return self._request('POST', url, body=body, form_data=form_data)

    def delete(self, url):
        return self._request('DELETE', url)
