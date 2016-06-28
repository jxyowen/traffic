# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20160628_0916'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='generatormodel',
            unique_together=set([('ip', 'port_in_use')]),
        ),
    ]
