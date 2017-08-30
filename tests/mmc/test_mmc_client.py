import pretend
import pytest


def test_mmc_client_base_url_force_base_url_end_with_slash():
    from aureus.mmc import client

    cli = client.MMCClient('http://fake.com', ('username', 'password'))

    assert cli.base_url == 'http://fake.com/'

    cli = client.MMCClient('http://fake.com/', ('username', 'password'))

    assert cli.base_url == 'http://fake.com/'


def test_mmc_client_get(monkeypatch):
    from aureus.mmc import client

    response = pretend.stub(json=lambda: {'a': 'value a'})

    monkeypatch.setattr(client.requests, 'request', lambda *a, **kw: response)

    cli = client.MMCClient('http://fake.com', ('username', 'password'))

    res = cli.get('/fake')

    assert res['a'] == 'value a'


def test_mmc_client_get_exception(monkeypatch):
    from requests.exceptions import Timeout
    from aureus.mmc import client
    def request(*a, **kwargs):
        raise Timeout()

    monkeypatch.setattr(client.requests, 'request', request)

    cli = client.MMCClient('http://fake.com', ('username', 'password'))

    with pytest.raises(Timeout) as exc_info:
        cli.get('/fake')


def test_mmc_client_post_form_data_and_body_fails():
    from aureus.mmc import client

    cli = client.MMCClient('http://fake.com', ('username', 'password'))

    with pytest.raises(ValueError) as exc_info:
        cli.post('value', 'value')
