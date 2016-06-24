# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_protocolmodel_generator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolmodel',
            name='generator',
            field=models.ForeignKey(to='api.GeneratorModel'),
        ),
    ]
