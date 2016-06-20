from django.db import models

# Create your models here.


class GeneratorModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID")
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.IntegerField(
        default=0
    )
    is_busy = models.BooleanField(default=False)
    # owner = models.ForeignKey('auth.User', related_name='generator')

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return 'id: %s  ip: %s ' % (self.id, self.ip)


class StreamModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID")
    generator = models.ForeignKey(GeneratorModel, null=False)
    created = models.DateTimeField(auto_now_add=True)

    configuration = models.TextField()

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'id: %s  configuration: %s ' % (self.id, self.configuration)

class ProtocolModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID")
    stream = models.ForeignKey(StreamModel, null=False)
    # generator = models.ForeignKey(GeneratorModel, null=True)
    created = models.DateTimeField(auto_now_add=True)

    configuration = models.TextField()

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'id: %s  configuration: %s ' % (self.id, self.configuration)


class SwitchModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID")
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

    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID")
    switch = models.ForeignKey(SwitchModel, null=False)
    created = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'id: %s  mode: %s ' % (self.id, self.mode)