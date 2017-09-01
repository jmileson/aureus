import requests
from ..helpers import resource_join
from .maven import MavenResource


class NexusClient(object):
    def __init__(self, base_url, credentials):
        self.base_url = base_url
        self.credentials = credentials

    def maven_resource(self, group_id, artifact_id, version=None):
        return MavenResource(self, group_id, artifact_id, version)

    def get_content(self, resource):
        url = resource_join(self.base_url, resource)

        try:
            res = requests.get(url, auth=tuple(self.credentials), verify=False)
            return res.content
        except requests.exceptions.RequestException:
            return None