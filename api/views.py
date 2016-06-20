from rest_framework.decorators import api_view
from rest_framework.response import Response
from .urls import API_VERSION
# Create your views here.

@api_view(['GET'])
def api_version_root(request, format=None):
    full_url = 'http://' + request.get_host() + request.path
    api_version_url = {}
    for version_name in API_VERSION.keys():
        api_version_url[version_name] = full_url + API_VERSION[version_name]
    return Response(api_version_url)

