import pretend


def test_nexus_client_get_content(monkeypatch):
    from aureus.nexus import client

    response = pretend.stub(content=b'content')
    requests = pretend.stub(get=lambda *a, **kw: response)
    monkeypatch.setattr(client, 'requests', requests)

    cli = client.NexusClient('http://fake.com', ('username', 'password'))

    assert cli.get_content('some/resource') == b'content'


def test_nexus_client_get_content_throws_exception_returns_none(monkeypatch):
    from requests.exceptions import Timeout
    from aureus.nexus import client

    def get(*a, **kw):
        raise Timeout()

    monkeypatch.setattr(client.requests, 'get', get)

    cli = client.NexusClient('http://fake.com', ('username', 'password'))

    assert cli.get_content('some/resource') is None
