# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20160621_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generatormodel',
            name='is_busy',
        ),
        migrations.AddField(
            model_name='generatormodel',
            name='status',
            field=models.CharField(default='Transmititng', max_length=10, choices=[('Transmititng', 'Transmititng'), ('Idle', 'Idle')]),
        ),
    ]
