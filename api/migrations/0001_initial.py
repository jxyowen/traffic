# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratorModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('port', models.IntegerField(default=0)),
                ('is_busy', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='ProtocolModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('configuration', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='StreamModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('configuration', models.TextField()),
                ('generator', models.ForeignKey(to='api.GeneratorModel', null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='SwitchModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('user', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='VLANModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mode', models.IntegerField(default=0)),
                ('switch', models.ForeignKey(to='api.SwitchModel')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='protocolmodel',
            name='stream',
            field=models.ForeignKey(to='api.StreamModel', null=True),
        ),
    ]
