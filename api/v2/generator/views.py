from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import status as http_response_status
from utils.nsr_log import log_nsr_service

from ostinato_light.drone import Drone
from ostinato_light.port_list import PortList
from ostinato_light.stream_list import StreamList
from ostinato_light.protocols import *


class GeneratorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = GeneratorModel.objects.all()
    serializer_class = GeneratorSerializer
    permission_classes = (# permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            tx_port_number = instance.port
            host_name = instance.ip
            tx_port_list = PortList()
            tx_port_list.add_port(port_number=tx_port_number)
            drone = Drone(host_name=host_name, tx_port_list=tx_port_list)
            drone.connect()
            instance.tx_rate = drone.fetch_stats_tx_port().tx_bps * 8
            drone.disconnect()
            log_nsr_service.warning('Drone fetch tx rate successful')
        except:
            instance.tx_rate = -1
            log_nsr_service.warning('Drone has not been started up')

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


    def perform_get_data(self, initial_data, field, default):
        if field in initial_data:
            return initial_data[field]
        else:
            return default

    def perform_update(self, serializer):
        instance = self.get_object()
        initial_data = serializer.initial_data
        status = self.perform_get_data(initial_data=initial_data, field='status', default=instance.status)
        tx_port_number = self.perform_get_data(initial_data=initial_data, field='port', default=instance.port)
        host_name = self.perform_get_data(initial_data=initial_data, field='ip', default=instance.ip)
        self.perform_error_status = None
        try:
            if 'status' in initial_data.keys():
                tx_port_list = PortList()
                tx_port_list.add_port(port_number=tx_port_number)
                tx_port = tx_port_list.current_port
                drone = Drone(host_name=host_name, tx_port_list=tx_port_list)
                drone.connect()
                # stream_list = StreamList(tx_port=tx_port, is_loop_mode=True)
                # stream_list.add_stream(is_stream_packet_size_random_mode=True,
                #                      stream_packet_size_random_min_bytes=800,
                #                      stream_packet_size_random_max_bytes=1200,
                #                      stream_packet_num=100,
                #                      stream_packets_per_second=50)
                # stream_list.current_stream.configure_protocols(MAC(src_mac='ab:cd:ef:11:00:22',
                #                                                 dst_mac='00:11:22:33:44:55',
                #                                                 src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
                #                                             Ethernet(),
                #                                             IP4(src_ip='1.1.1.1',
                #                                                 dst_ip='2.2.2.2'),
                #                                             TCP(src_port=77,
                #                                                 dst_port=90),
                #                                             )
                #
                # stream_list = StreamList(tx_port=tx_port, is_loop_mode=True)
                # stream_list.add_stream(is_stream_packet_size_random_mode=True,
                #                      stream_packet_size_random_min_bytes=800,
                #                      stream_packet_size_random_max_bytes=1200,
                #                      stream_packet_num=100,
                #                      stream_packets_per_second=30)
                # stream_list.current_stream.configure_protocols(MAC(src_mac='ab:cd:ef:11:00:22',
                #                                                 dst_mac='00:11:22:33:44:55',
                #                                                 src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
                #                                             Ethernet(),
                #                                             IP4(src_ip='1.1.1.1',
                #                                                 dst_ip='2.2.2.2'),
                #                                             TCP(src_port=77,
                #                                                 dst_port=90),
                #                                             )
                # drone.add_stream_list(stream_list)
                # drone.remove_stream_list(drone.fetch_stream_id_list())
                if status == 'Transmititing':
                    drone.start_transmit()
                else:
                    drone.stop_transmit()

                drone.disconnect()
            serializer.save()
            log_nsr_service.warning('Drone setup successful')
        except:
            self.perform_error_status = http_response_status.HTTP_304_NOT_MODIFIED
            log_nsr_service.warning('Drone has not been started up')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if self.perform_error_status:
            return Response(serializer.data, status=self.perform_error_status)
        else:
            return Response(serializer.data)

class StreamViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    jxyowen
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = StreamModel.objects.all()
    serializer_class = StreamSerializer
    permission_classes = (# permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(generator=self.kwargs['parent_lookup_generator_pk'])

    # def list(self, request, parent_lookup_pk=None):
    #     queryset = self.get_queryset()
    #     # queryset = self.queryset.filter(generator=self.kwargs['parent_lookup_pk'])
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None, **kwargs):
    #     queryset = self.queryset.get(id=pk)
    #     serializer = self.get_serializer(queryset)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     queryset = self.queryset.get(id=kwargs['pk'])
    #     serializer = self.get_serializer(queryset, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class ProtocolViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProtocolModel.objects.all()
    serializer_class = ProtocolSerializer
    permission_classes = (# permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    # lookup_field = 'generator'

    def get_queryset(self):
        return self.queryset.filter(stream=self.kwargs['parent_lookup_stream_pk'],
                                    # generator=self.kwargs['parent_lookup_generator_pk']
        )

    # def create(self, request, *args, **kwargs):
    #     kkk = request.data
    #     assert False
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def list(self, request, parent_lookup_stream_pk=None):
    #     queryset = self.queryset.filter(stream=self.kwargs['parent_lookup_stream_pk'])
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)