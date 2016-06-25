# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_remove_protocolmodel_generator'),
    ]

    operations = [
        migrations.AddField(
            model_name='switchmodel',
            name='logged_in_symbol',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='switchmodel',
            name='switch_type',
            field=models.CharField(default='Huawei', max_length=10, choices=[('Huawei', 'Huawei'), ('H3C', 'H3C')]),
            preserve_default=False,
        ),
    ]
