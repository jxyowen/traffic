from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import status



class SwtichViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = SwitchModel.objects.all()
    serializer_class = SwitchSerializer
    permission_classes = (# permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class VLANViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = VLANModel.objects.all()
    serializer_class = VLANSerializer
    permission_classes = (# permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(switch=self.kwargs['parent_lookup_switch_pk'])
