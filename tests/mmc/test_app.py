import pretend
import pytest


class Getter(object):
    def __init__(self, data):
        self.data = data

    def _get(self, key):
        return self.data.get(key, None)


class Application(Getter):
    class Version(Getter):

        @property
        def id(self):
            return self._get('id')

        @property
        def version(self):
            return self._get('name')

    def __init__(self, data):
        super().__init__(data)
        self.versions = [self.Version(v) for v in self._get('versions')]

    @property
    def id(self):
        return self._get('id')

    @property
    def name(self):
        return self._get('name')



def test_app():
    data = {
        'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/repository/local$0a9b74ef-96d1-4c51-9583-37c6d966394e',
        'id': 'local$0a9b74ef-96d1-4c51-9583-37c6d966394e',
        'name': 'websiteuploads',
        'versions': [{'id': 'local$3d924530-3931-492d-aa96-fc10a844a8fa',
                      'name': '1.0.3',
                      'parentPath': '/Applications/websiteuploads'},
                     {'id': 'local$79b7db8e-e1de-44c0-bfe2-a9e0d09b436f',
                      'name': '1.1.1',
                      'parentPath': '/Applications/websiteuploads'}]}
    app = Application(data)

    assert app.id == 'local$0a9b74ef-96d1-4c51-9583-37c6d966394e'
    assert app.name == 'websiteuploads'
    assert len(app.versions) == 2
    assert app.versions[0].id == 'local$3d924530-3931-492d-aa96-fc10a844a8fa'
    assert app.versions[0].version == '1.0.3'


def test_resource_upload_raises_exception_on_non_maven_resource_input():
    from aureus.mmc import app
    from aureus import exception

    mvn_res = pretend.stub()
    client = pretend.stub()
    res = app.Repository(client)

    with pytest.raises(exception.InvalidResource) as exc_info:
        res.upload(mvn_res)


def test_resource_upload():
    from aureus.mmc import app
    from aureus.nexus import maven
    val = {'key': 'value'}
    client = pretend.stub(post=lambda *a, **kw: val)

    mvn_res = Mock(spec=maven.MavenResource)
    mvn_res.content = Mock(return_value=b'')
    mvn_res.artifact_id = 'id'
    mvn_res.version = 'version'

    res = app.Repository(client)

    assert res.upload(mvn_res) is val
