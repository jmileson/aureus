import os.path
import re
from datetime import datetime

from bs4 import BeautifulSoup

from aureus.exception import ResourceMissing
from ..helpers import resource_join


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


def tag_value(tag):
    return str(tag.string)


class MavenResource(object):
    _URL_SEP = '/'

    _MAVEN_METADATA = 'maven-metadata.xml'

    _GROUP_ID = 'group_id'
    _ARTIFACT_ID = 'artifact_id'
    _LATEST_VERSION = 'latest_version'
    _VERSIONS = 'versions'
    _LAST_UPDATED_TIME = 'last_updated_time'

    def __init__(self, client, group, artifact_id, version=None):
        self.client = client
        self.group = group
        self.artifact_id = artifact_id
        self.version = version or self.latest_version()

    @property
    def meta_url(self):
        return resource_join(self.basepath, self._MAVEN_METADATA)

    @property
    def basepath(self):
        return resource_join(*self.group.split('.'), self.artifact_id)

    @property
    def filename(self):
        return '{0}-{1}.zip'.format(self.artifact_id, self.version)

    @property
    def contentpath(self):
        return resource_join(self.basepath, self.version, self.filename)

    def _metadata(self):
        return self.client.get_content(self.meta_url)

    @classmethod
    def _meta(cls, meta):
        soup = BeautifulSoup(meta, 'xml')
        print('complete')
        return {
            cls._GROUP_ID: tag_value(soup.groupId),
            cls._ARTIFACT_ID: tag_value(soup.artifactId),
            cls._LATEST_VERSION: tag_value(soup.versioning.release),
            cls._VERSIONS: [tag_value(x.string) for x in soup.versioning.versions.find_all('version')],
            cls._LAST_UPDATED_TIME: datetime.strptime(tag_value(soup.versioning.lastUpdated), '%Y%m%d%H%M%S')
        }

    def meta(self):
        meta_content = self._metadata()
        if not meta_content:
            raise ResourceMissing('resource meta information not found')
        return self._meta(meta_content)

    def latest_version(self):
        return self.meta()[self._LATEST_VERSION]

    def content(self):
        return self.client.get_content(self.contentpath)
