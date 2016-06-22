# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20160622_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolmodel',
            name='id',
            field=models.AutoField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
    ]
