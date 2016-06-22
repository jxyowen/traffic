# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160620_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatormodel',
            name='tx_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='mode',
            field=models.CharField(max_length=10, choices=[('None', 'None'), ('Access', 'Access'), ('Trunk', 'Trunk'), ('Hybrid', 'Hybrid')]),
        ),
    ]
