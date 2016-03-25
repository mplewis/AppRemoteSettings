from appremotesettings import models
from appremotesettings.models import App, Key, Identifier

from django.test import Client

import pytest
import sure

import json
import plistlib


def post_json(client, url, data, *args, **kwargs):
    return client.post(url, *args, data=json.dumps(data),
                       content_type='application/json', **kwargs)


def json_from(response):
    return json.loads(response.content.decode())


def create_app_and_keys():
    app = App(name='MyApp')
    app.save()
    ident = Identifier(value='com.mplewis.myapp', app=app)
    ident.save()
    keys = [
        Key(app=app, key='BOOL_SETTING', value='true', datatype=models.DATATYPE_BOOL),
        Key(app=app, key='INT_SETTING', value='42', datatype=models.DATATYPE_INT),
        Key(app=app, key='STRING_SETTING', value='yarn', datatype=models.DATATYPE_STRING),
        # TODO: Test and verify dates are serialized properly to JSON
    ]
    for key in keys:
        key.save()

expected_keys = {
    'BOOL_SETTING': True,
    'INT_SETTING': 42,
    'STRING_SETTING': 'yarn'
}


def test_v1_bad_method():
    c = Client()
    resp = c.get('/api/v1/')
    resp.status_code.should.eql(405)


@pytest.mark.django_db
def test_v1_no_json():
    c = Client()
    resp = c.post('/api/v1/', data={'dummy data': 'this is not json'})
    resp.status_code.should.eql(400)
    json_from(resp).should.eql({'error': 'Could not parse JSON'})


@pytest.mark.django_db
def test_v1_no_app():
    data = {'app_id': 'com.mplewis.myapp'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(400)
    json_from(resp).should.eql(
        {'error': 'No app found with identifier "com.mplewis.myapp"'})


@pytest.mark.django_db
def test_v1_json():
    create_app_and_keys()
    data = {'app_id': 'com.mplewis.myapp'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(200)
    resp['Content-Type'].should.eql('application/json')
    json_from(resp).should.eql(expected_keys)


@pytest.mark.django_db
def test_v1_plist():
    create_app_and_keys()
    data = {'app_id': 'com.mplewis.myapp', 'format': 'plist'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(200)
    resp['Content-Type'].should.eql('application/x-plist')
    plistlib.loads(resp.content).should.eql(expected_keys)


@pytest.mark.django_db
def test_v1_bad_format():
    create_app_and_keys()
    data = {'app_id': 'com.mplewis.myapp', 'format': 'invalid'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(400)
    json_from(resp).should.eql({'error': 'Unsupported format "invalid"'})
