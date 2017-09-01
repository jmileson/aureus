import pretend
from unittest.mock import Mock
import pytest

import aureus.mmc.app


def test_resource_url():
    from aureus.mmc import resource
    client = pretend.stub()

    res = resource.Resource(client)

    res._RESOURCE = 'fake'
    assert res.url == 'fake'

    res._RESOURCE = '/fake'
    assert res.url == 'fake'

    res._RESOURCE = 'fake/'
    assert res.url == 'fake'


def test_resource_member_url():
    from aureus.mmc import resource
    client = pretend.stub()

    res = resource.Resource(client)

    res._RESOURCE = 'fake'

    assert res.member_url('someResource') == 'fake/someResource'
    assert res.member_url('/someResource') == 'fake/someResource'
    assert res.member_url('/someResource/') == 'fake/someResource'


def test_resource_list():
    from aureus.mmc import resource

    val = {'key': 'value'}
    get = pretend.call_recorder(lambda *a, **kw: val)
    client = pretend.stub(get=get)

    res = resource.Resource(client)

    assert res.list() is val


def test_deletable_resource_delete():
    from aureus.mmc import resource

    val = {'key': 'value'}
    delete = pretend.call_recorder(lambda *a, **kw: val)
    client = pretend.stub(delete=delete)

    res = resource.DeletableResource(client)

    assert res.delete('someid') is val



def test_server_group():
    from aureus.mmc import resource

    val = {'data': [{
        'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/serverGroups/04cf9ef5-9d8b-4937-aa72-56c4b815b72f',
        'id': '04cf9ef5-9d8b-4937-aa72-56c4b815b72f',
        'name': 'Production',
        'serverCount': 1},
        {
            'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/serverGroups/1baf60d1-27f5-4aea-b8b9-aeb1d68abfd6',
            'id': '1baf60d1-27f5-4aea-b8b9-aeb1d68abfd6',
            'name': 'Test',
            'serverCount': 1}],
        'total': 2}
    client = pretend.stub(get=lambda *a, **kw: val)

    sg = resource.ServerGroup(client)

    assert sg.test['name'] == 'Test'
    assert sg.prod['name'] == 'Production'


def test_server_is_in_server_group():
    from aureus.mmc import resource

    val = {'data': [{
        'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/serverGroups/04cf9ef5-9d8b-4937-aa72-56c4b815b72f',
        'id': '04cf9ef5-9d8b-4937-aa72-56c4b815b72f',
        'name': 'Production',
        'serverCount': 1},
        {
            'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/serverGroups/1baf60d1-27f5-4aea-b8b9-aeb1d68abfd6',
            'id': '1baf60d1-27f5-4aea-b8b9-aeb1d68abfd6',
            'name': 'Test',
            'serverCount': 1}],
        'total': 2}
    client = pretend.stub(get=lambda *a, **kw: val)

    sg = resource.ServerGroup(client)

    server = {'agentUrl': 'https://jsstestmule01:7777/mmc-support',
              'agents': [{'description': 'Batch module default engine',
                          'name': 'DefaultBatchEngine'},
                         {'description': 'DevKit Extension Information',
                          'name': 'DevKitSplashScreenAgent'},
                         {'description': 'JMX Agent', 'name': 'jmx-agent'}],
              'groups': [{
                  'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/serverGroups/1baf60d1-27f5-4aea-b8b9-aeb1d68abfd6',
                  'name': 'Test'}],
              'hostIp': '10.14.0.99',
              'href': 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/servers/local$ffd9e51f-d241-4494-a9a1-19331cd19e47',
              'id': 'local$ffd9e51f-d241-4494-a9a1-19331cd19e47',
              'muleServerId': '.agent',
              'name': 'Test-3.8.4',
              'pausedServices': -1,
              'runningServices': -1,
              'started': 'Fri Aug 25 14:31:29 EDT 2017',
              'status': 'STOPPED',
              'stoppedServices': -1,
              'version': '3.8.4'}

    assert server in sg






    # todo: get server ids for Test and Production server groups
    # todo: get an application id (by name)
    # todo: get list of deployments for a specific application (by application name)

    # todo: logging for each phase
    # todo: build manifest rollback state to rollback the deployment in case of failures

    # find server ids for environment (Test or Production)
    # for each application in the manifest
    #   upload a new version of application to the repository
    #     this is convention based "application" is defined by
    #     the filename of the maven resource
    #   create a new deployment for an application
    #   find previous deployments for an application
    #   undeploy any deployed applications
    #   deploy the new deployment
