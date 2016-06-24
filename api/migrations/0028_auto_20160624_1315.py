# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20160624_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='id',
            field=models.PositiveIntegerField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='switchmodel',
            name='id',
            field=models.PositiveIntegerField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='id',
            field=models.PositiveIntegerField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
    ]
