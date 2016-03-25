import json

from django.test import Client

import pytest
import sure


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
