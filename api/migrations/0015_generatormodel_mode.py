# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20160622_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatormodel',
            name='mode',
            field=models.CharField(default='Normal', max_length=10, choices=[('Loop', 'Loop'), ('Normal', 'Normal')]),
        ),
    ]
