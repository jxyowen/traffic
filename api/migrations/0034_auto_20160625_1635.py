# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20160625_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='mode',
            field=models.CharField(default=b'normal', max_length=10, choices=[(b'normal', b'normal'), (b'loop', b'loop')]),
        ),
        migrations.AlterField(
            model_name='generatormodel',
            name='status',
            field=models.CharField(max_length=10, choices=[(b'idle', b'idle'), (b'transmititing', b'transmititing')]),
        ),
        migrations.AlterField(
            model_name='switchmodel',
            name='type',
            field=models.CharField(max_length=10, choices=[(b'huawei', b'huawei'), (b'h3c', b'h3c')]),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='mode',
            field=models.CharField(max_length=10, choices=[(b'none', b'none'), (b'access', b'access'), (b'trunk', b'trunk'), (b'hybrid', b'hybrid')]),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='status',
            field=models.CharField(max_length=10, choices=[(b'idle', b'idle'), (b'used', b'used')]),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='traffic',
            field=models.CharField(max_length=10, choices=[(b'off', b'off'), (b'on', b'on')]),
        ),
    ]
