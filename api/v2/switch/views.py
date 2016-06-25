# -*- coding:utf-8 -*-
import traceback
import re

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status as http_response_status

from rest_framework_extensions.mixins import NestedViewSetMixin

from api.rest_framework_common_extensions.ModelViewSetExtensions import ModelViewSetExtension

from utils.nsr_log import log_nsr_service
from utils.HWS5700SwitchController import HWS5700SwitchController

from .serializers import *
from .permissions import IsOwnerOrReadOnly


class SwitchViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
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


class VLANViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
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
        self.perform_error_status = None
        instance = self.get_object()
        initial_data = serializer.initial_data
        vlan_id = self.perform_get_data(initial_data=initial_data, field='vlan_id', model_instance=instance)
        status = self.perform_get_data(initial_data=initial_data, field='status', model_instance=instance)
        mode = self.perform_get_data(initial_data=initial_data, field='mode', model_instance=instance)
        traffic = self.perform_get_data(initial_data=initial_data, field='traffic', model_instance=instance)
        try:
            if self.find_key_and_value_changed('vlan_id', initial_data, instance):
                raise Exception('vlan_id cannot be modified!')

            if self.find_key_and_value_changed('status', initial_data, instance):
                switch = instance.switch
                hw_s5700 = HWS5700SwitchController()
                hw_s5700.connect(user=switch.user,
                                 password=switch.password,
                                 ip=switch.ip,
                                 logged_in_symbol=switch.type)
                hw_s5700.enter_system_view()


            if self.find_key_and_value_changed('mode', initial_data, instance):
                pass

            if self.find_key_and_value_changed('traffic', initial_data, instance):
                pass

            serializer.save()
            log_nsr_service.warning('Setup successful')
        except Exception, e:
            self.perform_error_status = http_response_status.HTTP_304_NOT_MODIFIED
            log_nsr_service.warning(traceback.format_exc())
            log_nsr_service.warning(e)
            log_nsr_service.warning('Setup failed')

    def foreign_key_information(self):
        foreign_key_information = dict(model=SwitchModel, field_name='switch', list_name='switches')
        return foreign_key_information