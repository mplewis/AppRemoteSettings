from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from appremotesettings.models import Identifier, DATATYPE_SLUGS

import plistlib
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()


def jsonify(data, *args, response=HttpResponse, **kwargs):
    for key, value in data.items():
        print(type(value))
    return response(*args, content=json.dumps(data, cls=DateTimeEncoder), content_type='application/json', **kwargs)


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
    keys = app.typed_keys()

    try:
        fmt = query['format']
    except KeyError:
        return jsonify(keys)

    if fmt == 'json':
        return jsonify(keys)

    elif fmt == 'json_annotated':
        # Store key-value pairs in "values"
        typed = {'values': keys}

        # Add type annotations and store in "types"
        annotations = {}
        for pair in app.key_set.all():
            key = pair.key
            ktype_raw = pair.datatype
            ktype = DATATYPE_SLUGS[ktype_raw]
            annotations[key] = ktype
        typed['types'] = annotations

        return jsonify(typed)

    elif fmt == 'plist':
        return HttpResponse(content=plistlib.dumps(keys), content_type='application/x-plist')

    else:
        return bad_request('Unsupported format "{}"'.format(fmt))
