from urllib.parse import urljoin

import requests

from aureus.maven.resource import LocalResource


class MMCClient(object):
    def __init__(self, base_url, credentials):
        self.base_url = base_url
        self.credentials = tuple(credentials)
        self.repository = Repository(self)
        self.server_group = Repository(self)
        self.deployment = Deployment(self)

    def _request(self, method, url, body=None, q=None, headers=None, form_data=None):
        res = requests.request(method, url, data=body, params=q, headers=headers, auth=self.credentials,
                               files=form_data)
        try:
            return res.json()
        except:  # yeah, I know
            return {'status_code': res.status_code, 'message': res.text}

    def get(self, url):
        return self._request('GET', url)

    def post(self, url, body=None, form_data=None):
        if body and form_data:
            raise ValueError('must specify either body or form_data')
        return self._request('POST', url, body=body, form_data=form_data)

    def delete(self, url):
        return self._request('DELETE', url)


class Resource(object):
    _RESOURCE = ''

    def __init__(self, client):
        self._client = client

    @property
    def url(self):
        return urljoin(self._client.base_url, self._RESOURCE)

    def member_url(self, id):
        return urljoin(self.url, id)

    def list(self):
        return self._client.get(self.url)

    def delete(self, id):
        return self._client.delete(self.member_url(id))

    def upload(self, filepath):
        res = LocalResource(filepath)
        form_data = {
            'file': res.file(),
            'name': res.name,
            'version': res.version
        }
        return self._client.post(self.url, form_data=form_data)


class Repository(Resource):
    _RESOURCE = 'repository/'

    def list_all_versions(self, id):
        return self._client.get(self.member_url(id))


class ServerGroup(Resource):
    _RESOURCE = 'serverGroups/'


class Deployment(Resource):
    _RESOURCE = 'deployments/'


if __name__ == '__main__':
    from aureus.config import configure

    settings = configure()
    client = MMCClient(settings['mmc.root.url'], settings['mmc.credentials'])
    res = client.repository.delete('local$56b729e4-1518-4ca3-8c97-997661b791aa')
    res = client.repository.list()
    res = client.repository.upload(
        r'D:\.m2\repository\com\jss\card-payment-system-api\1.0.1\card-payment-system-api-1.0.1.zip')
    print('complete')
