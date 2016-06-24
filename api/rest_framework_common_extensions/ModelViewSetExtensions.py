__author__ = 'jxy'

import re
from rest_framework.response import Response

class ModelViewSetExtension():
    def perform_get_data(self, initial_data, field, model_instance):
        if field in initial_data:
            return initial_data[field]
        else:
            return getattr(model_instance, field, None)

    def find_key_and_value_changed(self, key, data, model_instance):
        is_raise_exception = False
        request_value = data.get(key, None)
        model_instance_value = getattr(model_instance, key, None)
        if (model_instance_value is not None) and hasattr(model_instance_value, 'id'):
            model_instance_value = getattr(model_instance_value, 'id', None)
            if request_value is not None:
                request_value = re.findall(r'\d+', request_value)
                if len(request_value) > 0:
                    request_value = int(request_value[-1])
            is_raise_exception = True

        if (request_value is not None) and (request_value != model_instance_value):
            if is_raise_exception:
                raise Exception(key + ' field can not be modified!')
            return True
        return False

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
            self.add_url(data, request, data['id'])

        return Response(datas)