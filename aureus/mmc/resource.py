from ..helpers import resource_join


class Resource(object):
    _RESOURCE = ''

    def __init__(self, client):
        self._client = client

    @property
    def url(self):
        return resource_join(self._RESOURCE)

    def member_url(self, id):
        return resource_join(self.url, id)

    def list(self):
        return self._client.get(self.url)

    def inspect(self, id):
        return self._client.get(self.member_url(id))


class DeletableResource(Resource):
    def delete(self, id):
        return self._client.delete(self.member_url(id))


class Deployment(DeletableResource):
    _RESOURCE = 'deployments'


class ServerGroup(Resource):
    _RESOURCE = 'serverGroups'
    _TEST = 'Test'
    _PROD = 'Production'

    def _get_group(self, name):
        matches = [g for g in self.list()['data'] if g['name'] == name]
        if matches:
            return matches[0]
        return None

    @property
    def test(self):
        return self._get_group(self._TEST)

    @property
    def prod(self):
        return self._get_group(self._PROD)


class Server(Resource):
    _RESOURCE = 'servers'
