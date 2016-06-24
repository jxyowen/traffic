from django.db import models
from django.contrib import admin
# Create your models here.


class GeneratorModel(models.Model):
    STATUS_CHOICES = (
        (u'Idle', u'Idle'),
        (u'Transmititing', u'Transmititing'),
    )

    MODE_CHOICES = (
        (u'Normal', u'Normal'),
        (u'Loop', u'Loop'),
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
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default=u'Normal')
    # owner = models.ForeignKey('auth.User', related_name='generator')

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  ip: %s ' % (self.id, self.ip)
admin.site.register(GeneratorModel)


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
    id = models.PositiveIntegerField(primary_key=True, verbose_name="ID")
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    name = models.CharField(max_length=50, default='switch')
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  ip: %s ' % (self.id, self.ip)


class VLANModel(models.Model):
    MODE_CHOICES = (
        (u'None', u'None'),
        (u'Access', u'Access'),
        (u'Trunk', u'Trunk'),
        (u'Hybrid', u'Hybrid'),
    )

    STATUS_CHOICES = (
        (u'Idle', u'Idle'),
        (u'Used', u'Used')
    )

    TRAFFIC_CHOICES = (
        (u'Off', u'Off'),
        (u'On', u'On'),
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