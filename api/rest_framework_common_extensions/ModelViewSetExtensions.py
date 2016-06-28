__author__ = 'jxy'

import re

from django.db.models.query import QuerySet

from rest_framework.response import Response
from rest_framework import status as http_response_status

from utils.nsr_log import log_nsr_service

class ModelViewSetExtension():
    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.

            # queryset = queryset.all()

            queryset_filter_params = self.queryset_filter_params()
            queryset = self.queryset_filter_from_params(queryset, **queryset_filter_params)

            queryset_filter_fields = self.queryset_filter_fields()
            queryset = self.queryset_filter_from_url_params(queryset, *queryset_filter_fields)

        return queryset

    def queryset_filter_params(self):
        return {}

    def queryset_filter_fields(self):
        return []

    def queryset_filter_from_params(self, queryset, **kwargs):

        if len(kwargs) > 0:
            queryset = queryset.filter(**kwargs)
        else:
            queryset = queryset.all()

        return queryset

    def queryset_filter_from_url_params(self, queryset, *args):
        queryset_filter_dict = {}

        for field in args:
            value = self.request.query_params.get(field, None)
            if value:
                queryset_filter_dict[field] = value
        if len(queryset_filter_dict) > 0:
            queryset = queryset.filter(**queryset_filter_dict)
        else:
            queryset = queryset.all()

        return queryset

    def perform_get_data(self, initial_data, field, model_instance):
        if field in initial_data:
            return initial_data[field]
        else:
            return getattr(model_instance, field, None)

    def find_key_and_value_be_modified(self, key, data, model_instance):
        request_value = data.get(key, None)
        model_instance_value = getattr(model_instance, key, None)
        if (request_value is not None) and (str(request_value) != str(model_instance_value)):
            return True
        return False

    def value_cannot_be_modified(self, key, data, model_instance, request):
        if self.find_key_and_value_be_modified(key, data, model_instance) \
        and (not (request.user and request.user.is_authenticated())):
            raise Exception(key + ' cannot be modified!')

    def add_url(self, data, request, pk=None):
        data['url'] = 'http://' + request.get_host() + request.path
        if pk:
            data['url'] = data['url'] + str(pk) + '/'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        datas = serializer.data

        for data in datas:
            self.list_response_data_process(data, request, *args, **kwargs)
            self.add_url(data, request, data['id'])

        return Response(datas)

    def list_response_data_process(self, data, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, **self.perform_create_extra_parameters(request))
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        self.create_response_data_process(data, request, *args, **kwargs)
        return Response(data, status=http_response_status.HTTP_201_CREATED, headers=headers)

    def create_response_data_process(self, data, request, *args, **kwargs):
        pass

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def perform_create_extra_parameters(self, request):
        extra_parameters = dict()
        foreign_key_information = self.foreign_key_information()
        if foreign_key_information:
            model = foreign_key_information['model']
            field_name = foreign_key_information['field_name']
            pattern = foreign_key_information['list_name'] + r'/(?P<' + field_name + r'_pk>[^/.]+)/'
            match = re.search(pattern, request.path)
            if match:
                extra_parameters[field_name] = model.objects.get(id=match.group(field_name + '_pk'))

        return extra_parameters

    def foreign_key_information(self):
        return None

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, request)
        data = serializer.data
        self.update_response_data_process(data, request, *args, **kwargs)
        if self.perform_error_status:
            return Response(data, status=self.perform_error_status)
        else:
            return Response(data)

    def update_response_data_process(self, data, request, *args, **kwargs):
        pass

    def perform_update(self, serializer, request):
        self.perform_error_status = None
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.retrieve_response_data_process(data, request, *args, **kwargs)
        return Response(data)

    def retrieve_response_data_process(self, data, request, *args, **kwargs):
        pass