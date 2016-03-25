from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from appremotesettings.models import Identifier

import json


def jsonify(data, *args, response=HttpResponse, **kwargs):
    return response(*args, content=json.dumps(data), **kwargs)


def error(message):
    return {'error': message}


def not_found(message, *args, **kwargs):
    return jsonify(error(message), *args, response=HttpResponseNotFound, **kwargs)


def bad_request(message, *args, **kwargs):
    return jsonify(error(message), *args, response=HttpResponseBadRequest, **kwargs)


def not_allowed(message, *args, **kwargs):
    return jsonify(error(message), *args, response=HttpResponseNotAllowed, **kwargs)


def select_api_version(request, api_version):
    if api_version == '1':
        return api_v1(request)
    return not_found('Invalid API version: "{}"'.format(api_version))


def api_v1(request):
    if request.method != 'POST':
        return not_allowed('This endpoint only accepts POST', ['POST'])

    try:
        query = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return bad_request('Could not parse JSON')

    try:
        ident_raw = query['app_id']
    except KeyError:
        return bad_request('Key app_id was not present')

    ident = Identifier.objects.filter(value=ident_raw)
    if not ident:
        return bad_request('No app found with identifier "{}"'.format(ident_raw))

    app = ident[0].app
    return jsonify(app.typed_keys())
