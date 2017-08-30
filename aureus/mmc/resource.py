from urllib.parse import urljoin
from io import BytesIO


class Resource(object):
    _RESOURCE = ''

    def __init__(self, client):
        self._client = client

    @property
    def url(self):
        if self._RESOURCE.startswith('/'):
            self._RESOURCE = self._RESOURCE[1:]
        return urljoin(self._client.base_url, self._RESOURCE)

    def member_url(self, id):
        base = self.url
        if not self.url.endswith('/'):
            base += '/'
        if id.startswith('/'):
            id = id[1:]
        return urljoin(base, id)

    def list(self):
        return self._client.get(self.url)

    def delete(self, id):
        return self._client.delete(self.member_url(id))

    def upload(self, resource):
        form_data = {
            'file': BytesIO(resource.content()),
            'name': resource.artifact_id,
            'version': resource.version
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
