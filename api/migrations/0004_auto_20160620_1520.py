# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160620_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vlanmodel',
            name='mode',
            field=models.CharField(max_length=10, choices=[('N', 'None'), ('A', 'Access'), ('T', 'Trunk'), ('H', 'Hybrid')]),
        ),
    ]
