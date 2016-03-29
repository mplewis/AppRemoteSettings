from django.http import HttpResponseRedirect
from django.test import Client
from django.core.urlresolvers import resolve

import sure


def test_trailing_slash_optional():
    expected = 'appremotesettings.views.select_api_version'
    resolve('/api/v1').view_name.should.equal(expected)
    resolve('/api/v2/').view_name.should.equal(expected)


def test_redirect_to_admin():
    c = Client()
    resp = c.get('/invalid/route/etc')
    type(resp).should.eql(HttpResponseRedirect)
    resp.url.should.eql('/admin/')
