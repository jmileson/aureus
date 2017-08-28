from datetime import datetime
import pretend
import pytest


def test_local_resource_absolute_file_path_instantiates(tmpdir):
    import aureus.maven.resource as resource

    f = str(tmpdir.join('temp.txt'))

    res = resource.LocalResource(f)

    assert res.filepath == f


def test_local_resource_relative_path_throws_exception(tmpdir):
    import aureus.maven.resource as resource

    f = tmpdir.join('temp.txt').basename

    with pytest.raises(FileNotFoundError) as ex:
        res = resource.LocalResource(f)


def test_group_artifact_to_resource_path():
    import aureus.maven.resource as resource

    res = resource.Resource('com.somewhere.something', 'some-id')

    assert res.basepath == 'com/somewhere/something/some-id/'


def test_resource_client_get_resource_meta(monkeypatch):
    import aureus.maven.resource as resource

    get = pretend.call_recorder(lambda *a, **kw: """
        <metadata>
            <groupId>com.jss</groupId>
            <artifactId>payment-order-system-api</artifactId>
            <versioning>
                <release>1.0.10</release>
                <versions>
                    <version>1.0.4</version>
                    <version>1.0.5</version>
                    <version>1.0.6</version>
                    <version>1.0.7</version>
                    <version>1.0.8</version>
                    <version>1.0.9</version>
                    <version>1.0.10</version>
                </versions>
                <lastUpdated>20170825180820</lastUpdated>
            </versioning>
        </metadata>
    """)
    monkeypatch.setattr(resource.requests, 'get', get)

    client = resource.ResourceClient('http://fake.com/api', ('username', 'password'))

    meta_inf = client.meta('/blah')
    assert meta_inf['group_id'] == 'com.fake'
    assert meta_inf['artifact_id'] == 'fake-id'
    assert meta_inf['latest_version'] == '1.0.1'
    assert '1.0.0' in meta_inf['versions'] and '1.0.1' in meta_inf['versions']
    assert meta_inf['last_updated_time'] == datetime(2017, 8, 25, 12, 21, 0)


def test_find_latest_version():
    import aureus.maven.resource as resource

    res = resource.Resource('com.somewhere', 'some-id')

    res.latest_version()


def test_resource_client():
    class ResourceClient(object):
        def __init__(self, credentials):
            self.credentials = credentials
