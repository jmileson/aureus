from datetime import datetime
import pretend
import pytest


def test_local_resource_absolute_file_path_instantiates(tmpdir):
    import aureus.nexus.maven as resource

    f = str(tmpdir.join('temp.txt'))

    res = resource.LocalResource(f)

    assert res.filepath == f


def test_local_resource_relative_path_throws_exception(tmpdir):
    import aureus.nexus.maven as resource

    f = tmpdir.join('temp.txt').basename

    with pytest.raises(FileNotFoundError) as ex:
        res = resource.LocalResource(f)


def test_group_artifact_to_resource_path():
    import aureus.nexus.maven as resource

    res = resource.MavenResource(pretend.stub(), 'com.somewhere.something', 'some-id', 'some-version')

    assert res.basepath == 'com/somewhere/something/some-id/'


def test_resource_get_resource_meta():
    import aureus.nexus.maven as resource

    client = pretend.stub(get_content=lambda *a, **kw: """
        <metadata>
            <groupId>com.fake</groupId>
            <artifactId>fake-id</artifactId>
            <versioning>
                <release>1.0.1</release>
                <versions>
                    <version>1.0.0</version>
                    <version>1.0.1</version>
                </versions>
                <lastUpdated>20170825122100</lastUpdated>
            </versioning>
        </metadata>
    """)

    meta_inf = resource.MavenResource(client, 'com.fake', 'fake-id', 'some-version').meta()

    assert meta_inf['group_id'] == 'com.fake'
    assert meta_inf['artifact_id'] == 'fake-id'
    assert meta_inf['latest_version'] == '1.0.1'
    assert '1.0.0' in meta_inf['versions'] and '1.0.1' in meta_inf['versions']
    assert meta_inf['last_updated_time'] == datetime(2017, 8, 25, 12, 21, 0)


def test_resource_get_resource_meta_no_response_raises_resource_missing_exception():
    import aureus.nexus.maven as resource

    client = pretend.stub(get_content=lambda *a, **kw: None)

    with pytest.raises(resource.ResourceMissing) as exc_info:
        meta_inf = resource.MavenResource(client, 'com.fake', 'fake-id', 'some-version').meta()


def test_resource_latest_version():
    import aureus.nexus.maven as resource

    client = pretend.stub(get_content=lambda *a, **kw: """
        <metadata>
            <groupId>com.fake</groupId>
            <artifactId>fake-id</artifactId>
            <versioning>
                <release>1.0.1</release>
                <versions>
                    <version>1.0.0</version>
                    <version>1.0.1</version>
                </versions>
                <lastUpdated>20170825122100</lastUpdated>
            </versioning>
        </metadata>
    """)

    res = resource.MavenResource(client, 'com.fake', 'fake-id', 'some-version')

    assert res.latest_version() == '1.0.1'


def test_resource_unspecified_version_is_latest_version():
    import aureus.nexus.maven as resource

    client = pretend.stub(get_content=lambda *a, **kw: """
        <metadata>
            <groupId>com.fake</groupId>
            <artifactId>fake-id</artifactId>
            <versioning>
                <release>1.0.1</release>
                <versions>
                    <version>1.0.0</version>
                    <version>1.0.1</version>
                </versions>
                <lastUpdated>20170825122100</lastUpdated>
            </versioning>
        </metadata>
    """)

    res = resource.MavenResource(client, 'com.fake', 'fake-id', '')

    assert res.version == '1.0.1'


def test_resource_content_url():
    from aureus.nexus import maven
    client = pretend.stub()
    res = maven.MavenResource(client, 'com.fake', 'fake-id', '1.1.1')

    assert res.contentpath == 'com/fake/fake-id/1.1.1/fake-id-1.1.1.zip'


def test_resource_content():
    from aureus.nexus import maven

    client = pretend.stub(get_content=lambda *a, **kw: b'content')

    res = maven.MavenResource(client, 'com.fake', 'fake-id', 'fake-version')

    assert res.content() == b'content'
