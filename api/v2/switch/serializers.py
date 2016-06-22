# -*- coding:utf-8 -*-
__author__ = 'jxy'

from rest_framework import serializers
from api.models import *
from api.rest_framework_common_extensions.MultiplePKsHyperlinked import *


class SwitchSerializer(serializers.HyperlinkedModelSerializer):

    vlans = serializers.HyperlinkedIdentityField(
        view_name='vlan-list',
        lookup_url_kwarg='parent_lookup_switch_pk',
    )

    class Meta:
        model = SwitchModel
        fields = ('id',
                  'name',
                  'ip',
                  'user',
                  'password',
                  'vlans',
        )


class VLANSerializer(serializers.HyperlinkedModelSerializer):

    # protocols = MultiplePKsHyperlinkedIdentityField(view_name='protocol-list',
    #                                                 lookup_fields=['generator_id', 'id'],
    #                                                 lookup_url_kwargs=['parent_lookup_generator_pk', 'parent_lookup_stream_pk']
    # )

    switch = MultiplePKsHyperlinkedRelatedField(allow_null=True,
                                                 queryset=SwitchModel.objects.all(),
                                                 required=False,
                                                 view_name='switch-detail',
                                                 lookup_fields=['id'],
                                                 lookup_url_kwargs=['pk']
    )

    # 用于配置相应url的  ， 对应正则表达式上的变量名，设成对应表中的字段的值，由此生成 url
    # HyperlinkedIdentityField所用表为当前Serializer的model，HyperlinkedRelatedField所用表为设置queryset的model

    class Meta:

        model = VLANModel
        fields = (
                  'switch',
                  # 'protocols',
                  'id',
                  'mode'
                  )