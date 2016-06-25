# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20160625_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='switchmodel',
            old_name='switch_type',
            new_name='type',
        ),
    ]
