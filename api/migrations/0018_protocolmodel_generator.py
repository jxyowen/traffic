# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20160623_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocolmodel',
            name='generator',
            field=models.ForeignKey(default=1, to='api.GeneratorModel'),
        ),
    ]
