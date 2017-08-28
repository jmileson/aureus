import pretend


def test_configure_setting_value_present():
    import aureus.config as config

    k, actual = 'value', 'actual value'
    s = {k: actual}

    config.configure_setting(s, k, 'new value')

    assert s[k] == actual


def test_configure_setting_value_not_present():
    import aureus.config as config

    k, actual = 'value', 'actual value'
    s = dict()

    config.configure_setting(s, k, actual)

    assert s[k] == actual


def test_configure_no_defaults(monkeypatch):
    import aureus.config as config

    creds = pretend.stub()
    monkeypatch.setattr(config, 'mmc_credentials_factory', lambda *a, **kw: creds)
    monkeypatch.setattr(config, 'resource_credentials_factory', lambda *a, **kw: pretend.stub())
    s = config.configure()

    assert s['mmc.credentials'] is creds


def test_configure_with_defaults(monkeypatch):
    import aureus.config as config

    monkeypatch.setattr(config, 'mmc_credentials_factory', lambda *a, **kw: pretend.stub())
    monkeypatch.setattr(config, 'resource_credentials_factory', lambda *a, **kw: pretend.stub())

    creds = pretend.stub()
    defaults = {'mmc.credentials': creds}

    s = config.configure(defaults)

    assert s['mmc.credentials'] is creds
