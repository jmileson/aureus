from io import BytesIO

from ..exception import InvalidResource
from .resource import DeletableResource
from ..nexus.maven import MavenResource


class Repository(DeletableResource):
    _RESOURCE = 'repository'

    def upload(self, resource):
        if not isinstance(resource, MavenResource):
            raise InvalidResource('only maven resources can be uploaded')
        form_data = {
            'file': BytesIO(resource.content()),
            'name': resource.artifact_id,
            'version': resource.version
        }
        return self._client.post(self.url, form_data=form_data)


