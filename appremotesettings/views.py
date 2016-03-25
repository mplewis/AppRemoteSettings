from django.http import HttpResponse, Http404, HttpResponseNotAllowed

from appremotesettings.models import Identifier


def select_api_version(request, api_version):
    if api_version == '1':
        return api_v1(request)
    raise Http404('Invalid API version: "{}"'.format(api_version))


def api_v1(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], content='This endpoint only accepts POST')
    return HttpResponse('POST')
