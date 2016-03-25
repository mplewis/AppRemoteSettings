from appremotesettings import models
from appremotesettings.models import App, Key, Identifier

from django.test import Client

import pytest
import sure

import json


def post_json(client, url, data, *args, **kwargs):
    return client.post(url, *args, data=json.dumps(data),
                       content_type='application/json', **kwargs)


def test_v1_bad_method():
    c = Client()
    resp = c.get('/api/v1/')
    resp.status_code.should.eql(405)


@pytest.mark.django_db
def test_v1_no_json():
    c = Client()
    resp = c.post('/api/v1/', data={'dummy data': 'this is not json'})
    resp.status_code.should.eql(400)
    resp.content.decode().should.contain('Could not parse JSON')


@pytest.mark.django_db
def test_v1_no_app():
    data = {'app_id': 'com.mplewis.myapp'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(400)
    json.loads(resp.content.decode()).should.eql(
        {'error': 'No app found with identifier "com.mplewis.myapp"'})


@pytest.mark.django_db
def test_v1_app():
    app = App(name='MyApp')
    app.save()
    ident = Identifier(value='com.mplewis.myapp', app=app)
    ident.save()
    keys = [
        Key(app=app, key='BOOL_SETTING', value='true', datatype=models.DATATYPE_BOOL),
        Key(app=app, key='INT_SETTING', value='42', datatype=models.DATATYPE_INT),
        Key(app=app, key='STRING_SETTING', value='yarn', datatype=models.DATATYPE_STRING),
    ]
    for key in keys:
        key.save()

    data = {'app_id': 'com.mplewis.myapp'}
    c = Client()
    resp = post_json(c, '/api/v1/', data)
    resp.status_code.should.eql(200)
    json.loads(resp.content.decode()).should.eql(
        {'BOOL_SETTING': True,
         'INT_SETTING': 42,
         'STRING_SETTING': 'yarn'})
