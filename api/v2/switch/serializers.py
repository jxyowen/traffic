# -*- coding:utf-8 -*-
__author__ = 'jxy'

from rest_framework import serializers
from api.models import *
from api.rest_framework_common_extensions.HyperlinkedExtensions import *


class SwitchSerializer(serializers.HyperlinkedModelSerializer):

    # url = MultiplePKsHyperlinkedIdentityField(view_name='switch-detail',
    #                                           lookup_fields=['id'],
    #                                           lookup_url_kwargs=['pk']
    # )

    vlans = serializers.HyperlinkedIdentityField(
        view_name='vlan-list',
        lookup_url_kwarg='parent_lookup_switch_pk',
    )

    class Meta:
        model = SwitchModel
        fields = (
                  # 'url',
                  'id',
                  'name',
                  'ip',
                  'user',
                  'password',
                  'type',
                  'logged_in_symbol',
                  'vlans',
        )


class VLANSerializer(serializers.HyperlinkedModelSerializer):

    # url = MultiplePKsHyperlinkedIdentityField(view_name='vlan-detail',
    #                                           lookup_fields=['switch_id', 'id'],
    #                                           lookup_url_kwargs=['parent_lookup_switch_pk', 'pk']
    # )
    #
    # switch = MultiplePKsHyperlinkedRelatedField(allow_null=True,
    #                                              queryset=SwitchModel.objects.all(),
    #                                              required=False,
    #                                              view_name='switch-detail',
    #                                              lookup_fields=['id'],
    #                                              lookup_url_kwargs=['pk']
    # )

    # 用于配置相应url的  ， 对应正则表达式上的变量名，设成对应表中的字段的值，由此生成 url
    # HyperlinkedIdentityField所用表为当前Serializer的model，HyperlinkedRelatedField所用表为设置queryset的model

    class Meta:

        model = VLANModel
        fields = (
                  # 'url',
                  'vlan_id',
                  # 'switch',
                  'id',
                  'mode',
                  'status',
                  'traffic'
                  )