from django.test import Client

import sure


def test_v1_bad_method():
    c = Client()
    resp = c.get('/api/v1/',)
    resp.status_code.should.eql(405)


def test_v1_no_app():
    data = {'app_id': 'com.mplewis.myapp'}
    c = Client()
    resp = c.post('/api/v1/', data)
    resp.status_code.should.eql(400)
    resp.body.should.contain('No app found')
