# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20160622_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='protocolmodel',
            options={'ordering': ('id',)},
        ),
    ]
