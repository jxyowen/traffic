# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolmodel',
            name='stream',
            field=models.ForeignKey(to='api.StreamModel'),
        ),
        migrations.AlterField(
            model_name='streammodel',
            name='generator',
            field=models.ForeignKey(to='api.GeneratorModel'),
        ),
    ]
