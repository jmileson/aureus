def test_resource_join():
    from aureus.helpers import resource_join

    assert resource_join('fake', 'fake2', 'fake3') == 'fake/fake2/fake3'
    assert resource_join('fake/', 'fake2', 'fake3') == 'fake/fake2/fake3'
    assert resource_join('fake', '/fake2', 'fake3') == 'fake/fake2/fake3'
    assert resource_join('fake/', '/fake2', 'fake3') == 'fake/fake2/fake3'
    assert resource_join('fake/', '/fake2', 'fake3/') == 'fake/fake2/fake3'
    assert resource_join('http://fake.com/api', 'fake', 'fake2', 'fake3/') == 'http://fake.com/api/fake/fake2/fake3'
    assert resource_join('http://fake.com/api/', 'fake', 'fake2', 'fake3/') == 'http://fake.com/api/fake/fake2/fake3'
    assert resource_join('http://fake.com/api', '/fake', 'fake2', 'fake3/') == 'http://fake.com/api/fake/fake2/fake3'
    assert resource_join('http://fake.com/api/', '/fake', 'fake2', 'fake3/') == 'http://fake.com/api/fake/fake2/fake3'

    assert resource_join('http://fake.com/api', 'fake') == 'http://fake.com/api/fake'
    assert resource_join('http://fake.com/api/', '/fake') == 'http://fake.com/api/fake'
