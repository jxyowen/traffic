# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20160624_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocolmodel',
            name='generator',
        ),
    ]
