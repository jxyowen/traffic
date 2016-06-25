from django.db import models
from django.contrib import admin

from .const import *
# Create your models here.


class GeneratorModel(models.Model):
    STATUS_CHOICES = (
        (GeneratorEnum.STATUS_IDLE, GeneratorEnum.STATUS_IDLE),
        (GeneratorEnum.STATUS_TRANSMITITING, GeneratorEnum.STATUS_TRANSMITITING),
    )

    MODE_CHOICES = (
        (GeneratorEnum.MODE_NORMAL, GeneratorEnum.MODE_NORMAL),
        (GeneratorEnum.MODE_LOOP, GeneratorEnum.MODE_LOOP),
    )

    id = models.PositiveIntegerField(primary_key=True, verbose_name="ID")
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    port_in_use = models.IntegerField(
        default=0
    )
    # tx_rate = models.IntegerField(
    #     default=0
    # )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default=GeneratorEnum.MODE_NORMAL)
    # owner = models.ForeignKey('auth.User', related_name='generator')

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  ip: %s ' % (self.id, self.ip)


class StreamModel(models.Model):
    generator = models.ForeignKey(GeneratorModel, null=False)
    created = models.DateTimeField(auto_now_add=True)

    configuration = models.TextField()

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  configuration: %s ' % (self.id, self.configuration)


class ProtocolModel(models.Model):
    stream = models.ForeignKey(StreamModel, null=False)
    # generator = models.ForeignKey(GeneratorModel, null=False)
    created = models.DateTimeField(auto_now_add=True)

    configuration = models.TextField()

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  configuration: %s ' % (self.id, self.configuration)


class SwitchModel(models.Model):
    TYPE_CHOICES = (
        (SwitchEnum.TYPE_HUAWEI, SwitchEnum.TYPE_HUAWEI),
        (SwitchEnum.TYPE_H3C, SwitchEnum.TYPE_H3C),
    )

    id = models.PositiveIntegerField(primary_key=True, verbose_name="ID")
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    logged_in_symbol = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50, default='switch')
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  ip: %s ' % (self.id, self.ip)


class VLANModel(models.Model):
    MODE_CHOICES = (
        (VLANEnum.MODE_NONE, VLANEnum.MODE_NONE),
        (VLANEnum.MODE_ACCESS, VLANEnum.MODE_ACCESS),
        (VLANEnum.MODE_TRUNK, VLANEnum.MODE_TRUNK),
        (VLANEnum.MODE_HYBRID, VLANEnum.MODE_HYBRID),
    )

    STATUS_CHOICES = (
        (VLANEnum.STATUS_IDLE, VLANEnum.STATUS_IDLE),
        (VLANEnum.STATUS_USED, VLANEnum.STATUS_USED)
    )

    TRAFFIC_CHOICES = (
        (VLANEnum.TRAFFIC_OFF, VLANEnum.TRAFFIC_OFF),
        (VLANEnum.TRAFFIC_ON, VLANEnum.TRAFFIC_ON),
    )

    vlan_id = models.PositiveIntegerField(null=False)
    switch = models.ForeignKey(SwitchModel, null=False)
    created = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    traffic = models.CharField(max_length=10, choices=TRAFFIC_CHOICES)

    class Meta:
        ordering = ('vlan_id',)

    def __unicode__(self):
        return 'id: %s  mode: %s ' % (self.id, self.mode)


admin.site.register(GeneratorModel)
admin.site.register(SwitchModel)
