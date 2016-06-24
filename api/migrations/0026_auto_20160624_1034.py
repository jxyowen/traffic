# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20160624_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='id',
            field=models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='protocolmodel',
            name='id',
            field=models.AutoField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='streammodel',
            name='id',
            field=models.AutoField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='switchmodel',
            name='id',
            field=models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='vlanmodel',
            name='id',
            field=models.CharField(max_length=10, serialize=False, verbose_name=b'ID', primary_key=True),
        ),
    ]
