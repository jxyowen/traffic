# -*- coding:utf-8 -*-
__author__ = 'jxy'



from rest_framework import serializers
from api.models import *
from api.rest_framework_common_extensions.HyperlinkedExtensions import *
from utils.nsr_log import log_nsr_service

class GeneratorSerializer(serializers.HyperlinkedModelSerializer):

    # url = MultiplePKsHyperlinkedIdentityField(view_name='generator-detail',
    #                                           lookup_fields=['id'],
    #                                           lookup_url_kwargs=['pk']
    # )

    streams = serializers.HyperlinkedIdentityField(
        view_name='stream-list',
        lookup_url_kwarg='parent_lookup_generator_pk',
    )

    class Meta:
        model = GeneratorModel
        fields = (
                  'ip',
                  'id',
                  'port_in_use',
                  'status',
                  'mode',
                  'streams'
        )


class StreamSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    # url = MultiplePKsHyperlinkedIdentityField(view_name='stream-detail',
    #                                           lookup_fields=['generator_id', 'id'],
    #                                           lookup_url_kwargs=['parent_lookup_generator_pk', 'pk']
    # )

    protocols = MultiplePKsHyperlinkedIdentityField(view_name='protocol-list',
                                                    lookup_fields=['generator_id', 'id'],
                                                    lookup_url_kwargs=['parent_lookup_generator_pk', 'parent_lookup_stream_pk']
    )

    # generator = MultiplePKsHyperlinkedRelatedField(allow_null=True,
    #                                              queryset=GeneratorModel.objects.all(),
    #                                              required=False,
    #                                              view_name='generator-detail',
    #                                              lookup_fields=['id'],
    #                                              lookup_url_kwargs=['pk']
    # )

    # 用于配置相应url的  ， 对应view url正则表达式上的变量名，设成对应表中的字段的值，由此生成 url
    # HyperlinkedIdentityField所用表为当前Serializer的model，HyperlinkedRelatedField所用表为设置queryset的model

    class Meta:

        model = StreamModel
        fields = (
                  # 'url',
                  'configuration',
                  # 'generator',
                  'protocols',
                  'id'
                  )


class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    # url = MultiplePKsHyperlinkedIdentityField(view_name='protocol-detail',
    #                                           lookup_fields=['generator_id', 'stream_id', 'id'],
    #                                                 lookup_url_kwargs=['parent_lookup_generator_pk', 'parent_lookup_stream_pk', 'pk']
    # )


    # stream = MultiplePKsHyperlinkedRelatedField(
    #                                              allow_null=False,
    #                                              # queryset=StreamModel.objects.all(),
    #                                              required=False,
    #                                              view_name='stream-detail',
    #                                              lookup_fields=['generator_id', 'id'],
    #                                              lookup_url_kwargs=['parent_lookup_generator_pk', 'pk'],
    #                                              read_only=True
    # )
    #
    # generator = MultiplePKsHyperlinkedRelatedField(
    #                                              allow_null=False,
    #                                              # queryset=GeneratorModel.objects.all(),
    #                                              required=False,
    #                                              view_name='generator-detail',
    #                                              # lookup_fields=['id'],
    #                                              # lookup_url_kwargs=['pk'],
    #                                              read_only=True
    # )

    class Meta:

        model = ProtocolModel
        fields = (
                  # 'url',
                  'configuration',
                  # 'generator',
                  # 'stream',
                  'id'
                  )

        # read_only_fields = (
        #                   'configuration',
        #                   'id'
        # )
