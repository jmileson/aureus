import pretend
import pytest


def test_resource_url():
    from aureus.mmc import resource
    client = pretend.stub(base_url='http://fake.com/api/')

    res = resource.Resource(client)

    res._RESOURCE = 'fake'
    assert res.url == 'http://fake.com/api/fake'

    res._RESOURCE = '/fake'
    assert res.url == 'http://fake.com/api/fake'


def test_resource_member_url():
    from aureus.mmc import resource
    client = pretend.stub(base_url='http://fake.com/api/')

    res = resource.Resource(client)

    res._RESOURCE = 'fake'

    assert res.member_url('someResource') == 'http://fake.com/api/fake/someResource'
    assert res.member_url('/someResource') == 'http://fake.com/api/fake/someResource'

