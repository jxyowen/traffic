# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20160622_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='streammodel',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='streammodel',
            name='id',
            field=models.AutoField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
    ]
