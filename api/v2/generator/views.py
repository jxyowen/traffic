# -*- coding:utf-8 -*-
import json
import traceback

from rest_framework import viewsets
from rest_framework import permissions as official_permissions

from rest_framework import status as http_response_status

from rest_framework_extensions.mixins import NestedViewSetMixin

from api.rest_framework_common_extensions.ModelViewSetExtensions import ModelViewSetExtension
from api.const import *

from ostinato_light.drone import Drone
from ostinato_light.port_list import PortList
from ostinato_light.stream_list import StreamList
from ostinato_light.protocols import *

from utils.nsr_log import log_nsr_service

from .serializers import *


class GeneratorViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = GeneratorModel.objects.all()
    serializer_class = GeneratorSerializer
    permission_classes = (official_permissions.IsAuthenticatedOrReadOnly, )


    def generator_parameters_fetch_from_drone(self, generator):
        try:
            tx_port_number = generator['port_in_use']
            host_name = generator['ip']
            tx_port_list = PortList()
            tx_port_list.add_port(port_number=tx_port_number)
            drone = Drone(host_name=host_name, tx_port_list=tx_port_list)
            drone.connect()
            tx_stats = drone.fetch_stats_tx_port()
            generator['tx_rate'] = tx_stats.tx_bps * 8
            generator['port_available'] = list()
            for port in drone.get_port_config_list().port:
                generator['port_available'].append('port %d   name: %s   description: %s' % (port.port_id.id, port.name, port.description))
            if tx_stats.state.is_transmit_on:
                generator['status'] = GeneratorEnum.STATUS_TRANSMITITING
            else:
                generator['status'] = GeneratorEnum.STATUS_IDLE
            drone.disconnect()

            generator_object = GeneratorModel.objects.get(id=generator['id'])
            generator_object.status = generator['status']
            generator_object.save()

            log_nsr_service.warning('Drone fetch tx rate successful')
        except Exception, e:
            log_nsr_service.warning(traceback.format_exc())
            log_nsr_service.warning(e)
            generator['status'] = GeneratorEnum.STATUS_ERROR
            log_nsr_service.warning('Drone has not been started up')


    def get_protocol_class(self, protocol_class_name):
        protocol_class_mapping = dict(mac=MAC,
                                      vlan=VLAN,
                                      vlanstack=VLANStack,

                                      ethernet=Ethernet,

                                      ip4=IP4,
                                      arp=ARP,
                                      tcp=TCP,
                                      udp=UDP,
                                      icmp=ICMP,
                                      igmp=IGMP,
                                      igmpipaddress=IGMPIPAddress,

                                      textprotocol=TextProtocol,
                                      payload=Payload,
                                      hexdump=HexDump,
                                      userscript=UserScript
        )

        if protocol_class_name.lower() in protocol_class_mapping.keys():
            return protocol_class_mapping[protocol_class_name.lower()]
        return None

    def configure_protocol(self, protocol_configuration):

        if isinstance(protocol_configuration, dict):
            for field_name, configuration in protocol_configuration.items():
                protocol_configuration[field_name] = self.configure_protocol(configuration)
            protocol_class = self.get_protocol_class(protocol_configuration.pop('protocol_class_name', None))
            if protocol_class is None:
                return None
            else:
                return protocol_class(**protocol_configuration)
        elif isinstance(protocol_configuration, list):
            for index, configuration in enumerate(protocol_configuration):
                # log_nsr_service.warning(index)
                # log_nsr_service.warning(configuration)
                protocol_configuration[index] = self.configure_protocol(configuration)
            return protocol_configuration
        else:
            if isinstance(protocol_configuration, unicode):
                return protocol_configuration.encode('utf-8')
            else:
                return protocol_configuration

    def configure_stream_list(self, generator_id, stream_list):
        streams = StreamModel.objects.filter(generator=generator_id)
        for stream in streams:
            stream_configuration = json.loads(stream.configuration)
            # for k,v in stream_configuration.items():
            #     log_nsr_service.warning(k + '  ' + str(v))
            protocols = ProtocolModel.objects.filter(stream=stream.id)
            protocol_list = list()
            for protocol in protocols:
                protocol_configuration = json.loads(protocol.configuration)
                protocol_object = self.configure_protocol(protocol_configuration)
                if protocol_object is not None:
                    protocol_list.append(protocol_object)
            if len(protocol_list) > 0:
                stream_list.add_stream(**stream_configuration)
                stream_list.current_stream.configure_protocols(*protocol_list)

    def perform_update(self, serializer):
        instance = self.get_object()
        initial_data = serializer.initial_data
        generator_id = self.perform_get_data(initial_data=initial_data, field='id', model_instance=instance)
        status = self.perform_get_data(initial_data=initial_data, field='status', model_instance=instance)
        mode = self.perform_get_data(initial_data=initial_data, field='mode', model_instance=instance)
        tx_port_number = self.perform_get_data(initial_data=initial_data, field='port_in_use', model_instance=instance)
        host_name = self.perform_get_data(initial_data=initial_data, field='ip', model_instance=instance)
        self.perform_error_status = None
        try:
            if 'status' in initial_data.keys():
                tx_port_list = PortList()
                tx_port_list.add_port(port_number=tx_port_number)
                tx_port = tx_port_list.current_port
                drone = Drone(host_name=host_name, tx_port_list=tx_port_list)
                drone.connect()

                if status == GeneratorEnum.STATUS_TRANSMITITING:
                    drone.stop_transmit()
                    current_stream_id_list = drone.fetch_stream_id_list()
                    drone.remove_stream_list(current_stream_id_list)
                    if mode == GeneratorEnum.MODE_LOOP:
                        is_loop_mode = True
                    else:
                        is_loop_mode = False
                    stream_list = StreamList(tx_port=tx_port, is_loop_mode=is_loop_mode)
                    self.configure_stream_list(generator_id=generator_id, stream_list=stream_list)
                    drone.add_stream_list(stream_list)
                    drone.start_transmit()
                else:
                    drone.stop_transmit()

                drone.disconnect()
            serializer.save()
            log_nsr_service.warning('Drone setup successful')
        except Exception, e:
            self.perform_error_status = http_response_status.HTTP_304_NOT_MODIFIED
            log_nsr_service.warning(traceback.format_exc())
            log_nsr_service.warning(e)
            log_nsr_service.warning('Drone has not been started up')

    def update_response_data_process(self, data, request, *args, **kwargs):
        self.generator_parameters_fetch_from_drone(data)

    def list_response_data_process(self, data, request, *args, **kwargs):
        self.generator_parameters_fetch_from_drone(data)

    def retrieve_response_data_process(self, data, request, *args, **kwargs):
        self.generator_parameters_fetch_from_drone(data)


class StreamViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = StreamModel.objects.all()
    serializer_class = StreamSerializer

    def get_queryset(self):
        return self.queryset.filter(generator=self.kwargs['parent_lookup_generator_pk'])

    def foreign_key_information(self):
        foreign_key_information = dict(model=GeneratorModel, field_name='generator', list_name='generators')
        return foreign_key_information


class ProtocolViewSet(ModelViewSetExtension, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProtocolModel.objects.all()
    serializer_class = ProtocolSerializer

    def get_queryset(self):
        return self.queryset.filter(stream=self.kwargs['parent_lookup_stream_pk'],
                                    # generator=self.kwargs['parent_lookup_generator_pk']
        )

    def foreign_key_information(self):
        foreign_key_information = dict(model=StreamModel, field_name='stream', list_name='streams')
        return foreign_key_information