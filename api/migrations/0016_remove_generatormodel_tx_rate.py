# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_generatormodel_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generatormodel',
            name='tx_rate',
        ),
    ]
