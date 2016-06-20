from django.conf.urls import url, include
# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

API_VERSION = dict(v1='v1',
                   v2='v2'
)

urlpatterns = [
    url(r'^$', 'api.views.api_version_root'),
]

for version_name, version in API_VERSION.items():
    urlpatterns.append(url(r'^' + version + r'/', include(r'api.' + version + r'.urls', namespace=version)))