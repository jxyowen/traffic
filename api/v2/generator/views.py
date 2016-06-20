from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import status



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

    # def retrieve(self, request, parent_lookup_pk=None, pk=None):
    #     queryset = self.queryset.get(generator=parent_lookup_pk, id=pk)
    #     serializer = self.get_serializer(queryset)
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