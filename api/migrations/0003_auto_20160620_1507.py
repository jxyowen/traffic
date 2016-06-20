# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160620_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generatormodel',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='switchmodel',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='switchmodel',
            name='name',
            field=models.CharField(default=b'switch', max_length=50),
        ),
    ]
