from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter



# Create a router and register our viewsets with it.
from .generator import views
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

router.register(r'generators', views.GeneratorViewSet)\
      .register(r'streams',
                views.StreamViewSet,
                base_name='stream',
                parents_query_lookups=['generator_pk'])\
      .register(r'protocols',
                views.ProtocolViewSet,
                base_name='protocol',
                parents_query_lookups=['generator_pk', 'stream_pk'])

router1 = ExtendedDefaultRouter()

router1.register(r'streams', views.StreamViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(router1.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = router.urls

