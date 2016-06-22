# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160621_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='status',
            field=models.CharField(max_length=10, choices=[('Transmititing', 'Transmititing'), ('Idle', 'Idle')]),
        ),
    ]
