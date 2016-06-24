# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20160624_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='mode',
            field=models.CharField(default='Normal', max_length=10, choices=[('Normal', 'Normal'), ('Loop', 'Loop')]),
        ),
        migrations.AlterField(
            model_name='generatormodel',
            name='status',
            field=models.CharField(max_length=10, choices=[('Idle', 'Idle'), ('Transmititing', 'Transmititing')]),
        ),
    ]
