import os.path
import re
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class ResourceMissing(Exception):
    pass


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

    _MAVEN_METADATA = 'nexus-metadata.xml'

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
    def basepath(self):
        base_template = "{group}/{artifact}/"
        return base_template.format(group=self.group.replace('.', self._URL_SEP),
                                    artifact=self.artifact_id)

    @property
    def contentpath(self):
        content_template = '{version}/{artifact}-{version}.zip'
        content_url = content_template.format(basepath=self.basepath,
                                              version=self.version,
                                              artifact=self.artifact_id)
        return urljoin(self.basepath, content_url)

    def _metadata(self):
        meta_url = urljoin(self.basepath, self._MAVEN_METADATA)
        return self.client.get_content(meta_url)

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