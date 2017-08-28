import pretend


def test_credentials_from_env(monkeypatch):
    import aureus.login as login

    user = 'username'
    pw = 'password'

    monkeypatch.setenv(login._MMC_USER_ENV, user)
    monkeypatch.setenv(login._MMC_PW_ENV, pw)

    creds = login.BasicCredentials(login._MMC_USER_ENV, login._MMC_PW_ENV)

    assert creds.username == user
    assert creds.password == pw


def test_credentials_from_input(monkeypatch):
    import aureus.login as login

    fake_input = str(pretend.stub())
    prompt = pretend.call_recorder(lambda *a, **kw: fake_input)
    monkeypatch.setattr(login, 'prompt', prompt)

    creds = login.BasicCredentials(login._MMC_USER_ENV, login._MMC_PW_ENV)

    assert creds.username == fake_input
    assert creds.password == fake_input


def test_mmc_credentials_factory(monkeypatch):
    import aureus.login as login

    class FakeCredentials(object):
        pass

    monkeypatch.setattr(login, 'MMCCredentials', FakeCredentials)

    assert isinstance(login.mmc_credentials_factory(), FakeCredentials)


def test_resource_credentials_factory(monkeypatch):
    import aureus.login as login

    class FakeCredentials(object):
        pass

    monkeypatch.setattr(login, 'ResourceCredentials', FakeCredentials)

    assert isinstance(login.resource_credentials_factory(), FakeCredentials
                      )
