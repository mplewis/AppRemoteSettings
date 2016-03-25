from django.core.exceptions import ValidationError

from appremotesettings.models import App, Key
from appremotesettings import models

from datetime import datetime
from dateutil.tz import tzlocal

import pytest
import sure


@pytest.mark.django_db
def test_app_keys():
    app = App(name='TestApp', desc='TestDesc')
    app.save()
    keys = [
        Key(app=app, desc='KeyDesc', key='TEST_BOOL', value='true', datatype=models.DATATYPE_BOOL),
        Key(app=app, desc='KeyDesc', key='TEST_INT', value='42', datatype=models.DATATYPE_INT),
        Key(app=app, desc='KeyDesc', key='TEST_FLOAT', value='3.14159', datatype=models.DATATYPE_FLOAT),
        Key(app=app, desc='KeyDesc', key='TEST_STRING', value='yarn', datatype=models.DATATYPE_STRING),
        Key(app=app, desc='KeyDesc', key='TEST_DATE', value='2016-03-25T02:07:15+00:00', datatype=models.DATATYPE_DATE),
    ]
    for key in keys:
        key.save()
    app.typed_keys().should.eql({
        'TEST_BOOL': True,
        'TEST_INT': 42,
        'TEST_FLOAT': 3.14159,
        'TEST_STRING': 'yarn',
        'TEST_DATE': datetime(2016, 3, 25, 2, 7, 15, tzinfo=tzlocal())
    })


@pytest.mark.django_db
def test_bad_casting():
    app = App(name='TestApp', desc='TestDesc')
    app.save()
    key = Key(app=app, desc='KeyDesc', key='TEST_BOOL', value='Invalid', datatype=models.DATATYPE_BOOL)
    key.clean.when.called_with().should.throw(ValidationError)


@pytest.mark.django_db
def test_date_to_iso8601():
    app = App(name='TestApp', desc='TestDesc')
    app.save()
    key = Key(app=app, desc='KeyDesc', key='TEST_DATE', value='Jan 11, 1992, 7:34 PM -6', datatype=models.DATATYPE_DATE)
    key.clean()
    key.save()
    key.value.should.eql('1992-01-11T19:34:00-06:00')
