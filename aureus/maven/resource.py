import os.path
import re
import requests
from urllib.parse import urljoin



class LocalResource(object):
    _VERSION_PATTERN = re.compile(r'\d+\.\d+\.\d+(-SNAPSHOT)?')
    _NAME_PATTERN = re.compile(r'(.*)-\d+\.\d+\.\d+(-SNAPSHOT)?')

    def __init__(self, filepath):
        if not os.path.isabs(filepath):
            raise FileNotFoundError('cannot locate file')
        self.filepath = filepath

    @property
    def file_name(self):
        name, _ = os.path.splitext(os.path.basename(self.filepath))
        return name

    @property
    def name(self):
        match = self._NAME_PATTERN.search(self.file_name)
        if not match:
            return None

        try:
            return match[1]  # we only want the "unversioned" name
        except IndexError:
            return None

    @property
    def version(self):
        match = self._VERSION_PATTERN.search(self.file_name)
        if not match:
            return None
        return match[0]

    def file(self):
        return open(self.filepath, mode='rb')


class Resource(object):
    _URL_SEP = '/'

    _MAVEN_METADATA = 'maven-metadata.xml'

    def __init__(self, group, artifact_id, version=None):
        self.group = group
        self.artifact_id = artifact_id
        self.version = version

    @property
    def basepath(self):
        return urljoin(self.group.replace('.', self._URL_SEP) + self._URL_SEP, self.artifact_id + '/')

    def _metadata(self):
        meta_url = urljoin(self.basepath, self._MAVEN_METADATA)


class ResourceClient(object):
    def __init__(self, base_url, credentials):
        self.base_url = base_url
        self.credentials = credentials

    @staticmethod
    def _meta(meta):
        from xml.etree import ElementTree
        xml = ElementTree.fromstring(meta)

    def meta(self, resource):
        url = urljoin(self.base_url, resource)

        res = requests.get(url, auth=tuple(self.credentials))
        return self._meta(res.content)
