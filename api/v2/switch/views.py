# -*- coding:utf-8 -*-
import traceback
import re

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status as http_response_status

from rest_framework_extensions.mixins import NestedViewSetMixin

from api.rest_framework_common_extensions.ModelViewSetExtensions import ModelViewSetUpdateExtension

from utils.nsr_log import log_nsr_service
from utils.HWS5700SwitchController import HWS5700SwitchController

from .serializers import *
from .permissions import IsOwnerOrReadOnly


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


class VLANViewSet(NestedViewSetMixin, viewsets.ModelViewSet, ModelViewSetUpdateExtension):
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

    def perform_update(self, serializer):
        instance = self.get_object()
        initial_data = serializer.initial_data
        switch = self.perform_get_data(initial_data=initial_data, field='switch', model_instance=instance)
        status = self.perform_get_data(initial_data=initial_data, field='status', model_instance=instance)
        mode = self.perform_get_data(initial_data=initial_data, field='mode', model_instance=instance)
        traffic = self.perform_get_data(initial_data=initial_data, field='traffic', model_instance=instance)
        self.perform_error_status = None
        try:

            self.find_key_and_value_changed('switch', initial_data, instance)
            serializer.save()
            log_nsr_service.warning('Setup successful')
        except Exception, e:
            self.perform_error_status = http_response_status.HTTP_304_NOT_MODIFIED
            log_nsr_service.warning(traceback.format_exc())
            log_nsr_service.warning(e)
            log_nsr_service.warning('Setup failed')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        generators = serializer.data
        if self.perform_error_status:
            return Response(generators, status=self.perform_error_status)
        else:
            return Response(generators)

