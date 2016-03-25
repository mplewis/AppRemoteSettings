from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseBadRequest

from appremotesettings.models import Identifier

import json


def jsonify(response, data):
    return response(content=json.dumps(data))


def error(message):
    return {'error': message}


def bad_request(message):
    return jsonify(HttpResponseBadRequest, error(message))


def select_api_version(request, api_version):
    if api_version == '1':
        return api_v1(request)
    raise Http404('Invalid API version: "{}"'.format(api_version))


def api_v1(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], content='This endpoint only accepts POST')

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
    return app.name
