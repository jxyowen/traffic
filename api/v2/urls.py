from django.conf.urls import url, include
# Create a router and register our viewsets with it.
from .generator import views as generator_views
from .switch import views as switch_views
from rest_framework_extensions.routers import ExtendedDefaultRouter


nested_router = ExtendedDefaultRouter()

nested_router.register(r'generators',
                       generator_views.GeneratorViewSet,
                       base_name='generator')\
             .register(r'streams',
                       generator_views.StreamViewSet,
                       base_name='stream',
                       parents_query_lookups=['generator_pk'])\
             .register(r'protocols',
                       generator_views.ProtocolViewSet,
                       base_name='protocol',
                       parents_query_lookups=['generator_pk', 'stream_pk'])


nested_router.register(r'switches',
                       switch_views.SwitchViewSet,
                       base_name='switch')\
             .register(r'vlans',
                       switch_views.VLANViewSet,
                       base_name='vlan',
                       parents_query_lookups=['switch_pk'])

urlpatterns = [
    url(r'^', include(nested_router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = router.urls

