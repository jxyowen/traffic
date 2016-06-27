# -*- coding:utf-8 -*-
import traceback

from rest_framework import viewsets
from rest_framework import permissions as official_permissions

from rest_framework import status as http_response_status

from rest_framework_extensions.mixins import NestedViewSetMixin

from api.rest_framework_common_extensions.ModelViewSetExtensions import ModelViewSetExtension
from api.rest_framework_common_extensions.permissions import *

from utils.nsr_log import log_nsr_service

from .serializers import *


class SwitchViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = SwitchModel.objects.all()
    serializer_class = SwitchSerializer
    permission_classes = (official_permissions.IsAuthenticatedOrReadOnly, )




class VLANViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = VLANModel.objects.all()
    serializer_class = VLANSerializer
    permission_classes = (IsAuthenticatedOrNotPostDelete, )

    def get_queryset(self):
        return self.queryset.filter(switch=self.kwargs['parent_lookup_switch_pk'])

    def connect_switch_and_enter_system_view(self, switch_controller):
        if not self.__is_switch_configurations_need_to_save:
            self.__is_switch_configurations_need_to_save = True
            switch_controller.connect()
            switch_controller.enter_system_view()

    def perform_update_vlan_status_changed(self, switch_controller, vlan_id, status, initial_data, instance):
        if self.find_key_and_value_be_modified('status', initial_data, instance):
            self.connect_switch_and_enter_system_view(switch_controller)
            if status == VLANEnum.STATUS_IDLE:
                switch_controller.traffic_remove(vlan_id)
                switch_controller.acl_remove(vlan_id)
                switch_controller.vlan_remove(vlan_id)
            elif status == VLANEnum.STATUS_USED:
                switch_controller.vlan_add(vlan_id)
                switch_controller.acl_add(vlan_id)
                switch_controller.acl_add_deny_any()

    def perform_update_vlan_mode_changed(self):
        pass

    def perform_update_vlan_traffic_changed(self):
        pass

    def perform_update(self, serializer):
        self.perform_error_status = None
        instance = self.get_object()
        initial_data = serializer.initial_data
        switch = instance.switch
        vlan_id = instance.vlan_id
        status = self.perform_get_data(initial_data=initial_data, field='status', model_instance=instance)
        mode = self.perform_get_data(initial_data=initial_data, field='mode', model_instance=instance)
        traffic = self.perform_get_data(initial_data=initial_data, field='traffic', model_instance=instance)
        try:
            self.__is_switch_configurations_need_to_save = False

            self.value_cannot_be_modified('vlan_id', initial_data, instance)

            switch_controller = SwitchEnum.CLASS_MAPPING[switch.type](user=switch.user,
                                                                      password=switch.password,
                                                                      ip=switch.ip,
                                                                      system_name=switch.system_name)


            self.perform_update_vlan_status_changed(switch_controller, vlan_id, status, initial_data, instance)

            self.perform_update_vlan_mode_changed()

            self.perform_update_vlan_traffic_changed()

            if self.__is_switch_configurations_need_to_save:
                switch_controller.save()
                switch_controller.disconnect()

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