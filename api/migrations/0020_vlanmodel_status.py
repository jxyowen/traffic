# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20160624_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='vlanmodel',
            name='status',
            field=models.CharField(default='Idle', max_length=10, choices=[('Used', 'Used'), ('Idle', 'Idle')]),
        ),
    ]
